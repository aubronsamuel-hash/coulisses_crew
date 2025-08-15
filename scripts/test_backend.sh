#!/usr/bin/env bash
if [ -d .venv ]; then
  pytest -q
else
  docker compose exec api pytest -q
fi
