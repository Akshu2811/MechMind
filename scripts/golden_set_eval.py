"""Golden-set evaluation for MechMind's /ask endpoint LLM-as-judge scores.

Hits the real, running local server's /ask endpoint (no mocking -- a genuine
end-to-end call through retrieval, generation, and both judges) for six
hand-picked questions, compares the actual groundedness/relevance scores the
judges returned against a hardcoded "my own judgment" expected score for
each question, and flags any question where actual and expected differ by
more than FLAG_THRESHOLD as a judge calibration concern worth investigating.

Writes a markdown report to docs/golden_set_validation.md in addition to
printing the summary table to stdout.

Usage:
    python scripts/golden_set_eval.py [--base-url http://127.0.0.1:8000]

Requires the local server to already be running and OPENAI_API_KEY
configured, since /ask calls gpt-4o-mini for both generation and judging.
"""

from __future__ import annotations

import argparse
import json
import sys
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

FLAG_THRESHOLD = 0.15
REPORT_PATH = Path(__file__).resolve().parent.parent / "docs" / "golden_set_validation.md"

GOLDEN_SET = [
    {
        "question": "What is the recommended action for OIL_PRESS_03?",
        "my_expected_groundedness": 1.0,
        "my_expected_relevance": 1.0,
        "note": (
            "Clear, well-documented alarm code with a specific recommended action in the "
            "manual -- should be fully grounded and directly relevant."
        ),
    },
    {
        "question": "Why is Pump-3 overheating?",
        "my_expected_groundedness": 1.0,
        "my_expected_relevance": 1.0,
        "note": (
            "Requires synthesizing both the manual's troubleshooting guidance and Pump-3's "
            "own log history -- tests dual-perspective synthesis, not just single-source "
            "lookup."
        ),
    },
    {
        "question": "What is the capital of France?",
        "my_expected_groundedness": 1.0,
        "my_expected_relevance": 0.0,
        "note": (
            "Completely off-topic for an equipment maintenance KB. Correct behavior is a "
            "refusal ('I don't have enough information...'), which is trivially grounded "
            "(no unsupported claims) but should score ~0 relevance since it doesn't answer "
            "the geography question asked."
        ),
    },
    {
        "question": "What's the maintenance schedule for Compressor-3?",
        "my_expected_groundedness": 1.0,
        "my_expected_relevance": 0.0,
        "note": (
            "Compressor-3 doesn't exist in our fleet (only Compressor-1/2) -- correct "
            "behavior is a refusal, grounded but not relevant to a question about a "
            "nonexistent unit."
        ),
    },
    {
        "question": "Has Compressor-2 had recurring issues?",
        "my_expected_groundedness": 1.0,
        "my_expected_relevance": 1.0,
        "note": (
            "Answerable directly from Compressor-2's maintenance log history -- tests "
            "log-based grounding."
        ),
    },
    {
        "question": "What should I check if Motor-2's vibration sensor is reporting a fault?",
        "my_expected_groundedness": 1.0,
        "my_expected_relevance": 1.0,
        "note": (
            "Directly answerable from the motor manual's troubleshooting/alarm sections -- "
            "tests manual-based diagnostic grounding."
        ),
    },
]


def call_ask(base_url: str, question: str) -> dict:
    payload = json.dumps({"question": question}).encode("utf-8")
    req = urllib.request.Request(
        f"{base_url}/ask",
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=90) as resp:
        return json.loads(resp.read().decode("utf-8"))


def _diff(actual: float | None, expected: float) -> float | None:
    return None if actual is None else round(abs(actual - expected), 4)


def run(base_url: str) -> list[dict]:
    results = []
    for item in GOLDEN_SET:
        question = item["question"]
        print(f"Asking: {question!r} ...")
        try:
            data = call_ask(base_url, question)
        except urllib.error.URLError as exc:
            print(f"  ERROR: could not reach {base_url}/ask -- {exc}", file=sys.stderr)
            raise SystemExit(1) from exc
        except urllib.error.HTTPError as exc:
            body = exc.read().decode("utf-8", errors="replace")
            print(f"  ERROR: {base_url}/ask returned HTTP {exc.code}: {body}", file=sys.stderr)
            raise SystemExit(1) from exc

        actual_groundedness = data.get("groundedness")
        actual_relevance = data.get("relevance")
        groundedness_diff = _diff(actual_groundedness, item["my_expected_groundedness"])
        relevance_diff = _diff(actual_relevance, item["my_expected_relevance"])

        flagged = (
            (groundedness_diff is not None and groundedness_diff > FLAG_THRESHOLD)
            or (relevance_diff is not None and relevance_diff > FLAG_THRESHOLD)
        )

        result = {
            **item,
            "actual_groundedness": actual_groundedness,
            "actual_relevance": actual_relevance,
            "groundedness_diff": groundedness_diff,
            "relevance_diff": relevance_diff,
            "flagged": flagged,
            "answer": data.get("answer", ""),
        }
        results.append(result)
        print(
            f"  groundedness: expected={item['my_expected_groundedness']:.2f} "
            f"actual={_fmt(actual_groundedness)} diff={_fmt(groundedness_diff)}"
        )
        print(
            f"  relevance:    expected={item['my_expected_relevance']:.2f} "
            f"actual={_fmt(actual_relevance)} diff={_fmt(relevance_diff)}"
        )
        print(f"  {'*** FLAGGED ***' if flagged else 'OK'}\n")
    return results


