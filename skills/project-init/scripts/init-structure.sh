#!/bin/bash
# init-structure.sh — creates project folder structure from templates
# Usage: bash init-structure.sh <project-slug> [public|private]
# Example: bash init-structure.sh biography-agent private

set -e

SLUG=$1
PROJECTS_DIR="$HOME/projects"
TEMPLATES_DIR="$HOME/.claude/templates"
PROJECT_DIR="$PROJECTS_DIR/$SLUG"

# ── Guards ────────────────────────────────────────────────
if [ -z "$SLUG" ]; then
  echo "❌ Error: project slug required"
  echo "Usage: bash init-structure.sh <project-slug>"
  exit 1
fi

if [ -d "$PROJECT_DIR" ]; then
  echo "❌ Error: $PROJECT_DIR already exists"
  exit 1
fi

if [ ! -d "$TEMPLATES_DIR" ]; then
  echo "❌ Error: templates directory not found at $TEMPLATES_DIR"
  exit 1
fi

# ── Create structure ──────────────────────────────────────
echo "📁 Creating $PROJECT_DIR..."
mkdir -p "$PROJECT_DIR/.claude"
mkdir -p "$PROJECT_DIR/.claude/agents"

# Copy templates
cp "$TEMPLATES_DIR/CLAUDE.template.md"     "$PROJECT_DIR/CLAUDE.md"
cp "$TEMPLATES_DIR/CONTEXT.template.md"    "$PROJECT_DIR/.claude/CONTEXT.md"
cp "$TEMPLATES_DIR/DECISIONS.template.md"  "$PROJECT_DIR/.claude/DECISIONS.md"
cp "$TEMPLATES_DIR/LESSONS.template.md"    "$PROJECT_DIR/.claude/LESSONS.md"
cp "$TEMPLATES_DIR/DESIGN.template.md"     "$PROJECT_DIR/.claude/DESIGN.md"
cp "$TEMPLATES_DIR/TODOS.template.md"      "$PROJECT_DIR/.claude/TODOS.md"

# Create README
cat > "$PROJECT_DIR/README.md" << EOF
# $SLUG

> See CLAUDE.md for project context and .claude/ for detailed documentation.
EOF

# Create .gitignore
cat > "$PROJECT_DIR/.gitignore" << EOF
.env
*.local
.DS_Store
EOF

# ── Git init ──────────────────────────────────────────────
echo "🔧 Initializing git..."
cd "$PROJECT_DIR"
git init -q
git add -A
git commit -q -m "chore: scaffold — empty project structure"

# ── GitHub repo ───────────────────────────────────────────
VISIBILITY=${2:-private}
if [ "$VISIBILITY" != "public" ] && [ "$VISIBILITY" != "private" ]; then
  echo "❌ Invalid visibility: $VISIBILITY (must be 'public' or 'private')"
  exit 1
fi

echo "🐙 Creating GitHub repo CamilleLarpin/$SLUG ($VISIBILITY)..."
gh repo create "CamilleLarpin/$SLUG" --"$VISIBILITY" --source=. --remote=origin --push

echo "✅ Done: $PROJECT_DIR"
echo "   GitHub: https://github.com/CamilleLarpin/$SLUG"
echo "📋 Next: Claude fills content, then runs trigger-notion.sh"
