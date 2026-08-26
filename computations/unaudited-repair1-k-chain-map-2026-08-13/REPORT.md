# UNAUDITED REPAIR PROBE — repair item 1: the K chain map (2026-08-13)

**Pinned HEAD `7d57c552a3ef57d3a95c3bc933af547ad55e087d`; all four constructors
byte-identical at de74a1a mid-run. Exact arithmetic over Q; the two large
rank computations run at two primes (1000003/999983) with identical output.
Scripts + JSON + logs in this directory; common.py header explains re-runs.
UNAUDITED external probe — not spine material.**

## Verdict (three parts)

1. **The single-class comparison EXISTS and is verified cross-module.**
   The keystone identity that the secondary-transfer checker prints OPEN
   and the descent checker never touches — `shadow_2(K_phys) = D2(operator
   solution)` — is TRUE: 16 terms, values ±1, both sides computed in one
   process. Crucially, alpha=(−1,+1,+1,−1) was DERIVED (by acting with the
   descent checker's own involutions on the physical monomial E+T0), not
   typed in. This replaces "three files agree because the same literal was
   typed into each" with a genuine two-module verification.
2. **K is UNDER-DETERMINED: exactly 7 dimensions of freedom** after
   imposing EVERY committed readout jointly (342 rows; 13 dims in the
   orbit inventory). Certificate: 7 integral s-odd w-odd basis vectors
   with zero shadow, zero corners, zero aggregates; the smallest is a
   12-term ±1 chain supported on matchings where tail sites 2,5 are
   matched to each other. Adding it gives a 16-term physical chain K′ with
   an IDENTICAL compared signature. Nothing committed distinguishes K′
   from K_phys.
3. **A chain map on the whole constrained operator module is OBSTRUCTED
   in the direct-free presentation: 153-dimensional separator family.**
   dim S = 488 where S = D2(ker(source,D1)); the source/D1 conditions cut
   NOTHING from achievable D2 values (dim S = rank(pi_shadow M) exactly —
   sharpening audit defect 2). S projects with rank 153 onto pair
   coordinates that are NOT two disjoint cells of a direct-free matching;
   physical chains vanish there identically. CONSTRUCTIVE GUIDANCE: an
   honest target module must contain site-repeating terms. Also: the
   operator's fine-shift split of D2 (39+24) does NOT match K_phys's
   word-grade split (10+10) — the equality holds only after forgetting
   the grade; grade-refining the comparison fails outright.

## Reconstruction facts

Operator rebuilt (not replayed): 8,580 columns, exact row rank 1328,
343-term solution, source output 0, D1 output 0, D2 support 16 =
expected shadow; 540 source-row incidences (cancellation real).
Membership feasible in every physical inventory (two-row: fibre dim 21;
4-word orbit: 110; all 3^8 rows: ≥574,695). Readout ranks on the freedom:
s-odd 7, endpoint-even 7, w-odd 9, corners 4, augmentations/fine-degree/
codim-one shadow ALL 0; jointly 14 → residual 7.

## What would pin K

Only readouts injective on a fixed word row pin it (triple-cell shadow,
uncoloured matching, literal full-nine boundary — each rank 9/9 on the
grade-refined freedom 9; single-cell shadow 0/9). I.e. no coarser
committed readout pins K; pinning requires (i) constructing H_w termwise
on the physical presentation — the root cause, never constructed anywhere
— or (ii) defining the private full-nine boundary rows in the corners'
grade (they exist only for the 48-column EqSystem block whose words are
coloured {0, MIXED}; the pure/mixed corner words are not in it — exactly
the family M_v assumes K kills, undefined where K lives).

## Mutation controls

Four alpha mutations fail cross-module equality; 9 membership negative
controls all infeasible with explicit separators (support 7–13); wrong
shadow degree fails; perturbed chain fails. NOTES: exactly 2 of 28
transpositions reproduce K_phys (0↔1 AND 6↔7 — involution pinned to a
two-element set, not uniquely); dropping the Weyl sign leaves K_phys
unchanged (both tail sites coloured 1 at this corner — the committed data
cannot detect the sign convention there).

## Not reconstructible (exact list)

(1) the five abstract cap rows and r0/T/rho/C as physical functionals on
chains; (2) private_corner rows in the corners' grade; (3) eta/sigma
ridge (strings only); (4) the "canonical faces-(3,5) bridge" as a module
(used graded span of committed rows + orbit — the strongest reading);
(5) H_w termwise (root cause).

## Meaning for repair item 1

M_v's K-half cannot be promoted on present evidence. Either demote it to
conjecture, or do the construction the obstruction names: build H_w
termwise in a target module admitting site-repeating terms, and define
the private rows in the corners' grade. The verified single-class
comparison and the 153-dim separator are both usable spine inputs after
repo re-audit.
