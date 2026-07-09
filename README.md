# CV Formatter

Public Python package for resume/CV HTML and PDF rendering — single source of truth for SyncQues resume templates, schemas, and rendering.

**Repository:** https://github.com/SyncQues/CV-Formatter  
**PyPI:** https://pypi.org/project/sync_cv_formatter/

## Install

```bash
pip install sync_cv_formatter
# or
uv add sync_cv_formatter
```

## Consumers

- `SyncQues-Backend` — recompile and live preview
- `SyncQues-Resume` — initial resume generation

## Usage

```python
from sync_cv_formatter import ResumeDocument, populate_html_template, render_html_to_pdf

document = ResumeDocument.model_validate(content_json)
html = populate_html_template(document, template_id="modern")
pdf_bytes = render_html_to_pdf(html)
```

## Templates

| ID | Style |
|----|-------|
| `professional` | Centered serif, traditional |
| `executive` | Experience-first, navy serif/sans |
| `modern` | Inter sans-serif, teal accent |
| `classic` | Times New Roman, ATS-maximum |
| `compact` | Dense one-page, IBM Plex |

Legacy `creative` maps to `modern`.

## Local development

```bash
uv sync --dev
uv run pytest
```

Editable install from a checkout:

```bash
uv add --editable ../CV-Formatter
```

## Release process

1. Change templates/code in this repo
2. Bump `version` in `pyproject.toml`
3. Run `uv run pytest`
4. Commit, tag (`git tag v1.2.1`), push tag
5. GitHub Actions publishes to PyPI (or `uv build && uv publish`)
6. Bump pin in Backend + Resume `pyproject.toml` and `uv lock`

## Versioning

- **MAJOR** — breaking `content_json` schema changes
- **MINOR** — template/CSS changes or new optional fields
- **PATCH** — bug fixes