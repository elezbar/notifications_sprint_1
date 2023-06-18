from pydantic import BaseModel
from typing import Any


class UnsubscribeDB(BaseModel):
    id_unsubscriber: int
    id_event: int
    id_user: int


class EditUnsubscribeDB(UnsubscribeDB):
    pass


class AddUnsubscribeDB(BaseModel):
    id_event: int
    id_user: int


class RemoveUnsubscribeDB(BaseModel):
    id_unsubscriber: int
