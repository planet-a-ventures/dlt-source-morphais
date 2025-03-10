# generated by datamodel-codegen:
#   filename:  2025-02-10.openapi.yaml

from __future__ import annotations

from datetime import date
from enum import Enum
from typing import Annotated, List
from uuid import UUID

from pydantic import AnyUrl, Field, constr

from . import MyBaseModel


class ErrorResponse(MyBaseModel):
    error: Annotated[
        str | None, Field(examples=["There are no startups available."])
    ] = None


class StartupListItem(MyBaseModel):
    id: UUID
    """
    Unique identifier for the startup.
    """
    name: str | None = None
    """
    Name of the startup.
    """
    desc_short: str | None = None
    """
    A short description of the startup.
    """


class Resources(MyBaseModel):
    website: (
        AnyUrl
        | constr(
            pattern=r"^(([a-zA-Z0-9] | [a-zA-Z0-9][a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])\.)*([A-Za-z0-9] | [A-Za-z0-9][A-Za-z0-9\-]{0,61}[A-Za-z0-9])$"
        )
        | None
    ) = None
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


class Gender(Enum):
    MALE = "Male"
    FEMALE = "Female"


class ExperienceStart(Enum):
    NO_START_DATE = "No start date"


class ExperienceEnd(Enum):
    PRESENT = "Present"


class Experience(MyBaseModel):
    experience_company: str | None = None
    """
    Name of the company where the experience was gained.
    """
    experience_founder: int
    """
    Indicator if the person is a founder (0 or 1).
    """
    role: str | None = None
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


class Education(MyBaseModel):
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


class Person(MyBaseModel):
    person_name: str | None = None
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
    gender: Gender | None
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


class Startup(MyBaseModel):
    id: UUID
    """
    Unique identifier for the startup.
    """
    name: str | None = None
    """
    Name of the startup.
    """
    desc_short: str | None = None
    """
    A short description of the startup.
    """
    desc_long: str | None = None
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
    founding_date: date | None = None
    """
    The founding date of the startup.
    """
    funding_stage: str | None = None
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
    city: str | None = None
    """
    City where the startup is located.
    """
    country: str | None = None
    """
    Country where the startup is located.
    """
    address: str | None = None
    """
    Address of the startup.
    """
    persons: List[Person]
    """
    List of persons (e.g., founders) associated with the startup.
    """
