from mongodb_integration import (
    save_ticket_to_mongodb,
    get_tickets_from_mongodb,
)

# Create a test ticket
ticket = {
    "ticket_id": "TEST1001",
    "category": "VPN",
    "description": "Unable to connect to company VPN",
    "status": "Open",
    "priority": "Medium",
}

# Save ticket to MongoDB
saved_id = save_ticket_to_mongodb(ticket)
print("Ticket saved successfully!")
print("MongoDB ID:", saved_id)

# Retrieve tickets
tickets = get_tickets_from_mongodb()

print("\nTickets stored in MongoDB:")
for item in tickets:
    print(item)