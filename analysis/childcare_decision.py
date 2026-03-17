#!/usr/bin/env python3
"""
Childcare financing decision analysis.

Compares five strategies over 3 / 5 / 7-year horizons:
  SC1_au_pair      — buy apartment, au pair lives there (not rented), sell at end
  SC1_location     — buy apartment, rent it out fully, sell at end
                     (+ add babysitter cost separately to compare with SC2/SC3)
  SC2_solo         — Babysitter Solo: place money + one babysitter covers everything
                     21.5h/week: Mon/Tue/Thu 4–7:30pm + Wed 11:30–19:30 + 3h evenings
                     Cost: 21.5h × 11€ × 52 + 500€ = 12,798€/year
  SC3b_relais_part — Babysitter Relais partiel: primary can't do Wed 11:30 pickup
                     Primary +1€/h surcharge Mon/Tue/Thu/Fri 4–5:30pm only
                     Secondary: Mon–Fri 5:30–7:30pm + full Wed 11:30–19:30 + 3h extra
                     Cost: 312€ (primary) + 11,368€ (secondary) = 11,680€/year
  SC3_relais_comp  — Babysitter Relais complet: primary covers Wed 11:30 pickup too
                     Primary +1€/h surcharge Mon/Tue/Thu/Fri 4–5:30pm + Wed 11:30–17:30
                     Secondary: Mon–Fri 5:30–7:30pm + 3h extra evenings
                     Cost: 624€ (primary) + 7,936€ (secondary) = 8,560€/year
                     Assumption: primary babysitter's normal schedule ends at 5:30pm

All costs expressed as NET COST = total outflows − total inflows over the period.
Lower is better.

Output: childcare_decision.csv  (all combinations)
        childcare_summary.txt   (decision-ready comparison tables)
"""

import csv
from itertools import product
from pathlib import Path

# ─── Parameters ──────────────────────────────────────────────────────────────

APPORTS = [10_000, 30_000, 50_000]
PRIX_TOTAUX = [100_000, 110_000, 120_000]   # bien + notaire (≈7.5%) + travaux
FRAIS_ACHAT_RATE = 0.075                     # embedded in prix_total already
FRAIS_REVENTE_RATE = 0.075
TAEG = 0.033
DUREES_EMPRUNT = [10, 15, 20, 25]           # years
HORIZONS = [3, 5, 7]                        # years until sale
HORIZONS_TRANSITION = [2, 3, 5, 7]         # includes Y2 exit for transition scenarios
AU_PAIR_ANS = 2                             # au pair phase duration (years)
PRIX_REVENTE_FACTORS = [1.00, 0.98, 0.95]  # relative to original market value

COUT_AU_PAIR_AN = 6_200      # 450€/mois × 12 + 200€/trimestre URSSAF

# Babysitter Solo (SC2): one person covers everything
# Mon/Tue/Thu 4–7:30pm (3.5h×3=10.5h) + Wed 11:30–19:30 (8h) + 3h evenings = 21.5h/week
COUT_BABS_SOLO_AN = 12_798   # 21.5h × 11€ × 52 + 500€ = 12,798€

# Babysitter Relais partiel (SC3b): primary can't do Wed 11:30 pickup
# Primary: +1€/h × 6h/week (Mon/Tue/Thu/Fri 4–5:30pm) = 312€/year
# Secondary: Mon–Fri 5:30–7:30pm (10h) + full Wed 11:30–19:30 (8h, replaces primary) + 3h extra
#   = (8h Wed + 8h Mon/Tue/Thu/Fri + 3h extra) × 11€ × 52 + 500€ = 19h × 11€ × 52 + 500€ = 11,368€
COUT_BABS_RELAIS_PART_AN = 11_680  # 312 + 11,368

