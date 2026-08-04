from sync_cv_formatter.catalog import (
    DEFAULT_TEMPLATE_ID,
    ResumeTemplateMeta,
    assert_catalog_integrity,
    experience_first_template_ids,
    free_template_ids,
    get_template_meta,
    is_experience_first,
    is_premium,
    list_templates,
    premium_template_ids,
    template_ids,
)
from sync_cv_formatter.renderers.html_renderer import (
    populate_html_template,
    save_html_file,
)
from sync_cv_formatter.renderers.pdf_renderer import render_html_to_pdf
from sync_cv_formatter.schemas.resume_document import ResumeDocument

# Ensure catalog, Literal, and on-disk templates stay aligned at import time.
assert_catalog_integrity()

__all__ = [
    "DEFAULT_TEMPLATE_ID",
    "ResumeDocument",
    "ResumeTemplateMeta",
    "assert_catalog_integrity",
    "experience_first_template_ids",
    "free_template_ids",
    "get_template_meta",
    "is_experience_first",
    "is_premium",
    "list_templates",
    "populate_html_template",
    "premium_template_ids",
    "render_html_to_pdf",
    "save_html_file",
    "template_ids",
]