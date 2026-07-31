# Travel Booking Agent Frontend

Modern Next.js + React frontend for the travel booking agent. Beautiful UI for searching flights, hotels, and sending results via email.

## Setup

1. Install dependencies:
```bash
npm install
```

2. Configure `.env.local`:
```bash
cp .env.example .env.local
# Update with your backend API URL
# Development: http://localhost:8000
# Production: https://sgschincholkar-travel-booking-agent-api.hf.space
```

## Development

```bash
npm run dev
```

Open http://localhost:3000

## Build & Deploy

```bash
npm run build
npm start
```

## Deployment to Vercel

1. Push to GitHub
2. Connect repo to Vercel
3. Set environment variable:
   - `NEXT_PUBLIC_API_URL` = your HF Spaces backend URL
4. Deploy

## Features

- Search flights and hotels with natural language
- Real-time streaming results
- Email travel plans directly
- Responsive design (mobile, tablet, desktop)
- Dark mode ready
