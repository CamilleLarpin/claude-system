# Lessons — Docker

> Load when: writing Dockerfiles · Docker Compose · containerizing services · debugging container issues.
> Never delete entries. Add date and context.

---

## [docker] · Rule · Docker Compose v5: --env-file flag not supported on run
> 2026-03-26 · source: finances-ezerpin
- `docker compose run --env-file <file>` fails with `unknown flag: --env-file` on Compose v5
- Use shell substitution instead: `-e KEY=$(grep KEY .env | cut -d= -f2)`
- Works for single keys; for multiple keys, repeat `-e` flags

## [docker] · Rule · docker compose run does not mount project data dir by default
> 2026-03-26 · source: finances-ezerpin
- `docker compose run` only mounts volumes defined in `docker-compose.yml` — project host directories are not mounted
- If scripts need access to files in `data/`, `data/reference/`, etc., add explicit `-v /host/path:/container/path` flag
- Example: `docker compose run --rm -v /opt/project/data:/app/data pipeline python script.py`

## [docker] · Rule · docker-compose up -d without --build uses cached image
> 2026-03-26 · source: finances-ezerpin
- `docker-compose up -d` alone never rebuilds the image — it reuses whatever image was last built; new code is NOT picked up
- Fix: `docker-compose build --no-cache && docker-compose stop && docker-compose rm -f && docker-compose up -d`
- `--build` flag on `up` triggers an interactive "Continue?" prompt via SSH — blocks non-interactive execution; use the split form above
- `--no-cache` forces layer invalidation when Docker incorrectly caches `COPY api/` step

## [docker] · Rule · Check for existing systemd services before dockerizing a process
> 2026-04-11 · source: pea-pme-pulse
- Docker container crashes with `[Errno 98] address already in use` in a loop — systemd restarts the process after every kill (new PID each time)
- Detect: `sudo systemctl list-units --type=service --state=running | grep <keyword>` before assuming a port is free
- If systemd service is already robust (`Restart=always`), use it — no need to dockerize; avoids race conditions and duplicate processes
- Kill won't work permanently: must `sudo systemctl stop <service>` to free the port

## [docker] · Rule · docker cp into a running container updates files without rebuild or restart
> 2026-04-29 · source: audio-intelligence-pipeline
- Adding or updating non-code artifacts (templates, config files, static assets) in a running container: `docker cp <local_file> <container>:<path>` — file is immediately available, no restart needed
- Restart IS needed if the app loads the file once at startup (e.g. parsed config); not needed for files read on every request (e.g. prompt templates)
- Zero-downtime and zero-rebuild: faster than image rebuild for one-off file updates on live servers

## [docker] · Rule · Use --host 0.0.0.0 when running Uvicorn inside Docker
> 2026-03-12 · source: audio-intelligence-pipeline
- Default `--host 127.0.0.1` binds only inside the container — port mapping (`-p 8000:8000`) has no effect, requests never reach the app
- Always set `--host 0.0.0.0` in the Dockerfile CMD for any containerised FastAPI/Uvicorn app
