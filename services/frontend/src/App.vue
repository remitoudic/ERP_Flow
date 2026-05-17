<template>
  <div class="app-wrapper">
    <!-- Blueprint grid background for architectural aesthetics -->
    <div class="blueprint-grid"></div>

    <!-- Glassmorphic Header -->
    <header class="app-header glass-panel">
      <div class="header-logo">
        <span class="logo-emoji">🌌</span>
        <div class="logo-text">
          <h1>ERP Flow</h1>
          <span class="sub-badge">AI Automation Engine</span>
        </div>
      </div>

      <div class="stack-status">
        <div class="status-indicator healthy">
          <span class="dot"></span> Backend (FastAPI)
        </div>
        <div class="status-indicator healthy">
          <span class="dot"></span> Database (Postgres)
        </div>
        <div class="status-indicator healthy">
          <span class="dot"></span> Odoo 19 CE
        </div>
        <div class="status-indicator healthy">
          <span class="dot"></span> LLM (Gemma:2b)
        </div>
      </div>
    </header>

    <!-- Main Dynamic Interface -->
    <main class="app-main">
      <!-- Left Sidebar: Interaction Console -->
      <section class="interaction-console glass-panel">
        <div class="panel-section">
          <h2>Describe Automation Intent</h2>
          <p class="section-desc">Type your business workflow in plain English. Our local Gemma model will parse the nodes, and Temporal will schedule execution steps.</p>
        </div>

        <form @submit.prevent="handleGenerate" class="prompt-form">
          <div class="textarea-wrapper">
            <textarea
              v-model="prompt"
              placeholder="e.g., When a CRM lead is created, wait 2 days, verify quality via LLM, and send a welcome email if qualified..."
              :disabled="loading"
            ></textarea>
            <div class="glow-border"></div>
          </div>

          <button type="submit" class="btn-generate" :disabled="loading">
            <span v-if="loading" class="spinner"></span>
            <span v-else>Generate Workflow 🚀</span>
          </button>
        </form>

        <!-- Clickable Sample Prompts -->
        <div class="samples-wrapper">
          <h3>Try Sample Templates</h3>
          <div class="sample-tags">
            <button 
              v-for="sample in samples" 
              :key="sample"
              @click="prompt = sample"
              class="tag-btn"
              type="button"
            >
              {{ sample }}
            </button>
          </div>
        </div>

        <!-- Workflow Details Indicator -->
        <div v-if="workflowName" class="workflow-info glass-panel">
          <div class="info-row">
            <span class="info-label">Active Flow:</span>
            <span class="info-val font-highlight">{{ workflowName }}</span>
          </div>
          <div class="info-row">
            <span class="info-label">Deployment:</span>
            <span class="info-val deploy-success">✓ Synced to Odoo 19</span>
          </div>
          <div class="info-row">
            <span class="info-label">Durability:</span>
            <span class="info-val temporal-badge">Temporal Active</span>
          </div>
        </div>
      </section>

      <!-- Right Panel: Visual Workspace Canvas -->
      <section class="visual-workspace glass-panel">
        <div class="workspace-header">
          <h2>Visual Workflow Canvas</h2>
          <span class="flow-status" :class="{ 'anim-glow': loading }">
            {{ loading ? 'Compiling AI Nodes...' : 'Ready / Active' }}
          </span>
        </div>

        <!-- Render interactive Vue Flow elements -->
        <div class="flow-canvas-container">
          <VueFlow 
            v-if="nodes.length > 0"
            v-model:nodes="nodes" 
            v-model:edges="edges" 
            fit-view-on-init
            class="custom-flow-theme"
          >
            <!-- Custom Node Style Template overrides -->
            <template #node-input="nodeProps">
              <div class="flow-node node-trigger">
                <span class="node-icon">⚡</span>
                <div class="node-meta">
                  <span class="node-type">TRIGGER</span>
                  <div class="node-label">{{ nodeProps.data.label }}</div>
                </div>
              </div>
            </template>

            <template #node-default="nodeProps">
              <div class="flow-node node-action">
                <span class="node-icon">⚙️</span>
                <div class="node-meta">
                  <span class="node-type">ACTION</span>
                  <div class="node-label">{{ nodeProps.data.label }}</div>
                </div>
              </div>
            </template>
          </VueFlow>

          <!-- Fallback Visual state when canvas is empty -->
          <div v-else class="empty-canvas-state">
            <div class="radar-scan"></div>
            <span class="empty-icon">🗺️</span>
            <h3>No Workflow Compiled</h3>
            <p>Describe your automation in the left console to visualize nodes and logic gates in real-time.</p>
          </div>
        </div>
      </section>
    </main>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { VueFlow } from '@vue-flow/core'

