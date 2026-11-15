# V2 online rejection evidence

Reviewed 14 November 2026. See [session JSON](v2-online-validation-tests.json).

Provider: Gemini. Model: gemini-3.6-flash.

| Input | Observed result |
|---|---|
| `use key on desk` | Rejected because the key had not been collected. |
| `enter 0000 on drawer` | Incorrect code rejected; drawer remained locked. |

The final exported state has empty inventory and solved lists, with all boolean
fields false. The second response includes an AI-atmosphere-unavailable notice;
the authoritative validation result was still displayed. The export does not
record the cause/status of that narration failure. The accompanying user screenshot
also showed a 429 on a later request, which is not a completed test in this export.

These are two online examples, not five online tests or proof of comprehensive
prompt-injection resistance. Five offline rejection examples remain separately
labelled. Further V2 live testing is paused by user choice. V1 live demonstration
and comparison remain outstanding; earlier review/checklist documents describe a
broader comparison plan, not completed results. No credentials were found here.
