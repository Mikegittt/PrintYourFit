# Print Your Fit (PYF)

A full-stack marketplace application connecting customers, ambassadors, print shops, and admins.

## Backend

Location: `pyf-backend`

### Setup

1. Create a Python virtual environment.
2. Install dependencies: `pip install -r requirements.txt`
3. Copy `.env.example` to `.env` and set your SQLite, Cloudinary, Paystack, and VTPass credentials.
4. Run Alembic migrations:
   - `alembic upgrade head`
5. Start the app:
   - `uvicorn main:app --reload --host 0.0.0.0 --port 8000`

## Frontend

Location: `pyf-frontend`

### Setup

1. Install dependencies: `npm install`
2. Start the dev server: `npm run dev`
3. The app runs at `http://localhost:4173`

## Architecture

- Backend: FastAPI, SQLAlchemy async ORM, SQLite, JWT auth, Cloudinary uploads, Paystack integration.
- Frontend: React, Vite, Tailwind CSS, protected routes, Axios with refresh behavior.

## Notes

- The backend currently scaffolds Stage 1 and Stage 2-ready print shop onboarding.
- The frontend includes dashboards and basic role-based route protection.
