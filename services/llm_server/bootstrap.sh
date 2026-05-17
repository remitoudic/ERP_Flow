#!/bin/sh
set -e

# Start Ollama server in the background
/bin/ollama serve &

# Poll Ollama API until it is running and healthy
echo "Waiting for Ollama API server to start..."
until curl -s -f http://localhost:11434/ > /dev/null; do
  sleep 1
done

# Pull the desired model (defaulting to gemma:2b)
MODEL_TO_PULL=${OLLAMA_MODEL:-gemma:2b}
echo "Ollama is ready. Pre-pulling model: ${MODEL_TO_PULL}..."
ollama pull "$MODEL_TO_PULL"

echo "Model ${MODEL_TO_PULL} pulled successfully! Keeping container alive."

# Wait for the background 'ollama serve' process to keep the container running
wait
