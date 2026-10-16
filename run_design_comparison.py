"""Within vs. between design comparison (proposal Table D2).

For the same total sample size and 60 items per participant, compares power
when accountability is manipulated within participants (two blocks of 30)
or between participants (one block of 60). 500 repetitions per scenario.
Saves all results to results/design_comparison.json.

Run:  python run_design_comparison.py
This takes longer (about 10 minutes).
"""
from simulate import *
import itertools, json, os

res = []
R = 500
for dP, r, s, pv in itertools.product([0.15, 0.25], [0.0, 0.5], [0.5, 1.0], [0.15, 0.25]):
    eff = effects(dP, r, 0.2, s, -0.1)
    for n in [100, 200, 300, 400]:
        b = run_between(n, eff, 60, pv, R)
        w = run_within(int(n * 2), eff, 30, pv, R)   # same total N: 6n in both designs
        res.append(dict(dP=dP, r=r, s=s, prev=pv, totalN=6 * n, between=b, within=w))
os.makedirs('results', exist_ok=True)
json.dump(res, open('results/design_comparison.json', 'w'))
print(len(res), 'scenarios saved')
