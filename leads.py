# leads.py
import csv

def load_leads(csv_path: str):
    leads = []
    with open(csv_path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # name
            if "Name" in row and row["Name"].strip():
                name = row["Name"].strip()
            else:
                first = (row.get("First Name") or "").strip()
                last = (row.get("Last Name") or "").strip()
                name = (first + " " + last).strip() or "there"

            # company
            company = (row.get("Company") or row.get("Company Name") or "").strip() or "your company"

            # email
            email = (row.get("Email") or "").strip()
            if not email:
                continue

            # website
            website = (row.get("Website") or "").strip()

            leads.append({
                "name": name,
                "company": company,
                "email": email,
                "website": website,
            })
    return leads
