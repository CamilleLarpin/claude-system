# NanoClaw — Reference

> Source: Perplexity research 2026-04-28
> GitHub: github.com/qwibitai/nanoclaw

## What It Is
Lightweight open-source personal AI agent framework (MIT) built on Anthropic's Claude Agent SDK. Designed as a production-ready, security-first alternative to heavier frameworks. ~4,000 lines of code, ~15 source files, under 10 dependencies.

## Architecture
Single host process — no microservices, no message brokers. Routes inbound messages through an entity model:

`User → Messaging Group → Agent Group → Session → inbound.db`

Each agent group runs in its own isolated Docker container (MicroVM-based sandbox) with its own memory, skills, and filesystem mounts.

## Per-Group Config
Each agent group has its own CLAUDE.md, isolated filesystem, and AI provider config. One NanoClaw instance can run:
- A personal group (Claude Sonnet)
- A client-facing group (different tools + MCP servers)
- A marketing group (fully isolated)

Primary model: Claude (via Claude Agent SDK / Claude Code). Also supports GPT-4, Gemini, Llama via OpenRouter.

## Native Integrations
Channels: WhatsApp · Telegram · Slack · Discord · Microsoft Teams · Gmail
- Gmail: add via `/add-gmail` skill — email triage, replies, tracking
- Scheduling: built into the orchestration layer
- Agent Swarms (V2): multi-agent teams collaborating in the same chat interface
- Human-in-the-loop (V2): approval gates before risky actions

## Credential Management
Agents never hold raw API keys. Credentials routed through OneCLI Agent Vault — see `references/onecli.md`.

## Deployment
Single command on Linux, macOS, Windows, Raspberry Pi, NAS Synology, or VPS:
```
git clone && claude
```

## When to Reach For It
- Any project requiring agent-based automation with messaging channel integrations
- When you need multi-agent isolation without building the security layer yourself
- Before writing custom agent infrastructure — NanoClaw likely covers it
