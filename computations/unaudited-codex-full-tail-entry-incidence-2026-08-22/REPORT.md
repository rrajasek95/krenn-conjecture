# Full-tail entry and fixed-carrier incidence

Status: **UNAUDITED exact structural PASS, WITH A LOAD-BEARING CORRECTION**.
Carrier-to-tail entry is forced by the certified block-diagonal theorem, and
the possible normalized `X5` fibre is entirely remote.  However, the proposed
four fixed-**star** branches are tautological on normalized `X5`: the universal
five-set annihilator proves that every star carrier already has a diagonal
blocker.  The star-branch target below is retained only as a corrected audit
trail; it is not a remaining bridge problem.  See the
[source replay](../unaudited-codex-star-tautology-triangle-replacement-2026-08-22/REPORT.md).

## 1. The full 168-cell tail ideal is the unit ideal

Let

```text
R_Z = Z[A_uv[i,j] : 0<=u<v<8, 0<=i,j<3],
I5  = (all 6,558 mixed F_w, F_0^8-1, F_1^8-1, F_2^8-1),
J   = (A_uv[i,j] : i!=j).
```

There are 252 source cells, of which 84 are colour diagonal and 168 are
cross-colour.  Modulo `J`, the equations in `I5` are exactly the normalized
block-diagonal eight-site equations.  The certified dependency
[`N8-DIAGONAL`](../../certification/SUPERSESSIONS.md) says that those equations
have no solution over **any field, in any characteristic**.  Therefore

```text
                         I5 + J = R_Z.                 (1)
```

Indeed, if `I5+J` were proper, a maximal ideal containing it would give a
solution over its residue field, contradicting `N8-DIAGONAL`.  Thus (1) is
ordinary integral ideal membership, not merely a complex radical statement.
Equivalently, for fixed, finite integral polynomials (whose compact expanded
multipliers are not exported here),

```text
1 = sum_w P_w F_w + sum_c Q_c(F_c^8-1) + sum_e V_e T_e.   (2)
```

In `A=R_Z/I5`, (1) says

```text
                              J A = A.                 (3)
```

Consequently every normalized `X5` point has at least one nonzero
cross-colour source cell.  This is the smallest exact carrier-to-tail entry
statement: it uses all 168 literal tail labels and no selected 12-column
quotient, cofactor open, valuation, support degeneration, or Nakayama step.

There is an important direction correction.  Since `A/J A=0`, the zero-tail
factor is empty; every hypothetical exact point is on the remote locus.  A
global lift proving `J A=0` would combine with (3) to prove `A=0`, i.e. it
would already be the full conjecture rather than an intermediate tail lemma.

## 2. The literal full-168 `6+1+1` packet

The finite checker independently freezes the source labels behind the usual
cofactor relation.  For an edge `u<v`, ordered distinct endpoint colours
`i,j`, and the third colour `k`, put

```text
T_e = A_uv[i,j],
h_e = Haf(G_k on V\{u,v}),
w_e(u)=i, w_e(v)=j, and w_e(a)=k otherwise.
```

Direct enumeration of the 105 perfect matchings gives the literal identity

```text
F_w_e = h_e T_e + Q_e,              Q_e in J^2.       (4)
```

There are exactly 168 rows (one per cross cell).  Each `h_e` contains the 15
perfect matchings of the remaining six sites, while `Q_e` contains 90 terms:
one cross edge from `u` to a majority-colour site, one cross edge from `v` to
a different majority-colour site, and a diagonal matching on the remaining
four sites.  The 168 diagonal coefficients are 84 distinct cofactors, each
repeated for the two orders of the singleton colours.

Thus on the genuine full-source principal open

```text
D168 = product_(u<v,k) Haf(G_k[V\{u,v}]) != 0,
```

all 168 rows (4) give

```text
                    J A[D168^-1] = J^2 A[D168^-1].    (5)
```

This is the correct full-168 idempotent relation on the cofactor open.  It is
stronger in scope than repeating the fixed-pair `380 x 12` Nakayama argument,
but it is not a contradiction: by (3), `J` is already the unit ideal on any
hypothetical exact fibre.  The cofactor complement is irrelevant for
**entry**, although it would still matter to an attempted equation-by-equation
elimination.

The canonical row is

```text
e = A_06[0,1],   w_e = 02222212,
F_02222212 = h^2_06 A_06[0,1] + Q_06,
```

with 15 linear cofactor terms and 90 quadratic terms, agreeing with the
frozen remote-core provenance.

## 3. Fixed-entry/four-star-blocker reduction—and why it is tautological

The 168 cross cells form one orbit under `S8 x S3`.  Hence at any hypothetical
normalized `X5` point, (3) and site/colour symmetry allow the choice

```text
                         y0=A_06[0,1] != 0.            (6)
```

Choose the literal matched star carrier

```text
C0 = (cap pair {6,7}, residual star centre 0).
```

Its outside-response matrix `L_C0` has 90 rows and nine columns.  If all 728
star/triangle carriers are blocked, then in particular one of the following
four exact memberships holds:

