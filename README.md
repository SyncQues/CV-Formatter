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
    print(template.id, template.label, template.premium, template.experience_first)

document = ResumeDocument.model_validate(content_json)
html = populate_html_template(document, template_id="modern")
pdf_bytes = render_html_to_pdf(html)
```

Backend exposes the same catalog at `GET /api/v1/resume/templates`.

## Templates

**20 templates** total. Design notes live in [`TEMPLATES.md`](./TEMPLATES.md).

**Premium tier (metadata only):** 15 templates carry `premium: true` for picker badges and billing UX (5 core + 10 industry). The five free templates are the creative batch: `portfolio`, `editorial`, `studio`, `noir`, and `aurora`. This package is a **renderer only** — it does not gate rendering on tier; consumers (Backend / FE) enforce paid access using catalog helpers such as `is_premium()` and `list_templates()`.

| ID | Style | Best for | Tier |
|----|-------|----------|------|
| `professional` | Centered serif, traditional | Corporate, general | Premium |
| `executive` | Experience-first, navy serif/sans | Senior leadership | Premium |
| `modern` | Inter sans-serif, teal accent | Product, startups | Premium |
| `classic` | Times New Roman, ATS-maximum | Government, law | Premium |
| `compact` | Dense one-page, IBM Plex | Long career history | Premium |
| `tech` | Mono accents, indigo rail | Engineering, tech | Premium |
| `finance` | Baskerville + navy/gold | Banking, investment | Premium |
| `creative` | Outfit, terracotta accent | Design, marketing | Premium |
| `healthcare` | Calm teal, credential-forward | Clinical, nursing | Premium |
| `minimal` | Sparse whitespace, thin rules | Product, startups | Premium |
| `academic` | Garamond, double-rule header | Research, faculty | Premium |
| `sidebar` | Dark header band, sky accent | Mid-career general | Premium |
| `timeline` | Vertical timeline rail | Career progression | Premium |
| `bold` | Black header + amber underline | Sales, marketing | Premium |
| `consulting` | Tight navy strategy style | Consulting, strategy | Premium |
| `portfolio` | Fraunces display, violet→pink gradient | Designers, PDs | Free |
| `editorial` | Playfair masthead, rose accent | Writing, media | Free |
| `studio` | Soft card header, magenta pills | Freelancers | Free |
| `noir` | Cinematic black band, fuchsia→cyan | Film, fashion | Free |
| `aurora` | Teal→indigo gradient rail, Sora | UX eng, creative tech | Free |

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

### 1.5.0 notes

- **20 templates** via catalog SoT (`list_templates()` / `ResumeTemplateMeta`), including a creative batch and a `premium` flag for product UI.
- **`creative` is first-class** (Outfit + `resume-header-mark`). In ≤1.3.1, `template_id="creative"` was a renderer alias for `modern`. Callers that still expect modern chrome should pass `"modern"` explicitly. `ResumeTemplateId` also accepts the new ids that previously failed schema validation.