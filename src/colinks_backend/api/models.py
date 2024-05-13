from pydantic import BaseModel, ConfigDict


class BaseModelDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class SourceLink(BaseModelDTO):
    source_link: str


class Link(SourceLink):
    short_link: str
