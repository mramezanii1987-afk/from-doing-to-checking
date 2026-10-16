"""Print the within vs. between comparison for the interaction (H3) at total
N = 1,800, 25% errors and no self-benefit effect (r = 0): proposal Table D2.

Run:  python summarize_design_comparison.py
"""
import json

for g in json.load(open('results/design_comparison.json')):
    if g['prev'] == 0.25 and g['totalN'] == 1800 and g['r'] == 0.0:
        print(f"message effect {g['dP']}, substitution {g['s']}: "
              f"within {g['within']['Int_PN']:.2f}  vs.  between {g['between']['Int_PN']:.2f}")
