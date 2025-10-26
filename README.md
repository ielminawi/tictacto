# 🧠 TicTacTo - Never lose context again

### *"Never lose context again — across accounts, teams, or time."*

---

## 🚀 Overview

**TicTacTo** is an AI-powered shared brain for organizations. It captures every conversation, document, and insight across **clients, suppliers, and internal teams**, making them instantly searchable and conversational through multiple interfaces:

- 📞 **Voice Interface** - Interactive voice agent with AI avatar powered by LiveKit
- 💬 **Chat Interface** - Text-based Q&A powered by FastAPI
- 📊 **Knowledge Graphs** - Visual relationship mapping from documents
- 🎬 **Video Generation** - AI-generated Instagram Reels from PDF content

When someone leaves the company, the relationships don't reset — the memory stays.

> **"Because relationships shouldn't restart when people do."**

---

## ✨ Features

### 1. **Relationship Memory System**
- Capture and store relationship context for every account
- Context-aware Q&A using OpenAI GPT-4
- Per-account memory files for fast retrieval
- Support for multiple companies (TechParts, Tacto, Google, X, Meta, etc.)

### 2. **LiveKit Voice Agent** 🎙️
- Real-time voice interactions with AI avatar (Bey integration)
- Document-aware responses using OpenAI RAG
- Multi-document processing with semantic search
- Text chat support via LiveKit data channels

### 3. **Knowledge Graph Generator** 📊
- Extract entities and relationships from PDFs
- Interactive NetworkX visualizations with Pyvis
- Export to GraphML and GEXF formats
- Semantic understanding of company relationships

### 4. **Instagram Reel Generator** 🎬
- Direct PDF-to-video generation using Sora API
- 15-second optimized Reels for Instagram
- Vertical format (9:16 aspect ratio)
- Automatic content summarization and video prompt generation

### 5. **Modern Frontend** 🎨
- React + TypeScript + Vite
- Beautiful UI with shadcn/ui components
- Multiple pages: Chatbot, Avatar, Knowledge Graph, Reels
- Client account dashboards with relationship insights

---

## 💻 Tech Stack

### Backend
| Component | Technology | Purpose |
|-----------|-----------|---------|
| **API Server** | FastAPI + Uvicorn | Q&A endpoint for relationship memory |
| **Voice Agent** | LiveKit Agents | Real-time voice interactions |
| **RAG System** | OpenAI Embeddings | Semantic document search |
| **Avatar** | Bey API | AI avatar rendering |
| **Video** | Sora API | AI video generation |

### Frontend
| Component | Technology | Purpose |
|-----------|-----------|---------|
| **Framework** | React 18 + TypeScript | UI development |
| **Styling** | Tailwind CSS + shadcn/ui | Modern component library |
| **Build Tool** | Vite | Fast development experience |
| **Voice Client** | LiveKit Client | WebRTC voice integration |

### AI Services
- **OpenAI GPT-4o-mini** - Q&A and content generation
- **OpenAI Embeddings** - Semantic document search
- **Sora** - Video generation
- **LiveKit** - Real-time communication
- **Bey** - AI avatar

---

## 🗂️ Project Structure

```
tictacto/
│
├─ AGENT/                          # LiveKit voice agent
│  ├─ main.py                     # Agent entrypoint with OpenAI RAG
│  ├─ launcher.py                 # Agent launcher script
│  ├─ multi_doc_processor.py      # Multi-document processing
│  ├─ openai_rag.py               # OpenAI embeddings-based RAG
│  ├─ token_server.py              # JWT token server for web clients
│  └─ README.md                    # Agent-specific docs
│
├─ backend/                        # FastAPI backend
│  ├─ main.py                     # FastAPI app with /ask endpoint
│  ├─ models/
│  │   └─ ask_models.py            # Request/response schemas
│  ├─ services/
│  │   └─ qa_service.py            # OpenAI Q&A logic
│  ├─ context/                    # Account memory files
│  │   ├─ techparts_context.py
│  │   ├─ tacto_context.py
│  │   ├─ google_context.py
│  │   ├─ meta_context.py
│  │   └─ x_context.py
│  └─ requirements.txt
│
├─ frontend/                       # React + TypeScript frontend
│  ├─ src/
│  │   ├─ pages/
│  │   │   ├─ Index.tsx           # Home page
│  │   │   ├─ Chatbot.tsx          # Chat interface
│  │   │   ├─ Avatar.tsx           # Avatar page
│  │   │   ├─ KnowledgeGraph.tsx   # Knowledge graph viewer
│  │   │   ├─ Reels.tsx            # Reels page
│  │   │   └─ ClientDetail.tsx      # Client detail page
│  │   ├─ components/
│  │   │   ├─ ChatPanel.tsx       # Chat UI
│  │   │   ├─ ClientCard.tsx      # Client card
│  │   │   └─ ui/                  # shadcn/ui components
│  │   └─ App.tsx                  # Main app router
│  └─ package.json
│
├─ infos/                          # Source documents
│  ├─ ProcureMind_Client_Report_SteelCore.pdf
│  └─ summary.txt
│
├─ kg4.py                          # Knowledge graph generator
├─ reels.py                        # Instagram Reel generator
├─ requirements.txt                 # Python dependencies
└─ requirements_reels.txt          # Reel-specific dependencies
```

