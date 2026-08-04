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
from sync_cv_formatter import (
    ResumeDocument,
    list_templates,
    populate_html_template,
    render_html_to_pdf,
)

# Product catalog (ids + labels + tags) — use this instead of hardcoding ids
for template in list_templates():
    print(template.id, template.label, template.experience_first)

document = ResumeDocument.model_validate(content_json)
html = populate_html_template(document, template_id="modern")
pdf_bytes = render_html_to_pdf(html)
```

Backend exposes the same catalog at `GET /api/v1/resume/templates`.

## Templates

| ID | Style | Best for |
|----|-------|----------|
| `professional` | Centered serif, traditional | Corporate, general |
| `executive` | Experience-first, navy serif/sans | Senior leadership |
| `modern` | Inter sans-serif, teal accent | Product, startups |
| `classic` | Times New Roman, ATS-maximum | Government, law |
| `compact` | Dense one-page, IBM Plex | Long career history |
| `tech` | Mono accents, indigo rail | Engineering, tech |
| `finance` | Baskerville + navy/gold | Banking, investment |
| `creative` | Outfit, terracotta accent | Design, marketing |
| `healthcare` | Calm teal, credential-forward | Clinical, nursing |
| `minimal` | Sparse whitespace, thin rules | Product, startups |
| `academic` | Garamond, double-rule header | Research, faculty |
| `sidebar` | Dark header band, sky accent | Mid-career general |
| `timeline` | Vertical timeline rail | Career progression |
| `bold` | Black header + amber underline | Sales, marketing |
| `consulting` | Tight navy strategy style | Consulting, strategy |

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