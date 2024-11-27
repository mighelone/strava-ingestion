# Strava ingestion

## Event driven

In progress

## Ingestion pipeline

Use DLT to ingest data from Strava:

Set the following environment variables:

```bash
$ export DESTINATION__MOTHERDUCK__CREDENTIALS__DATABASE=my_db
$ export DESTINATION__MOTHERDUCK__CREDENTIALS__PASSWORD=
$ export STRAVA_REFRESH_TOKEN=
$ export STRAVA_CLIENT_ID=
$ export STRAVA_REFRESH_TOKEN=
```

or set the file `.dlt/secrets.toml`:

```toml
[strava_ingestion]
strava_client_id=
strava_client_secret=
strava_refresh_token=

[destination.motherduck.credentials]
database="my_db"
password=
```

