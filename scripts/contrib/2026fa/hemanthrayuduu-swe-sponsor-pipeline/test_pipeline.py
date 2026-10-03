#!/usr/bin/env python3
"""Offline test for swe-sponsor-pipeline. Fixtures only; any network call fails the test.

    python3 -m unittest discover -s scripts/contrib/2026fa/hemanthrayuduu-swe-sponsor-pipeline -p 'test_*.py' -v

The pipeline is run in-process (so the network patches apply to it); the scorer it calls is the
REAL scripts/score/role-scorer.mjs, run by node as a subprocess.
"""
import importlib.util
import io
import json
import tempfile
import unittest
import urllib.request
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path
from unittest import mock

HERE = Path(__file__).resolve().parent
FIX = HERE / "fixtures"
_spec = importlib.util.spec_from_file_location("ssp_pipeline", HERE / "pipeline.py")
P = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(P)

BASE = ["--offline", str(FIX / "boards"), "--csv", str(FIX / "80days.fixture.csv"),
        "--bls", str(FIX / "bls.fixture.csv"), "--formd", str(FIX / "formd.fixture.json"),
        "--today", "2026-10-01", "--persona", str(FIX / "persona.fixture.json")]
LABELS = {"record", "your-input", "model-judgment"}


def no_network(*a, **k):
    raise AssertionError("network call attempted during an offline test")


def run(argv):
    out, err = io.StringIO(), io.StringIO()
    with mock.patch.object(urllib.request, "urlopen", no_network), \
         mock.patch.object(urllib.request.OpenerDirector, "open", no_network), \
         mock.patch.object(P.GW, "fetch_board", no_network), \
         redirect_stdout(out), redirect_stderr(err):
        rc = P.main(argv)
    return rc, out.getvalue(), err.getvalue()


def sources(node, path="$"):
    """Yield (path, source) for every labelled value anywhere in the log."""
    if isinstance(node, dict):
        if "source" in node:
            yield path, node["source"]
        for k, v in node.items():
            yield from sources(v, f"{path}.{k}")
    elif isinstance(node, list):
        for i, v in enumerate(node):
            yield from sources(v, f"{path}[{i}]")