# Babysitter Relais complet (SC3): primary covers Wed 11:30 pickup too
# Primary: +1€/h × 12h/week (6h Mon/Tue/Thu/Fri + 6h Wed) = 624€/year
# Secondary: Mon–Fri 5:30–7:30pm (10h) + 3h extra = 13h × 11€ × 52 + 500€ = 7,936€
# Assumption: primary's normal schedule already ends at 5:30pm
COUT_BABS_RELAIS_COMP_AN = 8_560   # 624 + 7,936

RENDEMENTS_NETS = {
    "2.5%_brut": 0.0175,   # 2.5% gross → 1.75% net after flat tax 30%
    "3.0%_brut": 0.021,    # 3.0% gross → 2.10% net
}

LOYERS_MENSUEL = [600, 1_000]   # €/mois charges comprises
CHARGES_AN = 4_850              # copro 1800 + foncière 1200 + PNO 250
                                # + vacance 700 + gestion ~900 (8% × 1000 × 12)


# ─── Core formulas ───────────────────────────────────────────────────────────

def mensualite(principal: float, taeg: float, duree_ans: int) -> float:
    r = taeg / 12
    n = duree_ans * 12
    return principal * r * (1 + r) ** n / ((1 + r) ** n - 1)


def capital_restant(principal: float, taeg: float, duree_ans: int, annees: int) -> float:
    r = taeg / 12
    n = duree_ans * 12
    k = min(annees * 12, n)
    if k >= n:
        return 0.0
    m = mensualite(principal, taeg, duree_ans)
    return m * (1 - (1 + r) ** (-(n - k))) / r


def encaisse_revente(prix_total: float, rev_factor: float, cap_restant: float) -> float:
    """Net proceeds from sale: market value × factor × (1-fees) − remaining debt."""
    # Market value of the property (strip purchase fees from prix_total)
    prix_bien_achat = prix_total / (1 + FRAIS_ACHAT_RATE)
    prix_revente_marche = prix_bien_achat * rev_factor
    return prix_revente_marche * (1 - FRAIS_REVENTE_RATE) - cap_restant


# ─── Scenario builders ───────────────────────────────────────────────────────

def sc1_au_pair(apport, prix_total, duree, horizon, rev_factor):
    """Buy apartment, au pair lives there, sell at horizon."""
    if apport >= prix_total:
        return None
    principal = prix_total - apport
    m = mensualite(principal, TAEG, duree)
    cap = capital_restant(principal, TAEG, duree, horizon)
    encaisse = encaisse_revente(prix_total, rev_factor, cap)
    mortgage_paid = m * 12 * horizon
    childcare = COUT_AU_PAIR_AN * horizon
    # Net cost = everything spent that you don't recover
    # Outflows: apport (at t=0) + mortgage payments + childcare
    # Inflows: encaisse (= sale net of fees, with remaining debt already subtracted)
    net_cost = apport + mortgage_paid + childcare - encaisse
    cashflow_an = -(m * 12)  # no rental income
    return {
        "scenario": "SC1_au_pair",
        "apport": apport,
        "prix_total": prix_total,
        "duree_emprunt_ans": duree,
        "horizon_ans": horizon,
        "revente_factor": rev_factor,
        "loyer_mois": None,
        "rendement_label": None,
        "principal": round(principal),
        "mensualite_mois": round(m),
        "mortgage_paid_total": round(mortgage_paid),
        "capital_restant": round(cap),
        "encaisse_revente": round(encaisse),
        "cout_childcare_total": round(childcare),
        "cashflow_immo_an": round(cashflow_an),
        "cout_net_total": round(net_cost),
        "heures_semaine": 25,
    }


