from camoufox.sync_api import Camoufox
from bs4 import BeautifulSoup
import re
import json

base_url = "https://www.coursera.org/courses?query=free"


class CourseraScrapper:
    def __init__(self, **kwargs):
        self._camoufox = Camoufox(**kwargs)
        self.browser = None
        self.browser = self._camoufox.__enter__()
        self.page = None
        self.page = self.browser.new_page()
        self.base_url = "https://www.coursera.org/courses?query=free"

        # filters provided by apollo grapql
        self.filters_regex = re.compile(r'window\.__APOLLO_STATE__\s*=\s*({.*?});', flags = re.DOTALL)
        

    def get_filters(self) -> dict | None:
        """
        Get all filters available on the page.
        Since all filters are added to the url as query string, we can easily get all filters by parsing the url.
        return: dict of filters with filter name as key and filter options as value.
        """
        self.page.goto(self.base_url)
        content = self.page.content()
        matches = self.filters_regex.findall(content)
        if not len(matches) > 0:
            return None

        try:
            json_str = json.loads(matches.pop())
        except Exception as e:
            print(f"Can't return a json, see: {e}")
            return None
        else:
            return json_str
    

    def close(self):
        self._camoufox.__exit__(None, None, None)
    
        

if __name__ == "__main__":
    coursera_scrapper = CourseraScrapper(headless=False)
    filters = coursera_scrapper.get_filters()
    print(filters)