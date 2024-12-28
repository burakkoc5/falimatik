from typing import Type
from .base_service import BaseService
from .horoscope_service import HoroscopeService
from .numbers_service import NumbersService

def get_horoscope_service() -> BaseService:
    return HoroscopeService()

def get_numbers_service() -> BaseService:
    return NumbersService() 