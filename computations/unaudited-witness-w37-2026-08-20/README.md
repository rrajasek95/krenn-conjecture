# W37 — witness existence at N=8 (UNAUDITED, 2026-08-20)

**UNAUDITED probe lane.** Pinned HEAD in `PINNED_HEAD.txt` (`9b7accb`).
Nothing outside this directory was modified; nothing was committed.
Exact arithmetic only (`Fraction` / Singular over Q). Two-family
verification: this lane's from-scratch engine against W25's.

Start at **`THEOREM-W37-PER.md`** (the lane's theorem). The probe's
findings were reported to the manager in the agent's final message, per
lane policy; the machine-readable record is the `results_*.json` files.

| file | content |
|---|---|
| `w37_core.py` | from-scratch engine: hafnians, off-count/`X_k`, cap error by the DEFINITION and by the W22-M closed form, symbolic cap system in the nine cap unknowns |
| `w37_decide.py` | exact WITNESS/BLOCKED decider (Singular, `s = 1` slice + Rabinowitsch on `k00 k11 k22`), structured cap battery, ledger 6/11/13/19/22/23 guards |
| `run_a0_controls.py` | pre-launch control battery, manifest 7/7 |
| `run_a1_falsifier.py` | F8 defect census + the counterfactual cap systems |
| `run_a2_counterfactual.py` | exact decisions of `E0` / `E_X4` / `E_X5` / `E_o5` at all 21 live pairs |
| `run_a3_degeneration.py` | the 16-element nondegeneracy lattice at every pair |
| `run_b1_n6theorem.py`, `run_b2_permanent.py` | the permanent-collapse identity, cross-family checks, negative controls |
| `run_c1_builder.py`, `run_c2_local.py` | site-linear builder; F8's local `X_3` geometry |
| `run_c3_correlation.py` | defect-count vs witness-count over F8's component |
| `run_c4_resist.py` | which off-count-4 equations resist a single-site move |
