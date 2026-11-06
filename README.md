# EVREN LLM Provider for Agent Zero

Free AI credits for Turkish citizens via [evren.ssyz.org.tr](https://evren.ssyz.org.tr).

## Install
1. In Agent Zero: Settings → Plugins → Install → `evren_llm` (local plugin).
2. Go to Settings → Agent → EVREN LLM section.
3. Paste your API key (starts with `evren_llm_`).
4. Click **Save & Test**. The plugin checks connection, shows available models and your remaining credits.
5. Accept the one-time terms (button appears automatically if needed).

## Use
In Model settings, choose provider **EVREN AI (Free for Türkiye)** and pick a model:
- `deepseek-v4.1-flash` — fast reasoning
- `glm-5.3` — most capable
- `mimo-v2.6-pro` — largest, vision+video+audio
- `qwen3.8-flash-next` — highest concurrency
- `gemma-4-31b` — vision, handwriting
- `qwen3-vl-30b` — visual reasoning
- `auto` — gateway auto-routing

## Credits display
The config page shows daily token usage, 5-min window, and remaining credits, refreshing on Save & Test.

## Notes
- All inference is free (0.00 CR) until 2026-11-01.
- Daily quota: 15,000,000 tokens, resets 00:00 UTC.
- Rate: 500k TPM normal; DeepSeek bursts up to 1M accepted.
