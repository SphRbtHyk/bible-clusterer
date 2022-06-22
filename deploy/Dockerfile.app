
FROM python:3.8-slim

# Update pip
RUN python3 -m pip install --upgrade pip

# Copy project files of app
COPY app /app

# Make as workdir main Python directory
WORKDIR /app

# Install packages
RUN python3 -m pip install -r gnt_core/requirements.txt && \
    python3 -m pip install -e ./gnt_core && \
    python3 -m pip install -r gnt_nlp_utils/requirements.txt && \
    python3 -m pip install -e ./gnt_nlp_utils && \
    python3 -m pip install -r gnt_api/external-requirements.txt && \
    python3 -m pip install -e ./gnt_api

# Source environment file, fill database and serve API
ENTRYPOINT python3 ./gnt_core/gnt_core/database_filler.py && python -m uvicorn gnt_api.main:app --port 8000 --host 0.0.0.0

CMD "--root-path=/api"