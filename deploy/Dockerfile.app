# Dockerfile containing the Python backend
# Copyright 2020 BULL SAS All rights reserved

FROM python:3.8-slim

# Update pip
RUN python3 -m pip install --upgrade pip

# Make as workdir main Python directory
WORKDIR app/

# Copy project files
COPY . /app

# Install packages
RUN cd /app &&
    python3 -m pip install -r lxx_core/requirements.txt &&
    python3 -m pip install lxx_core --use-feature=in-tree-build &&
    python3 -m pip install -r lxx_nlp_utils/requirements.txt &&
    python3 -m pip install lxx_nlp_utils --use-feature=in-tree-build &&
    python3 -m pip install -r lxx_api/external-requirements.txt
    python3 -m pip install -r lxx_api --use-feature=in-tree-build

# Serve API
CMD ["python", "-m", "uvicorn", "lxx_api.main:app --port 8000 --host 0.0.0.0]