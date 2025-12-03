# logger.py
import csv
import os
import time

from config import LOG_PATH

def log_email(lead: dict, subject: str, body: str, status: str):
    file_exists = os.path.isfile(LOG_PATH)
    with open(LOG_PATH, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow([
                "timestamp",
                "name",
                "company",
                "email",
                "website",
                "subject",
                "body",
                "status",
            ])
        writer.writerow([
            time.strftime("%Y-%m-%d %H:%M:%S"),
            lead["name"],
            lead["company"],
            lead["email"],
            lead["website"],
            subject,
            body.replace("\n", "\\n"),
            status,
        ])
