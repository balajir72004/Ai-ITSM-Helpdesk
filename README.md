# AI-Powered ITSM & Intelligent Helpdesk Automation Platform

## Overview

An AI-powered IT Service Management platform that helps employees report IT issues, retrieve knowledge-base solutions, request software, and track support activities.

The application uses semantic search to retrieve relevant troubleshooting information from a knowledge base.

## Technology Stack

- **Frontend:** React.js, Vite, CSS
- **Backend:** Python, FastAPI, Uvicorn
- **AI and Search:** Sentence Transformers, FAISS
- **Database:** MongoDB Atlas, PyMongo

## Key Features

- Intelligent IT ticket classification
- Knowledge-base search with source attribution
- Escalation of unsupported questions
- Simulated password reset and account unlock workflows
- Software provisioning request simulation
- IT ticket creation and retrieval
- Audit logging
- ITSM dashboard statistics

## Architecture

The React frontend communicates with the FastAPI backend through REST APIs.

The backend processes support requests and uses Sentence Transformers and FAISS to retrieve relevant troubleshooting documents from the knowledge base.

MongoDB Atlas is used for application data storage when the database connection is configured successfully.

## Setup Instructions

### Prerequisites

- Python
- Node.js and npm
- MongoDB Atlas account

### Backend Setup

From the project directory, activate your Python virtual environment:

```powershell
.\venv\Scripts\Activate.ps1
cd backend
python -m uvicorn main:app --reload
