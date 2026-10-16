"""Main power table (proposal Table D1, slide "Choosing the sample size").

Within-participants design, 2 blocks x 40 items, 25% errors, 1,000 repetitions
per scenario. Prints power for several sample sizes; the planned sample is
500 per message condition (N = 1,500).

Run:  python run_main_power.py
Takes about 3-4 minutes.
"""
from simulate import *
import itertools

R = 1000
print('WITHIN design, 2 blocks x 40 items, prevalence .25, Monte Carlo reps', R)
print('dP  r   s  | n/group totalN | P-S  P-N  Acc  IntPS IntPN')
for dP, r, s in itertools.product([0.15, 0.25], [0.0, 0.5], [0.5, 1.0]):
    eff = effects(dP, r, 0.2, s, -0.1)
    for n in [300, 400, 500, 600]:
        w = run_within(n, eff, 40, .25, R)
        print(f'{dP} {r} {s} | {n:4d} {3*n:5d} | ' + ' '.join(f'{w[k]:.2f}' for k in ['P_vs_S', 'P_vs_N', 'Acc', 'Int_PS', 'Int_PN']))
