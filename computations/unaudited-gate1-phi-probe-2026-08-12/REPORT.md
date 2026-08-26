# UNAUDITED PROBE — Gate I output-side membership (2026-08-12)

**Status: UNAUDITED. Do not cite on the spine without independent re-audit.
Not written by the main proof lanes; produced by an external probe agent
pinned to HEAD `ed51e476d03495eae1e24a37a2d680546771290b` ("Compress the
endgame to two source gates"). All arithmetic exact rationals; one mod-p
rank certificate (p = 2^61−1) used only as a lower bound on rational rank.**

Scripts: `probe_taskB.py` (reconstruction), `probe_taskCDE.py`
(membership/coherence/mutations), `taskCDE.json` (frozen results).

## Headline (Task C)

In a common 32-row signature model ({private, Eq, W, target, R, D} × 4
corners, ainc, eta1..5_constant, eta1_U1, sigma_qpq22), with every
checker-constructible column family embedded (mapping-cone 20 columns, KS
transport graph, clean-separator repeated inventory both faithful and
per-corner-generous, endpoint-odd Cartan prism K=(1−s)H_w, plus an "ULTRA"
closure of free unit columns on every non-private non-terminal row):

1. **The residue/private/Eq part of J(M_v) is ALREADY a boundary of
   committed material.** Verified row-by-row on all 32 rows:

   ```
   J(M_v)|physical = Σ_j (−α_j)·(−r0_j + T_j + ρ_j) + K
                   = −(old cap aggregate) + (endpoint-odd Cartan prism)
   ```

   integer coefficients (−1,+1,+1,−1) per corner and +1 on K, giving
   private_c = α_c, Eq_c = α_c, W = target = R = D = ainc = 0.

2. **The note's primitive separator (private − W − target + R) is NOT
   robust**: it pairs +1 with the KS corner column D_w + R_w. The
   D-repaired separator dies once the Cartan prism is admitted (the
   endpoint-odd survivor at the faithful level disappears at INV3f).

3. **What persists is purely terminal.** For every legitimate inventory up
   to ULTRA, the left-null space is exactly 7-dimensional, supported on
   {eta1..5_constant, eta1_U1, sigma_qpq22}; the normalized separator
   L = eta1_constant reads 1 on J(M_v), 0 on every committed column.
   J(M_v) is NOT in the span of any legitimate inventory.

**Consequence: Gate I's output-side membership is exactly a terminal-packet
realizability question** — construct a source-provenant cell carrying
eta_z = 1 + δ_(1,z)·u_z/t and sigma = −q_pq^22 with zero D/W/target/ainc.
The residue/private lane is closed by committed material once the prism is
admitted. (Caveat: the terminal separator is coarse — insensitive to the
endpoint-odd signature α; it detects only that no committed column carries
a terminal value.)

## Reconstruction (Task B) — all note claims confirmed

- F: k^18 → k^15 has rank 15; ker = exactly the span of the three chart
  differences; shared labels (3,(0,2)), (4,(0,2)), (5,(0,2)).
- u support 12 (zeros exactly at shared labels), J_col(u) = −v,
  v = P_024 − P_012, occurrence support 8.
- All five repeated components: 288 one-chart columns rank 288 (mod-p
  certificate + private-feature count ≥42 per column — every column, not
  only pure r0); doubled 576 columns rank 288, kernel = pairwise pq−pr
  presentation differences exactly.
- Old inventory (20 cols) rank 16; +J(M_v) → 17;
  old_cap_aggregate + J(M_v) = desired_full.

## Coherence (Task D)

The two cut copies disagree on every overlap label (defect +2 each; sums
cancel — hence 12 not 15 nonzeros in u). Coherence has codimension exactly
3 = pullbacks from the 15-label quotient. NOTE: no committed checker
exposes a cutwise candidate filler, so the three equations could not be
evaluated on a real Φ candidate. (Superseded input-side: 74a44f9's
ρ=(1 4)-equivariance reduction makes the coherences automatic for
equivariant comparisons — this probe predates that commit.)

## Checker reproduction (Task A)

All three cited checkers pass in plain/-O/-I -S; frozen ledgers match
(fb3b3d40…, 7bf941df…, 75ae40a7…).

## Mutation controls (Task E)

10 mutation families; all substantive checks fail under fabricated
geometry (M1, M2b, M3/M3b, M4, M6, M8, M10). Two null mutations identified
with a real ledger observation: **J_col(u) = −v is strictly coarser than
the 15-label structure** — swaps of equal-coefficient labels and
within-matching-fibre swaps ((1,(0,1))↔(1,(2,4)), (9,(0,4))↔(9,(1,2))) are
invisible to the identity and to the tangent-lower ledger (counts/booleans
only). A future coherence checker should hash the labelled chain itself.

## Honest limits

1. The probe ran in the checkers' abstract corner model extended with D
   rows — NOT directly against the 576 literal columns, whose augmented
   signature values no checker exposes. A literal column with a nonzero
   terminal readout would escape the ULTRA closure; nothing in committed
   code rules that out.
2. The Cartan prism's private readouts are open (its source descent is the
   open obligation); the probe set them to zero — the choice most
   favourable to membership. Nonzero descended private values would
   require re-deriving the physical-part membership.
