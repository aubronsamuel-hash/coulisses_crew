# Clean Base

FastAPI backend with Vite + React frontend.

## Development

### Start services
- **PowerShell**: `./scripts/dev_up.ps1`
- **Bash**: `./scripts/dev_up.sh`

### Stop services
- **PowerShell**: `./scripts/dev_down.ps1`
- **Bash**: `./scripts/dev_down.sh`

Backend available at http://localhost:8001
Frontend available at http://localhost:5173

Frontend expects `VITE_API_URL` (see `frontend/.env.example`).

## Tests

- **PowerShell**: `./scripts/test_backend.ps1`
- **Bash**: `./scripts/test_backend.sh`

These run `pytest -q` against the backend.
