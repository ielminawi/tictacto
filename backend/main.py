import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Import Pydantic request/response models
from backend.models.ask_models import AskRequest, AskResponse

# Import the function that handles Q&A logic
from backend.services.qa_service import generate_answer


# --------------------------------------------------------------------
# Initialize FastAPI app
# --------------------------------------------------------------------
app = FastAPI(
    title="Relationship Memory API",
    description="Q&A over organizational relationship memory (Layer 2).",
    version="0.2.0",
)

# --------------------------------------------------------------------
# Allow frontend (Lovable) to access backend
# --------------------------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],           # allow all during dev / hackathon
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# --------------------------------------------------------------------
# Endpoint: /ask
# --------------------------------------------------------------------
@app.post("/ask", response_model=AskResponse)
def ask_endpoint(payload: AskRequest):
    """
    POST /ask
    Body example:
    {
        "question": "What did we agree on payment terms?",
        "company_id": "techparts"
    }

    Returns:
    {
        "answer": "..."
    }
    """
    answer_text = generate_answer(
        question=payload.question,
        company_id=payload.company_id,
    )
    return AskResponse(answer=answer_text)


# --------------------------------------------------------------------
# Local run entrypoint
# --------------------------------------------------------------------
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "backend.main:app",
        host="0.0.0.0",
        port=int(os.getenv("PORT", 8000)),
        reload=True,
    )
