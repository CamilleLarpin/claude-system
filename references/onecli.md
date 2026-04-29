# OneCLI — Reference

> Source: Perplexity research 2026-04-28
> GitHub: github.com/onecli/onecli · launched March 2026
> Docker: ghcr.io/onecli/onecli

## What It Is
Open-source HTTPS proxy gateway + credential vault written in Rust. Sits between AI agents and external services — agents never directly hold real API keys.

## How It Works
Agents use placeholder keys (e.g. `FAKE_KEY`) with `HTTPS_PROXY` pointing to the OneCLI gateway. No SDK changes, no wrapper code needed.

Flow:
1. Agent makes normal HTTP request using placeholder key
2. OneCLI authenticates agent via scoped `Proxy-Authorization` token
3. Gateway matches request by host + path pattern to a stored credential rule
4. Real credential decrypted (AES-256-GCM) and injected into the request header
5. Request forwarded to destination (Gmail, Telegram, OpenAI, Stripe, etc.)

Rules are defined by the operator — a compromised agent cannot trick OneCLI into injecting credentials for out-of-scope services.

## Security Properties
- Agents never see real credentials
- Per-agent scoped policies — each agent group has its own identity and allowed services
- Per-agent rate limiting + endpoint blocking — blast radius limited even if token is compromised
- Credentials stored in local KMS or OneCLI Cloud — never written to disk in plaintext
- Optional: layer on HashiCorp Vault for secret rotation (OneCLI handles injection layer)

## Deployment
Single Docker container — proxy gateway + encrypted vault + web dashboard:
```bash
docker run -d -p 10254:10254 -p 10255:10255 \
  -v onecli-data:/app/data ghcr.io/onecli/onecli
```

## Integration with NanoClaw
Default credential layer as of NanoClaw v2. Uses `@onecli-sh/sdk`:
```ts
const onecli = new OneCLI({ url: ONECLI_URL });
await onecli.applyContainerConfig(containerArgs, { agent: agentIdentifier });
```
Each NanoClaw agent group gets its own OneCLI identity with scoped credential policies.

## When to Reach For It
- Any agent that needs to call external services (Gmail, Telegram, Stripe, OpenAI, etc.)
- When you need credential isolation without baking API keys into env vars or agent memory
- Works with any HTTP-based agent or pipeline — not limited to NanoClaw
