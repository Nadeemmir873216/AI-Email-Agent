# config.py
import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

# Groq client
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    raise RuntimeError("GROQ_API_KEY missing in .env")

client = Groq(api_key=GROQ_API_KEY)

# Gmail
GMAIL_ADDRESS = os.getenv("gmail_id")
GMAIL_APP_PASSWORD = os.getenv("google_app_password")
if not GMAIL_ADDRESS or not GMAIL_APP_PASSWORD:
    raise RuntimeError("GMAIL_ADDRESS or GMAIL_APP_PASSWORD missing in .env")

# Paths & runtime config
CSV_PATH = "leads.csv"
LOG_PATH = "sent_emails.csv"

SEND_EMAILS = False
MIN_DELAY_SECONDS = 25
MAX_DELAY_SECONDS = 70
