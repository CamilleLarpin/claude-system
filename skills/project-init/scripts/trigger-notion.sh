#!/bin/bash
# trigger-notion.sh — creates a page in the Notion project tracker DB
# Usage: bash trigger-notion.sh <slug> <name> <type> <stack> <pain-point>
# Requires: NOTION_API_KEY + NOTION_PROJECT_DB_ID in ~/.claude/session-env

set -e

SLUG=$1
NAME=$2
TYPE=$3
STACK=$4
PAIN_POINT=$5

# ── Load credentials ──────────────────────────────────────
if [ -f "$HOME/.claude/credentials" ]; then
  source "$HOME/.claude/credentials"
fi

# ── Guards ────────────────────────────────────────────────
if [ -z "$NOTION_API_KEY" ] || [ -z "$NOTION_PROJECT_DB_ID" ]; then
  echo "⚠️  NOTION_API_KEY or NOTION_PROJECT_DB_ID not set — skipping Notion creation"
  echo "   Set both in ~/.claude/session-env and re-run manually:"
  echo "   bash trigger-notion.sh \"$SLUG\" \"$NAME\" \"$TYPE\" \"$STACK\" \"$PAIN_POINT\""
  exit 0
fi

if [ -z "$SLUG" ] || [ -z "$NAME" ]; then
  echo "❌ Error: slug and name are required"
  echo "Usage: bash trigger-notion.sh <slug> <name> <type> <stack> <pain-point>"
  exit 1
fi

# ── Build payload ─────────────────────────────────────────
COMMENT="Type: ${TYPE} | Stack: ${STACK} | Pain point: ${PAIN_POINT}"

PAYLOAD=$(cat <<EOF
{
  "parent": { "database_id": "${NOTION_PROJECT_DB_ID}" },
  "properties": {
    "Nom": {
      "title": [{ "text": { "content": "${NAME}" } }]
    },
    "Active": {
      "checkbox": true
    },
    "Comments": {
      "rich_text": [{ "text": { "content": "${COMMENT}" } }]
    }
  }
}
EOF
)

# ── Call Notion API ───────────────────────────────────────
echo "🔗 Creating Notion page for ${NAME}..."

RESPONSE=$(curl -s -X POST "https://api.notion.com/v1/pages" \
  -H "Authorization: Bearer ${NOTION_API_KEY}" \
  -H "Notion-Version: 2022-06-28" \
  -H "Content-Type: application/json" \
  -d "$PAYLOAD")

# ── Extract page URL ──────────────────────────────────────
NOTION_URL=$(echo "$RESPONSE" | grep -o '"url":"[^"]*"' | head -1 | sed 's/"url":"//;s/"//')

if [ -z "$NOTION_URL" ]; then
  echo "❌ Notion API call failed. Response:"
  echo "$RESPONSE"
  exit 1
fi

echo "✅ Notion page created: $NOTION_URL"
# Claude: add NOTION_URL to CLAUDE.md Quick Reference of the new project
