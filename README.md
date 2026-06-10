# ✨ ERP Flow Automation

Transforming natural language intent into durable, visual, and high-performance ERP workflows.

**ERP Flow Automation** is a modern, local-first orchestration engine that parses plain English instructions into visual flowcharts, executes them with absolute state resilience, and deploys them directly into the **Odoo 19 ERP** suite

---

## 🏗️ System Architecture

Our platform is engineered for **Durable Intelligence**—ensuring visual layout simplicity on the outside, and bulletproof transactional resilience on the inside

```
                  ┌────────────────────────────────────────┐
                  │            NGINX GATEWAY               │ (Port 80 / 443)
                  └───────────────────┬────────────────────┘
                                      │
             ┌────────────────────────┴────────────────────────┐
             ▼                                                 ▼
   ┌──────────────────┐                              ┌──────────────────┐
   │ Vue 3 Frontend   │ (Vite + VueFlow)             │ FastAPI Backend  │ (Port 8001)
   └──────────────────┘                              └─────────┬────────┘
                                                               │
             ┌────────────────────────┬────────────────────────┼────────────────────────┐
             ▼                        ▼                        ▼                        ▼
   ┌──────────────────┐      ┌──────────────────┐      ┌──────────────────┐      ┌──────────────────┐
   │  Ollama Server   │      │ Temporal Engine  │      │ PostgreSQL 16 DB │      │  Odoo 19 ERP CE  │
   │    (Gemma 2b)    │      │ (State Orchestr) │      │ (Cache + Store)  │      │  (Target Suite)  │
   │   (Port 11435)   │      │   (Port 7234)    │      │   (Port 5432)    │      │   (Port 8069)    │
   └──────────────────┘      └──────────────────┘      └──────────────────┘      └──────────────────┘
```

---

## 🛠️ The Tech Stack

*   🧠 **Local AI Server**: [Ollama](https://ollama.com/) running **Gemma 2B** to parse natural language prompt intents locally into validated JSON graph schemas.
*   ⚡ **Durable Orchestration**: [Temporal.io](https://temporal.io/) to coordinate long-running API tasks, retry loops, and visual workflows with transactional safety.
*   🎨 **Visual Canvas**: **Vue 3 + Vite + Bun** using [@vue-flow/core](https://vueflow.dev/) to build a fluid dark-mode blueprint panel for modifying and monitoring workflows.
*   🗄️ **Persistent & Caching Stores**: **PostgreSQL 16** utilizing advanced `UNLOGGED` structures for sub-millisecond local caching layers.
*   📊 **Deep Observability**: [Logfire](https://logfire.pydantic.dev/) for native OpenTelemetry real-time execution trace capture.
*   🌐 **Reverse Proxy Gateway**: **Nginx** acting as a high-performance single-point entry.

---

## 🚀 Getting Started

Bootstrap the entire multi-service workspace in a single command on your workstation.

### Prerequisites
Make sure you have [Docker Desktop](https://www.docker.com/products/docker-desktop/) started and running.

### 1. Launch the Stack
Run the tailored startup script inside the root folder:
```bash
./scripts/start_locally.sh
```
> [!NOTE]
> The script will automatically copy `.env.example` to `.env` if not present, verify Docker dependencies, print the network configuration layout, build all service container layers, and begin streaming application logs.

### 2. Standard Service Mappings (Host Ports)
Once running, you can connect directly to all components via your local ports:

| Service Name | Port | Description |
| :--- | :--- | :--- |
| **Nginx Reverse Gateway** | `http://localhost:80` | **Main Entry**—routes `/` to Frontend and `/api/` to Backend |
| **FastAPI Backend Core** | `http://localhost:8001` | Core REST APIs, health checks, and AI client queries |
| **Odoo 19 Community** | `http://localhost:8069` | Mapped ERP system instance |
| **Ollama LLM Engine** | `http://localhost:11435` | Local LLM host |
| **Temporal Workflow Web UI** | `http://localhost:8081` | Dashboard for monitoring executing workflow states |

### 3. Check System Status
You can verify the active backend, database, and Temporal orchestration statuses instantly using:
```bash
curl http://localhost/api/health
```
*(Should return `{"status":"healthy","database_connected":true,"temporal_connected":true}`)*

---

## 🗺️ Documentation Roadmap

Deep-dive into specific areas of the ERP Flow platform design inside our `docs` hub:

*   💡 [Automation Use Cases & Structures](docs/Automation_idea.md) — CRM pipeline triggers, workflow node types, and edge actions.
*   🔄 [End-to-End Sequence Diagram](docs/sequence_diagram.md) — Life of a prompt: visual layout generation, client parsing, and Odoo action.
*   🏗️ [Infrastructure & Container Configs](docs/infrastructure.md) — Multi-container details, PostgreSQL cache setups, and Docker bridge parameters.
*   ⚙️ [Odoo ERP Engine Integration](docs/ERP_flow_engine.md) — Remote Procedure Call (RPC) interfaces, security models, and server-side automated action rules...

---

## 🔒 Security & Local-First Philosophy
ERP data is highly sensitive. We enforce a strict **on-premise** design where natural language translation, database caching, and workflow orchestration reside completely within your local network or virtual private clouds, eliminating remote API leaks.
