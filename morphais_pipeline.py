import dlt
from dlt_source_morphais import source

DEV_MODE = True


def load_morphais_data() -> None:
    pipeline = dlt.pipeline(
        pipeline_name="morphais_pipeline", destination="duckdb", dev_mode=DEV_MODE
    )
    data = source(
        limit=-1 if not DEV_MODE else 1,
    )
    info = pipeline.run(
        data,
        refresh="drop_sources" if DEV_MODE else None,
        # we need this in case new resources, etc. are added
        schema_contract={"columns": "evolve"},
    )
    print(info)


if __name__ == "__main__":
    load_morphais_data()
