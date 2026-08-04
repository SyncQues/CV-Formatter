"""Public resume template catalog — single source of truth for ids + UI metadata.

Consumers (Backend, Frontend via API) should list templates from here rather than
hardcoding ids. Adding a template means: add files under templates/html/<id>/,
register in TEMPLATE_DIRS + ResumeTemplateId, and add a row to TEMPLATE_CATALOG.

Premium is **metadata only** for badges / billing UX. This package is a renderer;
tier enforcement (who may select a premium id) is the consumer's responsibility.
"""

from __future__ import annotations

from typing import get_args

from pydantic import BaseModel, Field

from sync_cv_formatter.schemas.resume_document import ResumeTemplateId

DEFAULT_TEMPLATE_ID: ResumeTemplateId = "professional"

# Layout families hint clients how to draw paper mocks / accents.
# Kept stable so frontends can map a small set of visual chrome styles.
LayoutFamily = str


class ResumeTemplateMeta(BaseModel):
    """Product-facing metadata for one renderable template."""

    id: ResumeTemplateId
    label: str
    description: str
    best_for: str = Field(description="Short audience / industry hint for the picker")
    tags: list[str] = Field(default_factory=list)
    recommended: bool = False
    premium: bool = False
    """When true, clients should show a Premium badge (paid / premium catalog tier)."""
    experience_first: bool = False
    """When true, default section order puts Work Experience above Skills."""
    swatch: tuple[str, str] = Field(
        description="[ink, paper] hex colors for picker chrome",
    )
    layout_family: LayoutFamily = "standard"
    """Hint for client-side paper mocks: standard | accent_rail | dark_header | timeline | sparse | creative | academic | compact."""


# Premium tier: core 5 + 10 industry batch.
# Creative batch (portfolio, editorial, studio, noir, aurora) stays non-premium.
_PREMIUM_TEMPLATE_IDS: frozenset[str] = frozenset(
    {
        "professional",
        "executive",
        "modern",
        "classic",
        "compact",
        "tech",
        "finance",
        "creative",
        "healthcare",
        "minimal",
        "academic",
        "sidebar",
        "timeline",
        "bold",
        "consulting",
    }
)


def _apply_premium_flags(
    catalog: tuple[ResumeTemplateMeta, ...],
) -> tuple[ResumeTemplateMeta, ...]:
    """Stamp premium=True on the premium catalog tier (single place to maintain)."""
    return tuple(
        item.model_copy(update={"premium": item.id in _PREMIUM_TEMPLATE_IDS})
        for item in catalog
    )


def _sort_premium_first(
    catalog: tuple[ResumeTemplateMeta, ...],
) -> tuple[ResumeTemplateMeta, ...]:
    """Premium tier first, then free — stable within each group."""
    premium = tuple(item for item in catalog if item.premium)
    free = tuple(item for item in catalog if not item.premium)
    return premium + free


