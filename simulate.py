"""
Power simulation for Study 1 of "From Doing to Checking".

The idea in plain words
-----------------------
Standard sample-size formulas do not fit this design (two blocks per person,
the outcome d' from signal detection theory, and an interaction). So we
estimate statistical power by simulation:

  1. Assume how large the effects are (e.g., the prosocial message raises d'
     by 0.15 or 0.25).
  2. Create virtual participants. Each one has a true sensitivity (d') and a
     true criterion (c), plus the assumed effects of their condition.
  3. Let each virtual participant "review" the replies: we draw how many
     errors they catch (hits) and how many correct replies they flag
     (false alarms) from the signal detection model.
  4. Compute d' from these counts and test the hypotheses.
  5. Repeat many times. Power = the share of repetitions in which the test
     was significant (p < .05).

Conditions
----------
Message (between participants): 0 = neutral, 1 = self-benefit, 2 = prosocial
Accountability (within or between): 0 = anonymous, 1 = accountable

Effect parameters
-----------------
dP : effect of the prosocial message on d'
r  : effect of the self-benefit message as a share of dP (0 = none)
dA : effect of accountability on d'
s  : strength of substitution: in the accountable condition the message
     effect is multiplied by (1 - s). s = 0.5 removes half, s = 1 removes all.
cA : effect of accountability on the criterion c

The random seed is fixed, so running the scripts gives the same numbers.
"""
import numpy as np
from scipy.stats import norm, t as tdist

rng = np.random.default_rng(2026)


def dprime(h, ns, f, nn):
    """d' and c from hits (h of ns errors) and false alarms (f of nn correct
    replies), with the log-linear correction of Hautus (1995)."""
    H = (h + 0.5) / (ns + 1)
    F = (f + 0.5) / (nn + 1)
    return norm.ppf(H) - norm.ppf(F), -(norm.ppf(H) + norm.ppf(F)) / 2


def gen(n, d_true, c_true, n_items, prev):
    """Simulate one block for n participants and return their d' and c."""
    ns = int(round(n_items * prev))   # number of error items
    nn = n_items - ns                 # number of correct items
    pH = norm.cdf(d_true / 2 - c_true)   # chance of catching an error
    pF = norm.cdf(-d_true / 2 - c_true)  # chance of flagging a correct reply
    h = rng.binomial(ns, pH)
    f = rng.binomial(nn, pF)
    return dprime(h, ns, f, nn)


def welch_p(a, b):
    """Two-sided Welch t-test; returns (p, t)."""
    va, vb = a.var(ddof=1) / len(a), b.var(ddof=1) / len(b)
    tt = (a.mean() - b.mean()) / np.sqrt(va + vb)
    df = (va + vb) ** 2 / (va ** 2 / (len(a) - 1) + vb ** 2 / (len(b) - 1))
    return 2 * tdist.sf(abs(tt), df), tt


def effects(dP, r, dA, s, cA):
    """Return a function that gives the shift in d' and c for message m and
    accountability a."""
    def f(m, a):
        dm = {0: 0.0, 1: r * dP, 2: dP}[m]
        mult = (1 - s) if a == 1 else 1.0
        return dm * mult + dA * a, cA * a
    return f


def run_between(n_cell, eff, n_items, prev, reps, mu_d=1.67, mu_c=0.45, sd_d=0.5, sd_c=0.3):
    """Accountability BETWEEN participants: six separate groups.
    Returns the share of significant results (power) for each test."""
    out = {'P_vs_S': 0, 'P_vs_N': 0, 'Acc': 0, 'Int_PS': 0, 'Int_PN': 0}
    for _ in range(reps):
        D = {}
        for m in range(3):
            for a in range(2):
                sd, sc = eff(m, a)
                dt = mu_d + sd + rng.normal(0, sd_d, n_cell)
                ct = mu_c + sc + rng.normal(0, sd_c, n_cell)
                D[m, a] = gen(n_cell, dt, ct, n_items, prev)[0]
        # main effects (averaged over accountability)
        P = np.r_[D[2, 0], D[2, 1]]; S = np.r_[D[1, 0], D[1, 1]]; N = np.r_[D[0, 0], D[0, 1]]
        out['P_vs_S'] += welch_p(P, S)[0] < .05
        out['P_vs_N'] += welch_p(P, N)[0] < .05
        A1 = np.r_[D[0, 1], D[1, 1], D[2, 1]]; A0 = np.r_[D[0, 0], D[1, 0], D[2, 0]]
        out['Acc'] += welch_p(A1, A0)[0] < .05
        # interaction: (prosocial - other) when accountable minus when anonymous
        for key, g in [('Int_PS', 1), ('Int_PN', 0)]:
            est = (D[2, 1].mean() - D[g, 1].mean()) - (D[2, 0].mean() - D[g, 0].mean())
            se = np.sqrt(sum(D[k].var(ddof=1) / n_cell for k in [(2, 1), (g, 1), (2, 0), (g, 0)]))
            out[key] += 2 * norm.sf(abs(est / se)) < .05
    return {k: v / reps for k, v in out.items()}


def run_within(n_group, eff, n_items_block, prev, reps, mu_d=1.67, mu_c=0.45, sd_d=0.5, sd_c=0.3, sd_slope=0.2):
    """Accountability WITHIN participants: each person does both blocks.
    Returns the share of significant results (power) for each test."""
    out = {'P_vs_S': 0, 'P_vs_N': 0, 'Acc': 0, 'Int_PS': 0, 'Int_PN': 0}
    for _ in range(reps):
        diff = {}; mean = {}
        for m in range(3):
            base_d = mu_d + rng.normal(0, sd_d, n_group)
            base_c = mu_c + rng.normal(0, sd_c, n_group)
            slope = rng.normal(0, sd_slope, n_group)   # people differ in how much accountability helps
            dh = []
            for a in range(2):
                sd, sc = eff(m, a)
                dh.append(gen(n_group, base_d + sd + slope * a, base_c + sc, n_items_block, prev)[0])
            diff[m] = dh[1] - dh[0]          # accountable minus anonymous, per person
            mean[m] = (dh[0] + dh[1]) / 2    # average of the two blocks, per person
        out['P_vs_S'] += welch_p(mean[2], mean[1])[0] < .05
        out['P_vs_N'] += welch_p(mean[2], mean[0])[0] < .05
        allD = np.r_[diff[0], diff[1], diff[2]]
        out['Acc'] += 2 * tdist.sf(abs(allD.mean() / (allD.std(ddof=1) / np.sqrt(len(allD)))), len(allD) - 1) < .05
        out['Int_PS'] += welch_p(diff[2], diff[1])[0] < .05
        out['Int_PN'] += welch_p(diff[2], diff[0])[0] < .05
    return {k: v / reps for k, v in out.items()}
