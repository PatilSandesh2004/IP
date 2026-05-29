# InterviewOS Redesign UI

This is a separate frontend app for the InterviewOS redesign.

## What it includes

- Auth pages with the new dark radial layout.
- Onboarding/profile setup wired to the backend schema.
- Dashboard shortcuts.
- Profile editor with chip inputs and JSON fields.
- Resume vs JD analysis with text/file support.
- Interview practice wired to the backend interview endpoints.

## Backend base URL

Set `NEXT_PUBLIC_API_URL=http://localhost:8100` in the app environment.

## Run

```bash
cd ui-redesign
npm install
npm run dev
```

## API Guide

See [API_GUIDE.md](API_GUIDE.md) for the exact endpoint contracts, payloads, and when to use each route.
