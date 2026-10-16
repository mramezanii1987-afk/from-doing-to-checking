# From Doing to Checking: power simulations for Study 1

This repository contains the code used to choose the sample size for Study 1 of the research proposal *From Doing to Checking: Beneficiary Impact, Accountability and the Quality of Human Oversight of AI*.

## The study in short

Participants review 80 customer-support replies drafted by an AI assistant and approve or flag each one. Twenty replies contain an error. Two things are manipulated:

- **Message** (between participants): neutral information, a self-benefit message, or a prosocial message about customers harmed by wrong replies.
- **Accountability** (within participants): one block of 40 replies is anonymous, the other is accountable (decisions are seen with the participant's ID).

The main outcome is **sensitivity (d′)** from signal detection theory: how well a reviewer tells errors apart from correct replies, separately from how readily they flag anything.

## Why a simulation?

Standard sample-size formulas do not fit this design, because it has two blocks per person, the outcome d′, and an interaction (H3). So power is estimated by simulation:

1. Assume how large the effects are.
2. Create virtual participants with a true d′ and criterion, plus the effects of their condition.
3. Simulate their hits and false alarms, and compute d′.
4. Test the hypotheses.
5. Repeat 1,000 times. **Power** is the share of repetitions in which the test was significant (p < .05).

## What is in this repository

| File | What it does |
|---|---|
| `power_analysis/simulate.py` | The simulation functions (commented) |
| `power_analysis/run_main_power.py` | Main power table for the planned within design (about 3–4 minutes) |
| `power_analysis/run_design_comparison.py` | Within vs. between design comparison (longer, about 10 minutes) |
| `power_analysis/summarize_design_comparison.py` | Prints the key rows of the design comparison |
| `power_analysis/results/` | The saved outputs of both runs |

The random seed is fixed, so running the scripts reproduces the saved results exactly.

The experimental materials (the 80 replies and the answer key) and the code that built and checked them are not included yet. They will be added after data collection, so that future participants cannot find the answers.

## How to run

You need Python 3 with `numpy` and `scipy`.

```
pip install -r requirements.txt
cd power_analysis
python run_main_power.py
python summarize_design_comparison.py
```

## Assumptions

- Two blocks of 40 items, 25% errors
- Baseline d′ = 1.67 (SD between participants 0.50), baseline criterion c = 0.45 (SD 0.30)
- Accountability raises d′ by 0.20 and lowers c by 0.10; people differ in this effect (SD 0.20)
- Prosocial message effect on d′: 0.15 or 0.25
- Self-benefit effect as a share of the prosocial effect (r): 0 or 0.5
- Substitution (s): in the accountable block the message effect is reduced by half (s = 0.5) or fully (s = 1)

## Main results at the planned sample (N = 1,500, 500 per message condition, r = 0)

| Message effect | Substitution | H1 | H2 | H3 |
|---|---|---|---|---|
| 0.15 | half | .81 | 1.00 | .28 |
| 0.15 | full | .46 | 1.00 | .83 |
| 0.25 | half | 1.00 | 1.00 | .72 |
| 0.25 | full | .87 | 1.00 | 1.00 |

H1 = prosocial vs. neutral (averaged over blocks); H2 = accountability; H3 = the interaction (prosocial vs. neutral). The full table, including r = 0.5 and other sample sizes, is in `power_analysis/results/main_power.txt` (columns `P-N`, `Acc` and `IntPN`).

## Within vs. between participants

At the same total sample size (N = 1,800) and 60 items per participant, power for the interaction (H3) was about twice as high in the within design:

| Message effect | Substitution | Within | Between |
|---|---|---|---|
| 0.15 | half | .33 | .16 |
| 0.15 | full | .85 | .48 |
| 0.25 | half | .70 | .38 |
| 0.25 | full | 1.00 | .90 |

## Limitations

- The tests here use d′ computed for each participant and block. After review, the primary analysis in the proposal was changed to a trial-level probit model with random effects for participants and items. The simulations will be run again for that model, with item differences and expected attrition, before preregistration.
- All effect sizes are assumptions, not estimates from data.
