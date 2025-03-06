"""A source loading entities and lists from Morphais  (morphais.com)"""

from enum import StrEnum
from typing import Any, Iterable, List, Optional, Sequence
import logging
from uuid import UUID
import dlt
from dlt.common.typing import TDataItem
from dlt.sources import DltResource
from dlt.common.logger import is_logging
from pydantic import AnyUrl, ValidationError
import asyncio
import re

from dlt.common.libs.pydantic import DltConfig
from dlt.common import json
from dlt.common.json import JsonSerializable
from .settings import LIST_STARTUPS, STARTUP
from pydantic import BaseModel
from .rest_client import get_rest_client, MAX_PAGE_LIMIT, hooks
from .type_adapters import startup_adapter, list_adapter
from .model.spec import Startup

from dlt.sources.helpers.rest_client.client import PageData


def anyurl_encoder(obj: Any) -> JsonSerializable:
    if isinstance(obj, AnyUrl):
        return obj.unicode_string()
    raise TypeError(f"Object of type {type(obj)} is not JSON serializable")


json.set_custom_encoder(anyurl_encoder)


def pydantic_model_dump(model: BaseModel, **kwargs):
    """
    Dumps a Pydantic model to a dictionary, using the model's field names as keys and NOT observing the field aliases,
    which is important for DLT to correctly map the data to the destination.
    """
    return model.model_dump(by_alias=True, **kwargs)


class Table(StrEnum):
    STARTUPS = "startups"
    PERSONS = "persons"


if is_logging():
    # ignore https://github.com/dlt-hub/dlt/blob/268768f78bd7ea7b2df8ca0722faa72d4d4614c5/dlt/extract/hints.py#L390-L393
    # This warning is thrown because of using Pydantic models as the column schema in a table variant
    # The reason we need to use variants, however, is https://github.com/dlt-hub/dlt/pull/2109
    class HideSpecificWarning(logging.Filter):
        def filter(self, record):
            if (
                "A data item validator was created from column schema"
                in record.getMessage()
            ):
                return False  # Filter out this log
            return True  # Allow all other logs

    logger = logging.getLogger("dlt")
    logger.addFilter(HideSpecificWarning())

    class HideSinglePagingNonsense(logging.Filter):
        def filter(self, record):
            msg = record.getMessage()
            if (
                "Extracted data of type list from path $ with length 1" in msg
                or re.match(
                    r"Paginator SinglePagePaginator at [a-fA-F0-9]+ does not have more pages",
                    msg,
                )
            ):
                return False
            return True

    logger.addFilter(HideSinglePagingNonsense())


def use_id(entity: Startup, **kwargs) -> dict:
    return pydantic_model_dump(entity, **kwargs) | {"_dlt_id": entity.id}


@dlt.resource(
    selected=False,
    parallelized=True,
)
def list_startups() -> Iterable[TDataItem]:
    rest_client = get_rest_client()

    yield from (
        [__get_id(entity) for entity in list_adapter.validate_python(entities)]
        for entities in rest_client.paginate(
            LIST_STARTUPS, params={"take": MAX_PAGE_LIMIT}, hooks=hooks
        )
    )


dlt_config: DltConfig = {"skip_nested_types": True}
setattr(Startup, "dlt_config", dlt_config)


def parse_startup(startup: PageData[Any]):
    ret = None
    try:
        ret = startup_adapter.validate_python(startup)[0]
    except ValidationError as e:
        logging.error(f"Failed to validate startup: {startup}")
        logging.error(e)
    return ret


async def fetch_startup(id: UUID):
    rest_client = get_rest_client(single_page=True)
    # Wrap the synchronous paginate call in asyncio.to_thread
    startups = await asyncio.to_thread(
        lambda: list(rest_client.paginate(STARTUP, params={"id": str(id)}, hooks=hooks))
    )
    return [
        parsed
        for parsed in (parse_startup(startup) for startup in startups)
        if parsed is not None
    ]


enum_fields = ["audience", "legal_form", "funding_stage", "industries", "solutions"]


def pluralize(field_name: str):
    return field_name + "s" if field_name[-1] != "s" else field_name


@dlt.transformer(
    # primary_key="id",
    # columns=Startup,
    max_table_nesting=1,
    # write_disposition="replace",
    parallelized=True,
    name=Table.STARTUPS.value,
)
async def startup_details(ids: List[UUID]):
    # Create a task for each id so that all calls run concurrently.
    tasks = [fetch_startup(id) for id in ids]
    # Wait for all tasks to complete concurrently.
    startups_list = await asyncio.gather(*tasks)

    # Flatten the list of results and yield each record.
    for startups in startups_list:
        for startup in startups:
            for person in startup.persons:
                yield dlt.mark.with_hints(
                    item=pydantic_model_dump(person) | {"startup_id": startup.id},
                    hints=dlt.mark.make_hints(
                        table_name=Table.PERSONS.value,
                        references=[
                            {
                                "columns": ["startup_id"],
                                "referenced_columns": ["id"],
                                "referenced_table": Table.STARTUPS.value,
                            }
                        ],
                    ),
                    # needs to be a variant due to https://github.com/dlt-hub/dlt/pull/2109
                    create_table_variant=True,
                )
                for highlight in person.highlights:
                    yield dlt.mark.with_hints(
                        item=highlight,
                        hints=dlt.mark.make_hints(
                            table_name="highlights",
                            primary_key="value",
                            merge_key="value",
                            write_disposition="merge",
                        ),
                        # needs to be a variant due to https://github.com/dlt-hub/dlt/pull/2109
                        create_table_variant=True,
                    )

            for field_name in enum_fields:
                data = getattr(startup, field_name)
                if not data or len(data) == 0:
                    continue
                items = (
                    [{"value": data}]
                    if not isinstance(data, list)
                    else [{"value": x} for x in data]
                )

                yield dlt.mark.with_hints(
                    item=items,
                    hints=dlt.mark.make_hints(
                        table_name=pluralize(field_name),
                        primary_key="value",
                        merge_key="value",
                        write_disposition="merge",
                    ),
                    # needs to be a variant due to https://github.com/dlt-hub/dlt/pull/2109
                    create_table_variant=True,
                )

            yield dlt.mark.with_hints(
                item=use_id(startup, exclude={"persons"}),
                hints=dlt.mark.make_hints(
                    table_name=Table.STARTUPS.value,
                ),
                # needs to be a variant due to https://github.com/dlt-hub/dlt/pull/2109
                create_table_variant=True,
            )


# TODO: Workaround for the fact that when `add_limit` is used, the yielded entities
# become dicts instead of first-class entities
def __get_id(obj):
    if isinstance(obj, dict):
        return obj.get("id")
    return getattr(obj, "id", None)


@dlt.source(name="morphais")
def source(limit=-1) -> Sequence[DltResource]:

    startups_list = list_startups()
    if limit > 0:
        startups_list = startups_list.add_limit(limit)

    return (startups_list | startup_details,)


__all__ = ["source"]
