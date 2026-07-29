# Three distinct lifts remain impossible with one deficient local frame

## 1. Exact theorem

Let \(U\) be a six-set with a distinguished site \(o\).  At the five sites
\(v\ne o\), choose three independent vectors
\(a_0^{(v)},a_1^{(v)},a_2^{(v)}\).  At \(o\), choose arbitrary nonzero
vectors \(a_0^{(o)},a_1^{(o)},a_2^{(o)}\) whose span has dimension at most
two.  For three pairwise distinct pairs \(P_0,P_1,P_2\), put

\[
 A_r(P_r)=\bigotimes_{u\notin P_r}a_r^{(u)}.
                                                               \tag{1}
\]

**Theorem 1.1 (sole-defect distinct-lift obstruction).**  For arbitrary
nonzero complex coefficients \(\lambda_0,\lambda_1,\lambda_2\), there is no
quadratic \(q\) in the site-square-zero algebra satisfying

\[
 q^{[2]}=\sum_{r=0}^2\lambda_rA_r(P_r),
 \qquad q^{[3]}=0.                                             \tag{2}
\]

The endpoint blocks of \(q\) are arbitrary tensors.  The theorem allows
arbitrary local dimensions, endpoint order, zero blocks, and complex
cancellation.  It is power-only and does not use response rows.

This extends the
[independently audited distinct-missing-pair theorem](distinct-missing-pair-common-power-obstruction-independent-audit.md)
across exactly one deficient local field frame.  It is deliberately not a
claim about two or more deficient sites or about a sum containing more than
one active pair for a field.

## 2. Reduction to three finite local matroids

Project every good-site space onto the span of its three field vectors and
project the bad-site space onto

\[
 W_o=\operatorname {span}\{a_0^{(o)},a_1^{(o)},a_2^{(o)}\}.       \tag{3}
\]

The induced unital algebra endomorphism fixes the right side of (2) and
commutes with bracket powers.  Thus the good local dimensions may be taken
to be three and the bad dimension is one or two.

All three coefficients can be normalized to one without changing the bad
local matroid.  For each \(r\), the four-site tensor \(A_r(P_r)\) occupies at
least three good sites.  Scale the \(r\)-axis at one such good site by
\(\lambda_r^{-1}\), independently for the three fields.  These diagonal
good-site automorphisms preserve the other field axes and the bad-site
incidences.

Up to a bad-site linear automorphism, individual field rescalings, and a
field permutation, there are three deficient matroids:

\[
\begin{array}{c|c|c}
\text{type}&\dim W_o&(a_0^{(o)},a_1^{(o)},a_2^{(o)})\\ \hline
\text{three-line circuit}&2&((1,0),(0,1),(1,1)),\\
\text{one coincident pair}&2&((1,0),(0,1),(1,0)),\\
\text{rank one}&1&((1),(1),(1)).
\end{array}                                                     \tag{4}
\]

The circuit and rank-one types permit every permutation of the three fields.
With site \(o\) distinguished, the 455 unordered triples of missing pairs
have 13 orbits under the remaining \(S_5\).  In the coincident type, fields
zero and two may be exchanged while field one is distinguished; the 1,365
labelled choices have 26 orbits.  The checker constructs these orbit sets
directly rather than assuming the counts.

## 3. Complete unsaturated common-power ideals

In the reduced coordinates, there are 120 arbitrary endpoint-ordered
coordinates of \(q\) in the two-dimensional bad-site cases and 105 in the
rank-one case.  From (2) and

\[
                              q q^{[2]}=3q^{[3]},                  \tag{5}
\]

every solution obeys the necessary linear equation

\[
                         q\sum_r A_r(P_r)=0.                     \tag{6}
\]

Only the \(P_r\)-block of \(q\) can multiply \(A_r(P_r)\), but equal
six-site words are collected before row reduction.  Exact rational RREF of
all coefficients of (6) gives the following ranges.

| bad type | orbits | \(q\)-cells | row ranks | kernel dimensions |
|---|---:|---:|---|---|
| circuit | 13 | 120 | 18, 21, 24, 27 | 102, 99, 96, 93 |
| coincident pair | 26 | 120 | 18, 21, 24, 27 | 102, 99, 96, 93 |
| rank one | 13 | 105 | 9, 15, 21, 27 | 96, 90, 84, 78 |

The checker substitutes a complete rational kernel basis into every
coefficient of

\[
                         q^{[2]}-\sum_rA_r(P_r).                  \tag{7}
\]

