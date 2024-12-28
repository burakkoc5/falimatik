from app.services.base_service import HoroscopeServiceInterface, NumberServiceInterface
from app.services.horoscope_service import HoroscopeService
from app.services.numbers_service import NumbersService

class ServiceFactory:
    @staticmethod
    def create_horoscope_service() -> HoroscopeServiceInterface:
        return HoroscopeService()

    @staticmethod
    def create_number_service() -> NumberServiceInterface:
        return NumbersService() 