from dataclasses import dataclass
from typing import Protocol

from mypy_boto3_sns.service_resource import _Topic

from app.models import WebhookEvent


class IMessageManager(Protocol):
    def __call__(self, event: WebhookEvent) -> None: ...


@dataclass
class SQSMessageManager(IMessageManager):
    topic: _Topic

    def __call__(self, event: WebhookEvent) -> None:
        response = self.topic.publish(
            Message=event.model_dump_json(),
        )
        status_code = response["ResponseMetadata"].get("HTTPStatusCode")
        if status_code != 200:
            raise RuntimeError(f"Failed to send message to SQS {response}")
