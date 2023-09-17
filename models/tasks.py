from datetime import datetime
from beanie import Document
from pydantic import Field


class Tasks(Document):
    title: str = Field(max_length=50)
    content: str
    is_done: bool = False
    date_created: datetime = datetime.now()

    class Settings:
        name = "tasks"