def sc1_location(apport, prix_total, duree, horizon, rev_factor, loyer_mois):
    """Buy apartment, rent it out fully (no au pair), sell at horizon.
    Net cost is the investment result ONLY — add babysitter cost separately."""
    if apport >= prix_total:
        return None
    principal = prix_total - apport
    m = mensualite(principal, TAEG, duree)
    cap = capital_restant(principal, TAEG, duree, horizon)
    encaisse = encaisse_revente(prix_total, rev_factor, cap)
    mortgage_paid = m * 12 * horizon
    # Rental income net of charges (ignore taxes for simplicity — first-order model)
    loyer_an_net = loyer_mois * 12 - CHARGES_AN
    loyer_total = loyer_an_net * horizon
    cashflow_an = loyer_an_net - m * 12
    # Net investment cost = apport + mortgage - rental income - encaisse
    net_immo = apport + mortgage_paid - loyer_total - encaisse
    # Add all babysitter options for convenience
    net_avec_babs_soir = net_immo + COUT_BABS_SOLO_AN * horizon
    net_avec_babs_mixte = net_immo + COUT_BABS_RELAIS_PART_AN * horizon
    net_avec_babs_comp  = net_immo + COUT_BABS_RELAIS_COMP_AN * horizon
    return {
        "scenario": "SC1_location",
        "apport": apport,
        "prix_total": prix_total,
        "duree_emprunt_ans": duree,
        "horizon_ans": horizon,
        "revente_factor": rev_factor,
        "loyer_mois": loyer_mois,
        "rendement_label": None,
        "principal": round(principal),
        "mensualite_mois": round(m),
        "mortgage_paid_total": round(mortgage_paid),
        "capital_restant": round(cap),
        "encaisse_revente": round(encaisse),
        "cout_childcare_total": None,
        "cashflow_immo_an": round(cashflow_an),
        "net_immo_only": round(net_immo),
        "net_avec_babs_soir": round(net_avec_babs_soir),
        "net_avec_babs_mixte": round(net_avec_babs_mixte),
        "net_avec_babs_comp": round(net_avec_babs_comp),
        "cout_net_total": round(net_immo),   # investment P&L only
        "heures_semaine": None,
    }


def sc1_transition_sell(apport, prix_total, duree, horizon, rev_factor, rendement_label, rendement_net):
    """Au pair AU_PAIR_ANS years, sell at Y2, place proceeds at r until horizon.
    No babysitter costs after the au pair phase. Pure investment comparison."""
    if apport >= prix_total:
        return None
    principal = prix_total - apport
    m = mensualite(principal, TAEG, duree)
    # Phase 1 (Y0 → Y2): au pair in apartment
    cap_Y2 = capital_restant(principal, TAEG, duree, AU_PAIR_ANS)
    encaisse_Y2 = encaisse_revente(prix_total, rev_factor, cap_Y2)
    mortgage_Y2 = m * 12 * AU_PAIR_ANS
    childcare = COUT_AU_PAIR_AN * AU_PAIR_ANS          # 12,400€ fixed
    # Phase 2 (Y2 → H): place encaisse_Y2 at rendement_net
    placement_years = horizon - AU_PAIR_ANS            # 0 if H=2, 1 if H=3, etc.
    proceeds_at_H = encaisse_Y2 * (1 + rendement_net) ** placement_years
    net_cost = apport + mortgage_Y2 + childcare - proceeds_at_H
    return {
        "scenario": "SC_trans_sell",
        "apport": apport,
        "prix_total": prix_total,
        "duree_emprunt_ans": duree,
        "horizon_ans": horizon,
        "revente_factor": rev_factor,
        "loyer_mois": None,
        "rendement_label": rendement_label,
        "principal": round(principal),
        "mensualite_mois": round(m),
        "mortgage_paid_total": round(mortgage_Y2),
        "capital_restant": round(cap_Y2),
        "encaisse_Y2": round(encaisse_Y2),
        "proceeds_at_H": round(proceeds_at_H),
        "cout_childcare_total": round(childcare),
        "cashflow_immo_an": None,
        "cout_net_total": round(net_cost),
        "heures_semaine": None,
    }


