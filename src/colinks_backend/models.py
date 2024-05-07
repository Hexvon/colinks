from pydantic import BaseModel, ConfigDict


class Link(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    link: str
    short_link: str
