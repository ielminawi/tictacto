import os
from typing import Dict
from dotenv import load_dotenv
from openai import OpenAI

# load env so OPENAI_API_KEY is available
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=OPENAI_API_KEY)

# ---- import all known account contexts here ----
from backend.context import techparts_context, tacto_context, google_context, x_context, meta_context
# in the future you'd also import altus_context, acme_context, etc.

# registry maps company_id -> the module (so we can scale)
ACCOUNT_REGISTRY: Dict[str, object] = {
    techparts_context.COMPANY_ID: techparts_context,
    tacto_context.COMPANY_ID: tacto_context,
    google_context.COMPANY_ID: google_context,
    x_context.COMPANY_ID: x_context,
    meta_context.COMPANY_ID: meta_context,
}


SYSTEM_PROMPT = (
    "You are Relationship Memory, a handover assistant for an account. "
    "You ONLY answer using the provided ACCOUNT CONTEXT. "
    "If the answer is not in context, say: 'I cannot verify this from account history.' "
    "Always speak like you're briefing a new account owner who just inherited this relationship. "
    "Answer in 4-6 sentences max. "
    "End with 'Why this matters:' and one sentence of risk."
)


def generate_answer(question: str, company_id: str) -> str:
    """
    Given a user's question and the selected company_id,
    return an answer using that account's memory file.
    """

    # 1. resolve company module
    company_module = ACCOUNT_REGISTRY.get(company_id)
    if company_module is None:
        # This is graceful fallback for unknown companies
        return (
            "I don't have memory for that account yet. "
            "Why this matters: this relationship hasn't been ingested into the system."
        )

    account_context = company_module.ACCOUNT_CONTEXT
    company_name = getattr(company_module, "COMPANY_NAME", company_id)

    # 2. build the user block for the model
    user_block = (
        f"ACCOUNT NAME: {company_name}\n\n"
        f"ACCOUNT CONTEXT:\n{account_context}\n\n"
        f"QUESTION FROM NEW ACCOUNT OWNER:\n{question}\n\n"
        "Remember: ONLY answer using the account context above."
    )

    # 3. call OpenAI
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        temperature=0.2,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_block},
        ],
    )

    answer = completion.choices[0].message.content.strip()
    return answer
