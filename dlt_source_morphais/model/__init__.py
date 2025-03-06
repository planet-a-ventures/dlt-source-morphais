from enum import StrEnum
import importlib
from pydantic import (
    BaseModel,
    ConfigDict,
    ValidationError,
    ValidationInfo,
    ValidatorFunctionWrapHandler,
    model_serializer,
    field_validator,
)


class Degree(StrEnum):
    UNKNOWN = "Degree unknown"


class LegalForm(StrEnum):
    NO_LEGAL_FORM = "No legal form"


class FundingStage(StrEnum):
    NO_FUNDING_ROUND = "No funding round"


class MyBaseModel(BaseModel):

    # Some of the `highlights` fields have leading whitespaces
    # This will strip them
    model_config = ConfigDict(str_strip_whitespace=True)

    @staticmethod
    def parse_possibly_broken_date(v, handler: ValidatorFunctionWrapHandler):
        try:
            return handler(v)
        except ValidationError as err:
            if err.errors()[0]["type"] == "date_from_datetime_parsing":
                return None
            else:
                raise err

    @field_validator("resources", mode="before", check_fields=False)
    def custom_parse_resources(cls, v):
        # if self.__class__.__qualname__ == "Resources":
        for key, value in v.items():
            # transforms any hostname only 'url' to a full url
            v[key] = (
                f"http://{value}"
                if value is not None and not value.startswith("http")
                else value
            )
        return v

    @field_validator("founding_date", mode="wrap", check_fields=False)
    def custom_parse_founding_date(cls, v, handler: ValidatorFunctionWrapHandler):
        return MyBaseModel.parse_possibly_broken_date(v, handler)

    @field_validator(
        "experience_start", "experience_end", mode="wrap", check_fields=False
    )
    def custom_parse_experience_date(
        cls, v, handler: ValidatorFunctionWrapHandler, info: ValidationInfo
    ):
        spec_module = importlib.import_module(".spec", package=__package__)
        Experience = getattr(spec_module, "Experience")
        NoStartDate = getattr(spec_module, "ExperienceStart").NO_START_DATE.value
        Present = getattr(spec_module, "ExperienceEnd").PRESENT.value

        if cls == Experience:
            ret = MyBaseModel.parse_possibly_broken_date(v, handler)
            if info.field_name == "experience_start" and v == NoStartDate:
                return None
            elif info.field_name == "experience_end" and v == Present:
                return None
            else:
                return ret
        else:
            return handler(v)

    @field_validator(
        "education_start", "education_end", mode="wrap", check_fields=False
    )
    def custom_parse_education_date(
        cls, v, handler: ValidatorFunctionWrapHandler, info: ValidationInfo
    ):
        spec_module = importlib.import_module(".spec", package=__package__)
        Education = getattr(spec_module, "Education")
        NoStartDate = getattr(spec_module, "EducationStart").NO_START_DATE.value
        Present = getattr(spec_module, "EducationEnd").PRESENT.value

        if cls == Education:
            ret = MyBaseModel.parse_possibly_broken_date(v, handler)
            if info.field_name == "education_start" and v == NoStartDate:
                return None
            elif info.field_name == "education_end" and v == Present:
                return None
            else:
                return ret
        else:
            return handler(v)

    @field_validator("education_degree", mode="wrap", check_fields=False)
    def custom_parse_education_degree(cls, v, handler: ValidatorFunctionWrapHandler):
        spec_module = importlib.import_module(".spec", package=__package__)
        Education = getattr(spec_module, "Education")

        if cls == Education and v == Degree.UNKNOWN.value:
            return None
        else:
            return handler(v)

    @field_validator("legal_form", mode="wrap", check_fields=False)
    def custom_parse_legal_form(cls, v, handler: ValidatorFunctionWrapHandler):
        spec_module = importlib.import_module(".spec", package=__package__)
        Startup = getattr(spec_module, "Startup")

        if cls == Startup and v == LegalForm.NO_LEGAL_FORM.value:
            return None
        else:
            return handler(v)

    @field_validator("funding_stage", mode="wrap", check_fields=False)
    def custom_parse_funding_stage(cls, v, handler: ValidatorFunctionWrapHandler):
        spec_module = importlib.import_module(".spec", package=__package__)
        Startup = getattr(spec_module, "Startup")

        if cls == Startup and v == FundingStage.NO_FUNDING_ROUND.value:
            return None
        else:
            return handler(v)

    @model_serializer(mode="wrap")
    def serialize_model(self, nxt):
        spec_module = importlib.import_module(".spec", package=__package__)
        Experience = getattr(spec_module, "Experience")
        ret = nxt(self)
        if self.__class__ == Experience:
            return ret | {"experience_founder": bool(self.experience_founder)}
        return ret
