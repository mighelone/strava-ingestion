import enum
import pydantic

class StravaTypeEnum(str, enum.Enum):
    activity = "activity"
    athlete = "athlete"
    
class StravaAspectType(str, enum.Enum):
    create = "create"
    update = "update"
    delete = "delete"
    

class StravaUpdate(pydantic.BaseModel):
    title: str | None = None
    type: str | None = None
    private: bool | None = None

class WebhookEvent(pydantic.BaseModel):
    object_type: StravaTypeEnum
    object_id: int
    aspect_type: StravaAspectType
    updates: StravaUpdate
    owner_id: int
    subscription_id: int
    event_time: int