# W25 — the X_3 core (UNAUDITED, 2026-08-15/17)

Pinned HEAD: see `PINNED_HEAD.txt` (3f91310a). Nothing outside this directory
was modified; nothing was committed by this probe.

Start at **`REPORT.md`**.

## NAMED CAMPAIGN OBJECT PRODUCED HERE

**`OBJECT_W25-F8_n8_allblocked_X3.json` — "W25-F8", the X_3 falsifier at N=8.**

An exact rational 8-site 3-colour source that

* satisfies **every** word of off-count ≤ 3 (all 1731 three-near-constant
  words: the three pures are exactly 1, every mixed one is exactly 0) — so it
  is a genuine point of X_3 at N=8; and
* has **every one of its 21 live pairs BLOCKED** — no admissible cap kills the
  pair error at any of them.

It therefore **refutes the N=8 analogue of "X_3 ⇒ witness"**. The first word it
fails is `(0,0,0,0,1,1,1,1)` — a (4,4)-balanced word, off-count 4 — so it sits
exactly one rung below the N=8 U-core candidate X_4.

Verification standard met (details in the file and in `REPORT.md` §T3):
X_3 membership re-derived from the raw word definition by an independent
hafnian engine; all 21 pairs decided by **three** independent routes (W25's
W22-M closed form, W23's subset-sum decider, and a Singular *saturation* route
instead of Rabinowitsch) with 0 disagreements, over Q and mod 32003 / 1000003 /
1000033; a 1244-cap explicit search over Q and Z[ω] finding nothing while the
same search fires 11 times on a positive control; mutation control fires.

**Future probes must calibrate any N-uniform witness-forcing claim at rung ≤ 3
against this object.**

## Files

| file | content |
|---|---|
| `w25_core.py` | independent core: bitmask-DP hafnians, the ladder, L1/L2/**L3**, cap error via the **W22-M closed form**, exact Q and Q(ω) arithmetic |
| `w25_walk.py` | exact site-linear projection/walk on X_k |
| `w25_decide.py` | independent witness decider (Singular + Rabinowitsch, Q and Q(ω), three primes) |
| `run_t1a_identities.py` | the L3 identity, the diagonal parity theorem, Δ³_N ⊂ X_3, control battery |
| `run_t1d_diagonal.py` | exhaustive N=6 diagonal-skeleton enumeration (1,646,850 → 24 classes) |
| `run_t1e_diagonal_uniform.py` | symbolic uniform-cap proofs per class + point sampling |
| `run_t1c_x2locus.py` | the all-blocked X_2 locus in closed form, and how X_3 meets it |
| `run_t1b_builder.py`, `run_t1f_builder2.py` | the adversarial builders at N=6 (857 X_3 objects) |
| `run_t2_u2.py` | the W23-U2 extension: obstruction table, W25-U3, the (5,5,5) class |
| `run_t3_n8.py`, `run_t3b_escalation.py`, `run_t3c_n8_rungs.py` | the N=8 ladder, the falsifier, and its verification |
