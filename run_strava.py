import os
from pathlib import Path

import dlt
from dotenv import load_dotenv

from strava.models import StravaToken
from strava.sources.activities import get_activities

token_path = Path("token.json")
token = StravaToken.model_validate_json(token_path.read_text())

load_dotenv()
strava_client_id = os.getenv("STRAVA_CLIENT_ID")
strava_client_secret: str = os.getenv("STRAVA_CLIENT_SECRET")

# if __name__ == "__main__":

# refreshed = refresh_access_token(
#     strava_client_id, strava_client_secret, token.refresh_token
# )

# response = requests.get(
#     BASE_URL + "athlete/clubs",
#     headers={"Authorization": f"Bearer {refreshed.access_token}"},
# )
# data = response.json()
# config: RESTAPIConfig = {
#     "client": {
#         "base_url": BASE_URL,
#         "headers": {"Authorization": f"Bearer {refreshed.access_token}"},
#     },
#     "resource_defaults": {"primary_key": "id", "write_disposition": "merge"},
#     "resources": [
#         # "activities",
#         {
#             "name": "clubs",
#             "endpoint": {"path": "athlete/clubs"},
#             "write_disposition": "replace",
#         },
#         {
#             "name": "activities",
#             "endpoint": {
#                 "path": "clubs/{club_id}/activities",
#                 "params": {
#                     "club_id": {"type": "resolve", "resource": "clubs", "field": "id"}
#                 },
#             },
#         },
#     ],
# }
# source = rest_api_source(config)

pipeline = dlt.pipeline(
    pipeline_name="strava_ingestion",
    destination="duckdb",
    dataset_name="strava",
    # full_refresh=True
)
# def f(item):
#     breakpoint()
#     print(item)
# get_activities.add_map(f)
pipeline_info = pipeline.run(data=get_activities)

# response = requests.get(
#     "https://www.strava.com/api/v3/athlete/activities",
#     headers={"Authorization": f"Bearer {refreshed.access_token}"},
#     params={
#         "after": calendar.timegm(datetime.datetime(2022, 1, 1).timetuple()),
#         "before": calendar.timegm(datetime.datetime(2022, 1, 10).timetuple()),
#     }
# )
