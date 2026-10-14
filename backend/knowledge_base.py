from pathlib import Path

import faiss
import numpy as np
from sentence_transformers import SentenceTransformer


# --------------------------------------------------
# 1. CONFIGURATION
# --------------------------------------------------

KNOWLEDGE_DIR = Path(__file__).parent / "knowledge"

MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

print("Loading embedding model...")

model = SentenceTransformer(MODEL_NAME)

documents = []
document_sources = []
index = None


# --------------------------------------------------
# 2. TOPIC KEYWORDS
# --------------------------------------------------

TOPIC_KEYWORDS = {
    "password_reset.txt": [
        "password",
        "reset password",
        "forgot password",
        "password reset",
        "reset my password",
        "password reset link",
        "reset email",
        "account unlock",
        "locked account",
    ],

    "vpn.txt": [
        "vpn",
        "virtual private network",
        "vpn connection",
        "vpn not connecting",
        "vpn authentication",
    ],

    "outlook.txt": [
        "outlook",
        "email",
        "e-mail",
        "mailbox",
        "send email",
        "receive email",
        "email synchronization",
        "email sync",
    ],

    "wifi.txt": [
        "wifi",
        "wi-fi",
        "wireless network",
        "internet connection",
        "network connection",
    ],

    "software_installation.txt": [
        "install software",
        "software installation",
        "install application",
        "visual studio code",
        "vscode",
        "install python",
        "install chrome",
    ],

    "account_locked.txt": [
        "account locked",
        "locked account",
        "account lockout",
        "unlock account",
        "account is locked",
    ],

    "printer.txt": [
        "printer",
        "printing",
        "paper jam",
        "printer offline",
        "not printing",
        "print queue",
    ],

    "laptop_performance.txt": [
        "slow laptop",
        "laptop performance",
        "slow computer",
        "computer is slow",
        "computer running slowly",
        "computer freezes",
        "laptop freezes",
    ],
}


# --------------------------------------------------
# 3. LOAD COMPLETE KNOWLEDGE DOCUMENTS
# --------------------------------------------------

def load_knowledge_documents():
    """
    Load each knowledge-base file as one complete document.

    Unlike paragraph-based chunking, this approach preserves
    the original order of instructions within each file.
    """

    global documents, document_sources

    documents = []
    document_sources = []

    if not KNOWLEDGE_DIR.exists():
        raise RuntimeError(
            f"Knowledge directory does not exist: {KNOWLEDGE_DIR}"
        )

    for file_path in sorted(KNOWLEDGE_DIR.glob("*.txt")):

        content = file_path.read_text(
            encoding="utf-8"
        ).strip()

        if not content:
            print(f"Skipping empty knowledge file: {file_path.name}")
            continue

        documents.append(content)

        document_sources.append({
            "source": file_path.name,
            "title": file_path.stem.replace("_", " ").title(),
        })

    if not documents:
        raise RuntimeError(
            f"No readable knowledge documents found in {KNOWLEDGE_DIR}"
        )

    print(f"Loaded {len(documents)} knowledge documents.")

    return documents


# --------------------------------------------------
# 4. BUILD FAISS INDEX
# --------------------------------------------------

def build_vector_index():
    """
    Build the FAISS index using complete knowledge documents.
    """

    global index

    load_knowledge_documents()

    embeddings = model.encode(
        documents,
        convert_to_numpy=True,
        normalize_embeddings=True,
        show_progress_bar=False,
    )

    embeddings = np.asarray(
        embeddings,
        dtype=np.float32,
    )

    index = faiss.IndexFlatIP(
        embeddings.shape[1]
    )

    index.add(embeddings)

    print("FAISS index created successfully.")

    return len(documents)


# --------------------------------------------------
# 5. IDENTIFY THE BEST-MATCHING TOPIC
# --------------------------------------------------

def identify_preferred_files(question):
    """
    Identify the most relevant knowledge-base topic.

    More specific topics are checked before general topics.
    """

    question_lower = question.lower()

    # Account-lock issues should be distinguished from
    # ordinary password-reset questions.
    if any(
        keyword in question_lower
        for keyword in [
            "account locked",
            "locked account",
            "account lockout",
            "unlock account",
            "account is locked",
        ]
    ):
        return ["account_locked.txt", "password_reset.txt"]

    matches = []

    for filename, keywords in TOPIC_KEYWORDS.items():

        if any(
            keyword in question_lower
            for keyword in keywords
        ):
            matches.append(filename)

    # If a password-related question does not explicitly
    # concern a locked account, prefer the password guide.
    return matches


# --------------------------------------------------
# 6. SEARCH KNOWLEDGE BASE
# --------------------------------------------------

def search_knowledge(question, top_k=3):
    """
    Retrieve relevant knowledge documents.

    The returned content contains complete documents,
    preserving the order of instructions in each file.
    """

    global index

    question = question.strip()

    if not question:
        return []

    if index is None or not documents:
        build_vector_index()

    # Embed the question.
    question_embedding = model.encode(
        [question],
        convert_to_numpy=True,
        normalize_embeddings=True,
        show_progress_bar=False,
    )

    question_embedding = np.asarray(
        question_embedding,
        dtype=np.float32,
    )

    # Search the complete FAISS index.
    scores, indices = index.search(
        question_embedding,
        len(documents),
    )

    results = []

    for score, idx in zip(scores[0], indices[0]):

        if idx < 0:
            continue

        source_info = document_sources[idx]

        results.append({
            "content": documents[idx],
            "source": source_info["source"],
            "title": source_info["title"],
            "similarity": round(float(score), 4),
        })

    # Results from FAISS are initially sorted by similarity.
    preferred_files = identify_preferred_files(question)

    if preferred_files:

        preferred_results = [
            result
            for result in results
            if result["source"] in preferred_files
        ]

        if preferred_results:
            # Only return topic-specific documents when
            # an appropriate document has been identified.
            results = preferred_results

    # Return at most top_k results.
    return results[:max(1, top_k)]


# --------------------------------------------------
# 7. TEST THE KNOWLEDGE BASE
# --------------------------------------------------

if __name__ == "__main__":

    total = build_vector_index()

    print("\nKnowledge base initialized successfully.")
    print("Total searchable documents:", total)

    test_questions = [
        "How can I reset my password?",
        "My VPN is not connecting",
        "I cannot send emails in Outlook",
        "My laptop cannot connect to Wi-Fi",
        "How do I install Visual Studio Code?",
        "My account is locked",
        "My printer is not printing",
        "My computer is running slowly",
    ]

    for question in test_questions:

        print("\n" + "=" * 60)
        print("Question:", question)

        results = search_knowledge(
            question,
            top_k=3,
        )

        if not results:
            print("No matching knowledge document found.")
            continue

        for result in results:

            print("\nSource:", result["source"])
            print("Title:", result["title"])
            print("Similarity:", result["similarity"])

            # Print only a short preview during testing.
            preview = result["content"][:300]

            print("Content preview:", preview)