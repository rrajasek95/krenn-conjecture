# The full site-0 star closes the 66-term coefficient debt

## Theorem

Let \(H\) be the direct-free 90-term pure matching row and put

\[
 x_i=x_{0i}^{11},\qquad 1\leq i\leq7.
\]

Every perfect matching in \(H\) contains exactly one \(x_i\).  Hence

\[
 H=\sum_{i=1}^7 S_i,
 \qquad S_i=x_i\partial_{x_i}H.                         \tag{1}
\]

The first collision on \((x_1,x_7)\) lands signlessly on \(S_1+S_7\).
Its 66-term complement is therefore

\[
 R_{66}=S_2+S_3+S_4+S_5+S_6.                          \tag{2}
\]

For each \(i<j\), form the source-valid response collision

\[
 C_{ij}=x_j\iota_i(e)-x_i\iota_j(e),
 \qquad
 dC_{ij}=x_j\partial_iH-x_i\partial_jH.                \tag{3}
\]

Private deletion/reinsertion uses the branch sign a second time, so the
formal cap projection is

\[
 \Phi(dC_{ij})=S_i+S_j.                                \tag{4}
\]

The 21 vectors in (4) have rank seven and satisfy the exact identity

\[
 {1\over6}\sum_{1\leq i<j\leq7}\Phi(dC_{ij})=H.        \tag{5}
\]

Thus one natural full-star pair-mate operation eliminates the complete
coefficient debt.  No additional cap coefficient orbit is required.

This operation is not yet constructed.  The unary Euler generator,
collision triangles, complete-response rows, root/Weyl transports, and
relative Taylor cells all remain in the response corner.  The current
operation algebra still has

\[
                         e_CAe_R=0,                    \tag{6}
\]

where \(e_C\) is the `AugP2/K_Eq` cap idempotent.  Equation (5) is therefore
the exact coefficient theorem conditional on one new natural operation,
not a declaration that the operation exists.

Exact checker:
[`verify_h3_first_collision_full_star_completion_gate.py`](../computations/verify_h3_first_collision_full_star_completion_gate.py).

## 1. Direct-free star partition

Before deleting matchings containing the edge \(36\), every site-0 sector
has 15 terms.  Direct-free restriction gives

| partner \(i\) | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
|---|---:|---:|---:|---:|---:|---:|---:|
| \(|S_i|\) | 12 | 12 | 15 | 12 | 12 | 15 | 12 |
| terms removed | 3 | 3 | 0 | 3 | 3 | 0 | 3 |

No site-0 sector is deleted.  The first pair has \(12+12=24\) terms and the
remaining five sectors have

\[
                     12+15+12+12+15=66.                \tag{7}
\]

Each term of \(H\) occurs in exactly six pair outputs \(S_i+S_j\), proving
(5) literally after restriction.  Per root the 21 collision boundaries have
540 signed branch terms; across the two separately labelled `AB` and `AC`
roots there are 1,080.  Their cap-output ranks are respectively seven and
fourteen.

## 2. Residual endpoint/root/tail orbits

The stabilizer of the first pair, the direct-free pair, and the three remote
tail sites is

\[
 S_{\{1,7\}}\times S_{\{3,6\}}\times S_{\{2,4,5\}},
 \qquad |G|=24.                                        \tag{8}
\]

At the coarse star-partner level, \(R_{66}\) has two orbits:

| star partner type | partners | terms |
|---|---|---:|
| remote tail `T` | 2,4,5 | 36 |
| direct-root pair `R` | 3,6 | 30 |

Retaining every matching edge splits these into six literal orbits.  Here
`O={1,7}`, `R={3,6}`, and `T={2,4,5}`; the last column records the types of
the three non-star matching edges.

| orbit | star type | remaining edge types | size |
|---:|---|---|---:|
| 1 | T | `OR+OR+TT` | 6 |
| 2 | T | `OR+OT+RT` | 24 |
| 3 | T | `OO+RT+RT` | 6 |
| 4 | R | `OR+OT+TT` | 12 |
| 5 | R | `OT+OT+RT` | 12 |
| 6 | R | `OO+RT+TT` | 6 |

The sizes sum to 66.  Thus the complement is not a single literal matching
orbit, but it is controlled by only two natural star-partner types.

## 3. The smallest completion family

The exact residual formula is

\[
 R_{66}=(S_3+S_6)
 +{1\over2}\bigl((S_2+S_4)+(S_2+S_5)+(S_4+S_5)\bigr). \tag{9}
\]

It uses the direct-root collision \(C_{36}\) and the complete triangle on
the remote-tail partners \(2,4,5\).  These four pair columns have rank four.
An exhaustive test of all subsets of the 21 pair outputs proves that no one-,
two-, or three-column family spans \(R_{66}\).  Hence four is minimal even
before imposing symmetry, and (9) is the minimal symmetry-stable choice.

The full-star form (5) is more natural globally.  It uses all 21 instances
of one rule and is equivariant before choosing the first pair.  Its
restriction to \((1,7)\), with two ordered branches and two receiving root
labels, is exactly the original set of four DQ/PS mates.  On the full star
the same rule has

\[
 21\text{ pairs}\times2\text{ branches}\times2\text{ roots}=84
\]

labelled instances, not 84 independent operation constructors.

## 4. Signs, fine degrees, and source telescoping

