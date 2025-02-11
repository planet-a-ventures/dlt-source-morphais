# generated by datamodel-codegen:
#   filename:  2025-02-10.yaml

from __future__ import annotations

from datetime import date
from enum import Enum
from typing import Annotated, List
from uuid import UUID

from pydantic import AnyUrl, BaseModel, Field


class StartupListItem(BaseModel):
    id: UUID
    """
    Unique identifier for the startup.
    """
    name: str
    """
    Name of the startup.
    """
    desc_short: str
    """
    A short description of the startup.
    """


class Resources(BaseModel):
    website: AnyUrl | None = None
    """
    Website URL of the startup.
    """
    linkedin: AnyUrl | None = None
    """
    LinkedIn profile URL.
    """
    facebook: AnyUrl | None = None
    """
    Facebook page URL.
    """
    twitter: AnyUrl | None = None
    """
    Twitter profile URL.
    """
    github: AnyUrl | None = None
    """
    GitHub repository URL.
    """
    filling_history: AnyUrl | None = None
    """
    Filing registry URL.
    """


class ExperienceStart(Enum):
    NO_START_DATE = "No start date"


class ExperienceEnd(Enum):
    PRESENT = "Present"


class Experience(BaseModel):
    experience_company: str | None = None
    """
    Name of the company where the experience was gained.
    """
    experience_founder: int
    """
    Indicator if the person is a founder (0 or 1).
    """
    role: str
    """
    Role of the person at the company.
    """
    experience_start: date | ExperienceStart
    """
    Start date of the experience, or "No start date" if unknown.
    """
    experience_end: date | ExperienceEnd
    """
    End date of the experience (or "Present" if ongoing).
    """


class EducationStart(Enum):
    NO_START_DATE = "No start date"


class EducationEnd(Enum):
    PRESENT = "Present"


class Education(BaseModel):
    education_school: str | None = None
    """
    Name of the school or college.
    """
    education_degree: str
    """
    Degree obtained.
    """
    education_subject: str | None = None
    """
    Subject studied.
    """
    education_start: date | EducationStart
    """
    Start date of the education, or "No start date" if unknown.
    """
    education_end: date | EducationEnd
    """
    End date of the education, or "Present" if the education is ongoing.
    """


class Person(BaseModel):
    person_name: str
    """
    Name of the person.
    """
    person_linkedin: AnyUrl | None = None
    """
    LinkedIn profile URL of the person.
    """
    highlights: List[str]
    """
    List of highlights for the person.
    """
    gender: str | None = None
    """
    Gender of the person.
    """
    experience: List[Experience]
    """
    Work experience of the person.
    """
    education: List[Education]
    """
    Educational background of the person.
    """


class Startup(BaseModel):
    id: UUID
    """
    Unique identifier for the startup.
    """
    name: str
    """
    Name of the startup.
    """
    desc_short: str
    """
    A short description of the startup.
    """
    desc_long: str
    """
    A long description of the startup.
    """
    industries: List[str]
    """
    List of industries associated with the startup.
    """
    solutions: List[str]
    """
    List of solutions provided by the startup.
    """
    resources: Resources
    """
    Social and external resources related to the startup.
    """
    founding_date: date
    """
    The founding date of the startup.
    """
    funding_stage: str
    """
    The funding stage of the startup.
    """
    registry_id: str | None = None
    """
    Registry identifier.
    """
    legal_form: Annotated[str, Field(examples=["Ltd."])]
    """
    Legal form of the startup.
    """
    audience: Annotated[str | None, Field(examples=["B2C"])] = None
    """
    The target audience.
    """
    city: str
    """
    City where the startup is located.
    """
    country: str
    """
    Country where the startup is located.
    """
    address: str
    """
    Address of the startup.
    """
    persons: List[Person]
    """
    List of persons (e.g., founders) associated with the startup.
    """
