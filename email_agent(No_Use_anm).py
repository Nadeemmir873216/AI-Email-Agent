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

SEND_EMAILS = True 
SECONDS_BETWEEN_EMAILS = 10  

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
    - Start with: Hi {name},
    - Keep the email between 100–120 words.
    - If possible, mention something relevant from their website (only if it’s obvious; no assumptions).
    - Do NOT start any sentence with “From ” because Gmail converts it to a quote.
    - Focus on how 3D visuals or 3D animation can help their business.
    - Maintain a professional but relaxed tone (not salesy).
    - Mention 3D visuals or 3D animation exactly once.
    - Use real paragraph breaks (double newline '\\n\\n').
    - Structure the email into 2–3 short paragraphs (not one big block).
    - Avoid any fake claims; only use phrases like "after a quick look online” or “after what I saw on your site.”
    - Include a soft CTA at the end (e.g., open to a quick call or seeing concepts?).
    - Add this line at the end of the email:

    Behance: https://www.behance.net/nadeemmirr  
    Instagram: https://www.instagram.com/_the.mesh/

    - Mention briefly that I’ve worked with AmazingThing (mobile accessories brand focusing on durable phone cases, chargers, power solutions, and MagSafe-compatible products).
    

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

def send_email_smtp(to_email: str, subject: str, body: str):
    msg = EmailMessage()
    msg["From"] = f"Nadeem Ahmed Mir <{GMAIL_ADDRESS}>"
    msg["To"] = to_email
    msg["Subject"] = subject
    msg.set_content(body)

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(GMAIL_ADDRESS, GMAIL_APP_PASSWORD)
        smtp.send_message(msg)

def main():
    leads = load_leads(CSV_PATH)
    print(f"Loaded {len(leads)} leads.\n")

    for idx, lead in enumerate(leads, start=1):
        email = generate_email_llm(lead)

        print("=" * 80)
        print(f"[{idx}/{len(leads)}]")
        print(f"To: {lead['email']}")
        print(f"Subject: {email['subject']}\n")
        print(email["body"])
        print()

        if SEND_EMAILS:
            try:
                send_email_smtp(lead["email"], email["subject"], email["body"])
                print("Sent.\n")
            except Exception as e:
                print(f"FAILED to send to {lead['email']}: {e}\n")

            delay = SECONDS_BETWEEN_EMAILS
            print(f"Waiting {delay:.1f} seconds before next email...\n")
            time.sleep(delay)
        else:
            print("SEND_EMAILS is False → not sending.\n")



if __name__ == "__main__":
    main()


