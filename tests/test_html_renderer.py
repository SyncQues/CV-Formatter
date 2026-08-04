from datetime import datetime, timezone

import pytest

from typing import get_args

from sync_cv_formatter import (
    DEFAULT_TEMPLATE_ID,
    assert_catalog_integrity,
    is_experience_first,
    list_templates,
    template_ids,
)
from sync_cv_formatter.renderers.html_renderer import (
    TEMPLATE_DIRS,
    populate_html_template,
    resolve_body_section_order,
)
from sync_cv_formatter.schemas.resume_document import (
    BasicsSection,
    CustomSection,
    CustomSectionEntry,
    ExperienceItem,
    ResumeDocument,
    ResumeDocumentMetadata,
    ResumeSections,
    ResumeTemplateId,
    SkillsSection,
)


def _sample_document() -> ResumeDocument:
    return ResumeDocument(
        basics=BasicsSection(
            full_name="Jane Doe",
            email="jane@example.com",
            summary="Software engineer with backend experience.",
        ),
        sections=ResumeSections(
            skills=SkillsSection(flat=["Python", "React"]),
            experience=[
                ExperienceItem(
                    title="Engineer",
                    company="SyncQues",
                    start_date="2024-01",
                    end_date="Present",
                    description="Built APIs\nImproved performance by 30%",
                )
            ],
        ),
        metadata=ResumeDocumentMetadata(
            generated_at=datetime.now(timezone.utc).isoformat(),
        ),
    )


def test_populate_html_template_renders_document():
    html = populate_html_template(_sample_document())

    assert "Jane Doe" in html
    assert "Software engineer with backend experience." in html
    assert "Built APIs" in html
    assert "<html" in html.lower()


def test_populate_html_template_includes_interactive_sections():
    html = populate_html_template(_sample_document(), interactive=True)

    assert 'data-resume-section="experience"' in html
    assert "cursor: pointer" in html


ALL_TEMPLATE_IDS = sorted(template_ids())


def test_catalog_integrity_and_public_api():
    assert_catalog_integrity()
    catalog = list_templates()
    assert len(catalog) == 20
    assert DEFAULT_TEMPLATE_ID == "professional"
    assert template_ids() == frozenset(get_args(ResumeTemplateId))
    assert template_ids() == frozenset(TEMPLATE_DIRS)
    assert is_experience_first("tech") is True
    assert is_experience_first("professional") is False
    assert all(item.label and item.swatch for item in catalog)
    premium = {item.id for item in catalog if item.premium}
    assert len(premium) == 15  # 10 industry premium + 5 creative batch
    assert "professional" not in premium
    assert "tech" in premium and "portfolio" in premium
    # Premium tier is listed first for picker UX
    first_free = next(i for i, item in enumerate(catalog) if not item.premium)
    assert all(item.premium for item in catalog[:first_free])
    assert all(not item.premium for item in catalog[first_free:])


@pytest.mark.parametrize("template_id", ALL_TEMPLATE_IDS)
def test_populate_html_template_renders_all_templates(template_id: str):
    document = _sample_document()
    document.template_id = template_id  # type: ignore[assignment]

    html = populate_html_template(document, template_id=template_id)  # type: ignore[arg-type]

    assert "Jane Doe" in html
    assert "Built APIs" in html
    assert "<html" in html.lower()
    assert "resume-page" in html


def test_creative_is_first_class_template():
    """creative is a real template (no longer an alias to modern)."""
    document = _sample_document()
    document.template_id = "creative"  # type: ignore[assignment]

    html = populate_html_template(document)

    assert "resume-header-mark" in html
    assert "Outfit" in html


@pytest.mark.parametrize(
    ("template_id", "marker"),
    [
        ("portfolio", "resume-name-rule"),
        ("editorial", "resume-masthead"),
        ("studio", "resume-header-chip"),
        ("noir", "resume-header-accent"),
        ("aurora", "resume-header-aurora"),
    ],
)
def test_creative_batch_has_distinct_chrome(template_id: str, marker: str):
    document = _sample_document()
    document.template_id = template_id  # type: ignore[assignment]

    html = populate_html_template(document, template_id=template_id)  # type: ignore[arg-type]

    assert marker in html
    assert "Jane Doe" in html


