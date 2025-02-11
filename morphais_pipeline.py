import dlt
from dlt_source_morphais import source

DEV_MODE = True


def load_morphais_data() -> None:
    pipeline = dlt.pipeline(
        pipeline_name="morphais_pipeline", destination="duckdb", dev_mode=DEV_MODE
    )
    data = source()
    if DEV_MODE:
        data.add_limit(1)
    info = pipeline.run(data, refresh="drop_sources")
    print(info)


if __name__ == "__main__":
    load_morphais_data()
