import json
from moto import mock_aws
import boto3

from app.message_manager import SQSMessageManager
from app.models import StravaTypeEnum, StravaUpdate, WebhookEvent


@mock_aws
def test_message_manager_send_notification():
    sns = boto3.client("sns")
    topic_response = sns.create_topic(Name="test")
    topic_arn = topic_response.get("TopicArn")
    topic = boto3.resource("sns").Topic(topic_arn)

    sqs = boto3.client("sqs")
    queue = sqs.create_queue(QueueName="test")
    sns.subscribe(TopicArn=topic_arn, Protocol="sqs", Endpoint=topic.arn)

    mgr = SQSMessageManager(topic)
    event = WebhookEvent(
        object_type=StravaTypeEnum.activity,
        object_id=1360128428,
        aspect_type="update",
        updates=StravaUpdate(title="Messy"),
        owner_id=134815,
        subscription_id=120475,
        event_time=1516126040,
    )
    mgr(event)

    queue = boto3.resource("sqs").get_queue_by_name(QueueName="test")
    messages = queue.receive_messages(MaxNumberOfMessages=1)
    msg = json.loads(messages[0].body)
    assert WebhookEvent.model_validate_json(msg["Message"]) == event
