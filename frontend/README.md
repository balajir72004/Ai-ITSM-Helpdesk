
This template provides a minimal setup to get React working in Vite with HMR and some ESLint rules.

Currently, two official plugins are available:

- [@vitejs/plugin-react](https://github.com/vitejs/vite-plugin-react/blob/main/packages/plugin-react) uses [Oxc](https://oxc.rs)
- [@vitejs/plugin-react-swc](https://github.com/vitejs/vite-plugin-react/blob/main/packages/plugin-react-swc) uses [SWC](https://swc.rs/)

## React Compiler

The React Compiler is not enabled on this template because of its impact on dev & build performances. To add it, see [this documentation](https://react.dev/learn/react-compiler/installation).

## Expanding the ESLint configuration

If you are developing a production application, we recommend using TypeScript with type-aware lint rules enabled. Check out the [TS template](https://github.com/vitejs/vite/tree/main/packages/create-vite/template-react-ts) for information on how to integrate TypeScript and [`typescript-eslint`](https://typescript-eslint.io) in your project.

# AI-Powered ITSM & Intelligent Helpdesk Automation Platform

## Overview

An AI-powered IT Service Management platform that helps employees
report IT issues, retrieve knowledge-base solutions, request software,
and track support activities.

## Technology Stack

### Frontend
- React
- Vite
- CSS

### Backend
- Python
- FastAPI
- Uvicorn

### AI and Search
- Sentence Transformers
- FAISS
- Hugging Face embeddings

### Database
- MongoDB Atlas
- PyMongo

## Features

1. Intelligent IT ticket classification
2. Knowledge-base search with source attribution
3. Safe escalation for unsupported questions
4. Password reset and account unlock simulations
5. Software provisioning request simulation
6. MongoDB-backed ticket storage
7. Persistent audit logs
8. ITSM dashboard statistics

## Project Structure

backend/
- main.py
- database.py
- mongodb_integration.py
- mongodb_service.py
- knowledge_base.py
- knowledge/

frontend/
- src/
- package.json

## Configuration

Create a `.env` file in the project root.

Add:

MONGODB_URI="YOUR_MONGODB_ATLAS_CONNECTION_STRING"
MONGODB_DATABASE="itsm_helpdesk"

Never commit `.env` to version control.

## Run the Backend

Activate the Python virtual environment and run:

python -m uvicorn main:app --reload

Backend:
http://127.0.0.1:8000

API documentation:
http://127.0.0.1:8000/docs

## Run the Frontend

Open another terminal:

cd frontend
npm run dev

Frontend:
http://localhost:5173

## Demo Scenarios

### VPN Incident
Submit an issue describing a company VPN connection failure.

### Knowledge Assistant
Ask how to fix Outlook email synchronization.

### Unsupported Question
Ask how to repair a helicopter engine.
The assistant should escalate unsupported questions.

### Software Request
Request Visual Studio Code from the software catalogue.

## Limitations

- ServiceNow integration is simulated.
- Password reset and account unlock are simulations.
- Software provisioning does not install software.
- Knowledge answers are retrieved from the knowledge base;
  LLM-generated responses are not yet implemented.