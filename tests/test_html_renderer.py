from datetime import datetime, timezone

from syncques_resume_renderer.renderers.html_renderer import populate_html_template
from syncques_resume_renderer.schemas.resume_document import (
    BasicsSection,
    ExperienceItem,
    ResumeDocument,
    ResumeDocumentMetadata,
    ResumeSections,
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