# The three cyclic five-set identities have no response-edge holonomy

Status: **UNAUDITED exact negative theorem and literal response guard**.

## Verdict

For the canonical cap pair `67` and residual triangle `012`, the three
five-set identities retain respectively `R_12`, `R_02`, and `R_01`.  Their
six matching terms occupy 18 pairwise distinct physical perfect matchings.
At coefficient level, each response has 162 endpoint-labelled terms
(`9` output cells times `9` cap covector cells times two crossed summands),
and the three supports are disjoint.  Thus there is no source-universal
linear/Bianchi identity that cancels the three residual packets.

The positive theorem is exactly the already identified determinantal open:
if the appropriate five-set quotient map has rank nine, every coordinate of
that `R_xy` lies in `rowspan L_T`, and the one cyclic augmented identity
already puts its selected diagonal blocker in `rowspan L_T`.  The three
edges are absorbed separately; cyclic holonomy adds nothing.

## Exact counterguard to the hoped-for dichotomy

There is also a literal response-star guard showing that the three augmented
rowspan statements alone imply neither the upgrade nor an active cap.  Put

```
A_60=I, A_70=0, A_61=0, A_71=I, A_62=I, A_72=I,
A_63=E00, A_74=E00, A_67=I,
```

with all other cap-star blocks zero.  Exact row reduction gives

```
rank L_T = 5,
K_00 in rowspan L_T,
K_11,K_22,<K,A_67> not in rowspan L_T.
```

The internal triangle responses are

```
R_01(K)=K,  R_02(K)=K,  R_12(K)=transpose(K).
```

Consequently the same blocker `K_11` lies in each
`rowspan[L_T;R_e]` (it is literally output row `11`) but not in
`rowspan L_T`.  Nevertheless the carrier is blocked, not active, because
`K_00` already lies in `rowspan L_T`.  This guard is a literal realization
of the response matrices; the three `Theta` maps are the named diagonal
projections with defect vector `b=e_1`.  It is not asserted to realize the
three internal cofactor annihilators simultaneously or to satisfy normalized
full `X5`.  Its exact role is to falsify any conclusion based only on the
three augmented linear memberships.

## What a valid continuation must add

The universal theorem chooses each five-set annihilator independently and
provides no comparison map between their defect spaces.  A source-faithful
cycle theorem would therefore need a genuinely new overlap relation among
the internal cofactor tensors and the three annihilators.  The literal term
audit shows that such a relation is not a matching-sector boundary.

The surviving split is:

1. on the simultaneous rank-nine open, absorb the three responses one by
   one and use the existing pure quotient identity;
2. on rank drop, use the full cross-word/Cramer equations or prove a
   good-pair/active-cap descent.

The known three-word cofactor determinant is a different holonomy: it acts
on the 27 internal triangle cells and leaves the direct/opposite-edge packet
as its explicit remainder.  It cannot be relabelled as a cycle identity
among `R_01,R_02,R_12`.

Replay:

```
python3 computations/unaudited-codex-triangle-cyclic-five-set-holonomy-2026-08-23/audit_triangle_cyclic_five_set_holonomy.py --check-results
python3 -O computations/unaudited-codex-triangle-cyclic-five-set-holonomy-2026-08-23/audit_triangle_cyclic_five_set_holonomy.py --check-results
python3 -I -S computations/unaudited-codex-triangle-cyclic-five-set-holonomy-2026-08-23/audit_triangle_cyclic_five_set_holonomy.py --check-results
```

The hostile `--mutate-crossed-orientation` mode must fail.
