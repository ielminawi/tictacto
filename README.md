# Galactactocus Voice Agent

Galactactocus is a LiveKit-powered voice assistant that answers document questions using an OpenAI RAG pipeline, drives a Bey avatar for video responses, and ships with a React frontend for real-time chat.

## Highlights
- LiveKit Realtime Agent (`AGENT/main.py`) with document-aware tools and Bey avatar integration
- Lightweight token server for browser clients (`AGENT/token_server.py`)
- React + Vite frontend (`frontend/`) built on `@livekit/components-react`
- Multi-document ingestion utilities in `infos/` consumed by the OpenAI-enhanced RAG

## Repository Layout
- `AGENT/` – Python agent, token server, and supporting RAG utilities
- `frontend/` – Vite React client (joins LiveKit room, renders audio/video/chat)
- `infos/` – Source PDFs/text files indexed at runtime
- `agent_worker.py` – Minimal sample worker for quick Bey avatar tests
- `requirements.txt` – Python dependencies shared across agent scripts

## Prerequisites
- Python 3.11 or newer
- Node.js 18+ (for the Vite dev server)
- Accounts/API keys for LiveKit, OpenAI, and Bey avatars

## Environment Variables
Create `AGENT/keys.env` (and optionally copy it to the repo root) with:

```
LIVEKIT_URL=wss://<your-livekit>.livekit.cloud
LIVEKIT_API_KEY=...
LIVEKIT_API_SECRET=...
LIVEKIT_DEFAULT_ROOM=galactactocus-room      # optional override
OPENAI_API_KEY=...
BEY_API_KEY=...
BEY_AVATAR_ID=...
```

> Do **not** commit credentials to version control.

## Installation
```bash
# Python deps
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Frontend deps
cd frontend
npm install
```

## Running the Stack
1. **Start the LiveKit agent**
   ```bash
   cd AGENT
   python main.py
   ```
   Logs confirm connection to the LiveKit cloud project and show data/chat events.

2. **Launch the token server** (serves `/token` for the frontend)
   ```bash
   cd AGENT
   python token_server.py --port 8081
   ```
   Adjust the port as needed; the server serves static assets and mints JWTs.

3. **Run the React client**
   ```bash
   cd frontend
   npm run dev
   ```
   Open the printed Vite URL (defaults to `http://127.0.0.1:5173`). Update `frontend/src/App.jsx` to fetch a token from `http://localhost:8081/token` instead of using the placeholder JWT.

4. **Chat**
   - Enter the same room name in the frontend that the agent joins (default `galactactocus-room`).
   - Send chat messages; the agent replies via data packets and renders the Bey avatar’s audio/video streams.

## Additional Scripts
- `agent_worker.py` – Simple example that starts an `AgentSession` with minimal instructions, useful for smoke tests without the full RAG pipeline.

## Troubleshooting
- **Authentication** – Confirm `AGENT/keys.env` is loaded (the agent logs missing credentials). Regenerate LiveKit API keys if tokens are rejected.
- **Token issues** – The React app must request a fresh token; placeholder JWTs expire quickly. Watch the token server logs for failures.
- **Document loading** – Ensure `infos/` contains readable PDFs or text files; initialization logs display counts and errors.
- **Room mismatch** – The agent, token server, and browser must reference the same `room` string.

## Next Steps
- Wire the React client to call the token endpoint automatically.
- Harden the token server (HTTPS, stricter CORS) before deploying beyond local environments.
