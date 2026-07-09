from datetime import datetime, timezone
from typing import Literal

from pydantic import BaseModel, Field

ResumeTemplateId = Literal["professional", "executive", "modern", "classic", "compact"]
ResumeTypeValue = Literal["standard", "ats_optimized"]


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


class ResumeSections(BaseModel):
    skills: SkillsSection = Field(default_factory=SkillsSection)
    experience: list[ExperienceItem] = Field(default_factory=list)
    education: list[EducationItem] = Field(default_factory=list)
    projects: list[ProjectItem] = Field(default_factory=list)
    achievements: list[AchievementItem] = Field(default_factory=list)


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