from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import datetime
import uuid

from knowledge_base import search_knowledge

from mongodb_integration import (
    save_ticket_to_mongodb,
    get_tickets_from_mongodb,
    save_software_request_to_mongodb,
    get_software_requests_from_mongodb,
    save_audit_log_to_mongodb,
    get_audit_logs_from_mongodb,
)


# --------------------------------------------------
# 1. CREATE FASTAPI APPLICATION
# --------------------------------------------------

app = FastAPI(
    title="AI-Powered ITSM Helpdesk",
    description="Intelligent IT Helpdesk Automation Platform",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# --------------------------------------------------
# 2. REQUEST MODELS
# --------------------------------------------------

class TicketRequest(BaseModel):
    message: str


class AutomationRequest(BaseModel):
    issue: str


class SoftwareRequest(BaseModel):
    software: str


# --------------------------------------------------
# 3. HOME ENDPOINT
# --------------------------------------------------

@app.get("/")
def home():
    return {
        "message": "AI-Powered ITSM Helpdesk is running!",
        "status": "success",
    }


# --------------------------------------------------
# 4. HEALTH CHECK
# --------------------------------------------------

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "application": "AI ITSM Helpdesk",
    }


# --------------------------------------------------
# 5. INTELLIGENT TICKET CLASSIFICATION
# --------------------------------------------------

def classify_ticket(message: str):
    text = message.lower()

    if "vpn" in text:
        return {
            "intent": "Incident",
            "category": "Network",
            "subcategory": "VPN",
            "priority": "P2",
            "impact": "Individual",
            "urgency": "High",
            "assignment_group": "Network Support",
            "summary": "VPN connectivity or authentication failure",
            "resolution": (
                "Check internet connectivity, VPN credentials, "
                "and authentication settings."
            ),
        }

    elif "password" in text:
        return {
            "intent": "Automatable Issue",
            "category": "Access",
            "subcategory": "Password",
            "priority": "P3",
            "impact": "Individual",
            "urgency": "Medium",
            "assignment_group": "IT Support",
            "summary": "Password reset request",
            "resolution": (
                "Follow the approved password reset procedure."
            ),
        }

    elif "outlook" in text:
        return {
            "intent": "Knowledge Question",
            "category": "Software",
            "subcategory": "Outlook",
            "priority": "P3",
            "impact": "Individual",
            "urgency": "Medium",
            "assignment_group": "IT Support",
            "summary": "Outlook troubleshooting request",
            "resolution": (
                "Check internet connectivity, restart Outlook, "
                "and verify synchronization settings."
            ),
        }

    elif (
        "install" in text
        or "software" in text
        or "visual studio code" in text
        or "vscode" in text
    ):
        return {
            "intent": "Service Request",
            "category": "Software",
            "subcategory": "Installation",
            "priority": "P3",
            "impact": "Individual",
            "urgency": "Medium",
            "assignment_group": "IT Support",
            "summary": "Software installation request",
            "resolution": (
                "Check the software catalogue and create "
                "a provisioning request."
            ),
        }

    elif "wifi" in text or "wi-fi" in text:
        return {
            "intent": "Incident",
            "category": "Network",
            "subcategory": "Wi-Fi",
            "priority": "P2",
            "impact": "Individual",
            "urgency": "High",
            "assignment_group": "Network Support",
            "summary": "Wi-Fi connectivity issue",
            "resolution": (
                "Check Wi-Fi settings, network availability, "
                "and device connectivity."
            ),
        }

    else:
        return {
            "intent": "Unknown",
            "category": "General",
            "subcategory": "Other",
            "priority": "P3",
            "impact": "Individual",
            "urgency": "Medium",
            "assignment_group": "IT Support",
            "summary": "General IT support request",
            "resolution": (
                "The knowledge base has not yet verified a solution. "
                "Further investigation or human support is required."
            ),
        }


# --------------------------------------------------
# 6. ANALYZE EMPLOYEE REQUEST
# --------------------------------------------------

@app.post("/analyze")
def analyze_ticket(request: TicketRequest):
    analysis = classify_ticket(request.message)

    return {
        "message": request.message,
        "analysis": analysis,
    }


# --------------------------------------------------
# 7. CREATE INCIDENT / SERVICE TICKET
# --------------------------------------------------

@app.post("/tickets")
def create_ticket(request: TicketRequest):
    analysis = classify_ticket(request.message)

    ticket_count = len(get_tickets_from_mongodb())
    ticket_id = "INC" + str(1000 + ticket_count + 1)

    ticket = {
        "ticket_id": ticket_id,
        "description": request.message,
        **analysis,
        "status": "Open",
        "created_at": datetime.now().isoformat(),
        "integration": "Mock ServiceNow",
    }

    save_ticket_to_mongodb(ticket)

    return {
        "message": "Ticket created successfully",
        "ticket": ticket,
    }


# --------------------------------------------------
# 8. VIEW ALL TICKETS
# --------------------------------------------------

@app.get("/tickets")
def get_tickets():
    stored_tickets = get_tickets_from_mongodb()

    return {
        "total_tickets": len(stored_tickets),
        "tickets": stored_tickets,
    }


# --------------------------------------------------
# 9. MOCK SELF-HEALING AUTOMATION
# --------------------------------------------------

