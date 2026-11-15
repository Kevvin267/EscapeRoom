# Assignment review - 14 November 2026

## Requirement mapping

| Assignment requirement | Repository evidence |
|---|---|
| Complete V1 and V2 | app.py version selector; escape_room/v1.py, v2.py, engine.py |
| Explain problem and solution | README.md and Project_Report.pdf |
| Installation and technologies | README quick start; requirements files; .env.example |
| Identify development versions | version-1 and version-2 milestone branches; integrated main |
| Explain improvements and limitations | ARCHITECTURE.md, TESTING.md, EXPLAINING_THE_CODE.md |
| Diagram for each version | ARCHITECTURE.md and diagrams/ PNG and DOT files |
| Screenshots or short video | screenshots/v1-online-success.jpg and v2-online-success.jpg |
| At least five test cases | TESTING.md: eleven cases with evidence scope |
| Meaningful development history | Existing milestones and incremental code, tests and evidence commits retained |
| Protect credentials | .gitignore excludes .env; .env.example contains blank keys |
| Accessible submission | Owner must grant instructor access or publish; submit repository URL |

## Verification scope

The current source and evidence were reviewed. The 49-test suite covers deterministic
engine behavior, mocked model contracts and Streamlit UI interactions. Both complete
online transcripts contain eight user actions. V2's recorded success state agrees
with replay through the Python engine. The five-move offline rejection sequence
and two-move online V2 rejection sequence preserve the initial state. V1's escape
is a model-generated claim, as intended by the baseline.

Both versions passed the two live rejection examples. No statistical reliability
comparison or demonstrated V1 prompt-injection failure is claimed. User exports
are not signed provider logs; no API request IDs or timestamps are stored.

Current tracked text and selected demonstration images were checked for exposed
credentials before this documentation update. This is not a certification of every
historical commit. The private .env screenshot is excluded. An exposed credential
must be revoked by its owner even if it was never committed.

## Remaining limitations

Model interpretation may be wrong; confirmation and engine checks serve different
purposes. Sessions are not persistent. Repeated unlock/answer commands may repeat
outdated narrative descriptions while state remains constrained. API availability
and quota affect online play; optional adapters have no successful live evidence.
Broader live paraphrase/adversarial trials would strengthen the evaluation.

The report is supplementary: the supplied instructions require the GitHub link.
Repository access and the university submission itself remain owner actions.