TEMPLATE_CATALOG: tuple[ResumeTemplateMeta, ...] = _sort_premium_first(
    _apply_premium_flags((
    ResumeTemplateMeta(
        id="professional",
        label="Professional",
        description=(
            "Centered serif header with clear section hierarchy — the default "
            "recruiters expect in traditional hiring."
        ),
        best_for="Corporate, general applications",
        tags=["ATS-friendly", "Serif", "Classic"],
        recommended=True,
        experience_first=False,
        swatch=("#1e293b", "#f8fafc"),
        layout_family="standard",
    ),
    ResumeTemplateMeta(
        id="executive",
        label="Executive",
        description=(
            "Experience-first layout with confident typography that puts impact "
            "and leadership front and center."
        ),
        best_for="Senior & leadership roles",
        tags=["ATS-friendly", "Impact-first"],
        experience_first=True,
        swatch=("#312e81", "#eef2ff"),
        layout_family="standard",
    ),
    ResumeTemplateMeta(
        id="modern",
        label="Modern",
        description=(
            "Clean sans-serif spacing and contemporary rhythm that feels at home "
            "in product and engineering orgs."
        ),
        best_for="Product, startups",
        tags=["ATS-friendly", "Sans-serif"],
        experience_first=True,
        swatch=("#0369a1", "#f0f9ff"),
        layout_family="accent_rail",
    ),
    ResumeTemplateMeta(
        id="classic",
        label="Classic",
        description=(
            "Conservative black-and-white formatting with maximum parser "
            "compatibility for strict ATS pipelines."
        ),
        best_for="Government, law",
        tags=["Maximum ATS", "Minimal"],
        experience_first=False,
        swatch=("#3f3f46", "#fafafa"),
        layout_family="academic",
    ),
    ResumeTemplateMeta(
        id="compact",
        label="Compact",
        description=(
            "Dense, efficient one-page layout that packs extensive experience "
            "without sacrificing scannability."
        ),
        best_for="10+ years experience",
        tags=["One-page", "Dense"],
        experience_first=False,
        swatch=("#047857", "#ecfdf5"),
        layout_family="compact",
    ),
    ResumeTemplateMeta(
        id="tech",
        label="Tech",
        description=(
            "Engineering-forward layout with mono accents and a sharp indigo rail "
            "— scans like a product ship log."
        ),
        best_for="Software engineering, tech",
        tags=["ATS-friendly", "Experience-first", "Tech"],
        experience_first=True,
        swatch=("#4f46e5", "#eef2ff"),
        layout_family="accent_rail",
    ),
    ResumeTemplateMeta(
        id="finance",
        label="Finance",
        description=(
            "Conservative Baskerville header with navy and subtle gold — the look "
            "investment desks trust."
        ),
        best_for="Banking, investment, FP&A",
        tags=["ATS-friendly", "Serif", "Conservative"],
        experience_first=True,
        swatch=("#0f2744", "#f5f0e8"),
        layout_family="standard",
    ),
    ResumeTemplateMeta(
        id="creative",
        label="Creative",
        description=(
            "Distinctive terracotta accent and modern Outfit type — personality "
            "without breaking ATS parsers."
        ),
        best_for="Design, marketing, brand",
        tags=["ATS-friendly", "Visual", "Creative"],
        experience_first=False,
        swatch=("#c2410c", "#fff7ed"),
        layout_family="creative",
    ),
    ResumeTemplateMeta(
        id="healthcare",
        label="Healthcare",
        description=(
            "Calm teal treatment that prioritizes credentials, licenses, and "
            "clinical clarity for care roles."
        ),
        best_for="Clinical, nursing, health",
        tags=["ATS-friendly", "Credential-forward"],
        experience_first=False,
        swatch=("#0f766e", "#f0fdfa"),
        layout_family="creative",
    ),
    ResumeTemplateMeta(
        id="minimal",
        label="Minimal",
        description=(
            "Maximum whitespace and thin rules — refined restraint that lets "
            "achievements carry the page."
        ),
        best_for="Product, design-aware tech",
        tags=["ATS-friendly", "Sparse", "Premium"],
        experience_first=False,
        swatch=("#111111", "#fafafa"),
        layout_family="sparse",
    ),
    ResumeTemplateMeta(
        id="academic",
        label="Academic",
        description=(
            "Garamond header with double-rule formality — ideal when education "
            "and publications lead."
        ),
        best_for="Research, faculty, PhD",
        tags=["ATS-friendly", "Traditional", "Education"],
        experience_first=False,
        swatch=("#7f1d1d", "#fafaf9"),
        layout_family="academic",
    ),
    ResumeTemplateMeta(
        id="sidebar",
        label="Sidebar",
        description=(
            "High-contrast dark header band with sky accent — modern "
            "recruiter-friendly hierarchy."
        ),
        best_for="Mid-career generalists",
        tags=["ATS-friendly", "Bold header"],
        experience_first=True,
        swatch=("#0f172a", "#e0f2fe"),
        layout_family="dark_header",
    ),
    ResumeTemplateMeta(
        id="timeline",
        label="Timeline",
        description=(
            "Vertical timeline rail and date pills that make career progression "
            "easy to scan in seconds."
        ),
        best_for="Career changers, progression stories",
        tags=["ATS-friendly", "Timeline", "Scannable"],
        experience_first=True,
        swatch=("#2563eb", "#eff6ff"),
        layout_family="timeline",
    ),
    ResumeTemplateMeta(
        id="bold",
        label="Bold",
        description=(
            "Black header band with amber underline — high visual impact for "
            "results-driven roles."
        ),
        best_for="Sales, marketing leadership",
        tags=["ATS-friendly", "High impact"],
        experience_first=True,
        swatch=("#111827", "#fffbeb"),
        layout_family="dark_header",
    ),
    ResumeTemplateMeta(
        id="consulting",
        label="Consulting",
        description=(
            "Tight, precise navy strategy styling — dense impact bullets without "
            "visual noise."
        ),
        best_for="Consulting, strategy, MBB",
        tags=["ATS-friendly", "Experience-first", "Dense"],
        experience_first=True,
        swatch=("#1e3a5f", "#f8fafc"),
        layout_family="standard",
    ),
    # --- Creative batch (new + inspired by current catalog) ---
    ResumeTemplateMeta(
        id="portfolio",
        label="Portfolio",
        description=(
            "Display-serif name with a dual-tone accent bar — built for designers "
            "and makers who want projects to feel curated (from creative + minimal)."
        ),
        best_for="Designers, product design, makers",
        tags=["ATS-friendly", "Visual", "Creative", "Projects"],
        experience_first=False,
        swatch=("#7c3aed", "#f5f3ff"),
        layout_family="creative",
    ),
    ResumeTemplateMeta(
        id="editorial",
        label="Editorial",
        description=(
            "Magazine masthead and Playfair display type — literary presence with "
            "justified summary (from classic + academic, more expressive)."
        ),
        best_for="Writing, content, media, journalism",
        tags=["ATS-friendly", "Serif", "Creative", "Media"],
        experience_first=False,
        swatch=("#9f1239", "#fff1f2"),
        layout_family="academic",
    ),
    ResumeTemplateMeta(
        id="studio",
        label="Studio",
        description=(
            "Soft studio card header, pill section labels, and rounded accent chip "
            "— agency energy without multi-column layout (from modern + creative)."
        ),
        best_for="Freelancers, agencies, brand studios",
        tags=["ATS-friendly", "Creative", "Modern"],
        experience_first=False,
        swatch=("#a21caf", "#fdf4ff"),
        layout_family="creative",
    ),
    ResumeTemplateMeta(
        id="noir",
        label="Noir",
        description=(
            "Cinematic black header band with fuchsia→cyan accent strip — high "
            "contrast impact (from bold + sidebar, more fashion/media)."
        ),
        best_for="Film, fashion, brand, creative leadership",
        tags=["ATS-friendly", "High impact", "Creative"],
        experience_first=True,
        swatch=("#09090b", "#fae8ff"),
        layout_family="dark_header",
    ),
    ResumeTemplateMeta(
        id="aurora",
        label="Aurora",
        description=(
            "Gradient teal→indigo aurora rail and airy Sora type — creative-tech "
            "polish that still scans like a clean product resume (from tech + modern)."
        ),
        best_for="Creative tech, UX engineering, product design",
        tags=["ATS-friendly", "Gradient accent", "Creative", "Tech"],
        experience_first=True,
        swatch=("#0d9488", "#ecfeff"),
        layout_family="accent_rail",
    ),
    ))
)

