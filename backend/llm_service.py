import os
from pathlib import Path

from dotenv import load_dotenv
from huggingface_hub import InferenceClient


# Load environment variables from the project root
PROJECT_ROOT = Path(__file__).resolve().parent.parent
load_dotenv(PROJECT_ROOT / ".env")

HF_TOKEN = os.getenv("HF_TOKEN")

# Choose a text-generation model available through
# Hugging Face Inference Providers.
HF_MODEL = os.getenv(
    "HF_MODEL",
    "Qwen/Qwen2.5-7B-Instruct"
)

client = InferenceClient(
    provider="auto",
    api_key=HF_TOKEN
)


def generate_answer(question: str, knowledge_context: str) -> str:
    """
    Generate an answer grounded in retrieved knowledge documents.
    """

    if not HF_TOKEN:
        raise RuntimeError(
            "HF_TOKEN is missing from the project .env file."
        )

    if not knowledge_context.strip():
        raise ValueError("Knowledge context cannot be empty.")

    response = client.chat.completions.create(
        model=HF_MODEL,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are an enterprise IT helpdesk assistant. "
                    "Answer the employee using only the supplied "
                    "knowledge documents. Do not invent procedures, "
                    "policies, or technical steps. If the documents "
                    "do not contain enough information, clearly say "
                    "that IT Support must investigate."
                )
            },
            {
                "role": "user",
                "content": (
                    f"Employee question:\n{question}\n\n"
                    f"Approved knowledge documents:\n"
                    f"{knowledge_context}\n\n"
                    "Provide a clear, concise, step-by-step answer "
                    "where the documents support it."
                )
            }
        ],
        max_tokens=400,
        temperature=0.2
    )

    return response.choices[0].message.content.strip()