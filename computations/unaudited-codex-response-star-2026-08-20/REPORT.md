# Response-star attack at `N=8`

Status: **UNAUDITED CONSTRUCTIVE WAVE-2 OUTPUT**.  Nothing here changes the
certified spine.

## Headline

The response-star mechanism is correct in raw endpoint coordinates and it
closes a meaningful structural stratum: **every point of the four-parameter
W40 level-4 family has six active clean caps `K=I_3`**.  The six
`(pair, residual centre)` choices are

```text
(12,3), (13,2), (23,1), (56,7), (57,6), (67,5).
```

The proof is support-theoretic, not a lucky specialization: every off-star
summand in every response cell is zero before addition, and the six direct
cap scalars are respectively

```text
1, b, 1, 1, -1/(abst), 1.
```

They are units on `(C*)^4`, while all three diagonal coordinates of `I_3`
are one.  Thus the requested `(67,5,I_3)` control is one of six uniform
choices.

This does **not** prove `X4-to-cap`.  It gives an exact finite residual for
the support-intersecting sector: an `X4` source evading all such caps must
satisfy 728 simultaneous four-way row-span disjunctions—168 star carriers
and a separate 560 triangle carriers.

## 1. Raw endpoint formula

Store `A_uv[i][j]` with `u<v`, with the first colour at `u`.  Fix an
**ordered** cap pair `(p,q)`, even though files use `p<q`, and give `K_ij`
the colour at `p` first and the colour at `q` second.  For residual
`a<b`, the literal coefficient of `K_ij` in response cell
`R_ab^(alpha,beta)` is

```text
A_pa[i,alpha] A_qb[j,beta]
  + A_pb[i,beta] A_qa[j,alpha].                         (1)
```

Here every displayed cell is interpreted in its requested endpoint order;
access to a stored reversed block transposes both site and colour order.
Equivalently, with `P_a=A_pa` and `Q_a=A_qa`,

```text
R_ab(K) = P_a^T K Q_b + Q_a^T K^T P_b.                 (2)
```

Swapping `p,q` and transposing `K` leaves (1) unchanged.  The audit checks
this on all 168 star and all 560 triangle matrices for each of W40 and
W25-F8.  An intentional residual-colour swap in the second summand changes
14,400 stored rows, so this control is capable of firing.

## 2. Exact response-star criterion

For a residual centre `v`, let `L_pqv(A)` have the 90 rows (1) belonging to
the ten residual edges not incident with `v`, with nine cells per edge.  Put

```text
ell_0(K)=K_00, ell_1(K)=K_11, ell_2(K)=K_22,
ell_3(K)=<K,A_pq>.
```

Then an active cap whose response support lies in the star at `v` exists
**if and only if**

```text
ell_i is not in rowspan L_pqv(A),  i=0,1,2,3.           (3)
```

Proof: in finite dimensions,

```text
ell in rowspan L  <=>  ker L is contained in ker ell.
```

If none of the four containments holds, their intersections with `ker L`
are four proper linear subspaces.  Over `C`, a vector space is not the union
of finitely many proper linear subspaces, so some `K in ker L` has all four
`ell_i(K)` nonzero.  The converse is immediate.  The implementation also
constructs such a rational `K` from an exact nullspace basis whenever (3)
passes; it does not infer existence from a rank count alone.

This formulation handles inactive pairs correctly.  If `A_pq=0`, then
`ell_3=0` is already in every row space and all six choices for that pair
fail.  W25-F8 has seven such pairs, and all 42 corresponding failures were
checked explicitly.

## 3. Why a star—or a triangle—is clean

Let the response-support graph have a residual edge when some cell of
`R_ab(K)` is nonzero.  If the graph has matching number at most one, any two
supported response edges intersect.  Consequently every term of `r^2` has
a repeated residual vertex and its squarefree degree-four component is
zero.  The same is true of `r^3`; hence at the eight-to-six boundary

```text
E_pq(K) = s [r^2/2 exp(x)]_U + [r^3/6]_U = 0.
```

The elementary classification of pairwise-intersecting edges must include
two cases.  Choose an edge `xy`.  Every other edge meets it.  If all edges
share one endpoint, the graph lies in a star.  Otherwise there are edges
`xz` and `yw`; since they must intersect, `z=w`.  Any further edge meeting
all three of `xy,xz,yz` is one of those three, so the graph lies in the
triangle on `x,y,z`.

Thus star and triangle carriers together cover exactly the
matching-number-at-most-one **support** mechanism.  Neither test subsumes
the other: a degree-four star is not contained in a triangle, while a full
triangle is not contained in a star.

For a residual triangle `T`, the analogous matrix `L_pqT` has 108 rows: all
nine cells on each of the twelve residual edges outside `T`.  The same four
row-span tests give an active cap supported on that triangle.  There are

```text
28 * 6 = 168 star choices,
28 * C(6,3) = 560 triangle choices.                    (4)
```

This is a sufficient clean-cap mechanism.  It does not cover clean caps
whose `r^2` vanishes by cancellation despite having disjoint supported
edges.

## 4. A support-only structural theorem

There is a convenient cancellation-free subcriterion for `K=I_3`.  For a
fixed `(p,q,v)` and cap colour `i`, let

```text
P_i = {a != p,q,v : row i of A_pa has a nonzero cell},
Q_i = {a != p,q,v : row i of A_qa has a nonzero cell}.
```

