from pydantic import BaseModel


class AskRequest(BaseModel):
    question: str
    company_id: str  # e.g. "techparts"


class AskResponse(BaseModel):
    answer: str
