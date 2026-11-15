# Explain the project in class

**Problem:** An LLM can generate plausible game narration without independently
verifiable inventory or puzzle progress. A stateful game needs explicit rules.

**V1:** `v1.respond` sends the room rules and conversation history through `llm.py`.
The model acts as narrator and referee. `app.py` trusts its escape marker. V1's
exported state is null because it has no independently validated engine state.

**V2:** `v2.propose` extracts an Action (verb, target, value). It validates the JSON,
checks entered values against the user's message and asks the user to confirm.
`engine.apply` enforces inventory and puzzle prerequisites against a State dataclass.
It returns a copied next state and factual outcome; rejected actions preserve state.

**Secrets:** Author solutions live in the Python game rules, not the V2 parser or
atmosphere prompts. They are still visible to source-code readers. API keys are
different: they belong only in environment variables/private .env files.

**Narration:** V2 chooses one of three safe atmosphere sentences and appends the
engine outcome. A failed atmosphere call preserves the validated result. This
reduces contradictory prose but also reduces creativity.

**Evidence:** Both V1 and V2 completed recorded online walkthroughs with Gemini.
Both rejected the two live invalid inputs. V2 additionally has five offline
rejection examples and automated rule checks. Do not describe hypothetical V1
vulnerabilities as observed failures or offline parsing as AI inference.

**Availability:** API quota and service errors interrupted testing. The app reports
sanitized errors and uses no unbounded retry loop. V2 normally needs two calls per
confirmed action; V1 needs one. A parser smoke-test success is not a full V1 test.

**Limitations:** Sessions are in memory; no durable save/reload. The model may choose
an unintended legal action. The export is a conversation plus final state, not a
complete audit log. Repeated successful commands can repeat stale descriptions.
Groq and Interactions have mocked tests but no successful live evidence here.

**Next improvements:** More live paraphrase trials, clearer repeated-action messages,
optional durable state, richer constrained narration and a more complete event log.

The project used AI coding assistance. Review the actual functions and tests so
you can explain the behavior and limitations in your own words.
