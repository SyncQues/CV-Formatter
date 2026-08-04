# Resume Template Catalog (v1.5.0)

HR-informed design notes for the **20** production templates in `sync_cv_formatter`.

## Architecture (all templates share)

| Layer | Contract |
|-------|----------|
| Schema | `ResumeDocument` / `ResumeTemplateId` in `schemas/resume_document.py` |
| HTML | `template.html.j2` + shared `_body_sections.html.j2` partials |
| CSS | Per-template `styles.css` (A4, semantic class names only) |
| Registry | `TEMPLATE_DIRS` + experience-first set in `renderers/html_renderer.py` |
| Catalog | `TEMPLATE_CATALOG` in `catalog.py` — **source of truth for ids + UI meta** |
| Consumers | Backend (preview/recompile), Resume service (generation), Frontend picker |

**ATS rules enforced across the catalog**

- Single-column DOM order (header → summary → sections); no tables for layout
- Semantic headings (`h1` name, `h2` sections, `h3` entries)
- Textual contact links (no icon-only contact)
- Standard body section ids: skills, experience, education, projects, achievements
- Decorative CSS only (rails, timelines, bands) — content remains parseable

**Experience-first defaults** (Work Experience above Skills):  
`executive`, `modern`, `tech`, `finance`, `consulting`, `bold`, `sidebar`, `timeline`, `noir`, `aurora`

---

## Core set (original 5)

| ID | Design rationale |
|----|------------------|
| `professional` | Centered serif default — matches traditional corporate hiring screens |
| `executive` | Navy leadership presence; experience leads for senior impact |
| `modern` | Teal Inter layout for product/startup culture fit |
| `classic` | Maximum ATS (Times, uppercase name, black/white) for strict parsers |
| `compact` | Dense one-pager for 10+ year careers that must stay on one page |

## Premium set

> **Total premium templates: 15** (10 industry + 5 creative batch).  
> Flag is catalog metadata for FE badges / billing. **This package does not enforce tier at render time** — consumers gate access.

### Industry (10) — `premium: true`

| ID | Industry / level | Layout cues | Why it converts |
|----|------------------|-------------|-----------------|
| `tech` | Software engineering | Indigo rail, mono name, code-like skill labels | Signals technical craft without graphics that break ATS |
| `finance` | Banking, investment, FP&A | Baskerville + navy/gold rule | Conservative trust palette used on Street and Big 4 resumes |
| `creative` | Design, marketing, brand | Outfit + terracotta mark | Personality for creative screens while staying text-first |
| `healthcare` | Clinical, nursing, allied health | Teal credential band | Calm, credential-forward readability for licensure-heavy roles |
| `minimal` | Product, design-aware tech | Sparse Inter, thin rules | Premium restraint; lets metrics dominate the page |
| `academic` | Research, faculty, PhD | EB Garamond, double-rule header | Formal education-first aesthetic for academic hiring |
| `sidebar` | Mid-career generalist | Dark header band + sky accent | High contrast identity block recruiters notice in stacks |
| `timeline` | Progression / career change | Vertical rail + date pills | Makes chronology obvious in 3-second scans |
| `bold` | Sales, marketing leadership | Black band + amber underline | High visual impact for results-driven narratives |
| `consulting` | Strategy, MBB, advisory | Tight navy serif/sans mix | Dense impact bullets, low decoration — case-interview ready |

### Creative batch (5) — also `premium: true`

| ID | Inspired by | Layout cues | Best for |
|----|-------------|-------------|----------|
| `portfolio` | creative + minimal | Fraunces display name, violet→pink gradient rule, project-friendly entries | Designers, makers, PDs |
| `editorial` | classic + academic | Playfair masthead, rose accent, justified summary, centered header | Writing, content, media |
| `studio` | modern + creative | Soft card header, magenta pill section labels, Space Grotesk | Freelancers, agencies |
| `noir` | bold + sidebar | Black cinematic band, fuchsia→cyan strip, Syne uppercase name | Film, fashion, brand |
| `aurora` | tech + modern | Teal→indigo gradient rail, Sora type, airy creative-tech | Creative tech, UX eng |

---

## Integration checklist (new template)

1. **Renderer**
   - Add `templates/html/<id>/{template.html.j2,styles.css}`
   - Add id to `ResumeTemplateId` Literal
   - Register in `TEMPLATE_DIRS`
   - Add `ResumeTemplateMeta` row to `TEMPLATE_CATALOG` in `catalog.py`
   - **Decide tier:** add the id to `_PREMIUM_TEMPLATE_IDS` in `catalog.py` if it is part of the paid catalog (the flag is stamped onto the meta row automatically)
   - `assert_catalog_integrity()` runs on package import
   - Bump version, `uv run pytest`, publish to PyPI
2. **Backend / Resume service** — bump `sync-cv-formatter` pin only  
   - `GET /api/v1/resume/templates` serves catalog automatically  
   - Validation uses `template_ids()` from the package
3. **Frontend** — **no code change required** for a new template  
   - Picker loads catalog from the API  
   - Paper mocks use `layout_family`; optional FE accent gradient map can be extended later
4. **Tests** — renderer catalog integrity + backend catalog endpoint

## Release

```bash
# In SyncQues-Resume-Renderer
uv run pytest
uv build
# tag v1.5.0 → publish to PyPI
# Then pin sync-cv-formatter==1.5.0 in Backend + Resume and uv lock
```

For **local monorepo testing**, Backend/Resume can use:

```toml
[tool.uv.sources]
sync-cv-formatter = { path = "../SyncQues-Resume-Renderer", editable = true }
```
