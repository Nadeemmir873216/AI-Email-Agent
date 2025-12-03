# scrape.py
import requests
from bs4 import BeautifulSoup

from config import client

def scrape_website(url: str) -> str:
    if not url:
        return ""

    if not url.startswith("http://") and not url.startswith("https://"):
        url = "https://" + url

    try:
        resp = requests.get(url, timeout=8)
        resp.raise_for_status()
    except Exception:
        return ""

    soup = BeautifulSoup(resp.text, "html.parser")

    title = soup.title.string.strip() if soup.title and soup.title.string else ""
    meta_desc = ""
    meta = soup.find("meta", attrs={"name": "description"})
    if meta and meta.get("content"):
        meta_desc = meta["content"].strip()

    h1 = soup.find("h1")
    h1_text = h1.get_text(strip=True) if h1 else ""

    text = "\n".join([t for t in (title, meta_desc, h1_text) if t])
    return text[:600]


def summarize_website(context: str, company: str) -> str:
    if not context:
        return ""

    prompt = f"""
        You are helping a 3D artist understand a potential client's business for cold outreach.

        Company: {company}

        Raw info scraped from their website:
        \"\"\"{context}\"\"\"

        In 1–2 short sentences, describe what this company does and who it serves, using ONLY the info above.
        Do NOT guess or invent anything.

        Return just those 1–2 sentences, plain text.
        """
    res = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
    )
    summary = res.choices[0].message.content.strip()
    return summary[:400]
