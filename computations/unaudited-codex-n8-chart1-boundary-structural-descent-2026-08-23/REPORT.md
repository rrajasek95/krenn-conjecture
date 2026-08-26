# Chart 1, `A_02[0,0]=0`: structural descent audit

Date: 2026-08-23  
Status: `EXACT_NATURAL_DESCENTS_NOT_FORCED_BRANCH_REMAINS_OPEN`

## Scope

This is a bounded source audit of the first C4-atlas boundary: chart 1 has

```text
A_01[c,c] = A_23[c,c] = A_45[c,c] = A_67[c,c] = 1  (c=0,1,2),
A_02[0,0] = 0.
```

It tests whether that antecedent alone supplies an active clean triangle cap, a matching-hole/block decomposition, or a literal six-site system covered by `SP-K6`.  It does not solve the 239-variable boundary.  In particular, the dense guard below is deliberately not an X5 point; it refutes implications from the chart support/rank antecedent only.

## Exact row cut

Among the 6,558 literal mixed eight-site rows, precisely the 728 words with endpoint colours `w_0=w_2=0` lose the 15 matchings containing edge `02`.  Hence their term count is 90, while the other 5,830 rows retain all 105 terms.  There are 78 normalized constant mixed rows.

Fix the endpoint pair `67`.  For every six-site word `u` and endpoint colour `c`, Laplace expansion gives the literal identity

```text
F_(u,c,c) = H6_boundary(u) + C_67(u,c),
```

because `A_67[c,c]=1`.  Here `H6_boundary` is the common-tail, six-site hafnian and `C_67` is the sum of matchings in which sites 6 and 7 cross into the residual six sites.  If `u_0=u_2=0`, the two packets have 12 and 78 terms; otherwise they have 15 and 90.  Thus the mixed X5 equations yield

```text
H6_boundary(u) = -C_67(u,c),
```

not the six-site GHZ equations required by `SP-K6`.  The crossing packet is genuinely present: in row `00000011`, matching `06|17|23|45` contributes

```text
A_06[0,1] A_17[0,1] A_23[0,0] A_45[0,0]
  = A_06[0,1] A_17[0,1]
```

on chart 1.

## Exact counterguards to the three natural descents

1. **Triangle clean cap is not forced by the boundary.**  Set every non-anchor, non-boundary cell to the deterministic positive integer in the replay script.  This gives exactly 251 live cells.  All 28 physical `3x3` edge blocks have nonzero integer determinant.  Every one of the 560 literal triangle response matrices has rank 9 modulo both 1009 and 1013, hence rank 9 over `Q`.  Consequently each of its four blocker forms lies in its row span.  This refutes `A_02[0,0]=0 => active triangle carrier`; it does not classify wider cancellation-clean caps.

2. **Matching hole/block is not forced.**  The same guard has only one zero cell and all 28 edge blocks full rank.  The archived matching-hole theorem requires a complete hole matching plus the corresponding zero-cross mask.  Neither follows from this boundary.

3. **Literal N6 descent is not forced.**  The displayed Laplace identity retains 78 or 90 crossing terms.  `SP-K6` requires one common endpoint-ordered six-site source array carrying all 729 target coefficients; no coefficient cut supplied by the lone zero cancels the three endpoint-colour crossing packets.

## Full-X5 finite-interface control

The archived exact D12 root has 250 rows, 18 columns, rank 18.  Its five-row dual is killed by 130 literal next-column orbits, so it gives neither membership nor nonmembership.  At round 6 the induced dual is the singleton row `0d55b8ee`, decoded as

```text
A_02[1,1] A_14[1,1] A_36[1,1] A_57[1,1],
```

and 42 literal columns kill it.  This selects the live colour-one `02` cell, not the vanished colour-zero cell.  Moreover, multiplying by the pure matching is a cone: it does not project away the 90 edge-avoiding matchings.  The checkpoint is therefore consistent with, but does not repair, the crossing-tail obstruction.

## Remaining exact target

Closure of this branch still needs a source-labelled combination of full X5 rows which, for one physical endpoint pair and all three endpoint colours, cancels every crossing correction `C_pq(u,c)` or identifies it with the response of one active clean cap.  Without that same-source cancellation, neither clean-pair descent, matching-hole descent, nor `SP-K6` applies.

## Replay

```bash
python3 computations/unaudited-codex-n8-chart1-boundary-structural-descent-2026-08-23/audit_chart1_boundary_structural_descent.py --check-results
python3 -O computations/unaudited-codex-n8-chart1-boundary-structural-descent-2026-08-23/audit_chart1_boundary_structural_descent.py --check-results
python3 -I -S computations/unaudited-codex-n8-chart1-boundary-structural-descent-2026-08-23/audit_chart1_boundary_structural_descent.py --check-results
```

The hostile `--mutate` mode changes the exact row census and must fail.

