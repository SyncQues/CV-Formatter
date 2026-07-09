# syncques-resume-renderer

Single source of truth for SyncQues resume templates, schemas, and HTML rendering.

## Consumers

- `SyncQues-Backend` — recompile and live preview
- `SyncQues-Resume` — initial resume generation

## Install (local path)

```bash
uv add --editable ../SyncQues-Resume-Renderer
```

## Versioning

- **MAJOR** — breaking `content_json` schema changes
- **MINOR** — template/CSS changes or new optional fields
- **PATCH** — bug fixes

Bump the version in `pyproject.toml` and update the pin in every consumer in the same release.

## Tests

```bash
uv run pytest
```