_CATALOG_BY_ID: dict[str, ResumeTemplateMeta] = {item.id: item for item in TEMPLATE_CATALOG}


def list_templates() -> list[ResumeTemplateMeta]:
    """Return all public templates ordered premium-first, then free (stable picker UX)."""
    return list(TEMPLATE_CATALOG)


def template_ids() -> frozenset[str]:
    """Set of valid template ids (for validation)."""
    return frozenset(_CATALOG_BY_ID)


def get_template_meta(template_id: str | None) -> ResumeTemplateMeta | None:
    """Lookup catalog entry by id (case-insensitive)."""
    if not template_id:
        return None
    return _CATALOG_BY_ID.get(str(template_id).strip().lower())


def is_experience_first(template_id: str | None) -> bool:
    """Whether the template defaults to experience-before-skills section order."""
    meta = get_template_meta(template_id)
    return bool(meta and meta.experience_first)


def experience_first_template_ids() -> frozenset[str]:
    return frozenset(item.id for item in TEMPLATE_CATALOG if item.experience_first)


def is_premium(template_id: str | None) -> bool:
    """Whether the template is in the paid / premium catalog tier (metadata only)."""
    meta = get_template_meta(template_id)
    return bool(meta and meta.premium)


def premium_template_ids() -> frozenset[str]:
    """Ids stamped premium=True for FE badges and consumer-side access checks."""
    return frozenset(item.id for item in TEMPLATE_CATALOG if item.premium)


def free_template_ids() -> frozenset[str]:
    """Ids that are not in the premium catalog tier."""
    return frozenset(item.id for item in TEMPLATE_CATALOG if not item.premium)


def assert_catalog_integrity() -> None:
    """Fail fast if catalog, Literal, and template dirs drift apart."""
    from sync_cv_formatter.renderers.html_renderer import TEMPLATE_DIRS

    literal_ids = frozenset(get_args(ResumeTemplateId))
    catalog_ids = template_ids()
    dir_ids = frozenset(TEMPLATE_DIRS)

    if catalog_ids != literal_ids:
        raise RuntimeError(
            f"TEMPLATE_CATALOG ids {sorted(catalog_ids)} != "
            f"ResumeTemplateId literal {sorted(literal_ids)}"
        )
    if catalog_ids != dir_ids:
        raise RuntimeError(
            f"TEMPLATE_CATALOG ids {sorted(catalog_ids)} != "
            f"TEMPLATE_DIRS keys {sorted(dir_ids)}"
        )
    if DEFAULT_TEMPLATE_ID not in catalog_ids:
        raise RuntimeError(f"DEFAULT_TEMPLATE_ID '{DEFAULT_TEMPLATE_ID}' missing from catalog")


__all__ = [
    "DEFAULT_TEMPLATE_ID",
    "ResumeTemplateMeta",
    "TEMPLATE_CATALOG",
    "assert_catalog_integrity",
    "experience_first_template_ids",
    "free_template_ids",
    "get_template_meta",
    "is_experience_first",
    "is_premium",
    "list_templates",
    "premium_template_ids",
    "template_ids",
]
