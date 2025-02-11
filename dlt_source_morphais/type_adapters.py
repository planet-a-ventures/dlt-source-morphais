from .model.spec import Startup, StartupListItem


from pydantic import TypeAdapter


list_adapter = TypeAdapter(list[StartupListItem])
startup_adapter = TypeAdapter(Startup)