---

## ⚙️ Setup & Installation

### Prerequisites
- Python 3.9+ (3.11+ recommended)
- Node.js 18+
- OpenAI API key
- LiveKit account (for voice agent)
- Bey API access (for avatar)

### 1. Clone the Repository
```bash
git clone <repository-url>
cd tictacto
```

### 2. Backend Setup

#### Create Virtual Environment
```bash
cd backend
python3 -m venv tic_venv
source tic_venv/bin/activate        # Mac/Linux
# or
tic_venv\Scripts\activate           # Windows
```

#### Install Dependencies
```bash
pip install -r requirements.txt
```

#### Configure Environment
Create `.env` in `backend/`:
```env
OPENAI_API_KEY=sk-xxxxx
```

### 3. Frontend Setup

```bash
cd frontend
npm install
```

### 4. Voice Agent Setup

#### Install Dependencies
```bash
pip install livekit livekit-agents livekit-plugins-openai livekit-plugins-bey
```

#### Configure Environment
Create `AGENT/keys.env`:
```env
LIVEKIT_URL=wss://your-project.livekit.cloud
LIVEKIT_API_KEY=...
LIVEKIT_API_SECRET=...
LIVEKIT_DEFAULT_ROOM=tictacto-room
OPENAI_API_KEY=...
BEY_API_KEY=...
BEY_AVATAR_ID=...
```

### 5. Knowledge Graph & Reels Scripts

Install additional dependencies:
```bash
pip install openai networkx pyvis pydantic

# For Reels (optional)
pip install -r requirements_reels.txt
```

---

## 🚀 Running the Application

### Option 1: Backend API Only
From project root:
```bash
uvicorn backend.main:app --reload --port 8000
```

Test the API:
```bash
curl -X POST http://localhost:8000/ask \
  -H "Content-Type: application/json" \
  -d '{
    "question": "What did we agree on payment terms?",
    "company_id": "techparts"
  }'
```

### Option 2: Voice Agent
```bash
cd AGENT
python main.py
```

In another terminal, start the token server:
```bash
cd AGENT
python token_server.py --port 8081
```

### Option 3: Frontend
```bash
cd frontend
npm run dev
```
Open http://localhost:5173

### Option 4: Knowledge Graph Generator
```bash
python kg4.py
```
This will:
- Process a PDF file
- Extract entities and relationships
- Generate an interactive HTML knowledge graph
- Open it automatically in your browser

### Option 5: Instagram Reel Generator
```bash
python reels.py
```
This will:
- Extract key information from a PDF
- Generate a Sora video prompt
- Create a 15-second Instagram Reel
- Open a preview HTML page

---

## 📡 API Documentation

### Backend API

**Base URL:** `http://localhost:8000`

#### POST /ask
Answer questions about a specific account using stored relationship memory.

**Request:**
```json
{
  "question": "What did we agree on payment terms?",
  "company_id": "techparts"
}
```

**Response:**
```json
{
  "answer": "Payment terms are Net 45 days standard, with Net 30 conditional on quarterly volume pre-commitments. Alex expects Net 30 based on verbal discussions. Why this matters: misalignment in expectations may risk renewal."
}
```

**Available Company IDs:**
- `techparts` - TechParts GmbH
- `tacto` - Tacto GmbH
- `google` - Google
- `x` - X (Twitter)
- `meta` - Meta

---

## 🧩 Architecture

### Relationship Memory Flow
```
┌─────────────┐      ┌──────────────┐      ┌─────────────┐
│  Frontend   │ ───> │  FastAPI     │ ───> │ Context     │
│  (React)    │      │  /ask        │      │ Store       │
└─────────────┘      └──────────────┘      └─────────────┘
                                            │
                                            v
                                     ┌─────────────┐
                                     │ OpenAI      │
                                     │ GPT-4o-mini │
                                     └─────────────┘
```

### Voice Agent Flow
```
┌─────────────┐      ┌──────────────┐      ┌─────────────┐
│  Frontend   │ ───> │  LiveKit     │ ───> │  Agent     │
│  (WebRTC)   │      │  Room        │      │  (RAG)     │
└─────────────┘      └──────────────┘      └─────────────┘
                                                  │
                                                  v
                                          ┌─────────────┐
                                          │ Documents   │
                                          │ + OpenAI    │
                                          │ Embeddings  │
                                          └─────────────┘
```

### Document Processing Flow
```
PDF → OpenAI API → Entities/Relations → NetworkX → Pyvis HTML
     (knowledge extraction)    (graph)        (visualization)
```

