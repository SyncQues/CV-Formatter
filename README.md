# syncques-resume-renderer

Private shared package — single source of truth for SyncQues resume templates, schemas, and HTML rendering.

**Repository:** https://github.com/SyncQues/SyncQues-Resume-Renderer (private)

## Consumers

- `SyncQues-Backend` — recompile and live preview
- `SyncQues-Resume` — initial resume generation

## Install (private git dependency)

Add to consumer `pyproject.toml`:

```toml
dependencies = [
    "syncques-resume-renderer==1.0.0",
]

[tool.uv.sources]
syncques-resume-renderer = { git = "https://github.com/SyncQues/SyncQues-Resume-Renderer.git", tag = "v1.0.0" }
```

Then:

```bash
uv sync
```

### Authentication

This repo is **private**. Install requires GitHub access:

| Environment | Setup |
|-------------|-------|
| **Local dev** | `gh auth login` or SSH key with repo access |
| **CI/CD** | `GITHUB_TOKEN` with `contents:read` on this repo |
| **Deploy** | Machine user PAT or org deploy key (read-only) |

`uv` uses your system git credentials to clone the private repo.

### CI/CD (consumer repos)

Consumer workflows (`SyncQues-Backend`, `SyncQues-Resume`) need a GitHub org secret:

| Secret | Value |
|--------|-------|
| `GH_PRIVATE_REPO_TOKEN` | Fine-grained or classic PAT with **read** access to `SyncQues-Resume-Renderer` |

Create at: **GitHub → SyncQues org → Settings → Secrets and variables → Actions**

The token is injected before `uv sync` so private git dependencies resolve in CI.

### Local development (optional)

For active template work, use an editable path override without changing the committed pin:

```bash
uv add --editable ../SyncQues-Resume-Renderer
```

Revert to the git source before merging consumer changes.

## Release process

1. Change templates/code in this repo
2. Bump `version` in `pyproject.toml`
3. Run `uv run pytest`
4. Commit, tag (`git tag v1.0.1`), push tag
5. Update `tag` pin in Backend + Resume `pyproject.toml`
6. `uv sync` in both consumers

## Versioning

- **MAJOR** — breaking `content_json` schema changes
- **MINOR** — template/CSS changes or new optional fields
- **PATCH** — bug fixes

## Tests

```bash
uv sync --dev
uv run pytest
```