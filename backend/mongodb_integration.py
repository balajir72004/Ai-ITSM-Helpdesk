from datetime import datetime, timezone

from database import (
    tickets_collection,
    software_requests_collection,
    audit_logs_collection,
)


def save_ticket_to_mongodb(ticket):
    """Save a ticket to MongoDB Atlas."""
    document = ticket.copy()
    document["created_at"] = datetime.now(timezone.utc)

    result = tickets_collection.insert_one(document)

    return str(result.inserted_id)


def save_software_request_to_mongodb(request):
    """Save a software request to MongoDB Atlas."""
    document = request.copy()
    document["created_at"] = datetime.now(timezone.utc)

    result = software_requests_collection.insert_one(document)

    return str(result.inserted_id)


def save_audit_log_to_mongodb(log):
    """Save an audit log to MongoDB Atlas."""
    document = log.copy()
    document["created_at"] = datetime.now(timezone.utc)

    result = audit_logs_collection.insert_one(document)

    return str(result.inserted_id)


def get_tickets_from_mongodb():
    """Retrieve all tickets from MongoDB Atlas."""
    tickets = list(
        tickets_collection.find().sort("_id", -1)
    )

    for ticket in tickets:
        ticket["_id"] = str(ticket["_id"])

    return tickets


def get_software_requests_from_mongodb():
    """Retrieve all software requests from MongoDB Atlas."""
    requests = list(
        software_requests_collection.find().sort("_id", -1)
    )

    for request in requests:
        request["_id"] = str(request["_id"])

    return requests


def get_audit_logs_from_mongodb():
    """Retrieve all audit logs from MongoDB Atlas."""
    logs = list(
        audit_logs_collection.find().sort("_id", -1)
    )

    for log in logs:
        log["_id"] = str(log["_id"])

    return logs