# Implementation Plan - AI ERP Automation Workflow Builder

Architect and implement the initial containerized infrastructure and core services for the AI-powered ERP workflow builder.

## User Review Required

> [!IMPORTANT]
> This plan involves setting up a multi-container environment. You will need **Docker** and **Docker Compose** installed on your machine.
> We are using **Ollama** locally. Ensure Ollama is running if you want to test LLM features outside of the docker network, or it will be started as a container.

## Proposed Changes

We will scaffold the project structure and implement the core communication layers.

### 1. Infrastructure Foundation
Set up the orchestration layer using Docker Compose and environment variables.

#### [NEW] docker-compose.yml
- Define services: `postgres`, `temporal`, `temporal-ui`, `ollama`, `backend`, `frontend`, `nginx`.
- Configure health checks for service dependency ordering.

#### [NEW] .env.example
- Environment variables for Odoo, Postgres, Temporal, and Logfire.

---

### 2. Backend (FastAPI)
Core logic for parsing natural language and orchestrating Odoo via Temporal.

#### [NEW] `backend/main.py`
- FastAPI app with Logfire instrumentation.
- Endpoints for receiving plain English and triggering workflows.

#### [NEW] `backend/ollama_client.py`
- Client to interact with the Ollama service to generate JSON workflow schemas.

#### [NEW] `backend/temporal/workflows.py` & `backend/temporal/worker.py`
- Define the base Odoo Workflow and the worker to execute it.

#### [NEW] `backend/database.py`
- PostgreSQL integration for Pub/Sub and caching (UNLOGGED tables).

---

### 3. Frontend (Vue.js + Vue Flow)
Visual editor for the generated workflows.

#### [NEW] `frontend/`
- Scaffold Vue.js 3 project via Vite.
- Install `vueflow.dev` (Vue Flow).
- Create basic UI to display the generated graph.

---

### 4. Reverse Proxy (Nginx)
Central entry point.

#### [NEW] `docker/nginx/nginx.conf`
- Route traffic to Frontend and Backend.

## Verification Plan

### Automated Tests
1. **Container Health**: Run `docker-compose up -d` and verify all containers reach a "healthy" state.
2. **Backend API**: Test the `/generate-workflow` endpoint with a sample prompt.
3. **Temporal UI**: Access `localhost:8080` to verify workflow registration.

### Manual Verification
1. Open the Vue.js frontend at `localhost`.
2. Input a CRM workflow in plain English (e.g., "When a lead is created, wait 2 days then send an email if not qualified").
3. Verify the workflow appears visually in the Vue Flow canvas.
