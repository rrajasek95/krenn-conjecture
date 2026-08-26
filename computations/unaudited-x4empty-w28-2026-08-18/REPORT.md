# W28 — the X_4-emptiness attacks — REPORT (UNAUDITED, 2026-08-18/19)

Pinned HEAD 7059a63. All-exact (Fraction / own Q(omega) class /
sparse polys over Q / Singular char 0; mod-p screens at two 1-mod-3
primes). Independent engines cross-checked vs W25/W27. 33
checkpoints + results_SUMMARY.json. Agent's write was policy-
blocked; this transcribes its report.

## THE THEOREM (the symmetric case of X_4-emptiness)
**W28-T1 [PROVED-HERE]: no sigma-symmetric diagonal background on
K_7 (sigma = (012)(345)(6) with colour rotation; 21 complex weight
parameters) admits a feasible X_4 site system at N=8** — all 127
free-set cases are the unit ideal in char 0 and char 32003. The
slice is PROVEN informative (exhaustive 16,384-pattern grid: 2,124
backgrounds reach X_3 with all three colours; 0 reach X_4; plus
86,688 exact weightings on the informative patterns: 0). Pipeline
calibrated (returns not-unit at k=3, dim 10 — as it must). Enabled
by three new lemmas: W28-SYM (averaging: transitive site symmetry
with trivial colour action => invariant solutions, 21 -> 3
unknowns), W28-DEC (diagonal decoupling: odd-part parity splits the
system into colour blocks, 21 -> 7), W28-FREE (the free-site case
split: feasibility forces a nonempty free set; 127 small ideals).
SOUNDNESS CATCH mid-run: sigma carries colour-0 systems to
colour-1, so orbit reduction would have been UNSOUND — all 127 run
individually (the earlier 47-rep run superseded).

## The route hygiene result
The F_21 slice (maximal symmetry, 9 parameters) is proved
infeasible at k = 2, 3, 4 — and thereby RETIRED as information-free
(empty already at X_2; a slice's X_4 emptiness is evidence only if
it carries X_3). Ledger-18 applied at attack scale.

## The diagonal case: reduced to ONE computation
- W28-DEL [proved] closes W27-D3's gap (monotone deletion => the
  disjoint-PM enumeration is complete for the no-cancellation
  stratum); census reproduced independently (32,970/16,800/8,610/0).
- W28-LAM [proved]: the diagonal X_4 problem = the Waring-type
  hafnian identity Haf(sum lambda_c t^c) = sum lambda_c^4
  (discriminates correctly: Delta^3_8 gives 7 not 3).
- W28-GOOD [proved]: three pairwise-disjoint spanning good classes
  forced.
- CANCELLATION STRATUM: exhaustive over ~745 MILLION skeleton
  triples (seven complete size profiles, PM + <= 2 extra edges,
  disjoint supports): 0 survivors. Builders: 75,000 calibrated
  starts over Q and Q(omega) (thousands land X_2/X_3; ZERO X_4).
  Census: 330,000 exact diagonal backgrounds: 0 with three colours
  at X_4 (max ever = 2).
- HONEST LIMIT (explicit ledger-18 point): the SINGLE-colour
  statement is FALSE on the unrestricted diagonal family (t^1 =
  t^2 = 0 gives colour-0 feasible at k=4) — the sigma theorem is
  genuinely slice-specific; closing the FULL diagonal family needs
  the THREE-colour free-site ideal (T1h: 96 generators, 66
  variables; timed out at 900 s char 32003). **If T1h terminates,
  "no diagonal exact source at N=8" becomes a THEOREM including
  cancellation — the classical edge-coloured Krenn–Gu statement at
  N=8.** Named tactics: better ordering, modStd, case split on
  trivially-vanishing free-site conditions.

## T3 — the N=8 skeleton invariant
95.8% local (4 clashing feature cells hold 16 of 377 pairs); new
best rule: npm_drop = 0 AND off_deg_pair = [2,2] => WITNESS (198
exact; npm_drop = matchings destroyed by the pair deletion is a new
feature); 22 width-<=2 rules classify 373/377.

## Controls
Full ledger battery (6/11/13/14/18/19/20/21/22 all exercised with
firing negatives); F8 and the calibration table reproduced ((8,4)
wears the (6,4) signature, 25/25 vs 0/25); W27-D3/R2 verified
independently. Soft spots: the non-diagonal sigma slice is search
silence (18,000 backgrounds); cancellation exhaustion bounded at
PM+2 disjoint supports (overlapping supports = builder + census
only); X_4 = empty overall remains CONJECTURED; T3 is a rule search
on a 377-pair sample; two non-terminating elimination formulations
superseded (logs retained, non-verdicts carry no information).
