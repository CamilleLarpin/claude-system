# Lessons — Google Cloud Platform

> Load when: working with GCP VMs · IAM · service accounts · firewall rules · BigQuery auth.
> Never delete entries. Add date and context.

---

## [gcp] · Rule · GCP firewall is the actual port boundary — nginx alone does not close ports
> 2026-04-19 · source: pea-pme-pulse
- nginx not routing a port ≠ port closed; GCP firewall filters traffic before it reaches the VM
- Firewall rules accumulate silently during debugging — verify with `gcloud compute firewall-rules list --project=<project>` from a principal with `compute.firewalls.list` (not the VM's SA — it typically has only data permissions)
- Common drift: multiple rules for same port (`allow-fastapi`, `allow-fastapi-8000`, `allow-api-8000`) created during incident response
- Only truly closed = no matching ALLOW rule in GCP firewall

## [gcp] · Rule · Every process on a GCP VM inherits the service account permissions automatically
> 2026-04-19 · source: pea-pme-pulse
- ADC via metadata server (169.254.169.254) available to any process on the VM — no opt-in, no credentials needed
- Security implication: code execution on the VM immediately grants all SA permissions (BQ, GCS, etc.)
- Mitigation: minimal SA permissions (least privilege) + close internal service ports in GCP firewall
