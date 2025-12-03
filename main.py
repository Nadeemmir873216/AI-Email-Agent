# main.py
from config import CSV_PATH
from leads import load_leads
from agent import OutreachAgent

def main():
    agent = OutreachAgent()
    leads = load_leads(CSV_PATH)
    print(f"Loaded {len(leads)} leads.\n")

    for idx, lead in enumerate(leads, start=1):
        print(f"[{idx}/{len(leads)}]")
        agent.process_lead(lead)

if __name__ == "__main__":
    main()
