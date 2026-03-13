# Global TODOs — Camille Larpin

> Cross-project and infrastructure tasks.
> Project-specific TODOs live in project .claude/TODOS.md.
> Load when: looking for what to work on next, or when a cross-project task surfaces.

---

## GitHub PAT Rotation

- [ ] **Rotate GitHub PAT "server"** by 2027-03-13 — no expiration set, manual rotation yearly
      Scope: fine-grained, all Hetzner repos. Stored in `.git/config` on server (plaintext).
      Update in: `/opt/finances-ezerpin/.git/config`, `/opt/api/.git/config`

---

## Server Security (n8n-server — 138.199.205.72)

- [ ] Install UFW as second firewall layer
- [ ] Install fail2ban for SSH brute-force protection
      Note: low priority — SSH password auth already disabled, key-only login in place
