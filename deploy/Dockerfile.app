FROM node:14-alpine AS build_front

WORKDIR /app

COPY frontend-vue/package*.json ./

RUN npm install

COPY frontend-vue/ .

RUN npm run build

FROM python:3.8-slim

# Update pip
RUN python3 -m pip install --upgrade pip

# Copy project files of app
COPY app /app

# Make as workdir main Python directory
WORKDIR /app

# Install packages
RUN python3 -m pip install -r clusterer_core/requirements.txt && \
    python3 -m pip install -e ./clusterer_core && \
    python3 -m pip install -r clusterer_nlp_utils/requirements.txt && \
    python3 -m pip install -e ./clusterer_nlp_utils && \
    python3 -m pip install -r clusterer_api/external-requirements.txt && \
    python3 -m pip install -e ./clusterer_api

# Copy web files from previous stage
COPY --from=build_front /app/dist /front

# Set environment variable for server
ENV STATIC_ROOT /front

# Expose port of API
EXPOSE 8000

# Source environment file, fill database and serve API
ENTRYPOINT python3 ./clusterer_core/clusterer_core/database_filler.py && python -m uvicorn --factory server:factory --port 80 --host 0.0.0.0
