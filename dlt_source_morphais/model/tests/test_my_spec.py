from datetime import date
import json

from .. import Degree, LegalForm, FundingStage
from ..spec import EducationEnd, EducationStart, Startup, ExperienceEnd, ExperienceStart

base = {
    "id": "123e4567-e89b-12d3-a456-426614174000",
    "name": "Example Startup",
    "desc_long": "A long description",
    "industries": ["Tech"],
    "solutions": ["Software"],
    "legal_form": "Ltd.",
    "country": "United Kingdom",
    "persons": [],
    "resources": {},
}


def test_domain_only_website():

    d = {
        **base,
        "resources": {"website": "www.example.com"},
    }

    s = Startup(**d)
    assert s.resources.website.unicode_string() == "http://www.example.com/"

    str_d = json.dumps(d)
    s2 = Startup.model_validate_json(str_d)
    assert s2.resources.website.unicode_string() == "http://www.example.com/"


def test_degree_unknown():
    d = {
        **base,
        "persons": [
            {
                "person_name": "John Doe",
                "gender": None,
                "experience": [],
                "highlights": [],
                "education": [
                    {
                        "education_start": "2021-01-01",
                        "education_end": "2021-02-01",
                        "education_degree": Degree.UNKNOWN.value,
                    }
                ],
            }
        ],
    }
    s = Startup(**d)
    assert s.persons[0].education[0].education_degree is None


def test_date():
    d = {
        **base,
        "founding_date": "2021-01-01",
    }
    s = Startup(**d)
    assert s.founding_date == date(2021, 1, 1)


def test_legal_form():
    d = {
        **base,
        "legal_form": LegalForm.NO_LEGAL_FORM.value,
    }
    s = Startup(**d)
    assert s.legal_form is None


def test_funding_stage():
    d = {
        **base,
        "funding_stage": FundingStage.NO_FUNDING_ROUND.value,
    }
    s = Startup(**d)
    assert s.funding_stage is None


def test_date_broken():
    d = {
        **base,
        "founding_date": "not_a_date",
    }
    s = Startup(**d)
    assert s.founding_date is None

    d = {
        **base,
        "persons": [
            {
                "person_name": "John Doe",
                "highlights": [],
                "gender": None,
                "education": [
                    {
                        "education_degree": "My degree",
                        "education_start": "not_a_date",
                        "education_end": "not_a_date",
                    }
                ],
                "experience": [
                    {
                        "experience_founder": 0,
                        "experience_start": "not_a_date",
                        "experience_end": "not_a_date",
                    }
                ],
            }
        ],
    }
    s = Startup(**d)
    assert s.persons[0].education[0].education_start is None
    assert s.persons[0].education[0].education_end is None
    assert s.persons[0].experience[0].experience_start is None
    assert s.persons[0].experience[0].experience_end is None


def test_date_not_sane():
    d = {
        **base,
        "persons": [
            {
                "person_name": "John Doe",
                "highlights": [],
                "gender": None,
                "education": [
                    {
                        "education_degree": "My degree",
                        "education_start": EducationStart.NO_START_DATE.value,
                        "education_end": EducationEnd.PRESENT.value,
                    }
                ],
                "experience": [
                    {
                        "experience_founder": 0,
                        "experience_start": ExperienceStart.NO_START_DATE.value,
                        "experience_end": ExperienceEnd.PRESENT.value,
                    }
                ],
            }
        ],
    }
    s = Startup(**d)
    assert s.persons[0].education[0].education_start is None
    assert s.persons[0].education[0].education_end is None
    assert s.persons[0].experience[0].experience_start is None
    assert s.persons[0].experience[0].experience_end is None


def test_serialize():
    s = Startup(
        id="123e4567-e89b-12d3-a456-426614174000",
        name="Example Startup",
        desc_long="A long description",
        industries=["Tech"],
        solutions=["Software"],
        legal_form="Ltd.",
        country="United Kingdom",
        persons=[
            {
                "person_name": "John Doe",
                "gender": None,
                "highlights": [],
                "experience": [
                    {
                        "experience_founder": 1,
                        "experience_start": "2021-01-01",
                        "experience_end": "2021-02-01",
                    }
                ],
                "education": [],
            }
        ],
        resources={
            "website": "http://www.example.com",
        },
    )

    x = s.model_dump()
    assert x["persons"][0]["experience"][0]["experience_founder"] is True
