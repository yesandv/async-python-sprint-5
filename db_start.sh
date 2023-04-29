#!/bin/sh

sqlite3 src/storage.db -cmd ".tables" ".quit"

alembic upgrade head

uvicorn src.main:app --host 0.0.0.0 --port 8080 --reload