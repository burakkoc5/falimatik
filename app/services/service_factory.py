from typing import Type

from app.services.auth_service import AuthService
from app.services.user_service import UserService
from .base_service import BaseService
from .horoscope_service import HoroscopeService
from .numbers_service import NumbersService

def get_horoscope_service() -> BaseService:
    return HoroscopeService()

def get_numbers_service() -> BaseService:
    return NumbersService() 

def get_user_service() -> BaseService:
    return UserService()

def get_auth_service() -> BaseService:
    return AuthService()

