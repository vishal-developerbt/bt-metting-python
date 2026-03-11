from pydantic import BaseModel, ConfigDict

class RoomCreate(BaseModel):
    name: str
    capacity: int
    location: str

class RoomResponse(BaseModel):
    id: int
    name: str
    capacity: int
    location: str
    is_active: bool

    model_config = ConfigDict(from_attributes=True)