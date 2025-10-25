# 🧠 TicTacTo  
### *“Never lose context again — across accounts, teams, or time.”*

---

## 🚀 Overview
**TicTacTo** is an AI-powered shared brain for organizations.  
It captures every conversation, document, and insight across **clients, suppliers, and internal teams**, and makes them instantly searchable and conversational.

When someone leaves the company, the relationships don’t reset — the memory stays.

> **“Because relationships shouldn’t restart when people do.”**

---

## ✨ Core Idea
Most organizations lose up to **80% of relationship context** when handovers happen — missed commitments, lost trust, and repeated conversations.  

**TicTacTo** solves that by combining:
1. **Layer 1 — Ingestion (Context Builder)**  
   - Takes raw emails, call transcripts, and notes.  
   - Uses OpenAI to generate structured `{company}_context.py` files (relationship briefs).  

2. **Layer 2 — Q&A Runtime**  
   - Loads the correct company memory file.  
   - Answers any question about that relationship using only stored context.  
   - Powers the conversational interface you see in the demo.

---

## 💻 Tech Stack

| Layer | Tech | Purpose |
|-------|------|----------|
| **Backend (API)** | 🐍 FastAPI + OpenAI API | Serve `/ask` endpoint and handle memory lookup |
| **Frontend (UI)** | 🎨 Lovable | Two-column dashboard: account summary + chat interface |
| **AI Engine** | GPT-4o-mini | Context-anchored conversational intelligence |
| **Environment** | `tic_venv` (Python venv) | Isolated dependencies |
| **Language** | Python 3.9+ | Main backend runtime |

---

## 🗂️ Project Structure

```
tictacto/
│
├─ backend/
│  ├─ main.py                     # FastAPI app
│  ├─ models/
│  │   └─ ask_models.py           # Request/response schemas
│  ├─ services/
│  │   └─ qa_service.py           # OpenAI Q&A logic
│  ├─ context_store/
│  │   ├─ techparts_context.py    # Example account memory file
│  │   └─ __init__.py
│  ├─ requirements.txt
│  ├─ .env                        # contains OPENAI_API_KEY
│  └─ tic_venv/                   # virtual environment (ignored by git)
│
└─ frontend/
   └─ (Lovable-generated UI)
```

---

## ⚙️ Setup & Run

### 1️⃣ Create and activate the virtual environment
```bash
cd backend
python3 -m venv tic_venv
source tic_venv/bin/activate        # (Mac/Linux)
# or
tic_venv\Scripts\activate           # (Windows)
```

### 2️⃣ Install dependencies
```bash
pip install -r requirements.txt
```

### 3️⃣ Add your API key
Create `.env` inside `backend/`:
```
OPENAI_API_KEY=sk-xxxxx
```

### 4️⃣ Run the backend
From the **project root (`tictacto`)**:
```bash
uvicorn backend.main:app --reload --port 8000
```

### 5️⃣ Test the API
```bash
curl -X POST http://localhost:8000/ask   -H "Content-Type: application/json"   -d '{"question":"What did we agree on payment terms?","company_id":"techparts"}'
```

Expected:
```json
{"answer": "Payment terms are Net 45 ... Why this matters: misalignment may risk renewal."}
```

---

## 🧩 API Contract

**POST** `/ask`  
**Body:**
```json
{
  "question": "string",
  "company_id": "string"
}
```

**Response:**
```json
{
  "answer": "string"
}
```

---

## 🖥️ Frontend (Lovable)

The Lovable interface consists of:
- **Left Column:** Account Summary (health, risk, key contacts)  
- **Right Column:** Chat with Relationship Memory  
- **Buttons:**  
  - **Brief Me:** Opens a short summary drawer  
  - **Play Reel:** Opens a 30 s visual recap of the relationship

All content is grounded in the same `ACCOUNT_CONTEXT` file used by the backend.

---

## 🧱 Architecture Diagram

```
+---------------------+          +-----------------------+
|  Lovable Frontend   |  --->    |  FastAPI Backend      |
|  (Chat UI, Buttons) |  <---    |  /ask endpoint        |
+---------------------+          |  uses qa_service.py   |
                                 +----------+------------+
                                            |
                                            v
                                 +-----------------------+
                                 |  context_store/       |
                                 |  techparts_context.py |
                                 |  altus_context.py ... |
                                 +-----------------------+
                                            |
                                            v
                                 +-----------------------+
                                 |  OpenAI GPT-4o-mini   |
                                 |  Context-anchored Q&A |
                                 +-----------------------+
```

---

## 🌍 Vision
**Short-term:** Smooth account handovers, zero lost context.  
**Mid-term:** One memory layer for *all* organizational knowledge — accounts, internal docs, and market insights.  
**Long-term:** A true **“Relationship Operating System”** for companies — memory that never resets.

---

## 🧠 Example Prompt
> “What did we agree on payment terms?”  
> → *“Verbal Net 45 agreement with Martin Vogel; he still believes Net 30 is pending. Why this matters: unmet expectations could damage trust and renewal.”*

---

## 🧩 Team Roles
| Member | Focus |
|---------|--------|
| You | Backend (FastAPI + OpenAI Q&A), UI logic, architecture |
| Others | Frontend (Lovable), pitch deck, design, presentation |

---

## 🏁 Status
✅ Backend complete  
✅ Q&A layer working  
🔧 Frontend integration (Lovable) in progress  
🧩 Layer 1 (context builder) — next milestone

---

## 🧾 License
MIT License © 2025 — TicTacTo Team
