from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from app.services.service_factory import ServiceFactory
from app.services.base_service import HoroscopeServiceInterface, NumberServiceInterface
from dotenv import load_dotenv
from app.services.numbers_service import NumbersService

# Load environment variables
load_dotenv()

app = FastAPI(title="Horoscope API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency injection
def get_horoscope_service() -> HoroscopeServiceInterface:
    return ServiceFactory.create_horoscope_service()

def get_number_service() -> NumberServiceInterface:
    return ServiceFactory.create_number_service()

@app.get("/horoscope/{sign}")
async def get_horoscope(
    sign: str,
    period: str = "today",
    service: HoroscopeServiceInterface = Depends(get_horoscope_service)
):
    """Get horoscope for a specific zodiac sign"""
    return service.get_horoscope(sign, period)

@app.get("/numbers/{user_id}")
async def get_daily_numbers(
    user_id: int,
    service: NumberServiceInterface = Depends(get_number_service)
):
    """Get daily lucky numbers for a specific user"""
    return service.generate_numbers(user_id) 