def sc1_transition_rent(apport, prix_total, duree, horizon, rev_factor, loyer_mois):
    """Au pair AU_PAIR_ANS years, rent from Y2 to horizon, sell at horizon.
    No babysitter costs after the au pair phase. Pure investment comparison."""
    if apport >= prix_total or horizon <= AU_PAIR_ANS:
        return None
    principal = prix_total - apport
    m = mensualite(principal, TAEG, duree)
    # Mortgage payments from Y0 to H (or to loan end)
    mortgage_total = m * 12 * min(horizon, duree)
    cap_YH = capital_restant(principal, TAEG, duree, horizon)
    encaisse_YH = encaisse_revente(prix_total, rev_factor, cap_YH)
    childcare = COUT_AU_PAIR_AN * AU_PAIR_ANS          # 12,400€ fixed
    # Rental income only during Phase 2 (Y2 → H)
    rental_years = horizon - AU_PAIR_ANS
    loyer_an_net = loyer_mois * 12 - CHARGES_AN
    rental_total = loyer_an_net * rental_years
    cashflow_phase2_an = loyer_an_net - m * 12
    net_cost = apport + mortgage_total + childcare - rental_total - encaisse_YH
    # Also compute encaisse_Y2 for reference
    cap_Y2 = capital_restant(principal, TAEG, duree, AU_PAIR_ANS)
    encaisse_Y2 = encaisse_revente(prix_total, rev_factor, cap_Y2)
    return {
        "scenario": "SC_trans_rent",
        "apport": apport,
        "prix_total": prix_total,
        "duree_emprunt_ans": duree,
        "horizon_ans": horizon,
        "revente_factor": rev_factor,
        "loyer_mois": loyer_mois,
        "rendement_label": None,
        "principal": round(principal),
        "mensualite_mois": round(m),
        "mortgage_paid_total": round(mortgage_total),
        "capital_restant": round(cap_YH),
        "encaisse_Y2": round(encaisse_Y2),
        "proceeds_at_H": round(encaisse_YH),
        "cout_childcare_total": round(childcare),
        "cashflow_immo_an": round(cashflow_phase2_an),
        "cout_net_total": round(net_cost),
        "heures_semaine": None,
    }


def placement_scenario(scenario_key, cout_an, heures_sem, apport, horizon, rendement_label, rendement_net):
    """Place money in safe vehicle + pay babysitter."""
    gain = apport * ((1 + rendement_net) ** horizon - 1)
    childcare = cout_an * horizon
    net_cost = childcare - gain
    return {
        "scenario": scenario_key,
        "apport": apport,
        "prix_total": None,
        "duree_emprunt_ans": None,
        "horizon_ans": horizon,
        "revente_factor": None,
        "loyer_mois": None,
        "rendement_label": rendement_label,
        "principal": None,
        "mensualite_mois": None,
        "mortgage_paid_total": None,
        "capital_restant": None,
        "encaisse_revente": round(apport + gain),
        "cout_childcare_total": round(childcare),
        "cashflow_immo_an": None,
        "cout_net_total": round(net_cost),
        "heures_semaine": heures_sem,
    }


# ─── Run all combinations ────────────────────────────────────────────────────

rows = []

for apport, prix_total, duree, horizon, rev_factor in product(
    APPORTS, PRIX_TOTAUX, DUREES_EMPRUNT, HORIZONS, PRIX_REVENTE_FACTORS
):
    r = sc1_au_pair(apport, prix_total, duree, horizon, rev_factor)
    if r:
        rows.append(r)
    for loyer in LOYERS_MENSUEL:
        r = sc1_location(apport, prix_total, duree, horizon, rev_factor, loyer)
        if r:
            rows.append(r)

# Transition scenarios: au pair 2yr → sell+place OR rent
for apport, prix_total, duree, horizon, rev_factor in product(
    APPORTS, PRIX_TOTAUX, DUREES_EMPRUNT, HORIZONS_TRANSITION, PRIX_REVENTE_FACTORS
):
    for lbl, rend in RENDEMENTS_NETS.items():
        r = sc1_transition_sell(apport, prix_total, duree, horizon, rev_factor, lbl, rend)
        if r:
            rows.append(r)
    for loyer in LOYERS_MENSUEL:
        r = sc1_transition_rent(apport, prix_total, duree, horizon, rev_factor, loyer)
        if r:
            rows.append(r)

