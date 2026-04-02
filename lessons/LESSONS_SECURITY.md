# Lessons — Security & Credentials

> Load when: handling API keys · managing secrets · configuring access controls · reviewing credentials.
> Never delete entries. Add date and context.

---

## 2026-03-25 — Never use cloud file storage as a secrets store

**Context**: API keys (Anthropic, OpenAI, Telegram, GitHub, n8n, Notion) were found in a Nextcloud folder that had been "deleted" ~6 weeks earlier but remained in the Nextcloud trash bin, accessible to any admin.

**What we learned**:
- Nextcloud (and any cloud file storage) trash retains deleted files for up to 30 days — deletion is not immediate erasure.
- Files in trash are still accessible to anyone with admin credentials.
- Nextcloud logs (`nextcloud.log`) can be grepped for file paths to check if access occurred.
- No evidence of access found in logs — risk was low retrospectively, but non-zero for 6 weeks.

**Lesson**: credentials belong in the n8n credential store (workflows), `.env` files on server (gitignored, never uploaded), or a password manager. Never in a cloud file system — even temporarily.

---

## 2026-03-25 — Never paste secrets in chat — rotate immediately if exposed

**Context**: CRM bearer token pasted in full into a Claude Code session while building a test curl command.

**Lesson**: Any secret pasted in a chat session should be treated as compromised — conversation logs may persist the value. Rotate immediately: generate new token, update `.env` on server, restart container, update n8n credential.

**Prevention**: use shell substitution to inject secrets without exposing them: `$(grep TOKEN .env | cut -d= -f2)` or `$(ssh server "grep TOKEN file | cut -d= -f2")`.

---

## [github] · Rule · Fine-grained PAT scoped to specific repos → 404 on unlisted private repos
> 2026-04-01 · source: Ghost n8n debug session
- GitHub returns 404 (not 403) for private repos not in the PAT's allowed list — designed to avoid leaking repo existence
- A PAT configured for "selected repos" silently excludes any new repos you create later
- If a service (e.g. n8n workflow) needs to read/write across multiple private repos: scope the PAT to "All repositories" or explicitly add each new repo when created
- Diagnosis: 404 from `GET /repos/{owner}/{repo}/contents/...` with a valid PAT = repo not in PAT scope (or doesn't exist)

---
