#!/usr/bin/env bash
# Create a new agent from agent-template.
# Usage: ./scripts/create-agent.sh <agent-name>

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "${SCRIPT_DIR}/.." && pwd)"
TEMPLATE_DIR="${ROOT_DIR}/agent-template"
AGENTS_DIR="${ROOT_DIR}/agents"

AGENT_NAME="${1:-}"

if [[ -z "${AGENT_NAME}" ]]; then
  echo "Error: agent name is required."
  echo "Usage: ./scripts/create-agent.sh <agent-name>"
  exit 1
fi

# Normalize: lowercase, hyphens instead of spaces/underscores
AGENT_NAME="$(echo "${AGENT_NAME}" | tr '[:upper:]' '[:lower:]' | tr ' _' '-')"
TARGET_DIR="${AGENTS_DIR}/${AGENT_NAME}"

if [[ ! -d "${TEMPLATE_DIR}" ]]; then
  echo "Error: agent-template not found at ${TEMPLATE_DIR}"
  exit 1
fi

if [[ -d "${TARGET_DIR}" ]]; then
  echo "Error: agent already exists at ${TARGET_DIR}"
  exit 1
fi

mkdir -p "${AGENTS_DIR}"
cp -r "${TEMPLATE_DIR}" "${TARGET_DIR}"

# Bundle shared-core for standalone runs and Docker builds
if [[ -d "${ROOT_DIR}/shared-core" ]]; then
  cp -r "${ROOT_DIR}/shared-core" "${TARGET_DIR}/shared-core"
fi

if [[ -f "${TEMPLATE_DIR}/Dockerfile.agent" ]]; then
  cp "${TEMPLATE_DIR}/Dockerfile.agent" "${TARGET_DIR}/Dockerfile"
fi

# Remove template artifacts that should not ship per-agent
rm -rf "${TARGET_DIR}/.venv" 2>/dev/null || true
rm -rf "${TARGET_DIR}/__pycache__" 2>/dev/null || true

# Customize .env for the new agent
if [[ -f "${TARGET_DIR}/.env.example" ]]; then
  cp "${TARGET_DIR}/.env.example" "${TARGET_DIR}/.env"
  if [[ "$(uname)" == "Darwin" ]]; then
    sed -i '' "s/APP_NAME=agent-template/APP_NAME=${AGENT_NAME}/" "${TARGET_DIR}/.env"
  else
    sed -i "s/APP_NAME=agent-template/APP_NAME=${AGENT_NAME}/" "${TARGET_DIR}/.env"
  fi
fi

echo "Agent '${AGENT_NAME}' created at: ${TARGET_DIR}"
echo "Commit from lab root: git add agents/${AGENT_NAME} && git commit -m 'Add ${AGENT_NAME} agent'"
echo "Next steps:"
echo "  cd ${TARGET_DIR}"
echo "  python -m venv .venv && source .venv/bin/activate"
echo "  pip install -r requirements.txt"
echo "  uvicorn main:app --reload --port 8000"
