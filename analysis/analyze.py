"""
Safe or Scam? - results analysis
Built by Astha Patel

Reads the Google Forms export (CSV) and prints the group-level results
used in the README: accuracy per scenario, missed scams vs. false alarms,
and confidence vs. performance.

Usage:  python3 analysis/analyze.py data/responses.csv

The raw responses are not part of this repo (participant privacy).
Researcher test runs submitted before launch are excluded by timestamp.
"""

import csv
import statistics as st
import sys
from datetime import datetime

LAUNCH = datetime(2026, 11, 21, 11, 45)  # responses before this were my own test runs

# Column where each scenario's "safe or scam?" answer starts in the export.
# Each scenario has 3 columns: answer, confidence (1-5), reason.
# (Columns 15-17 are an empty duplicate section removed before launch.)
SCENARIO_COLUMNS = {1: 6, 2: 9, 3: 12, 4: 18, 5: 21, 6: 24, 7: 27, 8: 30}
ANSWER_KEY = {1: "Scam", 2: "Safe", 3: "Scam", 4: "Scam",
              5: "Safe", 6: "Suspicious", 7: "Safe", 8: "Scam"}
SCAMS = {s for s, a in ANSWER_KEY.items() if a != "Safe"}


def load(path):
    with open(path, newline="", encoding="utf-8") as f:
        rows = list(csv.reader(f))[1:]
    people = []
    for r in rows:
        if datetime.strptime(r[0], "%m/%d/%Y %H:%M:%S") < LAUNCH or r[2] != "Yes":
            continue
        p = {"confidence": int(r[3]), "tech": r[4], "training": r[5], "answer": {}, "sure": {}}
        for s, c in SCENARIO_COLUMNS.items():
            p["answer"][s] = r[c]
            p["sure"][s] = int(r[c + 1])
        p["correct"] = {s: p["answer"][s] == ANSWER_KEY[s] for s in ANSWER_KEY}
        p["score"] = sum(p["correct"].values())
        people.append(p)
    return people


def pct(part, whole):
    return f"{part / whole * 100:.0f}%"


def main(path):
    people = load(path)
    n = len(people)
    scores = [p["score"] for p in people]
    print(f"Average score: {st.mean(scores):.1f} / 8\n")

    print("Correct by scenario:")
    for s in ANSWER_KEY:
        right = sum(p["correct"][s] for p in people)
        print(f"  Scenario {s} ({ANSWER_KEY[s]:<10}) {pct(right, n)}")

    missed = sum(not p["correct"][s] for p in people for s in SCAMS)
    false_alarms = sum(not p["correct"][s] for p in people for s in ANSWER_KEY if s not in SCAMS)
    print(f"\nScams missed:  {pct(missed, n * len(SCAMS))}")
    print(f"False alarms:  {pct(false_alarms, n * (8 - len(SCAMS)))}")

    print("\nSelf-rated confidence vs. average score:")
    for level in sorted({p["confidence"] for p in people}):
        group = [p["score"] for p in people if p["confidence"] == level]
        print(f"  Rated {level}/5 -> {st.mean(group):.1f} / 8")
    print(f"  Correlation (r): {st.correlation([p['confidence'] for p in people], scores):.2f}")

    wrong_sure = [p["sure"][s] for p in people for s in ANSWER_KEY if not p["correct"][s]]
    confident_wrong = sum(x >= 4 for x in wrong_sure)
    print(f"\nWrong answers given with confidence 4-5: {pct(confident_wrong, len(wrong_sure))}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    main(sys.argv[1])
