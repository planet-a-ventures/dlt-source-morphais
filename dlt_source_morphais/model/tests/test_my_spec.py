
import json
from ..my_spec import ExtendedStartup


def test_domain_only_website():

    d = {
        "id": "123e4567-e89b-12d3-a456-426614174000",
        "name": "Example Startup",
        "desc_long": "A long description",
        "industries": ["Tech"],
        "solutions": ["Software"],
        "legal_form": "Ltd.",
        "country": "United Kingdom",
        "persons": [],
        "resources": {"website": "www.example.com"},
    }

    s = ExtendedStartup(**d)
    assert s.resources.website.unicode_string() == "http://www.example.com/"

    str_d = json.dumps(d)
    s2 = ExtendedStartup.model_validate_json(str_d)
    assert s2.resources.website.unicode_string() == "http://www.example.com/"
