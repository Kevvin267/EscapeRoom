# Online setup and troubleshooting

The recorded successful route for both versions is Gemini with `generate_content`.
The saved sessions identify `gemini-3.6-flash`; this is historical evidence from the
user's project, not a guarantee that the model is available to every account.

1. Copy `.env.example` to `.env` in the project root.
2. Privately set GEMINI_API_KEY and a model ID available to your account. Leave
   LLM_PROVIDER=gemini and GEMINI_TRANSPORT=generate_content.
3. Use only a free-tier project without billing for this project.
4. Run the smoke test with your selected model ID:

```sh
python check_online.py --provider gemini --model YOUR_AVAILABLE_MODEL_ID --transport generate_content
```

Replace the placeholder; do not paste an API key into the command. The probe checks
one V2 action (`examine bookshelf`) and saves model/provider settings only on success.
It does not test V1, the complete game or long-term availability.

Stop the existing Streamlit process with Ctrl+C, then restart:

```sh
python -m streamlit run app.py --server.address 0.0.0.0 --server.port 8501
```

In Codespaces, open the current port 8501 forwarded link. If the port is occupied,
stop the existing app in its terminal first. Enable **Use online AI** and select the
version. Changes to .env require a process restart; restarting the game is different.

## Observed failures

| Message | Interpretation and next step |
|---|---|
| 429 | Check account quota/rate limits; repeated requests do not restore quota. |
| 503 | Service reported overload; retry later or use another available model. |
| 504 / timeout | Request did not finish; a subsequent request may still succeed. |
| 404 | Verify exact model ID and API route for the account. |
| App URL 404 | Check Codespace, running server and forwarded port; this is distinct from an API model error. |

These failures were observed during the project. Availability is external to the
game. Failed parser requests apply no move. After a confirmed V2 transition,
atmosphere failure leaves the engine result intact. Failed requests are not fully
recorded in exported conversation JSON; do not infer error history from JSON alone.

## Optional adapters

`--transport interactions` selects the optional Gemini REST adapter. Groq requires
its own private GROQ_API_KEY, available GROQ_MODEL and `--provider groq`.
Neither is an automatic fallback. Both have mocked adapter tests; neither has a
successful live session in the submitted evidence. Use the verified route first.
Never commit .env or share a screenshot of its values. Revoke any exposed key.

References: [Gen AI SDK](https://googleapis.github.io/python-genai/),
[Gemini API](https://ai.google.dev/api/generate-content),
[Groq documentation](https://console.groq.com/docs/overview).
