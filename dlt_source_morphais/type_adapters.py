from .model.spec import ErrorResponse, Startup, StartupListItem


from pydantic import TypeAdapter


error_adapter = TypeAdapter(ErrorResponse)
list_adapter = TypeAdapter(list[StartupListItem])
startup_adapter = TypeAdapter(list[Startup])