If, for every `i`, there is no distinct cross-pair

```text
a in P_i, b in Q_i, a != b,                            (5)
```

then each of the two summands of every off-star response cell in (1)
vanishes separately for `K=I_3`.  Therefore, if

```text
trace(A_pq) != 0,                                      (6)
```

`I_3` is an active response-star cap: its three `kappa_i` equal one and its
direct scalar is (6).

The W40 four-torus satisfies (5)-(6) at all six choices in the headline.
This proves the claimed stratum without Gröbner bases, specialisation, or
cancellation.  The symbolic audit independently rebuilds all 4,881 raw
level-4 word rows over
`Q[s^+-1,t^+-1,a^+-1,b^+-1]` before applying the lemma.

## 5. Literal level-4 residual

Let `C` range over the 728 carriers in (4), and let `L_C(A)` be the
corresponding 90-by-9 or 108-by-9 matrix.  Any level-4 source with no active
cap arising from pairwise-intersecting response support lies in the exact
set-theoretic residual

```text
X4  intersect  intersection_C union_{i=0}^3
    { A : ell_i is in rowspan L_C(A) }.                 (7)
```

In particular, an all-blocked level-4 source must lie in (7).  The converse
is not asserted.

This is a finite original-coordinate case system.  To express each
row-span branch polynomially, stratify by `r=rank(L_C)`, require one
`r`-minor of `L_C` to be nonzero and all `(r+1)`-minors of
`[L_C;ell_i]` to vanish.  The `r=0` branch simply says that both `L_C` and
`ell_i` vanish.  Site and colour symmetry make the star carriers one orbit,
the triangle carriers a second orbit, and the three diagonal blockers one
colour orbit; they do not by themselves identify simultaneous blocker
assignments across all 728 carriers.

This is the recommended next elimination target.  It is substantially
smaller-degree than the 729 cubic cap-error coefficients, although still a
large disjunctive incidence problem.

## 6. Exact controls and results

### W40 positive-through-filter

The integral W40 point was loaded from the pinned source and all 6,561 word
amplitudes were rebuilt.  All 4,881 level-4 rows pass.  Exactly six of the
168 star choices pass (3), precisely the six in the headline.  At
`(67,5,I_3)` the four nonzero response cells lie on edges
`05,15,25,45`; `s=kappa_0=kappa_1=kappa_2=1`.  Flipping the required
`A_26[2,2]=-st` sign produces four raw level-4 failures.

No W40 triangle choice passes.  This is expected: the exhibited response
support is a four-edge star, not a triangle.

### W25-F8 outside-locus negative control

The pinned rational W25-F8 source passes all 1,731 level-3 rows and fails
exactly 78 level-4 rows.  It has zero passing star choices and zero passing
triangle choices.  This is consistent with its independently established
all-blocked status, and demonstrates that the response-star test is not
being made to pass every input.  Because W25-F8 is outside `X4`, it is a
negative control only, not evidence for or against (7) on the target locus.

Full exact row matrices and their ranks are retained rather than summarized
away:

| ledger | contents |
|---|---|
| `raw_x4_rows_w40.jsonl` | all 6,561 rational W40 word rows |
| `raw_x4_rows_w25_f8.jsonl` | all 6,561 rational W25-F8 word rows |
| `raw_x4_rows_w40_laurent.jsonl` | all 4,881 symbolic W40 level-4 rows |
| `response_star_matrices_*.jsonl` | all 168 labelled 90-by-9 matrices per source |
| `response_triangle_matrices_*.jsonl` | all 560 labelled 108-by-9 matrices per source |

Every ledger hash is recorded in the result JSON.  Both control scripts
compare declared and actually executed control manifests.

The final portability battery ran each script in standard, optimized, and
isolated/no-site modes.  All three modes returned byte-identical stdout for
each script:

| script | standard / `-O` / `-I -S` stdout SHA-256 | result SHA-256 |
|---|---|---|
| `audit_response_star.py` | `9dba97d3da0522bd20f11c451457d9401a47ca4b6d6cb8be32f93bfcc759e214` | `630727db5ebfde862cb7df6b9529fddccdff803965bf7e663b372f3a12854ed1` |
| `audit_w40_laurent_response_star.py` | `33d3c2a2389e3dac8af64c1d2ffb52bbe14c95030e051d82dcc36aac0a54bd54` | `cc67a9dba1ae9921a1d9879b7933d8f3c5f75eb42865763b014bbd786ebcb775` |

## 7. Scope and hazards

* The response-star and response-triangle criteria are exact for their
  respective support carriers, but only sufficient for a general clean cap.
* No all-blocked level-4 source was constructed or ruled out.
* No claim is inferred from search failure; there is no stochastic search in
  this lane.
* All rank claims attach to the pinned source and full labelled raw matrix.
* The finite-union argument is stated over `C` (more generally, an infinite
  field).  No single-small-field inference is used.
* W40 is a level-4 point, not a fully exact point; this is exactly the
  hypothesis of the proposed `X4-to-cap` theorem.
* These are same-lane computations and remain unaudited.

## Replay

```text
PYTHONDONTWRITEBYTECODE=1 python3 -I -S computations/unaudited-codex-response-star-2026-08-20/audit_response_star.py
PYTHONDONTWRITEBYTECODE=1 python3 -I -S computations/unaudited-codex-response-star-2026-08-20/audit_w40_laurent_response_star.py
```
