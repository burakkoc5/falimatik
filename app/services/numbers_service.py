from datetime import date
import random

class NumbersService:
    def __init__(self, db):
        self.db = db

    def _generate_number(self, seed: int) -> int:
        """Generate a 6-digit number based on a seed"""
        random.seed(seed)
        return random.randint(100000, 999999)

    async def calculate_lucky_numbers(self, birthdate: date, user_id: int, date: date) -> dict:
        """Generate personal numbers based on birthdate, user_id and current date"""        
        # Create base seed from date, birthdate and user_id
        date_seed = int(date.strftime('%Y%m%d'))
        birth_seed = int(birthdate.strftime('%Y%m%d'))
        # Combine all factors to create unique seeds for each user
        base_seed = date_seed + birth_seed + (user_id * 1000)
        
        return {
            "date": date,
            "love_number": self._generate_number(base_seed + 1),
            "career_number": self._generate_number(base_seed + 2),
            "health_number": self._generate_number(base_seed + 3),
            "finance_number": self._generate_number(base_seed + 4)
        }

    async def get_daily_numbers(self, date: date) -> dict:
        """Generate the daily power number based on current date"""
        date_seed = int(date.strftime('%Y%m%d'))
        
        return {
            "date": date,
            "power_number": self._generate_number(date_seed)
        } 