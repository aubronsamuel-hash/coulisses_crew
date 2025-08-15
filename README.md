# Coulisses Crew

Minimal authentication service using FastAPI with bcrypt hashing.

## Development

A docker-compose setup runs the API and the front-end.

### Windows (PowerShell)

```powershell
./scripts/dev_up.ps1
./scripts/test_backend.ps1
./scripts/dev_down.ps1
```

### Bash

```bash
docker compose up -d --build
docker compose exec api pytest -q
docker compose down -v
```

### Local URLs

- API: http://localhost:8000
- Frontend: http://localhost:5173

See `frontend/index.html` for a simple login form.
