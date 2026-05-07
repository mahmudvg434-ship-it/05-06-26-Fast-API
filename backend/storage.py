import json
from pathlib import Path
from datetime import datetime

DATA_PATH = Path("backend/data/inquiries.json")

# =========================
# INIT FILE
# =========================
DATA_PATH.parent.mkdir(parents=True, exist_ok=True)

if not DATA_PATH.exists():
    with open(DATA_PATH, "w", encoding="utf-8") as f:
        json.dump([], f, ensure_ascii=False, indent=2)


# =========================
# LOAD DATA
# =========================
def load_inquiries():
    try:
        with open(DATA_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print("❌ Load Error:", e)
        return []


# =========================
# SAVE DATA
# =========================
def save_inquiry(name, email, question, category, priority, department, status, answer):

    data = load_inquiries()

    # safe ID generation (FIXED)
    new_id = 1
    if data:
        new_id = max(item["id"] for item in data) + 1

    item = {
        "id": new_id,
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "name": name,
        "email": email,
        "question": question,
        "category": category,
        "priority": priority,
        "department": department,
        "status": status,
        "answer": answer
    }

    data.append(item)

    try:
        with open(DATA_PATH, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    except Exception as e:
        print("❌ Save Error:", e)

    return item