#!/bin/bash
set -euo pipefail

log() { printf '▶ %s\n' "$*"; }
log "Starting Zuma server..."


if [ -f "zuma.db" ]; then
    log "Dropping existing database..."
    rm zuma.db
fi


log "Seeding database..."
python seed.py


log "Starting server..."
uvicorn main:app --host 0.0.0.0 --port 9000 --reload