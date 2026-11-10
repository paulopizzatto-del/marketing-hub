# AI contributor instructions

This repository contains a marketing agent skill and packaging scripts. For engineering, maintenance, or CI tasks, work on the repository normally. Do not automatically start writing marketing posts because this file exists.

If the user explicitly asks for marketing content, consult `skills/marketinghub/SKILL.md` and only the appropriate reference files. In a chat without file access, use the standalone `prompts/marketinghub-universal.md`.

Keep `skills/marketinghub/` as the single canonical skill. Preserve brand isolation, permissions, provenance and privacy constraints. Do not add real client profiles, tokens, or unsupported integrations.

For repository modifications, run `python scripts/check_repo.py` and `python -m unittest discover -s tests -v`. Prefer Python standard library, and avoid network-dependent tests.
