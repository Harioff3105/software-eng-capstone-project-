# AI-Based Scholarship Eligibility and Application Management System

ScholarAI is a full-stack capstone project for student registration, scholarship scheme management, AI-assisted eligibility verification, application tracking and administrator reporting.

## Current Flask implementation
- **Backend:** Python + Flask
- **Database:** SQLite + SQLAlchemy
- **UI:** HTML + CSS + Bootstrap + JavaScript
- **AI:** Gemini API integration through `google-genai`
- **Authentication:** Secure password hashing + Flask session authentication
- **Reporting:** Admin analytics + CSV export

## Five project modules
1. **Student Registration & Authentication** — account creation, login, logout and profile management.
2. **Scholarship Scheme Management** — search for active schemes and admin CRUD/deactivation.
3. **AI-Based Eligibility Verification** — profile/scheme rule checks with Gemini-assisted explanation when configured.
4. **Application Tracking** — duplicate protection, application history and admin status workflow.
5. **Reporting** — platform KPIs, status distribution, scholarship application counts and CSV export.

## Run locally
```bash
python -m venv .venv
# Windows
.venv\\Scripts\\activate
# macOS/Linux
# source .venv/bin/activate
pip install -r requirements.txt
copy .env.example .env  # Windows; use cp on macOS/Linux
python seed.py
python app.py
```

Open `http://127.0.0.1:5000` in a browser. The database is created under `instance/scholarship.db`.

### Admin demo account
The seed script creates `admin@scholarai.local` unless `ADMIN_EMAIL` is set. Set `ADMIN_PASSWORD` before running the seed script; its local-demo fallback is `ChangeMe123!`. Do not use the demo password in production.

### Gemini configuration
Put your Gemini API key in `.env`:
```text
GEMINI_API_KEY=your-key
GEMINI_MODEL=gemini-2.5-flash
```
If no key is configured, eligibility can still use the deterministic scholarship-rule verification path; Gemini is used for AI-assisted explanation when available.

## Tests
Run:
```bash
python -m unittest discover -s tests -v
```

## Existing implementation
The repository's original React/Node/MongoDB/FastAPI stack is retained in `frontend/`, `backend/` and `ml-service/`. The Flask implementation is the aligned capstone path for the requested Python + SQLite + SQLAlchemy + Bootstrap + Gemini architecture; the legacy services were not deleted.
