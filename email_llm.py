# email_llm.py
import json

from config import client

def _safe_parse_json(raw: str) -> dict:
    # Simple parser with fallback; extend if needed
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        start = raw.find("{")
        end = raw.rfind("}")
        if start != -1 and end != -1 and end > start:
            return json.loads(raw[start:end+1])
        raise

def generate_email(lead: dict, website_summary: str) -> dict:
    name = lead["name"]
    company = lead["company"]
    website = lead["website"]

    if website_summary:
        website_line = f"Company summary (from their site): {website_summary}"
    else:
        website_line = "No reliable website info was available, so keep personalization light and do not guess specifics."

    prompt = f"""
        You are writing a short cold email for a 3D artist/animator (sender: Nadeem Ahmed Mir)
        offering 3D product visualization and 3D animation services.

        Lead details:
        - Name: {name}
        - Company: {company}
        - Website: {website}
        - {website_line}

        Email requirements:
        - Start with: Hi {name},
        - Keep the email between 100–120 words.
        - If website summary is given, use it for light personalization. If not, stay generic and DO NOT guess specifics.
        - Do NOT start any sentence with "From ".
        - Focus on how 3D visuals or 3D animation can help this business (clarity, trust, product understanding, etc.).
        - Maintain a professional but relaxed tone (not salesy).
        - Mention 3D visuals or 3D animation exactly once.
        - Use real paragraph breaks (double newline).
        - Structure the email into 2–3 short paragraphs.
        - Avoid fake claims (Even don't say that 'I've been following you').
        - End with a soft CTA .
        - Add this at the very end:

        Behance: https://www.behance.net/nadeemmirr
        Instagram: https://www.instagram.com/_the.mesh/

        - Briefly mention that I’ve worked with AmazingThing, a mobile accessories brand (durable phone cases, chargers, power solutions, MagSafe-compatible products).

        Return ONLY valid JSON like:
        {{
        "subject": "subject line here",
        "body": "email body here"
        }}
        Escape newlines in the JSON body as \\n.
        """

    res = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.45,
    )

    raw = res.choices[0].message.content.strip()
    data = _safe_parse_json(raw)

    subject = data.get("subject", "").strip()
    body = data.get("body", "").strip().replace("\\n", "\n")

    return {"subject": subject, "body": body}