---

## 📝 Account Context Files

Account memories are stored in `backend/context/` as Python modules. Each file contains:

- **COMPANY_ID** - Unique identifier (used in URLs/API calls)
- **COMPANY_NAME** - Display name
- **ACCOUNT_CONTEXT** - Detailed relationship information including:
  - Payment terms history
  - Delivery performance
  - Relationship health status
  - Communication preferences
  - Key contacts and their preferences
  - Red flags to watch
  - Handling instructions for new account owners

**Example Structure:**
```python
COMPANY_ID = "techparts"
COMPANY_NAME = "TechParts GmbH"

ACCOUNT_CONTEXT = """
ACCOUNT: TechParts GmbH
...
PAYMENT TERMS HISTORY:
...
RELATIONSHIP HEALTH:
...
"""
```

To add a new account, create a new file following this pattern and import it in `qa_service.py`.

---

## 🎯 Use Cases

### 1. Account Handovers
When someone takes over an account:
- Query: "What's the status of the TechParts relationship?"
- Get: Complete context including payment terms, delivery history, preferences, and red flags

### 2. Relationship Briefings
Before a call:
- Query: "What did we last discuss with Martin at TechParts?"
- Get: Summary of recent communications and action items

### 3. Risk Assessment
Monthly reviews:
- Query: "What are the red flags for Tacto?"
- Get: Specific concerns and mitigation strategies

### 4. Voice Interactions
Through the LiveKit agent:
- Ask: "What's our current status with TechParts?"
- Receive: Voice response with context-aware details via avatar

### 5. Visual Insights
Generate knowledge graphs to:
- Understand relationship networks
- Identify key influencers
- Map communication flows

### 6. Marketing Content
Create Instagram Reels to:
- Highlight relationship milestones
- Share company insights
- Generate engaging social media content

---

## 🏁 Development Status

### ✅ Completed
- Backend API with Q&A endpoint
- OpenAI-powered relationship memory
- Multiple account contexts (TechParts, Tacto, Google, X, Meta)
- Frontend with React + TypeScript
- Voice agent with LiveKit integration
- OpenAI RAG for document processing
- Knowledge graph generator (kg4.py)
- Instagram Reel generator (reels.py)
- Bey avatar integration

### 🔧 In Progress
- Additional account contexts
- Enhanced frontend features
- Video generation improvements

### 🧩 Planned
- Batch document ingestion
- Automatic context file generation
- Real-time collaboration features
- Advanced analytics dashboard
- Multi-language support

---

## 🔐 Environment Variables

### Backend (.env)
```env
OPENAI_API_KEY=sk-xxxxx
```

### Voice Agent (AGENT/keys.env)
```env
LIVEKIT_URL=wss://your-project.livekit.cloud
LIVEKIT_API_KEY=...
LIVEKIT_API_SECRET=...
LIVEKIT_DEFAULT_ROOM=tictacto-room
OPENAI_API_KEY=...
BEY_API_KEY=...
BEY_AVATAR_ID=...
```

---

## 🐛 Troubleshooting

### Backend API Issues
- **Missing API key**: Ensure `.env` exists in `backend/` with valid `OPENAI_API_KEY`
- **Import errors**: Activate virtual environment (`source tic_venv/bin/activate`)
- **Port conflicts**: Change port with `--port` flag

### Voice Agent Issues
- **Authentication failures**: Check `keys.env` file exists and contains valid credentials
- **Token errors**: Ensure token server is running on correct port
- **Room mismatch**: All components must use the same room name

### Frontend Issues
- **Build errors**: Run `npm install` to ensure dependencies are installed
- **CORS issues**: Backend allows all origins during development
- **LiveKit connection**: Ensure token server is accessible from frontend

### Document Processing Issues
- **Missing PDF**: Ensure source PDF exists at specified path
- **API errors**: Check OpenAI API key is valid and has credits
- **Memory issues**: Process documents in smaller batches

---

## 📚 Additional Resources

- [LiveKit Documentation](https://docs.livekit.io/)
- [OpenAI API Reference](https://platform.openai.com/docs/api-reference)
- [Bey Avatar API](https://bey.ai/)
- [Sora API Documentation](https://platform.openai.com/docs/guides/video)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)

---

## 🧾 License

MIT License © 2025 — TicTacTo Team

---

## 👥 Team

**TicTacTo** - Building the relationship operating system for organizations.

**Contributors:**
- Backend & AI Integration
- Frontend Development (Lovable)
- Product Design
- Demo & Presentation

---

## 💡 Vision

**Short-term:** Smooth account handovers, zero lost context.  
**Mid-term:** One memory layer for *all* organizational knowledge — accounts, internal docs, and market insights.  
**Long-term:** A true **"Relationship Operating System"** for companies — memory that never resets.

---

**Questions?** Open an issue or reach out to the team!
