# Travel Booking Agent

AI travel agent: search flights/hotels via natural language, email results. Split into two deployable apps in one repo.

## Structure

- `backend/` — FastAPI + LangGraph agent (Claude Sonnet, SerpAPI, Resend). Deploy to Hugging Face Spaces.
- `frontend/` — Next.js + React UI. Deploy to Vercel.

## Deploy

**Backend (HF Spaces):**
1. Create a new Space (Docker/Python SDK), set root directory to `backend/`
2. Add secrets: `ANTHROPIC_API_KEY`, `SERPAPI_API_KEY`, `RESEND_API_KEY`, `FROM_EMAIL`

**Frontend (Vercel):**
1. Import this repo, set root directory to `frontend/`
2. Add env var: `NEXT_PUBLIC_API_URL` = your HF Spaces backend URL

See `backend/README.md` and `frontend/README.md` for local dev setup.
