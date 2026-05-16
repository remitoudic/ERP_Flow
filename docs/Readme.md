# ERP Flow Automation: Technical Architecture & Design

Welcome to the central documentation hub for the **AI ERP Automation** project. This repository contains the architectural blueprints and technical specifications for a platform that transforms natural language intent into durable, visual, and high-performance ERP workflows.

---

## 🗺️ Documentation Map

Navigate through the core pillars of our system:

| Phase | Document | Description |
| :--- | :--- | :--- |
| **Logic** | 💡 [Automation Idea](./Automation_idea.md) | Business logic, CRM use-cases, and workflow logic definition. |
| **Data Flow** | 🔄 [Sequence Diagram](./sequence_diagram.md) | End-to-end visualization of how User input becomes Odoo action. |
| **Architecture** | 🏗️ [Infrastructure](./infrastructure.md) | Docker orchestration, container inventory, and stack rationale. |
| **Integration** | ⚙️ [ERP Flow Engine](./ERP_flow_engine.md) | Odoo API patterns, deployment strategies, and server actions. |

---

## 🛠️ The Tech Stack

Our architecture is built on a "Durable Intelligence" philosophy:

*   🧠 **Ollama (Gemma 4)**: Local LLM processing for parsing plain English into JSON schemas.
*   ⚡ **Temporal.io**: Durable execution engine for retries, long-running timers, and state management.
*   🎨 **Vue.js + Vue Flow**: A premium visual canvas for monitoring and editing generated workflows.
*   🗄️ **PostgreSQL**: The "All-in-One" database (Persistence + High-speed Pub/Sub + Caching).
*   📊 **Logfire**: OpenTelemetry-native observability for real-time request tracing.

---

## 🎯 Project Goals

1.  **Zero-Code Automation**: Allow non-technical users to build ERP workflows via chat.
2.  **Durable Integrity**: Ensure workflows never "die" mid-execution (handled by Temporal).
3.  **Local Intelligence**: Keep sensitive business logic on-premise using Ollama.
4.  **Visual Clarity**: Provide a world-class UI for workflow visualization via `vueflow.dev`.

---

> [!TIP]
> Start with the **[Automation Idea](./Automation_idea.md)** to understand the business requirements, then move to the **[Infrastructure](./infrastructure.md)** to see how it's built.
