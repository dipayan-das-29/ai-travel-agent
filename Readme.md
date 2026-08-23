# AI Travel Agent Monorepo

Integrated travel planning agent with a Python FastAPI backend and Angular dashboard frontend.

## Structure
- `/backend`: Python FastAPI application powering agent workflows.
- `/frontend`: Angular SPA interface.

## Local Setup

### 1. Backend Setup

bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\activate
pip install -r requirements.txt
python main.py

### 2. Frontend Setup

bash
cd frontend
npm install
ng serve