```text
K00 in rowspan(L_C0),
K11 in rowspan(L_C0),
K22 in rowspan(L_C0),
<K,A_67> in rowspan(L_C0).                            (7)
```

Set-theoretically this yields a finite source-level cover by four branches.
A rank split is unnecessary: introduce 90 row-span witness coefficients
`c_r`, one inverse `s`, and impose

```text
s*y0-1 = 0,
ell_beta = sum_(r=1)^90 c_r (L_C0)_r                 (8)
```

in all nine coordinates, for one of the four blockers `beta`.  Each exact
branch has

```text
252 source variables + 90 witness variables + 1 inverse = 343 variables,
6,558 mixed + 3 pure + 9 membership + 1 inverse       = 6,571 equations.
```

Over the complex numbers, (6)--(8) are equivalent to the relevant localized
row-span branch.  No carrier-rank minor or response cofactor is inverted.
The reduction is source-labelled and same-point: symmetry changes only the
representative, and the matched carrier is one of the original 728.

But exact `X5` makes this cover automatic.  Put

```text
W={1,2,3,4,5}, C={0,6,7}.
```

The universal five-set theorem supplies `beta` annihilating every internal
one-hole cofactor of `W`, with
`b=delta_W(beta)!=0`.  It kills the one-crossing sector.  The endpoint-ordered
three-crossing sector factors through the ten response edges `R_ab(K)` with
`a,b in W`; these are exactly the ten rows killed by
`K in ker L_C0`.  Contracting exact GHZ therefore gives

```text
                         b_c K_cc=0 for every c.         (9)
```

Choose `c` with `b_c!=0`.  Then `K_cc=0` on `ker L_C0`, equivalently
`Kcc in rowspan L_C0`.  Thus one of the first three memberships in (7) holds
at **every** normalized `X5` point, independently of (6).

The former residual statement

```text
normalized X5 + all 728 blocked
  => after S8 x S3, one of the four ideals (I5, s*y0-1, (8)) has a point.
                                                              (10)
```

is true but supplies no constraint beyond normalized `X5`.  The four
343-variable ideals and the earlier 355-variable/405-equation star core are
retired as bridge targets.  Star carriers cannot be active on the exact
fibre; they remain useful only on truncated controls such as W40.

## 4. What this settles and what remains

Settled exactly:

1. **Carrier-to-tail entry.** A normalized `X5` point cannot have zero full
   tail; (1) is a fixed full-168 ideal relation.
2. **The direction of the tail lift.** There is no nonempty zero-tail factor
   to reach.  The remote factor is the entire possible exact fibre.
3. **Star-carrier retirement.** All 168 star carriers are automatically
   blocked by a diagonal membership on normalized `X5`; the non-tautological
   linear carrier cover has only the 560 triangles.
4. **Full cofactor-open relation.** The 168 literal `6+1+1` rows give (5)
   directly, without the associated-graded `3+3+2` matrix.

Not settled:

- triangle-carrier blocker branches are not proved empty; unlike a star
  kernel, a triangle kernel retains the response edge opposite the chosen
  cut vertex;
- no compact expanded multiplier list for (2) is extracted from the certified
  diagonal proof; its existence is nevertheless an exact consequence of the
  any-field theorem;
- the result does not manufacture an active cap.  Full-tail entry is solved,
  but the star incidence target is redundant.

Accordingly, both a “well-founded tail order to zero” and the fixed-star
four-branch solve are superseded.  The smallest non-tautological linear
replacement is the triangle identity frozen in the correction report; the
first cancellation-clean nonlinear replacement is a four-residual-site
response carrier with a quadratic Hafnian-zero condition.

## 5. Replay and artifacts

The checker enumerates all source labels and matching terms, verifies the
168-cell and 168-star orbits, and freezes the exact branch counts.  It does
not re-run the certified diagonal proof or a Groebner basis.

```text
python3 computations/unaudited-codex-full-tail-entry-incidence-2026-08-22/audit_full_tail_entry_incidence.py --write-results
python3 -O computations/unaudited-codex-full-tail-entry-incidence-2026-08-22/audit_full_tail_entry_incidence.py
python3 -I -S computations/unaudited-codex-full-tail-entry-incidence-2026-08-22/audit_full_tail_entry_incidence.py
```

All three modes are byte-identical.  Logical SHA-256:

```text
01118176d463e889c59eba81a77e27cc5710c1acd376596b57a083ff65556f01
```

Artifacts:

- [`audit_full_tail_entry_incidence.py`](audit_full_tail_entry_incidence.py)
- [`results_full_tail_entry_incidence.json`](results_full_tail_entry_incidence.json)
- [certified diagonal proof](../../proofs/eight-site-diagonal-obstruction.md)
- [response carrier theorem](../unaudited-codex-response-star-2026-08-20/REPORT.md)
- [tail source provenance](../unaudited-codex-tail-polar-source-lift-2026-08-21/REPORT.md)
