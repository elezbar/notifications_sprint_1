from datetime import datetime
from pydantic import BaseModel


class AddEventDB(BaseModel):
    name: str
    last_call: datetime | None
    interval: datetime | None


class EventDB(AddEventDB):
    id_wrapper: int


class EditEventDB(AddEventDB):
    id_wrapper: int


class DeleteEventDB(BaseModel):
    id_wrapper: int
