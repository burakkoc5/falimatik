from app.services.base_service import HoroscopeServiceInterface
from app.models.horoscope_model import HoroscopeModel
import requests
import os

class HoroscopeService(HoroscopeServiceInterface):
    def __init__(self):
        self.base_url = os.getenv('AZTRO_BASE_URL', 'https://aztro.sameerkumar.website/v1')
        self._initialize_validations()

    def _initialize_validations(self):
        self.valid_signs = {
            'aries', 'taurus', 'gemini', 'cancer', 'leo', 'virgo',
            'libra', 'scorpio', 'sagittarius', 'capricorn', 'aquarius', 'pisces'
        }
        self.valid_periods = {'today', 'tomorrow', 'yesterday'}

    def get_horoscope(self, sign: str, period: str = 'today') -> HoroscopeModel:
        self._validate_inputs(sign, period)
        response_data = self._fetch_horoscope_data(sign, period)
        return HoroscopeModel.from_api_response(response_data, sign, period)

    def _validate_inputs(self, sign: str, period: str) -> None:
        sign = sign.lower()
        period = period.lower()
        
        if sign not in self.valid_signs:
            raise ValueError(f"Invalid zodiac sign. Must be one of: {', '.join(self.valid_signs)}")
        
        if period not in self.valid_periods:
            raise ValueError(f"Invalid period. Must be one of: {', '.join(self.valid_periods)}")

    def _fetch_horoscope_data(self, sign: str, period: str) -> dict:
        try:
            response = requests.post(
                self.base_url,
                params={'sign': sign, 'day': period}
            )
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            raise ConnectionError(f"Failed to fetch horoscope data: {str(e)}")