class HappyPathOffline(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.TemporaryDirectory()
        cls.out = Path(cls.tmp.name)
        cls.rc, cls.stdout, cls.stderr = run(BASE + ["--out-dir", str(cls.out)])
        cls.log = json.loads((cls.out / "pipeline-log.json").read_text())
        cls.b = cls.log["buckets"]
        cls.roles_json = json.loads((cls.out / "roles.json").read_text())["roles"]

    @classmethod
    def tearDownClass(cls):
        cls.tmp.cleanup()

    def test_completes_and_writes_both_outputs(self):
        self.assertEqual(self.rc, 0, self.stderr)
        self.assertTrue((self.out / "pipeline-log.json").exists())
        report = (self.out / "pipeline-report.md").read_text()
        self.assertTrue(report.splitlines()[2].startswith("## Executive summary"))

    def test_real_scorer_produced_the_decisions(self):
        scores = json.loads((self.out / "role-scores.json").read_text())
        self.assertIn("_scorer", scores)                       # written by role-scorer.mjs, not by us
        self.assertEqual(self.log["scorer"]["exit_code"], 0)
        self.assertEqual({r["role_id"] for r in scores["roles"]}, {r["role_id"] for r in self.roles_json})

    def test_live_posting_at_proven_sponsor_is_apply(self):
        self.assertIn("greenhouse:lumenbyte:101", self.b["apply"])

    def test_soft_sponsorship_tier_is_demoted_to_consider(self):
        # ML posting at a company whose sponsored titles are software-only -> tier Possible
        self.assertIn("greenhouse:lumenbyte:103", self.b["consider"])
        self.assertIn("greenhouse:weaksponsor:401", self.b["consider"])

    def test_F6_senior_only_or_non_us_board_becomes_network_target(self):
        self.assertIn("company:ashby:quiet-harbor-labs", self.b["network"])
        self.assertIn("company:greenhouse:abroadonly", self.b["network"])
        ids = {r["role_id"] for r in self.roles_json}
        self.assertNotIn("ashby:quiet-harbor-labs:qh-1", ids)   # "Staff Machine Learning Engineer": staff still excluded

    def test_rules_030_senior_titles_are_scored(self):
        # 0.3.0 (author): Senior allowed. Fixture 102 says "7+ years." but not "years of experience", so the years rule
        # does not fire either: the posting is scored, as the rules say it should be.
        ids = {r["role_id"] for r in self.roles_json}
        self.assertIn("greenhouse:lumenbyte:102", ids)

    def test_F2_missing_or_failed_board_is_check_by_hand_and_never_scored(self):
        for name in ("Ghost Slug Corp", "Flaky Board Inc", "Mismatch Name Inc"):
            self.assertIn(name, self.b["check-by-hand"])
            self.assertFalse(any(r["company"] == name for r in self.roles_json),
                             f"{name} reached the scorer — a missing liveness gate would default to open")
        status = {c["company"]["value"]: c["board"]["status"] for c in self.log["companies"]}
        self.assertEqual(status["Flaky Board Inc"], "fetch-failed")
        self.assertEqual(status["Mismatch Name Inc"], "identity-mismatch")

    def test_F1_and_window_filters_drop_companies_without_a_record(self):
        names = {c["company"]["value"] for c in self.log["companies"]}
        for name in ("No Sponsor Apps Inc", "Old Money Software LLC", "Hardware Only Inc"):
            self.assertNotIn(name, names)
        self.assertEqual(self.log["funnel"]["csv_rows"], 10)
        self.assertEqual(self.log["funnel"]["candidates"], 7)

    def test_F4_soc_without_bls_row_shows_no_wage(self):
        w = next(r for r in self.log["roles"] if r["role_id"] == "greenhouse:lumenbyte:103")["result"]["wage_context"]
        self.assertEqual(w["status"], "unmapped")
        self.assertNotIn("annual_median_wage", w)

    def test_F5_form_d_match_and_miss_are_both_labelled(self):
        by = {c["company"]["value"]: c["form_d_sample"] for c in self.log["companies"]}
        self.assertIsNotNone(by["Lumen Byte Inc"]["value"])
        self.assertIsNone(by["Ghost Slug Corp"]["value"])
        self.assertIn("no Form D sample match", by["Ghost Slug Corp"]["note"])

    def test_every_value_carries_one_of_the_three_labels(self):
        found = list(sources(self.log))
        self.assertGreater(len(found), 50)
        bad = [(p, s) for p, s in found if s not in LABELS]
        self.assertEqual(bad, [])
        self.assertFalse(any(s == "model-judgment" for _, s in found))  # this tool makes no model calls

    def test_no_network_host_was_contacted(self):
        self.assertEqual(self.log["hosts_contacted"], [])
        self.assertEqual(self.log["http_calls"], 0)


    def test_TODO7_description_rules_rule_out_without_scoring(self):
        ids = {r["role_id"] for r in self.roles_json}
        ruled = {x["url"]["value"].rsplit("/", 1)[1]: x["reason"]["value"]
                 for c in self.log["companies"] for x in c.get("ruled_out_by_description", [])}
        self.assertEqual(set(ruled), {"105", "106", "402"}, "description rules did not rule out the expected postings")
        self.assertTrue(ruled["105"].startswith("eligibility:"), ruled)      # U.S. citizenship + clearance
        self.assertTrue(ruled["106"].startswith("experience:"), ruled)       # 7+ years vs persona 3.5 (+1)
        self.assertTrue(ruled["402"].startswith("no-sponsorship:"), ruled)   # "unable to sponsor"
        for jid in ("105", "106", "402"):
            self.assertFalse(any(i.endswith(":" + jid) for i in ids), f"{jid} reached the scorer")
        self.assertEqual(self.log["funnel"]["postings_ruled_out_by_description"], 3)

    def test_cant_sponsor_statements_are_counted_per_company_not_used_to_drop_it(self):
        # live run 2026-10-02: the statements were role-specific ("for this role"), so they count, they don't remove a company
        comp = {c["company"]["value"]: c for c in self.log["companies"]}
        self.assertEqual([x["phrase"]["value"] for x in comp["Abroad Only Inc"]["no_sponsorship_statements"]], ["unable to sponsor"])
        self.assertEqual(comp["Abroad Only Inc"]["bucket"], "network")                # non-target posting 502 doesn't drop it
        self.assertEqual(len(comp["Weak Sponsor Inc"]["no_sponsorship_statements"]), 1)  # posting 402
        self.assertIn("greenhouse:weaksponsor:401", self.b["consider"])                 # 401 has no statement: still listed
        self.assertIn("1 of 2 postings here say they can't sponsor that role", (self.out / "pipeline-report.md").read_text())

    def test_stack_terms_years_and_preferred_location_are_labelled_records(self):
        m = next(r for r in self.log["roles"] if r["role_id"] == "greenhouse:lumenbyte:107")["result"]
        self.assertIn("azure openai", m["microsoft_ai_stack_terms"]["value"])
        self.assertIn("semantic kernel", m["microsoft_ai_stack_terms"]["value"])
        self.assertEqual(m["years_required"]["value"], 3)
        self.assertEqual(m["preferred_location"]["value"], True)              # Austin, TX
        self.assertEqual(m["preferred_location"]["source"], "your-input")
        boston = next(r for r in self.log["roles"] if r["role_id"] == "greenhouse:lumenbyte:101")["result"]
        self.assertEqual(boston["preferred_location"]["value"], False)


class TitleAndDescriptionRules(unittest.TestCase):
    rules = json.loads((HERE / "rules.json").read_text())

    def test_family_of(self):
        cases = {"Software Engineer, Machine Learning": "ml_ai",   # role word + AI word → ml_ai wins (checked first)
                 "Software Engineer - AI Platform": "ml_ai",
                 "AI Engineer – Forward Deployed Engineering": "ml_ai",
                 "Generative AI Engineer": "ml_ai",
                 "Software Engineer II": "software",
                 "Backend Engineer - Connectivity": "software",
                 "Account Executive": None,
                 "AI Product Manager": None,                        # AI word but no role word
                 "Partner Engineer: Partner Intelligence, AI & Apps": None,   # 0.2.1 false positive, now excluded
                 "AI Automation QA Engineer": None,
                 "Senior Data Engineer": "data_engineering",          # 0.3.0 families
                 "Analytics Engineer": "data_engineering",
                 "Data Scientist II": "data_science",
                 "Senior Data Scientist, Machine Learning": "ml_ai"}  # ml_ai is checked first
        for title, want in cases.items():
            self.assertEqual(P.family_of(title, self.rules), want, title)

    def test_years_parse_reads_only_experience_requirements(self):
        persona = {"experience_years": 3.5}
        def years(text):
            return P.description_check({"title": "AI Engineer", "content": text}, self.rules, persona)
        self.assertEqual(years("5+ years of relevant experience")[1]["years_required"], 5)
        self.assertEqual(years("3-5 years of professional experience with LLMs")[1]["years_required"], 3)
        self.assertIsNone(years("Founded 10+ years ago; we value curiosity.")[1]["years_required"])
        self.assertTrue(years("6+ years of industry experience")[0].startswith("experience:"))
        self.assertIsNone(years("4+ years of experience")[0])               # 4 <= 3.5 + 1 tolerance


    def test_seniority_rules_030(self):
        for title, excluded in {"Senior AI Engineer": False, "Sr. Data Engineer": False, "AI Engineer III": False,
                                "Staff AI Engineer": True, "Lead Data Scientist": True, "Principal ML Engineer": True,
                                "Data Engineering Intern": True}.items():
            self.assertEqual(bool(P.seniority_hit(title, self.rules)), excluded, title)


class LocationRule(unittest.TestCase):
    """Regression: the first full live run (2026-10-02) classed 'Anywhere in the US' as non-US and
    sent a company with a matching posting to the networking list (evidence/06-full-live-run-before-us-fix)."""

    def test_location_classes(self):
        rules = json.loads((HERE / "rules.json").read_text())
        cases = {
            "ML Engineer, Manipulation — Anywhere in the US": "us",   # the live string that broke
            "San Mateo, CA United States": "us",
            "Mountain View, California": "us",
            "Remote - US": "us",
            "U.S. Remote": "us",
            "Boston, MA": "us",
            "Remote": "remote-unstated",
            "": "unstated",
            "Bengaluru, India": "non-us",
            "London, United Kingdom": "non-us",
            "Toronto, Canada": "non-us",
            "Remote - Europe (join us)": "non-us",                   # lowercase "us" is not the country
        }
        for loc, want in cases.items():
            self.assertEqual(P.location_class(loc, rules), want, loc)


class NamedFailures(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.out = Path(self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    def test_F3_closed_opt_window_fails_without_a_timeline_value(self):
        rc, _, err = run(BASE + ["--persona", str(FIX / "persona.past-opt.fixture.json"), "--out-dir", str(self.out)])
        self.assertEqual(rc, 1)
        self.assertIn("OPT window already closed", err)
        self.assertFalse((self.out / "pipeline-log.json").exists())
        self.assertFalse((self.out / "roles.json").exists())

    def test_missing_csv_fails_clearly(self):
        rc, _, err = run(BASE + ["--csv", str(FIX / "does-not-exist.csv"), "--out-dir", str(self.out)])
        self.assertEqual(rc, 1)
        self.assertIn("80 Days CSV not found", err)

    def test_wrong_schema_csv_halts_instead_of_reporting_zero_candidates(self):
        # regression: before the column check, passing the BLS file here printed "✓ … 0 candidates" and exited 0
        rc, _, err = run(BASE + ["--csv", str(FIX / "bls.fixture.csv"), "--out-dir", str(self.out)])
        self.assertEqual(rc, 1)
        self.assertIn("missing columns", err)
        self.assertFalse((self.out / "pipeline-log.json").exists())

    def test_never_writes_over_tracked_files(self):
        # the fixtures folder is git-tracked: the run must refuse it and write nothing there
        before = sorted(p.name for p in FIX.iterdir())
        rc, _, err = run(BASE + ["--out-dir", str(FIX)])
        self.assertEqual(rc, 1)
        self.assertIn("refusing to write into", err)
        self.assertEqual(sorted(p.name for p in FIX.iterdir()), before)

    def test_default_out_dir_is_gitignored_inside_own_folder(self):
        import subprocess
        default = HERE / ".build" / "runs" / "2026-10-01-offline" / "pipeline-log.json"
        self.assertTrue(str(default).startswith(str(HERE)))
        ignored = subprocess.run(["git", "-C", str(HERE), "check-ignore", "-q", str(default)])
        self.assertEqual(ignored.returncode, 0, "default output folder is not gitignored")

    def test_F1_named_company_not_in_csv_is_reported_not_scored(self):
        rc, out, _ = run(BASE + ["--company", "Imaginary Rocket Co", "--out-dir", str(self.out)])
        self.assertEqual(rc, 0)
        self.assertIn("Imaginary Rocket Co: not in the 80 Days CSV", out)
        log = json.loads((self.out / "pipeline-log.json").read_text())
        self.assertEqual(log["funnel"]["roles_scored"], 0)


if __name__ == "__main__":
    unittest.main()