def _fmt(value: float | None) -> str:
    return "N/A" if value is None else f"{value:.2f}"


def print_summary_table(results: list[dict]) -> None:
    print("=" * 100)
    print("SUMMARY")
    print("=" * 100)
    header = f"{'Question':52s} {'Expected G/R':14s} {'Actual G/R':14s} {'Diff G/R':14s} {'Flagged'}"
    print(header)
    print("-" * len(header))
    for r in results:
        q = r["question"] if len(r["question"]) <= 50 else r["question"][:47] + "..."
        expected = f"{r['my_expected_groundedness']:.2f}/{r['my_expected_relevance']:.2f}"
        actual = f"{_fmt(r['actual_groundedness'])}/{_fmt(r['actual_relevance'])}"
        diff = f"{_fmt(r['groundedness_diff'])}/{_fmt(r['relevance_diff'])}"
        flagged = "YES" if r["flagged"] else "no"
        print(f"{q:52s} {expected:14s} {actual:14s} {diff:14s} {flagged}")
    print()
    flagged_count = sum(1 for r in results if r["flagged"])
    print(f"{flagged_count} of {len(results)} question(s) flagged (diff > {FLAG_THRESHOLD}).")


def render_markdown(results: list[dict], base_url: str) -> str:
    flagged_count = sum(1 for r in results if r["flagged"])
    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

    lines = [
        "# Golden-Set Evaluation: LLM Judge Calibration",
        "",
        f"Generated by `scripts/golden_set_eval.py` against `{base_url}` on {timestamp}.",
        "",
        "Six hand-picked questions were run through the real `/ask` endpoint (real retrieval, "
        "real gpt-4o-mini generation, real groundedness/relevance judge calls -- nothing "
        "mocked). Each question carries an expected groundedness/relevance score based on my "
        "own judgment of what a well-behaved answer should look like, before seeing the "
        f"judge's actual scores. A difference greater than {FLAG_THRESHOLD} between expected "
        "and actual is flagged as a judge calibration concern.",
        "",
        "## Results",
        "",
        "| Question | My Expected (G/R) | Actual Judge Score (G/R) | Difference (G/R) | Flagged? |",
        "|---|---|---|---|---|",
    ]

    for r in results:
        expected = f"{r['my_expected_groundedness']:.2f} / {r['my_expected_relevance']:.2f}"
        actual = f"{_fmt(r['actual_groundedness'])} / {_fmt(r['actual_relevance'])}"
        diff = f"{_fmt(r['groundedness_diff'])} / {_fmt(r['relevance_diff'])}"
        flagged = "**YES**" if r["flagged"] else "no"
        question_escaped = r["question"].replace("|", "\\|")
        lines.append(f"| {question_escaped} | {expected} | {actual} | {diff} | {flagged} |")

    lines += [
        "",
        "## Per-Question Reasoning & Actual Answers",
        "",
    ]
    for i, r in enumerate(results, start=1):
        lines += [
            f"### {i}. {r['question']}",
            "",
            f"**Expected reasoning:** {r['note']}",
            "",
            f"**Actual scores:** groundedness={_fmt(r['actual_groundedness'])}, "
            f"relevance={_fmt(r['actual_relevance'])}",
            "",
            f"**Actual answer:** {r['answer']}",
            "",
        ]

    lines += [
        "## Conclusion",
        "",
    ]
    if flagged_count == 0:
        lines.append(
            f"All {len(results)} questions landed within {FLAG_THRESHOLD} of their expected "
            "score on both groundedness and relevance. On this sample, the LLM judge appears "
            "well-calibrated: it correctly gives full marks to well-documented, directly "
            "answerable questions, and correctly recognizes off-topic/nonexistent-equipment "
            "questions as ungrounded-in-relevance refusals rather than penalizing the "
            "groundedness of a refusal it shouldn't be penalizing."
        )
    else:
        lines.append(
            f"{flagged_count} of {len(results)} question(s) showed a difference greater than "
            f"{FLAG_THRESHOLD} between expected and actual judge scores (see flagged rows "
            "above). This sample suggests the judge's calibration should be investigated "
            "further on the flagged questions specifically before trusting its scores "
            "unreviewed in that area -- see the per-question actual answers above for what "
            "the judge was actually looking at when it produced that score."
        )
    lines.append("")

    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--base-url",
        default="http://127.0.0.1:8000",
        help="Base URL of the running MechMind server (default: %(default)s)",
    )
    args = parser.parse_args()

    results = run(args.base_url)
    print_summary_table(results)

    report = render_markdown(results, args.base_url)
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text(report, encoding="utf-8")
    print(f"\nReport written to {REPORT_PATH}")


if __name__ == "__main__":
    main()
