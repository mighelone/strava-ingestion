import calendar
import logging

import dlt
import pendulum
from dlt.sources.helpers.rest_client import RESTClient
from dlt.sources.helpers.rest_client.auth import OAuth2ClientCredentials
from dlt.sources.helpers.rest_client.paginators import PageNumberPaginator

logger = logging.getLogger("dlt")

BASE_URL = "https://www.strava.com/api/v3/"


@dlt.resource(
    name="activities",
    primary_key="id",
    write_disposition="merge",
)
def get_activities(
    strava_client_id: str = dlt.secrets.value,
    strava_client_secret: str = dlt.secrets.value,
    strava_refresh_token: str = dlt.secrets.value,
    start_activity=dlt.sources.incremental(
        cursor_path="start_date",
        initial_value="2021-01-01T00:00:00Z",
    ),
):
    after = start_activity.last_value
    after = pendulum.DateTime.fromisoformat(after)
    before = after.add(months=12)
    logger.info(f"Fetching activities between {after} and {before}")
    client = RESTClient(
        base_url=BASE_URL,
        auth=OAuth2ClientCredentials(
            access_token_url="https://www.strava.com/oauth/token",
            client_id=strava_client_id,
            client_secret=strava_client_secret,
            access_token_request_data={
                "grant_type": "refresh_token",
                "refresh_token": strava_refresh_token,
            },
        ),
        paginator=PageNumberPaginator(
            base_page=1, page_param="page", stop_after_empty_page=True, total_path=None
        ),
    )
    yield from client.paginate(
        "/athlete/activities",
        params={
            "after": calendar.timegm(after.timetuple()),
            "before": calendar.timegm(before.timetuple()),
            "per_page": 50,
        },
    )
