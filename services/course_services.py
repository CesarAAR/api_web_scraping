from schema.course import CourseSchema
from services.scrappers.udemy import UdemyScrapper

def get_courses(query: str):
    scrapers = [
        UdemyScrapper()
    ]

    results = []

    for scraper in scrapers:
        results.extend(scraper.search_courses(query))

    return results