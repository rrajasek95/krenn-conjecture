# Every shared-reciprocal low-rank packet is pure-support empty

## Outcome

The 4,419 finite residual rank rows from
[`shared-reciprocal-lowrank-headlabel-refinement.md`](shared-reciprocal-lowrank-headlabel-refinement.md)
are all empty before coefficient elimination.  In fact the rank flags are
irrelevant: the 477 omission/head-label packets collapse to six maximal
pure-support signatures, 462 packets miss a pure row, and the remaining 15
have a mandatory unique mixed matching after a three-way pure-anchor split.

Thus the entire coordinate-plane/low-rank side of the shared reciprocal
four-cover theorem is closed over every field.  There is no signed Laurent,
Groebner, or nonlinear survivor.  The only shared-reciprocal branch left by
this analysis is the residual full-span alternative in which some internal
incident space has dimension three.

## 1. Maximal literal support envelope

Use sites `p=0,q=1,r=2` and common sites `C={3,4,5,6,7}`.  For one of the
low-rank packets let `alpha` be the omitted-colour map in the `pq` deletion
and `beta` the omitted-colour map in the `pr` deletion.  Write

\[
 A_{pq}=\lambda E_{ba},\qquad A_{pr}=\mu E_{dc}.             \tag{1}
\]

The checker enlarges the actual cell support to the following maximal
envelope.

- `A_pq,A_pr` retain only their literal reciprocal coordinate cells.
- Every `p-C` block and the opposite chord `A_qr` retain all nine cells.
- On `q-u`, `u in C`, the endpoint colours lie in the two coordinate planes
  omitting `beta(q),beta(u)`.
- On `r-u`, they lie in the planes omitting `alpha(r),alpha(u)`.
- On a common-core block `u-v`, each endpoint lies in the intersection of
  its `alpha`- and `beta`-omission planes.

This is an over-approximation: it forgets block ranks, chord minors,
localization, and all coefficient relations.  Therefore a missing pure row
or a unique mixed matching in this envelope is also missing/unique in every
actual packet below it.

## 2. Pure-row census

Enumerating all 105 perfect matchings for each of the 477 canonical packets
gives exactly six pure matching-count signatures:

| counts `(pure0,pure1,pure2)` | packets |
|---|---:|
| `(0,0,0)` | 204 |
| `(0,0,1)` | 171 |
| `(0,1,0)` | 27 |
| `(0,1,1)` | 30 |
| `(3,0,0)` | 30 |
| `(3,1,1)` | 15 |

The first five rows comprise 462 packets.  At least one exact pure GHZ
equation there is literally

\[
                              0-1=-1,                         \tag{2}
\]

so those coefficient ideals are the unit ideal.

All 15 remaining packets share the single omission-contingency state

\[
 \alpha=(0,1,1,2,2;0),\qquad
 \beta =(0,1,2,1,2;0),                                     \tag{3}
\]

where the first five entries are on `C` and the last entries are at `r,q`.
Equivalently their common-site contingency matrix is

\[
 \begin{pmatrix}1&0&0\\0&1&1\\0&1&1\end{pmatrix}.          \tag{4}
\]

Each has three pure-zero matchings and unique pure-one and pure-two
matchings.

## 3. The 45 pure-anchor branches

The pure-one and pure-two equations have one matching monomial each, so all
cells in those two monomials are nonzero.  The pure-zero coefficient is a
sum of three matching monomials equal to one; at least one of the three is
nonzero.  Branch on that choice.  This gives

\[
                         15\cdot3=45                           \tag{5}
\]

anchor branches, with every cell in the chosen three pure monomials
mandatory nonzero.

For each branch the checker scans every ternary word and all 105 matchings
inside the maximal envelope.  It finds a mixed word with exactly one
supported matching, and every cell of that matching belongs to the mandatory
pure-anchor set.  Across all 45 branches only two witnesses occur:

\[
\begin{array}{c|c|c}
\text{mixed word}&\text{unique matching}&\text{branches}\\ \hline
01100110&03|15|26|47&15\\
12211221&04|16|25|37&30.
\end{array}                                                  \tag{6}
\]

The unique mixed coefficient is therefore one nonzero monomial, while exact
GHZ requires it to vanish.  This is a termwise contradiction in an integral
domain; no sign or cancellation issue remains.

## 4. Consequence

Combining (2) and (6):

\[
 \boxed{\text{every shared-reciprocal coordinate-plane packet is empty}.}
                                                                    \tag{7}
\]

This closes all 16 omission orbits, all 477 endpoint-label packets, and all
4,419 non-curvature rank rows from the previous refinement.  The signed
Laurent/low-class oracle requested after the pure-support pass has no input:
there are zero coefficient-feasible low-rank packets.

For `r>=5`, shared reciprocal pairs are automatic.  The remaining exact
frontier is consequently sharp: for every shared reciprocal pair, at least
one of its two six-site residual charts must contain a full three-dimensional
internal incident space.  Turning that full-span alternative into a curved
rank-one overlap, clean cap, or contradiction is the next theorem-level
task.

## Reproduction

```sh
python3 computations/verify_shared_reciprocal_lowrank_pure_support_closure.py
python3 -O computations/verify_shared_reciprocal_lowrank_pure_support_closure.py
```

The checker pins the 477-packet refinement, reconstructs the maximal cell
envelope from committed omission data, enumerates all 6,561 words, and
freezes all 45 unique-mixed certificates.
