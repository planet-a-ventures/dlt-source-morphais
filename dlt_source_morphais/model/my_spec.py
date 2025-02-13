import json
from pydantic import field_validator

from .spec import Startup

class ExtendedStartup(Startup):
    @field_validator('resources', mode='before')
    def custom_parse_my_field(cls, v):
        for key,value in v.items():
            # transforms any hostname only 'url' to a full url
            v[key] = f"http://{value}" if value is not None and not value.startswith("http") else value
        return v