PLACEMENT_SCENARIOS = [
    ("SC2_solo",         COUT_BABS_SOLO_AN,         21.5),
    ("SC3b_relais_part", COUT_BABS_RELAIS_PART_AN,  19.0),
    ("SC3_relais_comp",  COUT_BABS_RELAIS_COMP_AN,  13.0),
]

for apport, horizon, (lbl, rend) in product(
    APPORTS, HORIZONS, RENDEMENTS_NETS.items()
):
    for sc_key, cout_an, heures in PLACEMENT_SCENARIOS:
        rows.append(placement_scenario(sc_key, cout_an, heures, apport, horizon, lbl, rend))


# ─── CSV export ──────────────────────────────────────────────────────────────

out_dir = Path(__file__).parent
csv_path = out_dir / "childcare_decision.csv"

fieldnames = [
    "scenario", "apport", "prix_total", "duree_emprunt_ans", "horizon_ans",
    "revente_factor", "loyer_mois", "rendement_label",
    "principal", "mensualite_mois", "mortgage_paid_total",
    "capital_restant", "encaisse_revente", "encaisse_Y2", "proceeds_at_H",
    "cout_childcare_total", "cashflow_immo_an",
    "net_immo_only", "net_avec_babs_soir", "net_avec_babs_mixte", "net_avec_babs_comp",
    "cout_net_total", "heures_semaine",
]

