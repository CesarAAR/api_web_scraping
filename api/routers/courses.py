from typing import List
from fastapi import APIRouter, Query
from schema.course import CourseSchema
from services.course_services import get_courses

router = APIRouter(prefix="/courses")

@router.get("/", response_model=List[CourseSchema])
def search_courses(query: str = Query(..., min_length=1)):
    return get_courses(query)