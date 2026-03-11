import aiosmtplib
from email.message import EmailMessage
from app.core.config import settings

async def send_email(to: str, subject: str, body: str):
    message = EmailMessage()
    message["From"] = settings.EMAIL_HOST_USER
    message["To"] = to
    message["Subject"] = subject
    message.set_content(body)

    await aiosmtplib.send(
        message,
        hostname=settings.EMAIL_HOST,
        port=settings.EMAIL_PORT,
        start_tls=settings.EMAIL_USE_TLS,
        username=settings.EMAIL_HOST_USER,
        password=settings.EMAIL_HOST_PASSWORD
    )

    print(f"Email sent to {to}")