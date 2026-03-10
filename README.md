# Land Leasing Backend (Python)

Secure backend API for a land leasing platform built with **FastAPI** + **SQLAlchemy**.

## Security measures included
- Password hashing with bcrypt (`passlib`).
- JWT access tokens with issuer, audience, and expiration claims.
- Role-based authorization (`owner`, `tenant`, `admin`).
- Rate limiting on auth endpoints to reduce brute-force attacks.
- Restrictive CORS defaults.
- Security headers (`X-Frame-Options`, `X-Content-Type-Options`, CSP, Referrer-Policy).
- Server-side validation on all request payloads.

## Quick start
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# update SECRET_KEY in .env with a strong random secret
uvicorn app.main:app --reload
```

## Run tests
```bash
pytest -q
```

## API endpoints
- `POST /auth/register`
- `POST /auth/login`
- `GET /healthz`
- `POST /parcels` (owner/admin)
- `GET /parcels`
- `DELETE /parcels/{parcel_id}` (owner/admin)
- `POST /leases` (tenant/admin)
- `PATCH /leases/{lease_id}/status` (owner/admin)
