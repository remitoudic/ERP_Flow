# Odoo Workflow Import Strategy for AI Workflow Builder POC

## Overview

This document explains two practical approaches to convert the **JSON workflow** into a working automation in Odoo for your Proof of Concept.

---

### 3. Hybrid Approach (Recommended for AI Workflow Builder Vision)

This is the **most strategic** approach for building a real AI Workflow Builder product.

#### Concept
An **external AI engine** reads your JSON workflow and automatically deploys it into Odoo using Odoo’s external API.

#### Architecture

```mermaid
flowchart LR
    A[User / AI] --> B[JSON Workflow]
    B --> C[External Engine\nPython + FastAPI]
    C <--> D[Odoo External API\nXML-RPC or JSON-RPC]
    D --> E[Automated Actions\nServer Actions\nCustom Records]