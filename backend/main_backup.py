from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import datetime
import uuid
from knowledge_base import search_knowledge

# --------------------------------------------------
# 1. CREATE FASTAPI APPLICATION
# --------------------------------------------------

app = FastAPI(
    title="AI-Powered ITSM Helpdesk",
    description="Intelligent IT Helpdesk Automation Platform",
    version="1.0.0"
)

# Allow React frontend to communicate with FastAPI
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# Temporary in-memory storage
# We will connect MongoDB Atlas later.

tickets = []
software_requests = []
audit_logs = []


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
        "status": "success"
    }


# --------------------------------------------------
# 4. HEALTH CHECK
# --------------------------------------------------

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "application": "AI ITSM Helpdesk"
    }


# --------------------------------------------------
# 5. INTELLIGENT TICKET CLASSIFICATION
# --------------------------------------------------

def classify_ticket(message: str):

    text = message.lower()

    # VPN issue
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
            )
        }

    # Password issue
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
            )
        }

    # Outlook issue
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
            )
        }

    # Software installation request
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
            )
        }

    # Wi-Fi issue
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
            )
        }

    # Unknown request
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
            )
        }


# --------------------------------------------------
# 6. ANALYZE EMPLOYEE REQUEST
# --------------------------------------------------

@app.post("/analyze")
def analyze_ticket(request: TicketRequest):

    analysis = classify_ticket(request.message)

    return {
        "message": request.message,
        "analysis": analysis
    }


# --------------------------------------------------
# 7. CREATE INCIDENT / SERVICE TICKET
# --------------------------------------------------

@app.post("/tickets")
def create_ticket(request: TicketRequest):

    analysis = classify_ticket(request.message)

    ticket_id = "INC" + str(1000 + len(tickets) + 1)

    ticket = {
        "ticket_id": ticket_id,
        "description": request.message,
        **analysis,
        "status": "Open",
        "created_at": datetime.now().isoformat(),
        "integration": "Mock ServiceNow"
    }

    tickets.append(ticket)

    return {
        "message": "Ticket created successfully",
        "ticket": ticket
    }


# --------------------------------------------------
# 8. VIEW ALL TICKETS
# --------------------------------------------------

@app.get("/tickets")
def get_tickets():

    return {
        "total_tickets": len(tickets),
        "tickets": tickets
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
        "timestamp": datetime.now().isoformat()
    }

    audit_logs.append(audit_entry)

    return {
        "issue": request.issue,
        "action": action,
        "status": status,
        "message": message,
        "audit_log": audit_entry
    }


# --------------------------------------------------
# 10. SOFTWARE PROVISIONING
# --------------------------------------------------

SOFTWARE_CATALOGUE = [
    "Visual Studio Code",
    "Python",
    "Google Chrome",
    "Notepad++"
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
        None
    )

    if not available_software:

        return {
            "status": "Rejected",
            "message": "Software is not available in the catalogue.",
            "available_software": SOFTWARE_CATALOGUE
        }

    request_id = "REQ" + str(1000 + len(software_requests) + 1)

    software_request = {
        "request_id": request_id,
        "software": available_software,
        "status": "Provisioning",
        "integration": "Mock ServiceNow",
        "created_at": datetime.now().isoformat()
    }

    software_requests.append(software_request)

    audit_logs.append({
        "audit_id": str(uuid.uuid4()),
        "action": "Software Provisioning",
        "software": available_software,
        "request_id": request_id,
        "status": "Provisioning",
        "timestamp": datetime.now().isoformat()
    })

    return {
        "message": "Software request created successfully",
        "request": software_request
    }


# --------------------------------------------------
# 11. VIEW AUDIT LOGS
# --------------------------------------------------

@app.get("/audit-logs")
def get_audit_logs():

    return {
        "total_logs": len(audit_logs),
        "logs": audit_logs
    }


# --------------------------------------------------
# 12. DASHBOARD STATISTICS
# --------------------------------------------------

@app.get("/dashboard")
def get_dashboard():

    total_tickets = len(tickets)

    open_tickets = sum(
        1 for ticket in tickets
        if ticket["status"] == "Open"
    )

    total_software_requests = len(software_requests)

    successful_automations = sum(
        1 for log in audit_logs
        if log["status"] == "Success"
    )

    escalated_requests = sum(
        1 for log in audit_logs
        if log["status"] == "Escalated"
    )

    return {
        "total_tickets": total_tickets,
        "open_tickets": open_tickets,
        "software_requests": total_software_requests,
        "successful_automations": successful_automations,
        "escalated_requests": escalated_requests
    }

@app.post("/chat")
def chat(request: TicketRequest):
    question = request.message

    results = search_knowledge(question, top_k=3)

    if not results:
        return {
            "question": question,
            "status": "escalated",
            "answer": (
                "I could not find a reliable answer. "
                "Please contact IT support."
            ),
            "sources": [],
            "method": "Sentence Transformers + FAISS"
        }

    best_result = results[0]

    if best_result["similarity"] < 0.35:
        return {
            "question": question,
            "status": "escalated",
            "answer": (
                "I could not find a reliable answer. "
                "Please contact IT support."
            ),
            "sources": [],
            "method": "Sentence Transformers + FAISS"
        }

    return {
        "question": question,
        "status": "answered",
        "answer": best_result["content"],
        "sources": [
            {
                "title": result["title"],
                "source": result["source"],
                "similarity": result["similarity"]
            }
            for result in results
        ],
        "method": "Sentence Transformers + FAISS"
    }

# --------------------------------------------------
# AI KNOWLEDGE BASE CHAT API
# --------------------------------------------------
# --------------------------------------------------
# AI KNOWLEDGE BASE CHAT API
# --------------------------------------------------

@app.post("/chat")
def chat_with_knowledge_base(request: TicketRequest):

    question = request.message.strip()

    if not question:
        return {
            "question": question,
            "status": "error",
            "answer": "Please enter a question.",
            "sources": []
        }

    # Search the knowledge base
    results = search_knowledge(question, top_k=3)

    # Minimum similarity threshold
    min_similarity = 0.35

    relevant_results = [
        result
        for result in results
        if result["similarity"] >= min_similarity
    ]

    # Escalate unsupported questions
    if not relevant_results:
        return {
            "question": question,
            "status": "escalated",
            "answer": (
                "I could not find sufficiently relevant information "
                "in the approved knowledge base. Please contact IT Support."
            ),
            "sources": [],
            "method": "Sentence Transformers + FAISS"
        }

    # Return the best matching knowledge chunk
    best_result = relevant_results[0]

    answer = best_result["content"]

    # Return source attribution
    sources = [
        {
            "title": result["title"],
            "source": result["source"],
            "similarity": result["similarity"]
        }
        for result in relevant_results
    ]

    return {
        "question": question,
        "status": "answered",
        "answer": answer,
        "sources": sources,
        "method": "Sentence Transformers + FAISS"
    }
