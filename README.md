
# 📬 AI Email Outreach Agent

An end-to-end AI-powered outreach system that automatically scrapes websites, summarizes company info, generates personalized cold emails using LLMs, and sends them with human-like delays.

Built with **Groq**, **Python**, **BeautifulSoup**, and **SMTP** — designed as a clean, modular AI engineering project suitable for professional portfolios and ML/AI internships.

---

## 🚀 Features

- 🔹 **Fully automated outreach pipeline**  
  Scrapes → Summarizes → Generates → Sends → Logs

- 🔹 **LLM-powered personalization**  
  Emails are generated using Groq LLaMA models with strict JSON output.

- 🔹 **Website scraping**  
  Extracts page title, meta description, and H1 for personalization.

- 🔹 **Human-like randomness**  
  Adds randomized delays to mimic natural sending behavior.

- 🔹 **Modular Python architecture**  
  Each component is cleanly separated and easy to extend.

- 🔹 **SMTP email sending**  
  Works with Zoho Mail / Google Workspace / any SMTP provider.

- 🔹 **Automatic logging**  
  Saves every email (sent or not) to `sent_emails.csv`.

---

## 🧠 How It Works

1. Load leads from `leads.csv`  
2. Scrape the company website  
3. Summarize content using Groq LLM  
4. Generate personalized 2–3 paragraph cold email  
5. Validate & parse JSON output  
6. Send via SMTP  
7. Log results  
8. Wait random delay and move to next lead  

---

## 🏗️ Project Structure

```

project/
│
├── config.py         # API keys, SMTP, global config
├── leads.py          # Lead CSV parsing + validation
├── scrape.py         # Website HTML scraping + cleaning
├── email_llm.py      # LLM prompts + JSON-safe parsing
├── mailer.py         # SMTP email sending
├── logger.py         # Logs all sent emails
├── agent.py          # Orchestration logic per lead
└── main.py           # Program entrypoint

```

---

## 📦 Tech Stack

- 🧠 **Groq API (LLaMA models)**
- 🐍 **Python 3.x**
- 🌐 **Requests + BeautifulSoup4**
- ✉️ **SMTP (Zoho / Gmail / Workspace)**
- 🔐 **dotenv**
- 📊 **CSV logging**

---

## 📄 CSV Format

Your `leads.csv` should look like:

```

Name,Company,Email,Website
John Doe,Acme Inc,[john@acme.com](mailto:john@acme.com),[https://acme.com](https://acme.com)

````

Invalid or missing emails are automatically skipped.

---

## 🔧 Setup & Installation

### 1. Install dependencies
```bash
pip install -r requirements.txt
````

### 2. Create your `.env` file

```
GROQ_API_KEY=your_groq_key
EMAIL_ADDRESS=hello@yourdomain.com
EMAIL_PASSWORD=your_smtp_app_password
```

### 3. Run the agent

```bash
python main.py
```

---

## 📊 Example Output

```
================================================================================
Processing: John Doe <john@acme.com> (Acme Inc.)
Subject: Elevate Acme’s product showcase with 3D visuals

Hi John Doe,

After a quick look at your site...
...

Sent.

Waiting 37.4 seconds before next lead...
```

---

## 🚧 Future Enhancements

* 🔁 Automated follow-up sequences
* 🤖 Email reply classification
* 🧩 LangGraph multi-agent orchestration
* 📈 Open-rate + reply-rate analytics dashboard
* 🗄️ Database backend (PostgreSQL)
* 🌐 Web UI for non-technical users
* 💬 Multi-channel outreach (LinkedIn API, WhatsApp Business API*)

---

## 🧩 Why This Project Is Portfolio-Ready

This project demonstrates:

* AI agent design
* LLM orchestration
* Prompt engineering
* Website scraping + parsing
* Real SMTP automation
* Multi-file production architecture
* Applied AI (not just ML theory)
* Clean, scalable design

Perfect for showcasing ML/AI engineering skills.

---

## 📜 License

MIT License — feel free to use and modify.

