from sqlmodel import Field, SQLModel
from datetime import datetime


class Upgrade(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    server: str = Field(index=True)
    last_upgraded: datetime = Field()
    next_upgrade: datetime = Field(index=True)
    email: str = Field()
