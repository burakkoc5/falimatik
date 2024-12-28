# Falimatik API 🔮

A FastAPI-based horoscope and lucky numbers API that provides daily horoscopes and personalized lucky numbers using interface-based design.

> This project was developed with assistance from [Cursor](https://cursor.com/), an AI pair programming tool.

## Features

- 👤 User Management (CRUD operations)
- 🎲 Daily Lucky Numbers Generation
  - Power Numbers (universal daily number)
  - Personal Lucky Numbers (based on birthdate)
- 🌟 Daily Horoscope Readings with Aztro API Integration
- 🔐 PostgreSQL Database Integration
- 📝 Swagger Documentation
- 🎯 Interface-based Design with Dependency Injection

## Tech Stack

- FastAPI (0.110.0)
- PostgreSQL
- SQLAlchemy (2.0+)
- Pydantic (2.6.3)
- Python 3.8+

## Project Structure

falimatik/
├── app/
│ ├── models/
│ │ ├── user.py # User models (SQLAlchemy & Pydantic)
│ │ ├── daily_numbers.py # Lucky numbers models
│ │ └── horoscope_model.py# Horoscope models
│ ├── services/
│ │ ├── base_service.py # Service interfaces
│ │ ├── service_factory.py# Service factory for DI
│ │ ├── user_service.py # User business logic
│ │ ├── numbers_service.py# Numbers generation logic
│ │ └── horoscope_service.py# Horoscope logic
│ ├── routes/
│ │ ├── user_routes.py # User endpoints
│ │ ├── numbers_routes.py # Lucky numbers endpoints
│ │ └── horoscope_routes.py# Horoscope endpoints
│ ├── database.py # Database configuration
│ └── main.py # Application entry point
├── requirements.txt # Project dependencies
├── .env # Environment variables
├── .gitignore # Git ignore file
└── README.md # Project documentation

## Service Interfaces

### NumberServiceInterface

python
class NumberServiceInterface:
def get_power_number(self, target_date: date = None) -> str:
"""Generate universal daily power number"""
pass
def generate_numbers(self, user_id: int, birthdate: date = None, target_date: date = None) -> DailyNumbers:
"""Generate personal daily numbers"""
pass

### HoroscopeServiceInterface

python
class HoroscopeServiceInterface:
    def get_horoscope(self, sign: str, period: str = 'today') -> HoroscopeModel:
        """Get horoscope for a zodiac sign"""
        pass

## API Endpoints

### User Management
```
POST   /users/            # Create new user
GET    /users/            # Get all users
GET    /users/{user_id}   # Get user by ID
PUT    /users/{user_id}   # Update user
DELETE /users/{user_id}   # Delete user
```

### Lucky Numbers
```
GET /numbers/power             # Get universal daily power number
GET /numbers/personal/{user_id}# Get personal lucky numbers
```

### Horoscope
```
GET /horoscope/{sign}         # Get daily horoscope for zodiac sign
```

## Setup and Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd falimatik
```

2. Create and activate virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up PostgreSQL database and create .env file:
```env
DATABASE_URL=postgresql://username:password@localhost:5432/falimatik
AZTRO_BASE_URL=https://aztro.sameerkumar.website/v1
```

5. Run the application:
```bash
python run.py
```

## Example Requests

### Get Daily Power Number
```http
GET /numbers/power
Response:
{
    "date": "2024-03-19",
    "power_number": "123456"
}
```

### Get Personal Lucky Numbers
```http
GET /numbers/personal/1
Response:
{
    "date": "2024-03-19",
    "power_number": "123456",
    "love_number": "789012",
    "career_number": "345678",
    "health_number": "901234",
    "finance_number": "567890"
}
```

### Get Daily Horoscope
```http
GET /horoscope/leo?period=today
Response:
{
    "date": "2024-03-19",
    "sign": "leo",
    "message": "🌟 Your creative energy is high today. Your lucky number is 64, and your most fortunate time will be around 7am..."
}
```

## Development

### Adding New Services

1. Define interface in base_service.py
2. Implement service class
3. Add factory method in service_factory.py
4. Use dependency injection in routes

Example:
```python
# 1. Define interface
class NewServiceInterface:
    def some_method(self) -> Any:
        pass

# 2. Implement service
class NewService(NewServiceInterface):
    def some_method(self) -> Any:
        return "Implementation"

# 3. Add to factory
class ServiceFactory:
    @staticmethod
    def create_new_service() -> NewServiceInterface:
        return NewService()

# 4. Use in routes
@app.get("/new-endpoint")
async def endpoint(
    service: NewServiceInterface = Depends(get_new_service)
):
    return service.some_method()
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

* Project developed with [Cursor](https://cursor.com/) - An AI pair programming assistant
* Special thanks to the FastAPI and SQLAlchemy communities