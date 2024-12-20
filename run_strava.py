import dlt

from strava.sources.activities import get_activities

pipeline = dlt.pipeline(
    import_schema_path="./schemas/import",
    export_schema_path="./schemas/export",
    pipeline_name="strava_ingestion",
    destination="motherduck",
    dataset_name="strava",
    # full_refresh=True
)
pipeline_info = pipeline.run(data=get_activities())
print(pipeline.default_schema.to_pretty_yaml())
