#!/bin/bash
# trigger-notion.sh — calls n8n webhook to create Notion page + tracker entry
# Usage: bash trigger-notion.sh <slug> <name> <type> <pain-point>
# Requires: N8N_WEBHOOK_INIT env var set in ~/.claude/session-env or .env

set -e

SLUG=$1
NAME=$2
TYPE=$3
PAIN_POINT=$4
WEBHOOK_URL="${N8N_WEBHOOK_INIT}"

# ── Guards ────────────────────────────────────────────────
if [ -z "$WEBHOOK_URL" ]; then
  echo "⚠️  N8N_WEBHOOK_INIT not set — skipping Notion creation"
  echo "   Set it in ~/.claude/session-env and re-run this script manually"
  exit 0
fi

if [ -z "$SLUG" ] || [ -z "$NAME" ]; then
  echo "❌ Error: slug and name are required"
  echo "Usage: bash trigger-notion.sh <slug> <name> <type> <pain-point>"
  exit 1
fi

# ── Call webhook ──────────────────────────────────────────
echo "🔗 Creating Notion page for $NAME..."

RESPONSE=$(curl -s -X POST "$WEBHOOK_URL" \
  -H "Content-Type: application/json" \
  -d "{
    \"slug\": \"$SLUG\",
    \"name\": \"$NAME\",
    \"type\": \"$TYPE\",
    \"pain_point\": \"$PAIN_POINT\",
    \"status\": \"planning\",
    \"initiated_at\": \"$(date -u +%Y-%m-%dT%H:%M:%SZ)\"
  }")

# ── Output ────────────────────────────────────────────────
echo "✅ Notion webhook called"
echo "Response: $RESPONSE"
# Claude: extract notion_url from response and add to CLAUDE.md Quick Reference
