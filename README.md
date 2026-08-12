# Travel Booking Agent

AI travel agent: search flights/hotels via natural language, email results. Split into two deployable apps in one repo.

**Live:** [travel-booking-agent-app.vercel.app](https://travel-booking-agent-app.vercel.app/) (backend on Railway)

## Structure

- `backend/` — FastAPI + LangGraph agent (Claude Sonnet, SerpAPI, Resend). Deploy to Railway.
- `frontend/` — Next.js + React UI. Deploy to Vercel.

## Deploy

**Backend (Railway):**
1. Create a new project, deploy from this repo, set root directory to `backend/`
2. Add env vars: `ANTHROPIC_API_KEY`, `SERPAPI_API_KEY`, `RESEND_API_KEY`, `FROM_EMAIL`

**Frontend (Vercel):**
1. Import this repo, set root directory to `frontend/`
2. Add env var: `NEXT_PUBLIC_API_URL` = your Railway backend URL

See `backend/README.md` and `frontend/README.md` for local dev setup.
