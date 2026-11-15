# Demonstration and submission

## Recorded demonstration

Both online versions completed the eight-action walkthrough. See the
[V1 screenshot](screenshots/v1-online-success.jpg),
[V2 screenshot](screenshots/v2-online-success.jpg) and
[comparison with linked transcripts](evidence/online-comparison.md).
The V1 screenshot is from an earlier successful run; the full exported V1 repeat
is preserved separately. No missing transcript was reconstructed.

## Present in class

1. Explain the goal: escape a library by solving three linked puzzles.
2. Show V1 and its warning: the model manages rules and memory.
3. Show the V1 architecture and saved online walkthrough.
4. Switch to V2; explain explicit inventory and prerequisites, then show a proposed
   action and its Confirm/Cancel controls.
5. Show the V2 architecture and successful online export with final state.
6. Discuss the five challenging cases in TESTING.md. Both versions rejected the
   two live invalid inputs; other challenging cases were tested offline/automatically.
7. Explain the tradeoff: more enforceable rules, less free-form narration, more API calls.

For a new run, follow WALKTHROUGH.md. Download session evidence before restart,
mode/version changes or closing the session. If quota blocks a live demo, use the
recorded online evidence and label any V2 offline demonstration clearly.

## Submission checklist

- [x] Both versions implemented and selectable; milestone branches retained.
- [x] README covers problem, technologies, installation, usage and limitations.
- [x] Separate architecture diagrams for V1 and V2.
- [x] Five or more test cases, with scope and actual results identified.
- [x] Online success transcripts for both versions and screenshots.
- [x] Updated report and explanation of design decisions.
- [x] Blank credential template and ignored local .env.
- [ ] Owner ensures instructor can access this private repository, or deliberately publishes it.
- [ ] Owner submits repository URL through the university assignment page.

Submission URL: https://github.com/AlokKevadiya/AI-Escape-Room

The supplied assignment instructions request the repository link; a separately
uploaded PDF or permanently hosted application is not explicitly required. The
report is included in docs for convenience. Do not submit a temporary Codespaces
port URL as the only artifact. Review the code explanation guide before presenting.
