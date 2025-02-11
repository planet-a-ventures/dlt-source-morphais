from typing import Any

import dlt
from dlt.sources.helpers.rest_client.auth import APIKeyAuth
from dlt.sources.helpers.rest_client.client import RESTClient
from dlt.sources.helpers.rest_client.paginators import (
    PageNumberPaginator,
    SinglePagePaginator,
)

from .settings import API_BASE
from dlt.sources.helpers.requests.session import Session


# Share a session (and thus pool) between all rest clients
session: Session = None


def get_rest_client(
    email: str = dlt.secrets["morphais_email"],
    api_key: str = dlt.secrets["morphais_api_key"],
    api_base: str = API_BASE,
    single_page: bool = False,
):
    global session
    client = RESTClient(
        base_url=api_base,
        headers={"Accept": "application/json", "morphaisemail": email},
        auth=APIKeyAuth(name="morphaiskey", api_key=api_key),
        paginator=(
            SinglePagePaginator()
            if single_page
            else PageNumberPaginator(
                base_page=1,
                stop_after_empty_page=True,
                total_path=None,
            )
        ),
        session=session,
    )
    if not session:
        session = client.session
    return client


MAX_PAGE_LIMIT = 50
