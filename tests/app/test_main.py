from unittest import mock
import pytest
from fastapi.testclient import TestClient

from app.main import app, get_msg_manager
from app.models import StravaTypeEnum, StravaUpdate, WebhookEvent


@pytest.fixture
def mock_message_manager()->mock.MagicMock:
    return mock.MagicMock()

@pytest.fixture
def client(mock_message_manager: mock.MagicMock)->TestClient:
    app.dependency_overrides[get_msg_manager] = lambda: mock_message_manager
    return TestClient(app)


def test_process_message(client: TestClient, mock_message_manager: mock.MagicMock):
    response = client.post("/",
        json={
            "object_type": "activity",
            "object_id": 1360128428,
            "aspect_type": "create",
            "updates": {
                "title": "Messy"
            },
            "owner_id": 134815,
            "subscription_id": 120475,
            "event_time": 1516126040
        }
    )
    assert response.status_code == 200
    mock_message_manager.assert_called_once_with(
        WebhookEvent(
            object_type=StravaTypeEnum.activity,
            object_id=1360128428,
            aspect_type="create",
            updates=StravaUpdate(title="Messy"),
            owner_id=134815,
            subscription_id=120475,
            event_time=1516126040,
        )
    )