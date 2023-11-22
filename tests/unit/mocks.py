from pydantic import BaseModel


class ChatCompletionMessageMock(BaseModel):
    content: str

    class Config:
        arbitrary_types_allowed = True


class ChoiceMock(BaseModel):
    message: ChatCompletionMessageMock

    class Config:
        arbitrary_types_allowed = True


class ChatCompletionMock(BaseModel):
    choices: list[ChoiceMock]

    class Config:
        arbitrary_types_allowed = True
