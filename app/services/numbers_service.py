from app.services.base_service import NumberServiceInterface
from app.models.daily_numbers import DailyNumbers
from datetime import date
import random

class NumbersService(NumberServiceInterface):
    def __init__(self):
        self.seed_base = 1000000  # For 6-digit numbers

    def _generate_number(self, seed: int) -> str:
        """Generate a 6-digit number based on a seed"""
        random.seed(seed)
        return f"{random.randint(100000, 999999)}"

    def get_power_number(self, target_date: date = None) -> str:
        """
        Generate daily power number based only on date
        This number is same for all users on a given day
        """
        if target_date is None:
            target_date = date.today()
            
        date_seed = int(target_date.strftime('%Y%m%d'))
        return self._generate_number(date_seed)

    def generate_numbers(self, user_id: int, birthdate: date = None, target_date: date = None) -> DailyNumbers:
        """
        Generate personal daily numbers based on user's birthdate and current date
        Each number is unique to the user and changes daily
        """
        if target_date is None:
            target_date = date.today()

        # Create base seed from date and user info
        date_seed = int(target_date.strftime('%Y%m%d'))
        birth_seed = int(birthdate.strftime('%Y%m%d')) if birthdate else user_id
        base_seed = date_seed + birth_seed + user_id

        return DailyNumbers(
            date=target_date,
            power_number=self.get_power_number(target_date),
            love_number=self._generate_number(base_seed + 1),
            career_number=self._generate_number(base_seed + 2),
            health_number=self._generate_number(base_seed + 3),
            finance_number=self._generate_number(base_seed + 4)
        ) 