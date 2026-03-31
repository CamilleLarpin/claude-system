# Lessons — Machine Learning

> Load when: building classifiers · training models · feature engineering · deploying ML artifacts.
> Never delete entries. Add date and context.

---

## [features] · Rule · Sender (from) is the strongest TF-IDF feature for email classification
> 2026-03-30 · source: gmail-inbox-cleanup phase 1
- Classifier using subject + snippet only → 72.0% accuracy; adding full `from` field (name + address) → 76.8% (+4.8pp); Personal - Family & Friends accuracy 0.77 → 0.91
- Sender identity is often more predictive than content for routing decisions (personal vs. marketing vs. transactional)
- Always include the full `from` field as a feature in email classifiers; domain-only extraction loses the display name signal

---

## [training] · Rule · Collapse rare classes before stratified train/test split
> 2026-03-30 · source: gmail-inbox-cleanup phase 1
- sklearn's `train_test_split(stratify=labels)` raises ValueError if any class has fewer members than the number of CV folds; with many rare classes this crashes silently or noisily
- Rare classes (< MIN_SAMPLES, e.g. 5) learn no useful patterns and should fall through to an LLM fallback at runtime — collapsing them to "Other" before splitting is semantically correct
- Pattern: `counts = Counter(labels); rare = {c for c,n in counts.items() if n < MIN_SAMPLES}; labels = ["Other" if l in rare else l for l in labels]`

---

## [deploy] · Note · sklearn pickle version mismatch — retrain on target Python version
> 2026-03-31 · source: gmail-inbox-cleanup phase 1
- Training on sklearn 1.8.0 (Python 3.14) locally, deploying pickle to sklearn 1.7.2 (Python 3.10) on server produces InconsistentVersionWarning on every load; works for simple models (LinearSVC, TF-IDF) but is a latent risk
- Fix: retrain on the target server after transferring training data, or pin exact sklearn version in requirements.txt for both environments

---
