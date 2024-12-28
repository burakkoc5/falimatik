import asyncio
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from dotenv import load_dotenv
import os

load_dotenv()

# Email configuration with explicit settings
conf = ConnectionConfig(
    MAIL_USERNAME=os.getenv("MAIL_USERNAME"),
    MAIL_PASSWORD=os.getenv("MAIL_PASSWORD"),
    MAIL_FROM=os.getenv("MAIL_FROM"),
    MAIL_PORT=465,  # Back to TLS port
    MAIL_SERVER="smtp.gmail.com",
    MAIL_STARTTLS=False,
    MAIL_SSL_TLS=True,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True
)

async def send_test_email():
    try:
        message = MessageSchema(
            subject="Test Email from Falimatik",
            recipients=["burak.koc@tedu.edu.tr"],
            body="This is a test email from Falimatik application",
            subtype="plain"
        )

        fm = FastMail(conf)
        print("Attempting to send email...")
        await fm.send_message(message)
        print("Email sent successfully!")
        
    except Exception as e:
        print(f"Failed to send email: {str(e)}")
        print(f"Configuration used:")
        print(f"Username: {os.getenv('MAIL_USERNAME')}")
        print(f"Server: {os.getenv('MAIL_SERVER')}")
        print(f"Port: {os.getenv('MAIL_PORT')}")
        raise e

if __name__ == "__main__":
    asyncio.run(send_test_email()) 