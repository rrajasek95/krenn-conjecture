# Second external adversarial audit — the 2026-08-13 layer (consolidated)

**Four parallel audit agents, snapshots pinned at 1d1bc63 (± noted).
All reruns clean in 3 modes with matching digests. This report is
external and un-re-audited. Full agent transcripts in the session
scratchpad (audit2-terminal/, audit2-moment/, audit2-augp2/,
audit2-adoption/); ~40 mutation scripts + independent re-derivations
on disk. Scope: everything committed since the first campaign's
coverage (terminal chain, moment/Rodrigues layer, AugP2/E14 morning
layer, probe-adoption integrity, first-campaign follow-through).**

## One-paragraph verdict

The mathematics is sound everywhere it was tested — every headline
number across all four audits reproduced independently, several
verified further than the committed range (endpoint spectra to h=6;
Bernstein moments to s=39), zero arithmetic errors found. But the
evening's headline compression ("one census + eight scalars") does
NOT survive audit: the terminal chain's honest residue is TWO
mismatch scalars plus an uncovered chart-switch family plus an open
census hypothesis plus an unproved B=Eq tie on which everything
rests — and the scalars are not yet computable, because the
word-changing arrow that defines their domain has never been
constructed. One link of the chain (c24b09c) proves its headline by
asserting 24 hardcoded zero vectors are zero, and a later commit
(1d1bc63) used that circularly to tighten the gluing note. Prop 5.2
rests on four independent open hypotheses, not on Conjecture 6.2
alone, and its output is a refutation, not a clean pair. The psiz
probe's conclusions were adopted into spine 52 minutes after its
report with no attribution, no supersession, none of its evidence,
and its refutations dropped. Zero of the first campaign's criticized
checkers were repaired across ~300 commits (add-only culture).

## The honest endgame ledger (post-audit)

1. **The word-changing arrow** (occurrence-local Cartan/Spencer/PP
   map, word 11:110000 -> 01211222): required before ANY mismatch
   scalar has a value. The recurring source-typing kernel. NOT
   constructed; 9 named prerequisites enumerated in the AugP2 audit.
2. **The B = Eq tie** for physical response/cap rows: THE hinge of
   the terminal chain; asserted in one sentence, no checker, no
   derivation. Sensitivity probe: untie one row and the detector
   reads 0 — conclusion evaporates while the rank survives.
3. **The census hypothesis** (no other primitive cap-grade
   operation-changing generator): open, and to the lanes' credit the
   ONLY granted edge properly flagged False in a ledger field.
4. **Two scalars, not one/eight**: chi(kappa_AB), chi(kappa_AC)
   (fb45b07), which provably cannot cancel by root-forgetting; PLUS
   the (A+B)H/(A+C)H chart-switch family excluded from the gluing
   note's hypothesis (its "one hypothesis suffices" is FALSE as
   stated — 3 independent reasons; also contradicted by fb45b07 at
   the same HEAD).
5. **Win-win is a trichotomy**: the filler criterion is 1 of ~11
   filler requirements (correctly disclaimed in the notes); fb45b07
   names the third outcome (higher multi-parent generator).
6. **If the filler branch wins**: four more independent hypotheses
   (A2 class identification — the master note explicitly forbids
   the raw fold; A3 common descent; A4 k[q,r]-module structure; A11
   exceptional-class nonvanishing, with a committed countermodel
   showing it is not free) before the moment collapse (whose
   Leibniz/Rodrigues/span core IS proved) refutes the counterexample.

## Critical defects (new)

- c24b09c: db01/dL01 "conservation" = (ZERO8,)*6 and (ZERO8,)*18
  hardcoded; no term ever mapped; commit titled "Prove...". The
  1d1bc63 tightening that consumed it should be reverted/retitled.
- The section-3 "dark families" tables (121+24+24+30+6+18 columns)
  are zero-by-definition (off-grade zero-extension) presented as
  checked; rank(121 zero vectors)==0 consumed cross-file.
- B=Eq undeclared-default-argument hole (companions' Eq row has no
  constructor; 12/15 alternative configurations have NO kernel).
- Silent + selective adoption of the psiz probe (conclusions without
  evidence; refutations dropped; refuted cone dual still live and
  pinned; no supersession; propagated into 5+ artifacts).
- E14 rank-three quotient = rank(I_3)==3 on hardcoded basis vectors;
  dq-conormal "automatic" = assign-then-assert; packaging rank
  ladder = manufactured literals required cross-file.
- Descent theorem (Theorem B): complete prose proof, but checker
  verifies 3*2==6 while BASELINE says Proved; only pillar with no
  proof page and no audit. (Sketch relabelled [P-prose].)
- Frontier note: "induction complete" and "all-order coefficient
  problem completely solved" are overclaims (Pi_match not idempotent
  off 1+E1 — restriction deleted from upstream docstring; composite
  never computed); zero checker links in the note carrying the
  repo's strongest declaratives.

## Verified true (usable after formal adoption)

Rank 7/8 + kernel uniqueness; 126/127 with im=ker (granted set);
27-vector pullback (8 substantive rows); spectator scaling 8k-1/8k
symbolic-in-k with correct proof; Rodrigues triangularity, diagonal
(-1)^j (j!)^3/(2j+1)!; Hilbert-Cauchy span h=3..12 with valid uniform
proof; moment-prefix tightness; association-scheme eigenvalue +
endpoint spectra now verified h=2..6; O_alpha - K_alpha = -M_v; 446
concepts; fixed-window 100/46/2; 1/840 separation; fb45b07's 4-case
operation-parent enumeration.

## Ordered repair list

1. Retitle c24b09c; revert/rewrite the 1d1bc63 tightening; disclose
   zero-extension as definitional wherever used.
2. Construct or refute the B=Eq tie (a finite physical computation —
   the cheapest decisive item in the program).
3. Reconcile 7a41e34 (one hypothesis) with fb45b07 (two scalars +
   excluded family); fix the gluing ledger self-contradiction.
4. Record the psiz adoption: status-audit checker + SUPERSESSIONS
   entries (incl. the refuted cone dual and the target companion Y
   now being in the image); attribute per the repo's own convention.
5. Build the word-changing arrow (the actual remaining construction).
6. State and attack the census as the theorem it is.
7. First campaign's untouched list (ridge backwards-solve; ores
   formula; placement contradiction — now in 2 more checkers;
   bordered domain; six repaired checkers; six-concept pivot).
8. Evidence discipline: pins import no mathematics (560/644
   text-freshness only); require executed dependencies or content
   hashes of computed objects; ban assign-then-assert.
