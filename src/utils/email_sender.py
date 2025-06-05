import smtplib
from email.message import EmailMessage
import os
from dotenv import load_dotenv

load_dotenv()  

EMAIL_ADDRESS = os.getenv("SMTP_MAIL")
EMAIL_PASSWORD = os.getenv("SMTP_PASSWORD")

def send_credentials_email(to_email: str, user_email: str, password: str):
    msg = EmailMessage()
    msg["Subject"] = "Your HR Portal Account Credentials"
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = to_email
    msg.set_content(f"""
    Hello,

    Your HR Portal account has been created.

    Email: {user_email}
    Password: {password}

    Regards,
    HR Portal Team
    """)

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            smtp.send_message(msg)
        print("✅ Email sent successfully.")
    except Exception as e:
        print(f"❌ Error sending email: {e}")