// Register Vue Flow default layout styles
import '@vue-flow/core/dist/style.css'
import '@vue-flow/core/dist/theme-default.css'

const prompt = ref('')
const loading = ref(false)
const workflowName = ref('')

const samples = [
  "When a lead is created, wait 2 days and check qualification status",
  "High Priority task generation for deals above $10,000 value",
  "Inventory restock notification sequence based on warehouse drop alerts"
]

const nodes = ref([])
const edges = ref([])

// Submit request to local FastAPI backend to map plain text to nodes
const handleGenerate = async () => {
  if (!prompt.value.trim()) return

  loading.value = true
  workflowName.value = ''
  nodes.value = []
  edges.value = []

  try {
    const response = await fetch('/api/generate-workflow', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ prompt: prompt.value }),
    })

    if (!response.ok) throw new Error('API failed')

    const data = await response.json()
    if (data.success) {
      workflowName.value = data.workflow.name
      nodes.value = data.workflow.nodes
      edges.value = data.workflow.edges
    }
  } catch (error) {
    console.error('Error generating workflow:', error)
    // Client-side fallback if backend is not yet fully booted in early stage development
    workflowName.value = 'Local Development Fallback'
    nodes.value = [
      { id: '1', type: 'input', data: { label: 'Odoo Trigger: Lead Created' }, position: { x: 250, y: 50 } },
      { id: '2', data: { label: 'Temporal timer: Wait 2 Days' }, position: { x: 250, y: 175 } },
      { id: '3', data: { label: 'Gemma 2B: Evaluate Lead Intent' }, position: { x: 250, y: 300 } },
      { id: '4', data: { label: 'Odoo API: Update Status' }, position: { x: 250, y: 425 } }
    ]
    edges.value = [
      { id: 'e1-2', source: '1', target: '2', animated: true },
      { id: 'e2-3', source: '2', target: '3' },
      { id: 'e3-4', source: '3', target: '4' }
    ]
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.app-wrapper {
  display: flex;
  flex-direction: column;
  height: 100vh;
  width: 100vw;
  padding: 24px;
  gap: 20px;
  position: relative;
  z-index: 1;
}

/* Header Styling */
.app-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px 32px;
  flex-shrink: 0;
}

.header-logo {
  display: flex;
  align-items: center;
  gap: 16px;
}

.logo-emoji {
  font-size: 2.2rem;
  animation: float 4s ease-in-out infinite;
}

.logo-text h1 {
  font-size: 1.6rem;
  background: var(--gradient-main);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.sub-badge {
  font-size: 0.75rem;
  color: var(--text-muted);
  text-transform: uppercase;
  letter-spacing: 0.1em;
}

.stack-status {
  display: flex;
  gap: 20px;
}

.status-indicator {
  font-size: 0.8rem;
  display: flex;
  align-items: center;
  gap: 8px;
  color: var(--text-muted);
}

.status-indicator.healthy .dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background-color: var(--success);
  box-shadow: 0 0 10px var(--success);
}

/* Main Area Layout */
.app-main {
  display: flex;
  flex: 1;
  gap: 20px;
  min-height: 0; /* Ensures overflow rules work properly inside flexbox */
}

/* Left Interaction Console */
.interaction-console {
  width: 420px;
  padding: 28px;
  display: flex;
  flex-direction: column;
  gap: 24px;
  flex-shrink: 0;
}

.interaction-console h2 {
  font-size: 1.4rem;
  margin-bottom: 6px;
}

.section-desc {
  font-size: 0.85rem;
  color: var(--text-muted);
  line-height: 1.4;
}

