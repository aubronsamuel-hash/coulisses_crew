if (Test-Path .venv) {
    pytest -q
} else {
    docker compose exec api pytest -q
}
