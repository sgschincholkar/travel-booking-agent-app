# Travel Booking Agent Backend

FastAPI backend for the travel booking agent. Handles LangGraph agent logic, flight/hotel search, and email sending.

## Setup

1. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure `.env`:
```bash
cp .env.example .env
# Edit .env with your API keys:
# - ANTHROPIC_API_KEY
# - SERPAPI_API_KEY
# - RESEND_API_KEY
# - FROM_EMAIL
```

## Run Locally

```bash
python main.py
```

Server runs on `http://localhost:8000`
- Health check: `GET /health`
- API docs: `http://localhost:8000/docs`

## API Endpoints

### POST `/api/query`
Process travel query through agent.

**Request:**
```json
{
  "query": "Flights from NYC to LA next week, 3-star hotels"
}
```

**Response:**
```json
{
  "thread_id": "uuid",
  "response": "Agent's travel recommendation..."
}
```

### POST `/api/send-email`
Send travel results via email.

**Request:**
```json
{
  "thread_id": "uuid-from-query",
  "sender": "your@email.com",
  "receiver": "recipient@email.com",
  "subject": "Your Travel Plan"
}
```

**Response:**
```json
{
  "status": "Email sent (id xxx)"
}
```

## Deployment (HF Spaces)

1. Create Space at huggingface.co/spaces
2. Add secrets:
   - `ANTHROPIC_API_KEY`
   - `SERPAPI_API_KEY`
   - `RESEND_API_KEY`
   - `FROM_EMAIL`
3. Connect GitHub repo and deploy
