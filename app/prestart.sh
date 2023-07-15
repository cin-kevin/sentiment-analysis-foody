#! /usr/bin/env bash

# Let the DB start
python prestart.py

# Run migrations
alembic upgrade head

# # Create initial data in DB
python initdb.py

uvicorn webapi.app.main:app --host 0.0.0.0 --port 80
