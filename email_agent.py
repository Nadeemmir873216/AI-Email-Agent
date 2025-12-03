import csv
import os
import json
from dotenv import load_dotenv
from groq import Groq

import smtplib
import time
from email.message import EmailMessage


load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# SEND_EMAILS = False 
# SECONDS_BETWEEN_EMAILS = 20  

GMAIL_ADDRESS = os.getenv("gmail_id")
GMAIL_APP_PASSWORD = os.getenv("google_app_password")


if not GMAIL_ADDRESS or not GMAIL_APP_PASSWORD:
    raise RuntimeError("GMAIL_ADDRESS or GMAIL_APP_PASSWORD missing in .env")

CSV_PATH = "leads.csv"   # adjust file name if needed

def load_leads(csv_path: str):
    leads = []
    with open(csv_path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # name parsing
            if "Name" in row and row["Name"].strip():
                name = row["Name"].strip()
            else:
                first = (row.get("First Name") or "").strip()
                last = (row.get("Last Name") or "").strip()
                name = (first + " " + last).strip() if (first or last) else "there"

            # company
            company = (row.get("Company") or row.get("Company Name") or "").strip() or "your company"

            # email
            email = (row.get("Email") or "").strip()
            if not email:
                continue  # skip useless rows

            # website
            website = (row.get("Website") or "").strip()

            leads.append({
                "name": name,
                "company": company,
                "email": email,
                "website": website,
            })
    return leads


def generate_email_llm(lead: dict) -> dict:
    name = lead["name"]
    company = lead["company"]
    website = lead["website"]

    prompt = f"""
    Write a short cold email for a 3D artist/animator (sender: Nadeem Ahmed Mir)
    offering 3D product visualization and animation.

    Lead details:
    - Name: {name}
    - Company: {company}
    - Website: {website}

    Email requirements:
    - Start with "Hi {name},"
    - Check their website and mention something relevant if possible
    - Focus on how 3D visuals/3D animation can help their business
    - 120- 150 words max
    - Professional but relaxed, not salesy
    - Mention 3D visuals/3D animation one time
    - Avoid fake claims
    - Soft CTA at the end (e.g., "open to a quick chat?" or similar)
    - Mention working with a AmazingThing. 

    Return JSON only:
    {{
      "subject": "...",
      "body": "..."
    }}
    """

    res = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.45,
    )

    raw = res.choices[0].message.content.strip()

    # Parse JSON strictly
    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        # Try to salvage JSON if wrapped in text
        start = raw.find("{")
        end = raw.rfind("}")
        if start != -1 and end != -1:
            data = json.loads(raw[start:end+1])
        else:
            raise RuntimeError(f"Model did not return valid JSON:\n{raw}")

    return {"subject": data["subject"].strip(), "body": data["body"].strip()}


def main():
    leads = load_leads(CSV_PATH)
    print(f"Loaded {len(leads)} leads.\n")

    for lead in leads:
        email = generate_email_llm(lead)
        print("=" * 80)
        print(f"To: {lead['email']}")
        print(f"Subject: {email['subject']}\n")
        print(email["body"])
        print()


if __name__ == "__main__":
    main()


