from pydantic import BaseModel

class CourseSchema(BaseModel):
    title: str
    author: str
    score: float
    source: str
