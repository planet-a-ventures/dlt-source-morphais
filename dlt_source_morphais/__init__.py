"""A source loading entities and lists from Morphais  (morphais.com)"""

from enum import StrEnum
from typing import Any, Iterable, List, Optional, Sequence
import logging
from uuid import UUID
import dlt
from dlt.common.typing import TDataItem
from dlt.sources import DltResource
from dlt.common.logger import is_logging
from pydantic import ValidationError
import asyncio

# from dlt.common.schema.typing import TTableReferenceParam
from dlt.common.libs.pydantic import DltConfig
from .settings import LIST_STARTUPS, STARTUP
from pydantic import BaseModel
from .rest_client import get_rest_client, MAX_PAGE_LIMIT
from .type_adapters import startup_adapter, list_adapter
from .model.spec import Startup

# from .model.my_spec import ExtendedStartup as Startup
from dlt.sources.helpers.rest_client.client import PageData


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
    logger.addFilter
    logger.addFilter(HideSpecificWarning())


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
            LIST_STARTUPS, params={"take": MAX_PAGE_LIMIT}
        )
    )


# FlattenedInteraction = flatten_root_model(Interaction)
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
        lambda: list(
            rest_client.paginate(
                STARTUP,
                params={"id": id},
            )
        )
    )
    return [
        parsed
        for parsed in (parse_startup(startup) for startup in startups)
        if parsed is not None
    ]


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

            yield dlt.mark.with_hints(
                item=use_id(startup, exclude={"persons"}),
                hints=dlt.mark.make_hints(
                    table_name=Table.STARTUPS.value,
                ),
                create_table_variant=True,
            )


# async def startup_details(
#     ids: List[UUID],
# ):
#     rest_client = get_rest_client(single_page=True)

#     for id in ids:
#         for startup in rest_client.paginate(
#             STARTUP,
#             params={
#                 "id": id,
#             },
#         ):
#             yield use_id(parse_startup(startup))


# TODO: Workaround for the fact that when `add_limit` is used, the yielded entities
# become dicts instead of first-class entities
def __get_id(obj):
    if isinstance(obj, dict):
        return obj.get("id")
    return getattr(obj, "id", None)


# def __create_entity_resource(entity_name: ENTITY, dev_mode=False) -> DltResource:
#     datacls = get_entity_data_class_paged(entity_name)
#     name = entity_name

#     @dlt.transformer(
#         # we fetch IDs for all entities first,
#         # without any data, so we can parallelize the more expensive data fetching
#         # whilst not hitting the API limits so fast and we can parallelize
#         # because we don't need to page with cursors
#         data_from=__create_id_resource(entity_name, dev_mode=dev_mode),
#         write_disposition="replace",
#         parallelized=True,
#         primary_key="id",
#         merge_key="id",
#         max_table_nesting=3,
#         name=name,
#     )
#     def __entities(
#         entity_arr: List[Company | Person | Opportunity],
#     ) -> Iterable[TDataItem]:
#         rest_client = get_v2_rest_client()

#         ids = [__get_id(x) for x in entity_arr]
#         response = rest_client.get(
#             entity_name,
#             params={
#                 "limit": len(ids),
#                 "ids": ids,
#                 "fieldTypes": [
#                     Type2.ENRICHED.value,
#                     Type2.GLOBAL_.value,
#                     Type2.RELATIONSHIP_INTELLIGENCE.value,
#                 ],
#             },
#             hooks=hooks,
#         )
#         response.raise_for_status()
#         entities = datacls.model_validate_json(json_data=response.text)

#         for e in entities.data:
#             (ret, references) = yield from process_and_yield_fields(e, name)
#             yield dlt.mark.with_hints(
#                 item=pydantic_model_dump(e, exclude={"fields"})
#                 | ret
#                 | {"_dlt_id": e.id},
#                 hints=dlt.mark.make_hints(
#                     table_name=name,
#                     references=references,
#                 ),
#                 # needs to be a variant due to https://github.com/dlt-hub/dlt/pull/2109
#                 create_table_variant=True,
#             )

#     __entities.__name__ = name
#     __entities.__qualname__ = name
#     return __entities


@dlt.source(name="morphais")
def source(dev_mode: bool = False) -> Sequence[DltResource]:

    startups_list = list_startups()
    if dev_mode:
        startups_list = startups_list.add_limit(5)

    return (startups_list | startup_details,)


__all__ = ["source"]
