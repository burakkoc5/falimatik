from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from pydantic import EmailStr
from fastapi import HTTPException
import os
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()

# Use the working email configuration
conf = ConnectionConfig(
    MAIL_USERNAME=os.getenv("MAIL_USERNAME"),
    MAIL_PASSWORD=os.getenv("MAIL_PASSWORD"),
    MAIL_FROM=os.getenv("MAIL_FROM"),
    MAIL_PORT=465,  # SSL port
    MAIL_SERVER="smtp.gmail.com",
    MAIL_STARTTLS=False,
    MAIL_SSL_TLS=True,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True
)

TEMPLATES_DIR = Path(__file__).parent.parent / "templates"

async def send_verification_email(email: EmailStr, token: str):
    try:
        # Read email template with UTF-8 encoding
        with open(TEMPLATES_DIR / "verification_email.html", 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        # Replace placeholder with actual verification URL
        verification_url = f"{os.getenv('BASE_URL')}/auth/verify/{token}"
        html_content = html_content.replace("{verification_url}", verification_url)

        message = MessageSchema(
            subject="Welcome to Falimatik - Verify Your Email",
            recipients=[email],
            body=html_content,
            subtype="html"
        )

        fm = FastMail(conf)
        await fm.send_message(message)
        
    except Exception as e:
        print(f"Failed to send email: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Failed to send verification email. Please try again later."
        ) 