with open(csv_path, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
    writer.writeheader()
    writer.writerows(rows)

print(f"CSV → {csv_path}  ({len(rows)} rows)")


# ─── Summary tables ──────────────────────────────────────────────────────────

def fmt(v, prefix=""):
    if v is None:
        return "    —   "
    sign = "+" if v > 0 else ""
    return f"{prefix}{sign}{v:,.0f}€"


summary_path = out_dir / "childcare_summary.txt"
lines = []
lines.append("=" * 90)
lines.append("CHILDCARE FINANCING DECISION — NET COST COMPARISON")
lines.append("TAEG 3.3% | Frais achat/revente 7.5% | Au pair 6 200€/an")
lines.append("SC2 Solo 12 798€/an | SC3b Relais partiel 11 680€/an | SC3 Relais complet 8 560€/an")
lines.append("Net cost = total spend − total recovered.  Lower = better.  Negative = you made money.")
lines.append("=" * 90)

for horizon in HORIZONS:
    lines.append(f"\n{'─'*90}")
    lines.append(f" HORIZON {horizon} ANS")
    lines.append(f"{'─'*90}")

    for apport in APPORTS:
        lines.append(f"\n  Apport {apport:,}€")
        lines.append(f"  {'Scenario':<38} {'Prix':<8} {'Durée':>6} {'Revente':>8} {'Loyer':>7} {'Mensual.':>9} {'Cashflow/an':>11} {'COÛT NET':>10}")
        lines.append(f"  {'─'*38} {'─'*8} {'─'*6} {'─'*8} {'─'*7} {'─'*9} {'─'*11} {'─'*10}")

        sc_rows = [r for r in rows if r["horizon_ans"] == horizon and r["apport"] == apport]

        # SC1 au pair — show best duree per (prix, revente)
        for prix in PRIX_TOTAUX:
            for rev in PRIX_REVENTE_FACTORS:
                candidates = [r for r in sc_rows
                              if r["scenario"] == "SC1_au_pair"
                              and r["prix_total"] == prix
                              and r["revente_factor"] == rev]
                if not candidates:
                    continue
                best = min(candidates, key=lambda r: r["cout_net_total"])
                label = f"SC1 au pair (best duree {best['duree_emprunt_ans']}ans)"
                lines.append(
                    f"  {label:<38} {prix//1000}k€    {best['duree_emprunt_ans']:>4}a  "
                    f"{rev:.0%}    {fmt(best.get('loyer_mois')):>7} "
                    f"{fmt(best['mensualite_mois']):>9} "
                    f"{fmt(best['cashflow_immo_an']):>11} "
                    f"{fmt(best['cout_net_total']):>10}"
                )

        # SC1 location — show best duree per (prix, revente, loyer)
        for prix in PRIX_TOTAUX:
            for rev in PRIX_REVENTE_FACTORS:
                for loyer in LOYERS_MENSUEL:
                    candidates = [r for r in sc_rows
                                  if r["scenario"] == "SC1_location"
                                  and r["prix_total"] == prix
                                  and r["revente_factor"] == rev
                                  and r["loyer_mois"] == loyer]
                    if not candidates:
                        continue
                    best = min(candidates, key=lambda r: r["cout_net_total"])
                    label = f"SC1 location {loyer}€/m (best {best['duree_emprunt_ans']}ans)"
                    lines.append(
                        f"  {label:<38} {prix//1000}k€    {best['duree_emprunt_ans']:>4}a  "
                        f"{rev:.0%}  {loyer:>5}€/m "
                        f"{fmt(best['mensualite_mois']):>9} "
                        f"{fmt(best['cashflow_immo_an']):>11} "
                        f"{'immo: '+fmt(best['net_immo_only']):>10}"
                    )
                    lines.append(
                        f"  {'  → + SC2 Solo':<38} {'':>8} {'':>6} {'':>8} {'':>7} {'':>9} {'':>11} "
                        f"{fmt(best['net_avec_babs_soir']):>10}"
                    )
                    lines.append(
                        f"  {'  → + SC3b Relais partiel':<38} {'':>8} {'':>6} {'':>8} {'':>7} {'':>9} {'':>11} "
                        f"{fmt(best['net_avec_babs_mixte']):>10}"
                    )
                    lines.append(
                        f"  {'  → + SC3 Relais complet':<38} {'':>8} {'':>6} {'':>8} {'':>7} {'':>9} {'':>11} "
                        f"{fmt(best['net_avec_babs_comp']):>10}"
                    )

        # SC2 / SC3b / SC3
        for sc_label, sc_key in [
            ("SC2 Solo 21.5h/sem",           "SC2_solo"),
            ("SC3b Relais partiel 19h/sem",   "SC3b_relais_part"),
            ("SC3 Relais complet 13h/sem",    "SC3_relais_comp"),
        ]:
            for lbl in RENDEMENTS_NETS:
                r_rows = [r for r in sc_rows
                          if r["scenario"] == sc_key and r["rendement_label"] == lbl]
                if not r_rows:
                    continue
                r = r_rows[0]
                lines.append(
                    f"  {sc_label+' '+lbl:<38} {'':>8} {'':>6} {'':>8} {'':>7} {'':>9} {'':>11} "
                    f"{fmt(r['cout_net_total']):>10}"
                )

lines.append(f"\n{'='*90}")
lines.append("TRANSITION SCENARIO: AU PAIR 2 ANS → PURE INVESTMENT (no babysitter costs after Y2)")
lines.append("Phase 1 (Y0–Y2): au pair in apartment — 12,400€ childcare, mortgage running, no rental income")
lines.append("Phase 2 (Y2–H): two paths compared:")
lines.append("  PATH SELL  → sell at Y2, place proceeds at 2.5% or 3% net until H")
lines.append("  PATH RENT  → rent apartment at 600€ or 1000€/mois until H, then sell")
lines.append("Net cost = total permanently spent.  Lower = better.  Negative = you made money overall.")
lines.append("=" * 90)

for apport in APPORTS:
    lines.append(f"\n{'─'*90}")
    lines.append(f" Apport {apport:,}€")
    lines.append(f"{'─'*90}")

    for prix in PRIX_TOTAUX:
        for rev in [1.00, 0.98]:   # flat and mild drop — most relevant cases
            lines.append(f"\n  {prix//1000}k€ apt | Revente {rev:.0%} | best loan duration shown")
            lines.append(f"  {'Path':<42} {'H=2':>10} {'H=3':>10} {'H=5':>10} {'H=7':>10}")
            lines.append(f"  {'─'*42} {'─'*10} {'─'*10} {'─'*10} {'─'*10}")

            trans_rows = [r for r in rows
                          if r["apport"] == apport
                          and r["prix_total"] == prix
                          and r["revente_factor"] == rev]

            # PATH SELL at r=2.5% and 3%
            for lbl in RENDEMENTS_NETS:
                sell_by_H = {}
                for h in HORIZONS_TRANSITION:
                    cands = [r for r in trans_rows
                             if r["scenario"] == "SC_trans_sell"
                             and r["horizon_ans"] == h
                             and r["rendement_label"] == lbl]
                    if cands:
                        sell_by_H[h] = min(cands, key=lambda r: r["cout_net_total"])
                label = f"SELL → place {lbl}"
                vals = [fmt(sell_by_H.get(h, {}).get("cout_net_total")) for h in HORIZONS_TRANSITION]
                lines.append(f"  {label:<42} {vals[0]:>10} {vals[1]:>10} {vals[2]:>10} {vals[3]:>10}")

            # PATH RENT at 600 and 1000
            for loyer in LOYERS_MENSUEL:
                rent_by_H = {}
                for h in HORIZONS_TRANSITION:
                    cands = [r for r in trans_rows
                             if r["scenario"] == "SC_trans_rent"
                             and r["horizon_ans"] == h
                             and r["loyer_mois"] == loyer]
                    if cands:
                        rent_by_H[h] = min(cands, key=lambda r: r["cout_net_total"])
                label = f"RENT {loyer}€/m → sell at H"
                vals = []
                for h in HORIZONS_TRANSITION:
                    if h == 2:
                        vals.append("  n/a   ")   # can't rent if H=2 = au pair end
                    else:
                        best = rent_by_H.get(h)
                        vals.append(fmt(best["cout_net_total"]) if best else "    —   ")
                lines.append(f"  {label:<42} {'  n/a   ':>10} {vals[1]:>10} {vals[2]:>10} {vals[3]:>10}")

lines.append(f"\n  NOTE: H=2 = sell right after au pair ends (no phase 2)")
lines.append(f"        H=3 = 1 year of investment phase after au pair")
lines.append(f"        H=5 = 3 years | H=7 = 5 years")
lines.append(f"        All paths include the 12,400€ au pair cost in Y1–Y2")

lines.append(f"\n{'='*90}")
lines.append("KEY READING GUIDE")
lines.append("─" * 90)
lines.append("SC1 au pair     → net cost already includes childcare (au pair living in apt)")
lines.append("SC1 location    → 'immo:' is the pure investment P&L (you still need to pay a babysitter)")
lines.append("                → '+ SC2/SC3b/SC3' = total cost if you switch to that babysitter setup")
lines.append("SC2 Solo        → 1 babysitter covers everything (21.5h/week) — 12,798€/year")
lines.append("SC3b Relais pt  → primary can't do Wed 11:30; secondary covers full Wednesday — 11,680€/year")
lines.append("SC3 Relais comp → primary covers Wed 11:30; secondary evenings only — 8,560€/year")
lines.append("")
lines.append("Revente factor  → 1.00 = sell at same price | 0.98 = -2% | 0.95 = -5%")
lines.append("Cashflow/an     → annual mortgage − rental income (negative = you receive money net)")
lines.append("=" * 90)

summary = "\n".join(lines)
print(summary)

with open(summary_path, "w", encoding="utf-8") as f:
    f.write(summary)

print(f"\nSummary → {summary_path}")
