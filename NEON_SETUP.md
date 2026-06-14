# Neon Setup for Print Your Fit

## Project Details
- **Project ID**: proud-dawn-25444586
- **Project Name**: pyf-db
- **Organization**: org-damp-cell-12280598
- **Region**: us-east-1 (AWS)

## Branches

### Production Branch
- **Branch ID**: br-little-night-aile52ic
- **Name**: production (default)
- **Connection String** (sync): `postgresql://neondb_owner:npg_D3JyvWqInPk6@ep-wandering-tree-aieuwvuh-pooler.c-4.us-east-1.aws.neon.tech/neondb?channel_binding=require&sslmode=require`
- **Connection String** (async): Use in `.env` for production deployments

### Development Branch
- **Branch ID**: br-winter-unit-aisg0hgb
- **Name**: development
- **Connection String** (sync): `postgresql://neondb_owner:npg_D3JyvWqInPk6@ep-noisy-forest-ai7q3teh-pooler.c-4.us-east-1.aws.neon.tech/neondb?channel_binding=require&sslmode=require`
- **Connection String** (async): Use in `.env.development` for local testing

## Environment Files

### `.env` (Production)
Uses production branch connection string. This is what will be deployed.

### `.env.development` (Local Development)
Uses development branch connection string. Switch to this locally to test schema changes safely.

## Quick Start

### 1. Install Dependencies
```bash
cd pyf-backend
pip install -r requirements.txt
```

### 2. Run Migrations
```bash
# Against development branch
alembic upgrade head

# Or explicitly:
ALEMBIC_SQLALCHEMY_URL=$(grep DATABASE_URL .env.development | cut -d= -f2-) alembic upgrade head
```

### 3. Start Development Server
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## Schema Management

- All migrations are in `alembic/versions/`
- The async database connection is configured in `app/core/database.py`
- Use `alembic revision --autogenerate -m "description"` to create new migrations

## Important Notes

- Neon automatically provisions SSL/TLS, enforced via `sslmode=require` in connection strings
- The pooler endpoint (`-pooler.`) is used for connection pooling
- Development branch is isolated from production—safe for testing schema changes
- Always test migrations in the development branch before applying to production

## Next Steps

1. ✅ Environment configured with Neon connection
2. ✅ Development branch created for safe testing
3. **Run migrations**: `alembic upgrade head`
4. **Start backend**: `uvicorn main:app --reload`
5. **Continue with frontend**: `npm run dev` from `pyf-frontend/`
