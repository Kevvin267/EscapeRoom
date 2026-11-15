# Observed online comparison

Reviewed 14 November 2026. All four exports record Gemini / gemini-3.6-flash.
The rejection session for each version started fresh and used the same two inputs
in order. Successful walkthroughs were separate sessions.

| Scenario | V1 baseline | V2 validated |
|---|---|---|
| Complete eight-action walkthrough | Model reports escape; full transcript saved | Escape with explicit inventory, three solved puzzles and escaped=true |
| Use key before collecting it | Refused: no key; desk remains locked | Rejected: item must be collected |
| Wrong drawer code 0000 | Refused: code incorrect | Rejected: lock unchanged |

Evidence:
- [V1 complete online walkthrough](v1-online-success.json)
- [V2 complete online walkthrough](v2-online-success.json)
- [V1 two rejection cases](v1-online-validation-tests.json)
- [V2 two rejection cases](v2-online-validation-tests.json)

Both versions passed the two online rejection cases. No observed V1 rule-breaking
failure is claimed. V2 improves the architecture by enforcing inventory, codes and
prerequisites in Python rather than relying on generated statements. V1 exports
state=null by design; V2 exposes structured final state. V2's wrong-code response
also demonstrates an authored outcome surviving unavailable AI atmosphere.

The first V1 successful run was captured only in a screenshot. The player then
repeated all eight moves and downloaded the complete transcript linked above.
The screenshot and repeat export are separate runs, not a single synchronized log.

These are user-exported sessions, not signed provider logs. A single observed run
per scenario is not a reliability estimate. Five offline rejection cases and the
49-check automated suite provide additional coverage, not additional live V1/V2
comparisons. General adversarial robustness remains unmeasured.
