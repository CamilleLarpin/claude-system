# Lessons — dlt (data load tool)

> Load when: building or debugging dlt pipelines — ingestion, normalization, schema behavior.

---

## [dlt] · Rule · dlt normalizes column names camelCase → snake_case
> 2026-03-17 · source: finances-ezerpin
- dlt automatically normalizes column names on load: `dateOp` → `date_op`, `supplierFound` → `supplier_found`, `categoryParent` → `category_parent`
- Exception: already-lowercase names like `accountbalance` stay as-is (no underscore inserted)
- dbt models written against dlt-loaded tables must use normalized names, not original CSV names — mismatch causes "column not found" errors at compile time
- After any new dlt pipeline: inspect actual column names in DB before writing dbt models
