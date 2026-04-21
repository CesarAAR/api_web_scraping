from typing import List, Dict
from .base import BaseScrapper
from camoufox.sync_api import Camoufox
from bs4 import BeautifulSoup
import re

class UdemyScrapper(BaseScrapper):

    baseUrl = "https://www.udemy.com/courses/search/"

    def _fetch_page(self,query: str) -> str:
        url = f"{self.baseUrl}?src=ukw&q={query.replace(' ','+')}"

        with Camoufox(
            headless = True,
             geoip=True,
        ) as browser:
            
            page = browser.new_page()
            page.goto(url, wait_until="domcontentloaded", timeout=60000)

            try:
                page.wait_for_timeout(3000)

                page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
                page.wait_for_timeout(3000)

                page.wait_for_selector('a[href*="/course/"]', timeout=15000)

                html = page.content()
            except Exception as e:
                print(f"Error esperando elementos: {e}")
                html = ""

        return html


    def _parse_courses(self, html: str) -> List[Dict]:
        soup = BeautifulSoup(html, "html.parser")

        courses = []

        links = soup.select('a[href*="/course/"]')

        for link in links:
            try:
                container = link.find_parent("div")

                for _ in range(3):
                    if container and not container.select_one('[data-purpose="course-price-text"]'):
                        container = container.find_parent("div")

                title_elem = container.select_one('[class*="card-title"]')
                title = title_elem.get_text(strip=True) if title_elem else "N/A"

                author_elem = container.select_one('[data-purpose*="visible-instructors"]')
                author = author_elem.get_text(strip=True) if author_elem else "N/A"

                score_elem = container.select_one('[data-purpose="rating-number"]')
                score = self._parse_score(score_elem.get_text(strip=True)) if score_elem else 0.0

                price_elem = container.select_one('[data-purpose="course-price-text"]')
                price = self._parse_price(price_elem.get_text(strip=True)) if price_elem else 0.0
                
                href = link.get("href")
                url = f"https://www.udemy.com{href}" if href else ""

                courses.append({
                    "title": title,
                    "author": author,
                    "price": price,
                    "score": score,
                    "source": url
                })
            except Exception:
                continue

        return courses
    
    def _parse_price(self, price_text: str) -> float:
        numbers = re.findall(r"\d+[\.,]?\d*", price_text)

        if not numbers:
            return 0.0

        return float(numbers[0].replace(",", "."))
    
    def _parse_score(self, score_text: str) -> float:
        try:
            return float(score_text.replace(",", "."))
        except:
            return 0.0

    def search_courses(self, query: str)->List[Dict]:
        html = self._fetch_page(query)
        return self._parse_courses(html)
    
