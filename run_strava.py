from enum import StrEnum
from typing import Annotated

import dlt
import typer
from rich import print

from strava.sources.activities import get_activities


class Datasets(StrEnum):
    activities = "activities"
    bikes = "bikes"


class RefreshOptions(StrEnum):
    drop_resources = "drop_resources"
    drop_sources = "drop_sources"
    drop_tables = "drop_tables"


def main(
    datasets: Annotated[
        list[Datasets] | None,
        typer.Option(show_choices=True, help="Select dataset to run"),
    ] = None,
    refresh: Annotated[
        RefreshOptions | None,
        typer.Option(
            show_choices=True,
            help="Refresh options",
        ),
    ] = None,
):
    pipeline = dlt.pipeline(
        # import_schema_path="./schemas/import",
        export_schema_path="./schemas/export",
        pipeline_name="strava_ingestion",
        destination="postgres",
        dataset_name="strava",
    )
    source = get_activities()
    if datasets:
        source = source.with_resources(*datasets)
    pipeline_info = pipeline.run(data=source, refresh=refresh)
    print(pipeline_info)
    print(pipeline.default_schema.to_pretty_yaml())


if __name__ == "__main__":
    app = typer.Typer(
        add_completion=True,
        pretty_exceptions_short=True,
        pretty_exceptions_enable=False,
    )
    # typer.run(main)
    app.command()(main)
    app()
