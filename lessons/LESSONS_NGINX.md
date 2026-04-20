# Lessons — nginx

> Load when: configuring nginx as reverse proxy · serving static files · sub-path routing · Docker + nginx.
> Never delete entries. Add date and context.

---

## [nginx] · Rule · `alias` + `try_files` causes internal redirect loop for static file serving
> 2026-04-09 · source: pea-pme-pulse
- `alias /path/` combined with `try_files $uri $uri/ /prefix/index.html` → nginx enters an infinite internal redirect loop (500)
- Fix: use `alias /path/;` + `index index.html;` only — no `try_files` needed for static single-page apps served at a sub-path
- Host-side files are invisible to the nginx container — must be volume-mounted into the container via `docker-compose.yml`

## [nginx] · Rule · nginx /var/www/ is root-owned — scp to home first, then sudo mv
> 2026-04-13 · source: pea-pme-pulse
- `gcloud compute scp` directly to `/var/www/` fails with "Permission denied" even as the VM's SSH user
- Two-step fix: `gcloud compute scp files prefect-server:~` → then `gcloud compute ssh --command="sudo mv ~/files /var/www/target/"`
- No service restart needed for static files — nginx serves them on-read

## [nginx] · Rule · nginx compose volume path is relative to compose file location, not cwd
> 2026-04-16 · source: pea-pme-pulse
- `./nginx.conf` in `infra/docker-compose.yml` resolves to `infra/nginx.conf` — NOT the cwd `nginx.conf`
- If the VM runs compose from a flat dir (`~/prefect/`), live nginx.conf is `~/prefect/nginx.conf`, separate from `infra/nginx.conf` in the repo
- After merging nginx changes: `cp /opt/<repo>/infra/nginx.conf ~/prefect/nginx.conf && docker compose restart nginx`

## [nginx] · Rule · Use host.docker.internal instead of hardcoded IPs in nginx proxy_pass
> 2026-04-16 · source: pea-pme-pulse
- `172.17.0.1` and internal VM IPs break on VM rebuild or network change
- Add `extra_hosts: host.docker.internal:host-gateway` to the nginx service in docker-compose
- Then use `proxy_pass http://host.docker.internal:<port>` for any host service (systemd, separate compose stacks)

## [nginx] · Rule · Next.js SPA cannot be reverse-proxied at a sub-path without recompilation
> 2026-04-18 · source: pea-pme-pulse
- nginx `proxy_pass http://host:port/;` strips the sub-path prefix → server responds 200
- But the SPA client-side router initialises with the browser URL (e.g. `/nao/`), finds no route, renders 404
- Root cause: Next.js bakes `basePath` into compiled JS at build time — not overridable via env var at runtime
- Fix: modify `next.config.js` (`basePath: '/sub-path'`) + rebuild · or serve at root on a dedicated port
- For third-party/bonus apps: expose on their own port rather than recompiling
