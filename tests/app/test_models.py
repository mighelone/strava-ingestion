import pytest
from app.models import StravaTypeEnum, StravaUpdate, WebhookEvent


@pytest.mark.parametrize(
    "json_string,expected",
    [
        (
            """{
                    "aspect_type": "update",
                    "event_time": 1516126040,
                    "object_id": 1360128428,
                    "object_type": "activity",
                    "owner_id": 134815,
                    "subscription_id": 120475,
                    "updates": {
                        "title": "Messy"
                    }
                }""",
            WebhookEvent(
                object_type=StravaTypeEnum.activity,
                object_id=1360128428,
                aspect_type="update",
                updates=StravaUpdate(title="Messy"),
                owner_id=134815,
                subscription_id=120475,
                event_time=1516126040,
            ),
        )
    ],
)
def test_deserialize(json_string: str, expected: WebhookEvent):
    result = WebhookEvent.model_validate_json(json_string)
    assert result == expected