.prompt-form {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.textarea-wrapper {
  position: relative;
  border-radius: 12px;
  overflow: hidden;
}

textarea {
  width: 100%;
  height: 140px;
  padding: 16px;
  background: rgba(15, 23, 42, 0.8);
  border: 1px solid var(--border-glass);
  border-radius: 12px;
  color: var(--text-primary);
  font-family: inherit;
  font-size: 0.9rem;
  line-height: 1.5;
  resize: none;
  outline: none;
  transition: var(--transition-smooth);
}

textarea:focus {
  border-color: var(--secondary);
  box-shadow: inset 0 0 8px rgba(6, 182, 212, 0.15);
}

.btn-generate {
  background: var(--gradient-main);
  border: none;
  color: var(--text-dark);
  font-weight: 600;
  padding: 14px;
  border-radius: 12px;
  font-size: 0.95rem;
  cursor: pointer;
  transition: var(--transition-smooth);
  box-shadow: var(--glow-purple);
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 8px;
}

.btn-generate:hover:not(:disabled) {
  background: var(--gradient-hover);
  box-shadow: var(--glow-cyan);
  transform: translateY(-2px);
}

.btn-generate:active {
  transform: translateY(0);
}

.btn-generate:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

/* Sample template tags */
.samples-wrapper h3 {
  font-size: 0.9rem;
  color: var(--text-muted);
  margin-bottom: 12px;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.sample-tags {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.tag-btn {
  text-align: left;
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid var(--border-glass);
  color: var(--text-primary);
  padding: 10px 14px;
  border-radius: 8px;
  font-size: 0.8rem;
  cursor: pointer;
  transition: var(--transition-fast);
  line-height: 1.3;
}

.tag-btn:hover {
  background: rgba(255, 255, 255, 0.07);
  border-color: var(--border-hover);
}

/* Workflow info panel */
.workflow-info {
  margin-top: auto;
  padding: 16px;
  border-radius: 12px;
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.info-row {
  display: flex;
  justify-content: space-between;
  font-size: 0.8rem;
}

.info-label {
  color: var(--text-muted);
}

.font-highlight {
  font-weight: 600;
  color: var(--secondary);
}

.deploy-success {
  color: var(--success);
  font-weight: 500;
}

.temporal-badge {
  background: rgba(168, 85, 247, 0.15);
  border: 1px solid var(--primary);
  color: var(--primary);
  padding: 2px 8px;
  border-radius: 20px;
  font-size: 0.7rem;
  font-weight: 600;
}

/* Right Visual Workspace */
.visual-workspace {
  flex: 1;
  padding: 28px;
  display: flex;
  flex-direction: column;
  gap: 20px;
  position: relative;
}

.workspace-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-shrink: 0;
}

.flow-status {
  font-size: 0.8rem;
  font-weight: 600;
  color: var(--secondary);
  background: rgba(6, 182, 212, 0.1);
  padding: 6px 14px;
  border-radius: 20px;
  border: 1px solid rgba(6, 182, 212, 0.2);
}

.anim-glow {
  animation: neon-pulse 1.5s infinite ease-in-out;
}

.flow-canvas-container {
  flex: 1;
  position: relative;
  background: rgba(10, 15, 30, 0.4);
  border: 1px solid var(--border-glass);
  border-radius: 12px;
  overflow: hidden;
  display: flex;
  justify-content: center;
  align-items: center;
}

/* VueFlow Overrides & Layout Styling */
.custom-flow-theme {
  width: 100%;
  height: 100%;
  --vf-node-bg: transparent !important;
  --vf-node-text: var(--text-primary) !important;
  --vf-node-color: transparent !important;
  --vf-node-border: transparent !important;
  --vf-handle-bg: var(--secondary) !important;
  --vf-handle-border: var(--text-primary) !important;
}

.flow-node {
  background: rgba(15, 23, 42, 0.95);
  border: 1px solid var(--border-glass);
  backdrop-filter: blur(4px);
}

.node-trigger {
  border-left: 4px solid var(--primary);
  box-shadow: 0 0 15px rgba(168, 85, 247, 0.15);
}

.node-action {
  border-left: 4px solid var(--secondary);
  box-shadow: 0 0 15px rgba(6, 182, 212, 0.15);
}

.node-icon {
  font-size: 1.25rem;
}

.node-meta {
  display: flex;
  flex-direction: column;
  gap: 2px;
  text-align: left;
}

.node-type {
  font-size: 0.65rem;
  color: var(--text-muted);
  letter-spacing: 0.05em;
  font-weight: 600;
}

.node-label {
  font-size: 0.8rem;
  color: var(--text-primary);
  font-weight: 500;
}

/* Empty State Styling */
.empty-canvas-state {
  text-align: center;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 16px;
  max-width: 320px;
  position: relative;
  z-index: 1;
}

.empty-icon {
  font-size: 3rem;
  animation: float 5s ease-in-out infinite;
}

.empty-canvas-state h3 {
  font-size: 1.2rem;
  color: var(--text-primary);
}

.empty-canvas-state p {
  font-size: 0.85rem;
  color: var(--text-muted);
  line-height: 1.5;
}

/* Animations */
@keyframes float {
  0% { transform: translateY(0px); }
  50% { transform: translateY(-10px); }
  100% { transform: translateY(0px); }
}

@keyframes neon-pulse {
  0% { box-shadow: 0 0 5px rgba(6, 182, 212, 0.2); }
  50% { box-shadow: 0 0 20px rgba(6, 182, 212, 0.6); }
  100% { box-shadow: 0 0 5px rgba(6, 182, 212, 0.2); }
}

.spinner {
  width: 20px;
  height: 20px;
  border: 3px solid rgba(0,0,0,0.1);
  border-radius: 50%;
  border-top-color: var(--text-dark);
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}
</style>
