from fastapi import Depends, FastAPI, Response

from .models import WebhookEvent

app = FastAPI()


class MessageManager:
    def __call__(self, event: WebhookEvent) -> None:
        print(event.model_dump_json())


def get_msg_manager() -> MessageManager:
    return MessageManager()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/")
async def event(event: WebhookEvent, mgr: MessageManager = Depends(get_msg_manager)):
    mgr(event)
    return Response(status_code=200)
