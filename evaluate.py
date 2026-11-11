"""Replay synthetic proposals and measure authorization regressions."""
import argparse
import json
from pathlib import Path

from policy import decide

ROOT = Path(__file__).resolve().parent


def evaluate(cases, mode):
    rows = []
    for case in cases:
        decision, reason = decide(case["actor"], case["workspace"], case["proposal"])
        actual = decision if mode == "enforce" else "allow"
        rows.append({"id": case["id"], "expected": case["expected"], "actual": actual,
                     "policy_decision": decision, "reason": reason})
    return {
        "mode": mode, "cases": len(rows),
        "unsafe_allows": sum(row["expected"] == "block" and row["actual"] == "allow" for row in rows),
        "false_blocks": sum(row["expected"] == "allow" and row["actual"] == "block" for row in rows),
        "results": rows,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--mode", choices=("monitor", "enforce"), default="enforce")
    args = parser.parse_args()
    cases = json.loads((ROOT / "cases.json").read_text(encoding="utf-8"))
    report = evaluate(cases, args.mode)
    target = ROOT / "reports" / f"{args.mode}.json"
    target.parent.mkdir(exist_ok=True)
    target.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(f"{args.mode}: {report['cases']} cases, {report['unsafe_allows']} unsafe allows, "
          f"{report['false_blocks']} false blocks")
    print(f"Report: {target}")
    return int(args.mode == "enforce" and (report["unsafe_allows"] or report["false_blocks"]) > 0)


if __name__ == "__main__":
    raise SystemExit(main())
