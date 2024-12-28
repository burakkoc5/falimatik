from abc import ABC, abstractmethod
from typing import Any

class HoroscopeServiceInterface(ABC):
    @abstractmethod
    def get_horoscope(self, sign: str, period: str) -> Any:
        pass

class NumberServiceInterface(ABC):
    @abstractmethod
    def generate_numbers(self, user_id: int) -> Any:
        pass 