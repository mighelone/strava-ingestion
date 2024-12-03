import calendar
import logging

import dlt
import pendulum
from dlt.sources.helpers.rest_client.auth import OAuth2ClientCredentials
from dlt.sources.helpers.rest_client.paginators import PageNumberPaginator
from dlt.sources.rest_api import RESTAPIConfig, rest_api_resources

logger = logging.getLogger("dlt")

BASE_URL = "https://www.strava.com/api/v3/"


@dlt.source
def get_activities(
    strava_client_id: str = dlt.secrets.value,
    strava_client_secret: str = dlt.secrets.value,
    strava_refresh_token: str = dlt.secrets.value,
):
    """
    Strava activities source.

    This source pulls activities from Strava. To use it, you must have a Strava
    developer account and have registered an application. You can then use the
    client id and secret to generate a refresh token, which you can use as
    the strava_refresh_token argument to this source.

    The source will pull all activities from Strava, starting from the given
    after date (inclusive) up to the current date. It will also pull activities
    that have been updated since the given after date.

    The source will yield the following resources:

    - athlete: This resource contains the activities for the authenticated
      athlete. The activities are sorted in descending order by start date.

    The source will write the activities to the following tables:

    - strava_athlete_activities: This table contains the activities for the
      authenticated athlete. The activities are sorted in descending order by
      start date.

    :param strava_client_id: The client id for your Strava application.
    :param strava_client_secret: The client secret for your Strava application.
    :param strava_refresh_token: The refresh token for your Strava application.
    """
    config: RESTAPIConfig = {
        "client": {
            "base_url": BASE_URL,
            "auth": OAuth2ClientCredentials(
                access_token_url="https://www.strava.com/oauth/token",
                client_id=strava_client_id,
                client_secret=strava_client_secret,
                access_token_request_data={
                    "grant_type": "refresh_token",
                    "refresh_token": strava_refresh_token,
                },
            ),
        },
        "resource_defaults": {
            "primary_key": "id",
            "write_disposition": "merge",
            "endpoint": {"params": {"per_page": 100}},
        },
        "resources": [
            {
                "name": "activities",
                "endpoint": {
                    "path": "/athlete/activities",
                    "params": {
                        "after": {
                            "type": "incremental",
                            "cursor_path": "start_date",
                            "initial_value": "2010-01-01T00:00:00Z",
                            "convert": lambda x: calendar.timegm(
                                pendulum.DateTime.fromisoformat(x).timetuple()
                            ),
                        }
                    },
                    "paginator": PageNumberPaginator(
                        base_page=1,
                        page_param="page",
                        stop_after_empty_page=True,
                        total_path=None,
                    ),
                },
            },
            {
                "name": "bikes",
                "endpoint": {
                    "path": "/athlete",
                    "data_selector": "bikes",
                    "paginator": None,
                },
                "write_disposition": "replace",
            },
        ],
    }
    yield from rest_api_resources(config)