For the ordered branch \(i\mid j\), a cap matching containing \(x_i\) is
sent to the response monomial

\[
 x_j(M/x_i).
\]

This monomial is missing site \(i\), doubles site \(j\), and has exact fine
degree

\[
 \deg(w)-e_{i,w_i}+e_{j,w_j}.                          \tag{10}
\]

The opposite branch has boundary sign \(-1\).  Its map sign is also \(-1\),
so both branches reconstruct their parent cap matching with coefficient
\(+1\).  The checker verifies (10) on every branch of all 21 pairs before
collection, for the literal word and repeated-site labels.

The raw response collisions have the standard source-valid triangle
syzygies

\[
 x_kdC_{ij}-x_jdC_{ik}+x_idC_{jk}=0                   \tag{11}
\]

for all 35 triples.  Thus the source boundaries telescope through ordinary
Koszul triangles; no new response-side coefficient generator is needed.

There is also a unary presentation.  Including the homogenizer direction,

\[
 G_0=\sum_i x_i\iota_i(e)+u\iota_u(e),
 \qquad dG_0=H-u.                                     \tag{12}
\]

The matching component of (12) is exactly (1), and its DQ/PS-decomposed cap
coefficient projection is exactly the 21-pair average (5).  This proves that
the apparent 66-term gap is internally present on the response side.

## 5. Why the second seed and ordinary response do not finish the map

The second exact seed-cycle type has word `11211211`; the first complement
has word `11111111`.  Rebuilding its \((1,7)\) collision gives 24 terms, but
its word/fine-labelled intersection with the pure 66-term complement is
zero.  Moreover the exact seed cycle remains a response-to-response
operation with zero `r0` projection.

If all labels are forgotten, the ordinary complete response gives the
tautological formula

\[
 R_{66}=H-(S_1+S_7).                                  \tag{13}
\]

The untyped rank ladder is therefore `1 -> 2`: first-pair row, then complete
row.  With operation tags retained, the complete row lies in
`response/EqSystem`, while \(R_{66}\) is required in `cap/AugP2_K_Eq`.
The typed rank ladder is `1 -> 2 -> 3`; adjoining the cap residual still
raises rank.  Ordinary complete response proves coefficient availability,
not the missing off-diagonal operation.

## 6. Relative Taylor/private factorization

The off-diagonal pair label \((x_1,x_7)\) is visible in the ordinary Taylor
resolution, but its literal boundary is not yet the collision packet.  There
are 12 matching parents containing \(x_1\) and 12 containing \(x_7\).  Their
144 cross-parent pairs give 135 distinct squarefree lcms with the exact
census

| lcm cell degree | 6 | 7 | 8 |
|---|---:|---:|---:|
| parent pairs | 12 | 42 | 90 |

Equivalently, the two parents share respectively 2, 1, or 0 matching cells.
By contrast, the 24 missing/doubled collision branches have cell degree four,
and none is one of those lcms.  Thus the original four DQ/PS mates are not
the literal boundary of one existing Taylor cell.  A labelled
Taylor-to-Spencer deletion/contraction must first lower the 6/7/8-cell lcm
packet to the four-cell branches in (3).

There is a second general guard.  Ordinary matching lcms are squarefree in
decorated cells.  A diagonal pair \((a,a)\) therefore occurs with
multiplicity one and has zero ordinary second Hasse face.  Any full
site-repeating comparison must enlarge the ordinary Taylor object by the
divided-power cells \(\gamma_2(\iota_a)\).  The first star pairs are
off-diagonal, but the whole-module comparison cannot omit this diagonal
augmentation.

Even after this relative contraction, Taylor differentials preserve the
response operation parent, whereas the DQ/PS mates land in the cap parent.

The existing two-word calculation nevertheless proves that the proposed
comparison has a unique target if it exists:

```text
literal matching coordinates                         180
pair-shadow rank                                      159
pair-shadow fibre                                      21
committed readout rank on that fibre                    14
remaining termwise/private module                       7
private insertion rank on the residual                  7
```

Thus the matching-occurrence and repeated/private resolutions share the
same seven-dimensional formal comparison module, and the private rows kill
it completely.  Root naturality then gives the unique normalized tied
solution with `B=Eq` and zero residual.

What fails is the first categorical step.  Complete-word covariance remains
in \(e_RAe_R\), cap normalization remains in \(e_CAe_C\), and their generated
`Hom(response,cap)` has dimension zero.  Even granting every diagonal
word/fine/repeated repair leaves a two-dimensional `AB/AC` receiving-section
quotient.  Target-zero transport does not change this operation idempotent.

The smallest positive datum is therefore:

> one root-natural full-star mixed divided-Hasse/Taylor-to-Spencer-to-`AugP2`
> module action, compatible with restriction and private insertion, whose 84
> labelled star instances include the original four pair mates.

Conditional on that single action, (5) removes the entire 66-term debt and
the pinned seven-dimensional uniqueness theorem leaves no further scalar,
root, or termwise ambiguity.

## Scope

All star, orbit, sign, fine-degree, rank, and minimality claims are exact over
\(\mathbb Q\) for the canonical `h=3` direct-free 90-term row.  Both root
labels and the pure/second-seed word distinction are literal.  The conclusion
constructs the response-side Euler/Taylor data and the cap coefficient
formula; it does not construct the nonzero \(e_CAe_R\) operation.
