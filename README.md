# AI Security Regression Suite

A local defensive regression suite for an assistant's authorization layer.
The fixtures represent structured proposals that a model might produce.
The evaluator records decisions and never executes a proposed tool.

```powershell
python evaluate.py --mode monitor
python evaluate.py --mode enforce
Get-Content reports/enforce.json -Encoding utf8
```

Monitor records what the policy would decide while simulating a baseline
that allows every proposal. Enforce applies the policy. The expected results
are six unsafe allows in monitor, zero in enforce, and zero false blocks in both.
The enforce command exits nonzero on a mismatch and runs in GitHub Actions.

The identity and workspace are supplied by the test harness as trusted
request context. The policy checks membership, document scope and whether
approval matches the actor, workspace, tool and target. Approval records are
fixtures. Integrating this policy into an application requires authenticating
the caller and managing approval lifecycle on the server.

This suite measures the authorization decision on nine synthetic proposals.
It does not assess live model behavior or execute external tools.

## Add a regression case

Add a case to cases.json and decide its expected result before running the
suite. Include both denied and allowed variants so a broad rejection cannot
appear to improve results by blocking legitimate work.
