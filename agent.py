# agent.py
import random
import time

from config import SEND_EMAILS, MIN_DELAY_SECONDS, MAX_DELAY_SECONDS
from scrape import scrape_website, summarize_website
from email_llm import generate_email
from mailer import send_email
from logger import log_email

class OutreachAgent:
    def process_lead(self, lead: dict):
        print("=" * 80)
        print(f"Processing: {lead['name']} <{lead['email']}> ({lead['company']})")

        website_raw = scrape_website(lead["website"])
        website_summary = summarize_website(website_raw, lead["company"]) if website_raw else ""

        email = generate_email(lead, website_summary)

        print(f"Subject: {email['subject']}\n")
        print(email["body"])
        print()

        if SEND_EMAILS:
            try:
                send_email(lead["email"], email["subject"], email["body"])
                log_email(lead, email["subject"], email["body"], "sent")
                print("Sent.\n")
            except Exception as e:
                log_email(lead, email["subject"], email["body"], f"error: {e}")
                print(f"FAILED to send: {e}\n")
        else:
            log_email(lead, email["subject"], email["body"], "not_sent")
            print("SEND_EMAILS is False → not sending.\n")

        delay = random.uniform(MIN_DELAY_SECONDS, MAX_DELAY_SECONDS)
        print(f"Waiting {delay:.1f} seconds before next lead...\n")
        time.sleep(delay)
