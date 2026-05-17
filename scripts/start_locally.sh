#!/usr/bin/env bash
# Script to start ERP Flow locally for development
# Use this on your laptop/workstation, NOT on the production server

set -euo pipefail

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🚀 Starting ERP Flow - LOCAL DEVELOPMENT MODE"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Error: Docker is not running!"
    echo "   Please start Docker Desktop and try again."
    exit 1
fi

# Check if .env exists, if not use .env.example
ENV_FILE=".env"
ENV_EXAMPLE=".env.example"

if [ ! -f "$ENV_FILE" ]; then
    if [ -f "$ENV_EXAMPLE" ]; then
        echo "⚠️  No .env file found at $ENV_FILE. Creating from $ENV_EXAMPLE..."
        # Create .env from example
        cp "$ENV_EXAMPLE" "$ENV_FILE"
        echo "✅ Created $ENV_FILE"
        echo ""
        echo "📝 NOTE: Edit $ENV_FILE and set your optional variables if needed:"
        echo "   - LOGFIRE_TOKEN (optional, for observability tracking)"
        echo ""
    else
        echo "❌ Error: No $ENV_EXAMPLE file found!"
        exit 1
    fi
fi

# Ensure our local development urls and ports are displayed
echo "📋 Configuration (from $ENV_FILE):"
if [ -f "$ENV_FILE" ]; then
    GATEWAY_PORT=$(grep -E "^GATEWAY_PORT=" "$ENV_FILE" | cut -d'=' -f2 || echo "80")
    BACKEND_PORT=$(grep -E "^BACKEND_PORT=" "$ENV_FILE" | cut -d'=' -f2 || echo "8001")
    FRONTEND_PORT=$(grep -E "^FRONTEND_PORT=" "$ENV_FILE" | cut -d'=' -f2 || echo "3001")
    ODOO_PORT=$(grep -E "^ODOO_PORT=" "$ENV_FILE" | cut -d'=' -f2 || echo "8069")
    OLLAMA_PORT=$(grep -E "^OLLAMA_PORT=" "$ENV_FILE" | cut -d'=' -f2 || echo "11435")
    TEMPORAL_UI_PORT=$(grep -E "^TEMPORAL_UI_PORT=" "$ENV_FILE" | cut -d'=' -f2 || echo "8081")
    
    echo "   Nginx Gateway (Web App): http://localhost:${GATEWAY_PORT}"
    echo "   FastAPI Backend Core   : http://localhost:${BACKEND_PORT}/health"
    echo "   Odoo 19 Community      : http://localhost:${ODOO_PORT}"
    echo "   Ollama LLM Server      : http://localhost:${OLLAMA_PORT}"
    echo "   Temporal Workflow UI   : http://localhost:${TEMPORAL_UI_PORT}"
fi
echo ""

# Start services
echo "🐳 Starting Docker containers..."
echo ""

# Use docker-compose if available, else docker compose
if command -v docker-compose > /dev/null 2>&1; then
    docker-compose up --build -d
    echo ""
    echo "✅ Containers started successfully!"
    echo "📊 Following logs for Nginx Gateway, Frontend, and Backend..."
    echo "👉 Press Ctrl+C to stop viewing logs (containers will keep running)."
    echo ""
    docker-compose logs -f gateway frontend backend
else
    docker compose up --build -d
    echo ""
    echo "✅ Containers started successfully!"
    echo "📊 Following logs for Nginx Gateway, Frontend, and Backend..."
    echo "👉 Press Ctrl+C to stop viewing logs (containers will keep running)."
    echo ""
    docker compose logs -f gateway frontend backend
fi
