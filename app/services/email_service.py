from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from pydantic import EmailStr
from typing import List
import os
from dotenv import load_dotenv

load_dotenv()

conf = ConnectionConfig(
    MAIL_USERNAME=os.getenv("MAIL_USERNAME"),
    MAIL_PASSWORD=os.getenv("MAIL_PASSWORD"),
    MAIL_FROM=os.getenv("MAIL_FROM"),
    MAIL_PORT=int(os.getenv("MAIL_PORT", 587)),
    MAIL_SERVER=os.getenv("MAIL_SERVER"),
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=True
)

class EmailService:
    def __init__(self):
        self.fastmail = FastMail(conf)

    async def send_verification_email(self, email: EmailStr, token: str):
        # You might want to move this URL to config
        verification_url = f"{os.getenv('BASE_URL')}/verify-email?token={token}"
        
        message = MessageSchema(
            subject="Verify your email",
            recipients=[email],
            body=f"""
            Hi there,
            
            Please verify your email by clicking on this link: {verification_url}
            
            This link will expire in 24 hours.
            
            If you didn't create an account, please ignore this email.
            """,
            subtype="plain"
        )

        await self.fastmail.send_message(message) 