There are 945 possible four-site coordinate words in the two-dimensional
bad cases and 675 in the rank-one case; identically zero equations are
omitted.  Singular computes an exact Gröbner basis over \(\mathbb Q\).
Every one of the \(13+26+13=52\) unsaturated affine ideals is the unit
ideal.  No nonvanishing saturation, monomial support, block-rank assumption,
or generic chart is used.  A unit ideal over \(\mathbb Q\) remains a unit
ideal over \(\mathbb C\), proving Theorem 1.1.

The complete ordered cell, linear-row, RREF, and quadratic-generator streams
have the combined SHA-256 values

| bad type | combined ledger SHA-256 |
|---|---|
| circuit | 29a338ee82a625787b6a755f392c718fb06f2daca3974a4ef6e9956376eacb07 |
| coincident pair | dc8b15a0d3cc09e53a49c850e6b55b1f5938f47c6534d4e61f190ac72fb488fc |
| rank one | 263028527daeecd8561a6b847f7247452e46ba4f51c7bdb528a3a747da279b65 |

## 4. Field-selection consequence

The theorem has a useful exact application to an arbitrary three-field sum.
Let \(H_r=\{P:\lambda_{rP}\ne0\}\), and suppose distinct representatives
\(P_r\in H_r\) have been chosen.  Put

\[
                         K=\{r:o\in P_r\}.                        \tag{8}
\]

Call the representatives **locally separable at \(o\)** if there is a
linear map \(\tau_o:W_o\to Z\) such that

\[
 \tau_o(a_r^{(o)})=0\quad(r\in K),\qquad
 \tau_o(a_r^{(o)})\ne0\quad(r\notin K).                           \tag{9}
\]

At every good site \(v\), independently kill the axis \(a_r^{(v)}\) when
\(v\in P_r\) and fix it otherwise.  Use \(\tau_o\) at the bad site.  A term
\(A_r(P)\) survives exactly when \(P=P_r\): the good selectors impose the
good part of \(P_r\), while (9) kills a nonincident term of a field whose
selected pair is incident.

There is one harmless but necessary bookkeeping point.  A selected lift
omits every site at which its own field vector was killed.  At a good site,
replace each such unused zero by its original field axis; the surviving axes
were fixed, so the three declared vectors are again independent.  This
does not alter any selected lift.

Likewise, if \(r\in K\), then \(\tau_o(a_r^{(o)})=0\), while Theorem 1.1
states its field vectors as nonzero.  The selected lift \(A_r(P_r)\) omits
\(o\), so its value is independent of the unused bad-site field vector.
Replace that zero by an arbitrary nonzero dummy vector in the span of the
nonzero \(\tau_o(a_s^{(o)})\)'s.  If \(K=\{0,1,2\}\), adjoin one dummy line
and use the same nonzero vector for all three fields.  This leaves the
projected multiplier literally unchanged, including when \(K\) is all
three fields, and the three declared bad-site vectors still span at most
two dimensions.

The resulting unital algebra map therefore turns the full multiplier into
three nonzero distinct lifts in the sense of Theorem 1.1.  Functoriality and
that theorem give:

**Corollary 4.1.**  In a sole-defect common-power solution, the three active
families \(H_0,H_1,H_2\) have no locally separable system of distinct
representatives.

The exact nonseparable membership patterns are finite.  Writing
\(K=\{r:o\in P_r\}\):

* for a three-line circuit, only \(|K|=2\) is nonseparable;
* if \(L_0^{(o)}=L_2^{(o)}\ne L_1^{(o)}\), the nonseparable sets are
  \(\{0\},\{2\},\{0,1\},\{1,2\}\);
* in rank one, every nonempty proper \(K\) is nonseparable.

The empty and full sets are always separable (use the identity and zero
maps).  This list is the sharp local-matroid obstruction to extending the
full-frame private-pair projection through one deficient site.

## 5. Reproduction and scope

Run

    uv run python computations/verify_sole_defect_distinct_common_power.py

with
[verify_sole_defect_distinct_common_power.py](../computations/verify_sole_defect_distinct_common_power.py).
The default run requires Singular.  The
`--ledger-only` option rapidly checks the complete frozen construction
without invoking Singular:

    uv run python computations/verify_sole_defect_distinct_common_power.py --ledger-only

The default run reconstructs all orbit censuses, all 52 exact kernels and
quadratic ideals, every ledger, and every unit-ideal result.  The
ledger-only run reconstructs the same cells, linear rows, RREFs, and
quadratic generators and checks their three combined SHA-256 values.

This theorem closes every locally separable three-pair projection.  The
companion
[sole-defect two-pair theorem](sole-defect-two-pair-common-power-obstruction.md)
closes ordinary Hall failure, while the
[sole-defect packet theorem](sole-defect-nonseparable-packet-common-power-obstruction.md)
closes all 157 locally nonseparable SDR packet orbits, including the twelve
full-packet coefficient families.  Together they close the entire
one-deficient-site response branch.
