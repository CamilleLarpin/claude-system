#!/bin/sh
input=$(cat)

# --- Core fields ---
cwd=$(echo "$input" | jq -r '.cwd // empty')
dir=$(basename "${cwd:-/}")
user=$(whoami)
model=$(echo "$input" | jq -r '.model.display_name // empty')
version=$(echo "$input" | jq -r '.version // empty')

# --- Session ---
session_name=$(echo "$input" | jq -r '.session_name // empty')

# --- Context window ---
used_pct=$(echo "$input" | jq -r '.context_window.used_percentage // empty')
ctx_window=$(echo "$input" | jq -r '.context_window.context_window_size // empty')

# --- Token costs (cumulative) ---
total_in=$(echo "$input" | jq -r '.context_window.total_input_tokens // 0')
total_out=$(echo "$input" | jq -r '.context_window.total_output_tokens // 0')

# --- Optional: vim, agent, worktree ---
vim_mode=$(echo "$input" | jq -r '.vim.mode // empty')
agent_name=$(echo "$input" | jq -r '.agent.name // empty')
worktree_branch=$(echo "$input" | jq -r '.worktree.branch // empty')
worktree_name=$(echo "$input" | jq -r '.worktree.name // empty')

# --- Colors (dim-friendly) ---
RESET='\033[0m'
GREEN='\033[32m'
BLUE='\033[34m'
CYAN='\033[36m'
YELLOW='\033[33m'
MAGENTA='\033[35m'
RED='\033[31m'
GRAY='\033[90m'

# --- Build output ---

# user + dir (from original PS1: green user, blue dir)
printf "${GREEN}%s${RESET} ${BLUE}%s${RESET}" "$user" "$dir"

# session name (if set)
if [ -n "$session_name" ]; then
  printf " ${GRAY}[%s]${RESET}" "$session_name"
fi

# worktree (branch preferred, fallback to name)
if [ -n "$worktree_branch" ]; then
  printf " ${MAGENTA}wt:%s${RESET}" "$worktree_branch"
elif [ -n "$worktree_name" ]; then
  printf " ${MAGENTA}wt:%s${RESET}" "$worktree_name"
fi

# agent
if [ -n "$agent_name" ]; then
  printf " ${CYAN}agent:%s${RESET}" "$agent_name"
fi

# vim mode
if [ -n "$vim_mode" ]; then
  printf " ${YELLOW}[%s]${RESET}" "$vim_mode"
fi

# model + version
if [ -n "$model" ]; then
  if [ -n "$version" ]; then
    printf " ${GRAY}%s v%s${RESET}" "$model" "$version"
  else
    printf " ${GRAY}%s${RESET}" "$model"
  fi
fi

# context usage
if [ -n "$used_pct" ]; then
  # color the percentage: green < 50, yellow 50-80, red > 80
  pct_int=$(printf "%.0f" "$used_pct" 2>/dev/null || echo 0)
  if [ "$pct_int" -ge 80 ]; then
    ctx_color="$RED"
  elif [ "$pct_int" -ge 50 ]; then
    ctx_color="$YELLOW"
  else
    ctx_color="$GREEN"
  fi
  printf " ${ctx_color}ctx:%s%%${RESET}" "$pct_int"
fi

# cumulative token costs
if [ "$total_in" -gt 0 ] || [ "$total_out" -gt 0 ]; then
  # Format in K
  in_k=$(awk "BEGIN {printf \"%.1f\", $total_in / 1000}")
  out_k=$(awk "BEGIN {printf \"%.1f\", $total_out / 1000}")
  printf " ${GRAY}in:%sk out:%sk${RESET}" "$in_k" "$out_k"
fi

printf '\n'