@app.post("/automation")
def execute_automation(request: AutomationRequest):
    issue = request.issue.lower()

    if "password" in issue:
        action = "Password Reset Simulation"
        status = "Success"

        message = (
            "The password reset workflow completed in simulation. "
            "No actual account password was changed."
        )

    elif "account unlock" in issue or "locked account" in issue:
        action = "Account Unlock Simulation"
        status = "Success"

        message = (
            "The account unlock workflow completed in simulation. "
            "No actual account was unlocked."
        )

    else:
        action = "Manual Investigation"
        status = "Escalated"

        message = (
            "This issue is not supported by the current "
            "automation rules. Human support is required."
        )

    audit_entry = {
        "audit_id": str(uuid.uuid4()),
        "issue": request.issue,
        "action": action,
        "status": status,
        "timestamp": datetime.now().isoformat(),
    }

    save_audit_log_to_mongodb(audit_entry)

    return {
        "issue": request.issue,
        "action": action,
        "status": status,
        "message": message,
        "audit_log": audit_entry,
    }


# --------------------------------------------------
# 10. SOFTWARE PROVISIONING
# --------------------------------------------------

SOFTWARE_CATALOGUE = [
    "Visual Studio Code",
    "Python",
    "Google Chrome",
    "Notepad++",
]


@app.post("/software-requests")
def create_software_request(request: SoftwareRequest):
    requested_software = request.software.strip()

    available_software = next(
        (
            software
            for software in SOFTWARE_CATALOGUE
            if software.lower() == requested_software.lower()
        ),
        None,
    )

    if not available_software:
        return {
            "status": "Rejected",
            "message": "Software is not available in the catalogue.",
            "available_software": SOFTWARE_CATALOGUE,
        }

    existing_requests = get_software_requests_from_mongodb()
    request_id = "REQ" + str(1000 + len(existing_requests) + 1)

    software_request = {
        "request_id": request_id,
        "software": available_software,
        "status": "Provisioning",
        "integration": "Mock ServiceNow",
        "created_at": datetime.now().isoformat(),
    }

    save_software_request_to_mongodb(software_request)

    audit_entry = {
        "audit_id": str(uuid.uuid4()),
        "action": "Software Provisioning",
        "software": available_software,
        "request_id": request_id,
        "status": "Provisioning",
        "timestamp": datetime.now().isoformat(),
    }

    save_audit_log_to_mongodb(audit_entry)

    return {
        "message": "Software request created successfully",
        "request": software_request,
    }


# --------------------------------------------------
# 11. VIEW AUDIT LOGS
# --------------------------------------------------

@app.get("/audit-logs")
def get_audit_logs():
    stored_logs = get_audit_logs_from_mongodb()

    return {
        "total_logs": len(stored_logs),
        "logs": stored_logs,
    }


# --------------------------------------------------
# 12. DASHBOARD STATISTICS
# --------------------------------------------------

@app.get("/dashboard")
def get_dashboard():
    stored_tickets = get_tickets_from_mongodb()
    stored_requests = get_software_requests_from_mongodb()
    stored_logs = get_audit_logs_from_mongodb()

    total_tickets = len(stored_tickets)

    open_tickets = sum(
        1
        for ticket in stored_tickets
        if ticket.get("status") == "Open"
    )

    total_software_requests = len(stored_requests)

    successful_automations = sum(
        1
        for log in stored_logs
        if log.get("status") == "Success"
    )

    escalated_requests = sum(
        1
        for log in stored_logs
        if log.get("status") == "Escalated"
    )

    return {
        "total_tickets": total_tickets,
        "open_tickets": open_tickets,
        "software_requests": total_software_requests,
        "successful_automations": successful_automations,
        "escalated_requests": escalated_requests,
    }


# --------------------------------------------------
# 13. KNOWLEDGE BASE CHAT API
# Sentence Transformers + FAISS
# Retrieval-only; no external LLM required
# --------------------------------------------------

@app.post("/chat")
def chat_with_knowledge_base(request: TicketRequest):
    question = request.message.strip()

    if not question:
        return {
            "question": question,
            "status": "error",
            "answer": "Please enter a question.",
            "sources": [],
            "method": "Sentence Transformers + FAISS (retrieval-only)",
        }

    results = search_knowledge(question, top_k=8)

    min_similarity = 0.25

    relevant_results = [
        result
        for result in results
        if result.get("similarity", 0) >= min_similarity
    ]

    # Prefer results from the most relevant document.
    if relevant_results:
        best_source = relevant_results[0].get("source")

        if best_source:
            relevant_results = [
                result
                for result in relevant_results
                if result.get("source") == best_source
            ]

    if not relevant_results:
        return {
            "question": question,
            "status": "escalated",
            "answer": (
                "I could not find a sufficiently relevant solution "
                "in the approved knowledge base. Please contact IT Support."
            ),
            "sources": [],
            "method": "Sentence Transformers + FAISS (retrieval-only)",
        }

    answer_parts = []
    seen_content = set()

    for result in relevant_results:
        content = result.get("content", "").strip()

        if content and content not in seen_content:
            answer_parts.append(content)
            seen_content.add(content)

    if not answer_parts:
        return {
            "question": question,
            "status": "escalated",
            "answer": (
                "No readable solution was found in the knowledge base. "
                "Please contact IT Support."
            ),
            "sources": [],
            "method": "Sentence Transformers + FAISS (retrieval-only)",
        }

    answer = (
        "Based on the IT knowledge base:\n\n"
        + "\n\n".join(answer_parts)
    )

    if "contact it support" not in answer.lower():
        answer += (
            "\n\nIf the issue persists, please contact IT Support."
        )

    sources = [
        {
            "title": result.get("title", "IT Knowledge Base"),
            "source": result.get("source", "Unknown"),
            "similarity": result.get("similarity", 0),
        }
        for result in relevant_results
    ]

    return {
        "question": question,
        "status": "answered",
        "answer": answer,
        "sources": sources,
        "method": "Sentence Transformers + FAISS (retrieval-only)",
    }