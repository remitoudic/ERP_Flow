# ERP Flow — Sequence Diagram

## Data Flow: From Plain English to Odoo Automation

This diagram shows the end-to-end data flow when a user describes a CRM workflow in plain English, and the system deploys it as live automation in Odoo.

---

### Full Sequence Diagram

```mermaid
sequenceDiagram
    actor User
    participant FE as Frontend<br/>React / Next.js
    participant BE as Backend<br/>ERP Flow Engine<br/>Python + FastAPI
    participant API as Odoo External API<br/>XML-RPC / JSON-RPC
    participant Odoo as Odoo<br/>Automated Actions<br/>Server Actions

    Note over User,Odoo: Phase 1 — Workflow Creation

    User->>FE: Describe CRM workflow in plain English
    Note right of User: "When a new lead comes in<br/>from website or LinkedIn,<br/>check company size > 50..."

    FE->>FE: Display visual workflow editor
    FE->>BE: POST /workflows — Send plain English description

    Note over BE: AI parses natural language<br/>into structured JSON workflow

    BE-->>FE: Return JSON workflow structure
    FE->>FE: Render visual workflow graph
    FE-->>User: Show workflow for review & validation

    Note over User,Odoo: Phase 2 — User Validation

    User->>FE: Review, edit & approve workflow
    FE->>BE: POST /workflows/deploy — Send approved JSON workflow

    Note over BE,Odoo: Phase 3 — Deployment to Odoo

    BE->>BE: Parse JSON workflow nodes & edges

    BE->>API: Create Automated Action<br/>"Trigger: New Lead Created"
    API->>Odoo: Register ir.actions.server
    Odoo-->>API: Action ID confirmed
    API-->>BE: Success + Action ID

    BE->>API: Create Server Action<br/>"Check company size & industry"
    API->>Odoo: Register decision logic
    Odoo-->>API: Action ID confirmed
    API-->>BE: Success + Action ID

    BE->>API: Create Email Template<br/>"Welcome email for qualified leads"
    API->>Odoo: Register mail.template
    Odoo-->>API: Template ID confirmed
    API-->>BE: Success + Template ID

    BE->>API: Create Activity Type<br/>"Schedule Discovery Call (+48h)"
    API->>Odoo: Register mail.activity
    Odoo-->>API: Activity ID confirmed
    API-->>BE: Success + Activity ID

    BE->>API: Create Follow-up Sequence<br/>"3 emails over 2 weeks if no reply"
    API->>Odoo: Register scheduled actions
    Odoo-->>API: Sequence IDs confirmed
    API-->>BE: Success + Sequence IDs

    BE->>API: Create Stage Automation<br/>"On Proposal Sent → Create Quotation"
    API->>Odoo: Register sale.order automation
    Odoo-->>API: Automation ID confirmed
    API-->>BE: Success + Automation ID

    BE-->>FE: Deployment complete — all actions registered
    FE-->>User: ✅ Workflow deployed successfully

    Note over User,Odoo: Phase 4 — Live Execution (Runtime)

    Note right of Odoo: A new lead arrives<br/>from website form

    Odoo->>Odoo: Trigger: New Lead Created
    Odoo->>Odoo: Evaluate: Company Size ≥ 50?<br/>Industry in Tech/Manufacturing?

    alt Qualified Lead
        Odoo->>Odoo: Convert Lead → Opportunity
        Odoo->>Odoo: Assign to Enterprise Sales Team
        Odoo->>Odoo: Send Welcome Email
        Odoo->>Odoo: Create Task: Discovery Call (+48h)
        Note right of Odoo: Wait 7 days...
        Odoo->>Odoo: No reply → Start nurture sequence
    else Not Qualified
        Odoo->>Odoo: Add to Cold Nurture list
        Odoo->>Odoo: Assign lower lead score
    end
```

---

### System Components

| Component | Role | Technology |
|-----------|------|------------|
| **Frontend** | User interface for workflow description, visual editing, and monitoring | React / Next.js |
| **Backend (ERP Flow Engine)** | AI parsing, JSON workflow generation, deployment orchestration | Python + FastAPI |
| **Odoo External API** | Bridge between the engine and Odoo's internal models | XML-RPC / JSON-RPC |
| **Odoo Automated Actions** | Live execution of deployed workflows inside Odoo | ir.actions.server, mail.template, mail.activity |
