from datetime import datetime, timezone
from typing import Literal

from pydantic import BaseModel, Field, model_validator

ResumeTemplateId = Literal["professional", "executive", "modern", "classic", "compact"]
ResumeTypeValue = Literal["standard", "ats_optimized"]

BUILTIN_BODY_SECTION_IDS: tuple[str, ...] = (
    "skills",
    "experience",
    "education",
    "projects",
    "achievements",
)

DEFAULT_BODY_SECTION_ORDER: tuple[str, ...] = BUILTIN_BODY_SECTION_IDS
EXPERIENCE_FIRST_BODY_SECTION_ORDER: tuple[str, ...] = (
    "experience",
    "skills",
    "education",
    "projects",
    "achievements",
)


class BasicsSection(BaseModel):
    full_name: str = ""
    email: str = ""
    phone: str | None = None
    location: str | None = None
    summary: str | None = None
    syncques_url: str | None = None
    social_links: dict[str, str] = Field(default_factory=dict)


class SkillsSection(BaseModel):
    flat: list[str] = Field(default_factory=list)
    categorized: dict[str, list[str]] = Field(default_factory=dict)


class ExperienceItem(BaseModel):
    title: str = ""
    company: str = ""
    location: str | None = None
    start_date: str | None = None
    end_date: str | None = "Present"
    description: str = ""


class EducationItem(BaseModel):
    institution: str = ""
    degree: str = ""
    field_of_study: str | None = None
    location: str | None = None
    start_date: str | None = None
    end_date: str | None = "Present"
    gpa: str | None = None
    description: str | None = None


class ProjectItem(BaseModel):
    title: str = ""
    description: str = ""
    technologies: list[str] = Field(default_factory=list)
    project_url: str | None = None
    repository_url: str | None = None
    start_date: str | None = None
    end_date: str | None = None


class AchievementItem(BaseModel):
    title: str = ""
    organization: str | None = None
    description: str | None = None
    date_earned: str | None = None
    credential_url: str | None = None


class CustomSectionLink(BaseModel):
    """One external link on a custom section entry (paper, demo, repo, …)."""

    url: str = ""
    label: str | None = None


class CustomSectionEntry(BaseModel):
    """Single entry inside a user-defined custom section."""

    title: str = ""
    subtitle: str | None = None
    location: str | None = None
    start_date: str | None = None
    end_date: str | None = None
    description: str | None = None
    # Preferred multi-link field (date above, links below on the right).
    links: list[CustomSectionLink] = Field(default_factory=list)
    # Legacy single-link fields — migrated into `links` on validate.
    link_url: str | None = None
    link_label: str | None = None

    @model_validator(mode="after")
    def _migrate_legacy_link(self) -> "CustomSectionEntry":
        cleaned = [link for link in self.links if (link.url or "").strip()]
        if cleaned:
            object.__setattr__(self, "links", cleaned[:5])
            return self
        if self.link_url and self.link_url.strip():
            object.__setattr__(
                self,
                "links",
                [
                    CustomSectionLink(
                        url=self.link_url.strip(),
                        label=self.link_label,
                    )
                ],
            )
        return self


class CustomSection(BaseModel):
    """User-defined section (Volunteer, Publications, Languages, etc.)."""

    id: str = ""
    title: str = ""
    items: list[CustomSectionEntry] = Field(default_factory=list)


class ResumeSections(BaseModel):
    skills: SkillsSection = Field(default_factory=SkillsSection)
    experience: list[ExperienceItem] = Field(default_factory=list)
    education: list[EducationItem] = Field(default_factory=list)
    projects: list[ProjectItem] = Field(default_factory=list)
    achievements: list[AchievementItem] = Field(default_factory=list)
    custom: list[CustomSection] = Field(default_factory=list)
    # Builtin keys and/or `custom:<id>` tokens controlling body section order.
    section_order: list[str] = Field(default_factory=list)


class ResumeDocumentMetadata(BaseModel):
    generated_at: str
    resume_type: ResumeTypeValue = "standard"
    job_title: str | None = None
    job_description: str | None = None
    last_edited_at: str | None = None
    content_version: int = 1


class ResumeDocument(BaseModel):
    schema_version: str = "1.0"
    template_id: ResumeTemplateId = "professional"
    basics: BasicsSection = Field(default_factory=BasicsSection)
    sections: ResumeSections = Field(default_factory=ResumeSections)
    metadata: ResumeDocumentMetadata

    @classmethod
    def default_metadata(
        cls,
        resume_type: ResumeTypeValue = "standard",
        job_title: str | None = None,
        job_description: str | None = None,
    ) -> ResumeDocumentMetadata:
        return ResumeDocumentMetadata(
            generated_at=datetime.now(timezone.utc).isoformat(),
            resume_type=resume_type,
            job_title=job_title,
            job_description=job_description,
            content_version=1,
        )
