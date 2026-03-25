# Lessons — Infrastructure & Security

> Load when: setting up backups · managing credentials · configuring servers · securing services.
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

## 2026-03-25 — Rsync Nextcloud: exclude cache and internal folders

**Context**: first rsync of `/opt/nextcloud/files/` pulled Nextcloud app cache (preview thumbnails, theming) and internal trash/version history — massively inflating backup size with non-essential data.

**Folders to always exclude when rsyncing Nextcloud user data**:
- `appdata_oc8odmpvrrzm/` — Nextcloud app cache (preview thumbnails, theming icons)
- `admin/files_trashbin/` — Nextcloud internal trash bin (soft-deleted files with timestamps)
- `admin/files_versions/` — Nextcloud file version history
- `admin/files/Trash/` — user-facing trash folder

**Essential to keep**: `admin/files/Archive/` · `admin/files/Inbox/` · `admin/files/system/`

**Lesson**: always scope Nextcloud rsync to user data only. The named volume `nextcloud_nextcloud_data` contains both app code and user data — the bind mount at `/opt/nextcloud/files/` is cleaner but still includes internal Nextcloud folders.

---
