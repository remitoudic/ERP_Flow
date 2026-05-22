# Implementation Plan: Custom AI Interface for Odoo (FastAPI + Vue.js + MCP)

This document outlines the end-to-end implementation strategy for building a custom, AI-powered frontend for an Enterprise Odoo environment. By combining Vue.js, FastAPI, and the `mcp-server-odoo` protocol, we can bypass standard LLM clients and deliver a deeply integrated, tailored user experience specifically suited for complex business workflows and your specific infrastructure.

---

## 1. System Architecture Overview

The system operates on a decoupled, four-tier architecture:
1. **Frontend (Vue.js):** A lightweight, custom UI that captures user intent and displays formatted Odoo data.
2. **Orchestrator (FastAPI):** The backend brain. It manages API keys, maintains conversation state, and orchestrates calls between the LLM and the MCP server.
3. **Agent / Bridge (MCP Client + LLM):** The reasoning engine (e.g., Anthropic Claude or OpenAI) paired with an MCP client adapter (like `langchain-mcp-adapters`).
4. **Data Layer (`mcp-server-odoo` + Odoo):** The standard XML-RPC bridge directly interfacing with the Odoo Enterprise database.

---

## 2. Phase 1: Environment & Infrastructure Setup

**Goal:** Establish the foundational communication channels between the backend and the Odoo instance.

* **Deploy the MCP Module:**
    * Download the official `mcp_server` module from the `mcp-server-odoo` repository.
    * Install it within the target Odoo Enterprise instance.
    * Navigate to *Settings > MCP Server > Enabled Models* to whitelist specific models (e.g., `res.partner`, `sale.order`) and configure exact CRUD permissions.
* **Provision API Keys:**
    * Create a dedicated Odoo integration user with restricted access rights.
    * Generate a secure API key for this user to avoid username/password authentication.
* **Configure the MCP Server:**
    * Set up a local Python environment (`uv` or `pipx`) to run the `mcp-server-odoo` process alongside the FastAPI backend.
    * **Critical:** Ensure `ODOO_YOLO=off` to enforce strict Odoo access control lists (ACLs) and record rules in the production environment.

---

## 3. Phase 2: FastAPI Backend Development

**Goal:** Build the API layer that acts as the MCP client and communicates with the LLM.

* **Initialize the FastAPI Project:**
    * Set up routing, CORS middleware (to allow Vue.js requests), and dependency injection for database/LLM sessions.
* **Implement the MCP Client:**
    * Use the official `mcp` Python SDK to spawn the `mcp-server-odoo` process via the `stdio` transport.
    * *Example Snippet:*
      ```python
      from mcp import ClientSession, StdioServerParameters
      from mcp.client.stdio import stdio_client

      server_params = StdioServerParameters(
          command="uvx",
          args=["mcp-server-odoo"],
          env={"ODOO_URL": "...", "ODOO_API_KEY": "..."}
      )
      ```
* **LLM Integration (Tool Binding):**
    * Fetch the available tools from the Odoo MCP server (`session.list_tools()`).
    * Format these tools into the JSON schema expected by your chosen LLM (e.g., Anthropic's tool use format).
* **Endpoint Creation:**
    * Create a `/api/chat` POST endpoint.
    * **Workflow:**
        1. Receive user prompt from Vue.
        2. Send prompt + Odoo tool definitions to LLM.
        3. If LLM calls a tool (e.g., `search_records`), FastAPI intercepts, executes the tool via the MCP session, and returns the raw JSON to the LLM.
        4. Return the LLM's final natural language response to Vue.

---

## 4. Phase 3: Vue.js Frontend Development

**Goal:** Create a responsive, intuitive interface that abstracts away the complexity of ERP data structures.

* **Project Scaffolding:**
    * Initialize a Vue 3 project using Vite (`npm create vite@latest`).
    * Integrate Tailwind CSS for rapid styling and Pinia for state management.
* **Component Architecture:**
    * `ChatInterface.vue`: The main conversational UI.
    * `RecordCard.vue`: A dynamic component designed to render structured JSON data returned from Odoo (e.g., displaying an invoice status with color-coded badges) rather than just plain text.
* **Handling Server-Sent Events (SSE) / WebSockets:**
    * Because LLM generation and database lookups can take a few seconds, implement a streaming response connection to FastAPI. This ensures the user sees the agent "thinking" and typing in real-time, greatly improving perceived performance.

---

## 5. Phase 4: Production Deployment & Security

**Goal:** Secure the stack and ensure high availability.

* **Transport Switching:**
    * Move from `stdio` (which requires FastAPI and the MCP server to share the same container/machine) to `streamable-http`. This allows the `mcp-server-odoo` to run as a standalone microservice within your VPC.
* **Containerization:**
    * Write a `docker-compose.yml` that defines three services: the Vue frontend (served via Nginx), the FastAPI backend, and the `mcp-server-odoo` container.
* **Authentication & Tenant Isolation:**
    * Implement JWT-based authentication on the FastAPI layer. 
    * Map the logged-in Vue user to their specific Odoo API context, ensuring that cross-tenant or cross-department data access is impossible at the backend orchestration level.

---

## 6. Next Steps & Milestones

1. **Week 1:** Setup local Odoo YOLO mode and validate standard queries using the raw CLI MCP inspector.
2. **Week 2:** Develop the FastAPI MCP client wrapper and successfully execute an end-to-end tool call via an LLM script.
3. **Week 3:** Build the Vue.js frontend and wire it to the FastAPI `/chat` endpoint.
4. **Week 4:** Transition to the Enterprise Odoo environment, disable YOLO mode, install the required Odoo MCP module, and configure production security.
