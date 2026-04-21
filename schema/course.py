from pydantic import BaseModel

class CourseSchema(BaseModel):
    title: str
    author: str
    price: float
    score: float
    source: str
