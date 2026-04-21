from abc import ABC, abstractmethod
from typing import List,Dict

class BaseScrapper(ABC):
    @abstractmethod
    def search_courses(self, query:str)->List[Dict]:
        pass