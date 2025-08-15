# Coulisses Crew Clean Base

## Development Environment

### Windows PowerShell

```powershell
# start containers
./scripts/dev_up.ps1

# run backend tests
./scripts/test_backend.ps1

# stop containers
./scripts/dev_down.ps1
```

### Bash

```bash
# start containers
docker compose up -d --build

# run backend tests
docker compose exec api pytest -q

# stop containers
docker compose down -v
```