def test_custom_sections_render_in_html():
    document = _sample_document()
    document.sections.custom = [
        CustomSection(
            id="opensource-1",
            title="Opensource",
            items=[
                CustomSectionEntry(
                    title="Redis",
                    location="Hyderabad",
                    start_date="Jun 2026",
                    end_date="Present",
                    description="Contributed core module fixes\nImproved docs",
                    link_url="https://www.youtube.com/",
                    link_label="Youtube",
                )
            ],
        )
    ]
    document.sections.section_order = [
        "skills",
        "experience",
        "education",
        "projects",
        "achievements",
        "custom:opensource-1",
    ]

    html = populate_html_template(document, template_id="professional")

    assert "Opensource" in html
    assert "Redis" in html
    assert "Hyderabad" in html
    assert "Contributed core module fixes" in html
    assert 'data-resume-section="custom:opensource-1"' in html
    assert "https://www.youtube.com/" in html
    # Link is in the right-side header column (under date), not below description
    assert 'class="entry-aside"' in html
    aside_start = html.index('class="entry-aside"')
    desc_start = html.index("Contributed core module fixes")
    link_start = html.index("https://www.youtube.com/")
    assert aside_start < link_start < desc_start
    date_in_aside = html.index("entry-date", aside_start)
    links_in_aside = html.index("entry-links", aside_start)
    assert date_in_aside < links_in_aside


def test_custom_section_multiple_links_render_under_date():
    from sync_cv_formatter.schemas.resume_document import CustomSectionLink

    document = _sample_document()
    document.sections.custom = [
        CustomSection(
            id="oss-2",
            title="Open Source",
            items=[
                CustomSectionEntry(
                    title="Cool Project",
                    start_date="2026-02",
                    end_date="2026-01",
                    description="Did things",
                    links=[
                        CustomSectionLink(url="https://github.com/example/repo", label="Repo"),
                        CustomSectionLink(url="https://example.com/demo", label="Demo"),
                    ],
                )
            ],
        )
    ]
    document.sections.section_order = ["custom:oss-2", "skills"]

    html = populate_html_template(document, template_id="professional")

    assert "Repo" in html
    assert "Demo" in html
    assert "https://github.com/example/repo" in html
    assert "https://example.com/demo" in html
    aside_start = html.index('class="entry-aside"')
    date_idx = html.index("entry-date", aside_start)
    links_idx = html.index("entry-links", aside_start)
    repo_idx = html.index("https://github.com/example/repo")
    demo_idx = html.index("https://example.com/demo")
    desc_idx = html.index("Did things")
    assert date_idx < links_idx < repo_idx < demo_idx < desc_idx


def test_section_order_places_custom_before_skills():
    document = _sample_document()
    document.sections.custom = [
        CustomSection(
            id="vol-1",
            title="Volunteer",
            items=[CustomSectionEntry(title="Mentor", description="Helped juniors")],
        )
    ]
    document.sections.section_order = [
        "custom:vol-1",
        "experience",
        "skills",
        "education",
        "projects",
        "achievements",
    ]

    order = resolve_body_section_order(document, "professional")
    assert order[0] == "custom:vol-1"
    assert order.index("experience") < order.index("skills")

    html = populate_html_template(document, template_id="professional")
    volunteer_pos = html.index("Volunteer")
    skills_pos = html.index("Technical Skills")
    assert volunteer_pos < skills_pos


def test_model_validate_preserves_custom_sections():
    payload = {
        "schema_version": "1.0",
        "template_id": "professional",
        "basics": {"full_name": "Test", "email": "t@e.com"},
        "sections": {
            "skills": {"flat": [], "categorized": {}},
            "experience": [],
            "education": [],
            "projects": [],
            "achievements": [],
            "custom": [
                {
                    "id": "abc",
                    "title": "Opensource",
                    "items": [
                        {
                            "title": "Redis",
                            "description": "did stuff",
                            "link_url": "https://example.com",
                        }
                    ],
                }
            ],
            "section_order": ["custom:abc", "skills"],
        },
        "metadata": {
            "generated_at": "2026-07-21T00:00:00+00:00",
            "resume_type": "standard",
            "content_version": 1,
        },
    }
    document = ResumeDocument.model_validate(payload)
    assert len(document.sections.custom) == 1
    assert document.sections.custom[0].title == "Opensource"
    assert document.sections.section_order[0] == "custom:abc"

    html = populate_html_template(document)
    assert "Opensource" in html
    assert "Redis" in html
