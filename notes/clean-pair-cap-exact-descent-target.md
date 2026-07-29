# The exact clean-pair target for an \(N\)-to-\(N-2\) descent

## 1. Outcome

This note isolates the terminal theorem which a four-cut curvature argument
must feed.  It does not assert that a clean cap always exists.

Let \(B\) have even cardinality \(N=2m\geq8\), let \(p,q\in B\), and put

\[
                       U=B\setminus\{p,q\},\qquad |U|=2h,
                       \qquad h=m-1.                    \tag{1}
\]

Suppose endpoint-ordered aggregate blocks \(A_{uv}\in V_u\otimes V_v\),
with \(V_u=\mathbb C^3\), satisfy

\[
                       H_B(A)=\Delta_{B,3}.             \tag{2}
\]

For a cap covector \(K\in(V_p\otimes V_q)^*\), Section 2 defines a scalar
\(s=s(K)\), a quadratic effective-edge correction \(r=r(K)\), and target
coefficients

\[
                       \kappa_c=K(e_c^{(p)},e_c^{(q)}).
                                                               \tag{3}
\]

The uniform homogeneous cap error is

\[
 {\cal E}_{p,q}(K)=
 \sum_{k=2}^{h}s^{\,h-k}
       \left[{r^k\over k!}\exp(x)\right]_U
 =
 \sum_{k=2}^{h}
 {s^{\,h-k}r^kx^{h-k}\over k!(h-k)!}.                 \tag{4}
\]

Every product is in the site-square-zero algebra on \(U\), and the second
display means its full-\(U\)-support component.

**Theorem 1.1 (exact clean-pair descent).**  If

\[
                 s\kappa_0\kappa_1\kappa_2\ne0,
                 \qquad {\cal E}_{p,q}(K)=0,            \tag{5}
\]

then there is a finite endpoint-coloured aggregate source on \(U\) whose
matching tensor is exactly

\[
                              \Delta_{U,3}.             \tag{6}
\]

It retains arbitrary complex coefficients and endpoint asymmetry.  It
lifts to a finite decorated source in the original graph formulation, and
its palette is exactly the three selected colours.

The condition in (4) is necessary and sufficient for the canonical
effective quadratic \(x+r/s\) to realize the capped tensor.  The stronger
condition \(r^2=0\) is sufficient but is not built into the definition.

Consequently the uniform conjecture-level existence theorem has one exact
target:

\[
 \boxed{\text{Every exact ternary source on even }N\geq8
 \text{ has }p,q,K\text{ satisfying (5).}}             \tag{7}
\]

Together with the proved six-site obstruction, (7) would give the full
upper bound by induction.

## 2. Exact cap formula

Work in the square-free commutative tensor algebra

\[
 {\cal S}_U=\bigoplus_{T\subseteq U}\bigotimes_{u\in T}V_u.     \tag{8}
\]

Products with overlapping positive site support are zero.  Orient all
blocks by their displayed endpoints and put

\[
                              x=\sum_{\{a,b\}\subset U}A_{ab}. \tag{9}
\]

The direct cap scalar is

\[
                              s=\langle K,A_{pq}\rangle.       \tag{10}
\]

For \(a,b\in U\), \(a\ne b\), contract the two ways in which \(p,q\)
can match to \(a,b\):

\[
 R_{ab}
 =K\mathbin{\lrcorner}
     \left(A_{p\mid a}A_{q\mid b}
           +A_{p\mid b}A_{q\mid a}\right)
 \in V_a\otimes V_b,
 \qquad
                              r=\sum_{\{a,b\}\subset U}R_{ab}. \tag{11}
\]

Endpoint order in (11) is physical: the \(p\)-slot and \(q\)-slot are
contracted by the corresponding slots of \(K\), while the \(a,b\) slots
remain in their named local spaces.

Every perfect matching of \(B\) uses either the edge \(pq\), or sends
\(p,q\) to two distinct sites of \(U\).  Therefore

\[
 K\mathbin{\lrcorner}H_B(A)
 =\left[(s+r)\exp(x)\right]_U.                         \tag{12}
\]

By (2), the same cap is

\[
 K\mathbin{\lrcorner}\Delta_{B,3}
 =\sum_{c=0}^2\kappa_cX_c^U,
 \qquad
 X_c^U=\bigotimes_{u\in U}e_c^{(u)}.                  \tag{13}
\]

Equations (12)--(13) retain every parallel aggregate coefficient and every
complex cancellation.  They select no individual source term.

## 3. The homogeneous canonical error

Assume \(s\ne0\) and set

\[
                              y=x+{r\over s}.           \tag{14}
\]

Since \(x,r\) have even site degree, they commute.  Direct expansion gives

\[
\begin{aligned}
 sH_U(y)
 &=s\left[\exp\left(x+{r\over s}\right)\right]_U\\
 &=\left[(s+r)\exp(x)\right]_U
   +\sum_{k=2}^{h}s^{1-k}
      \left[{r^k\over k!}\exp(x)\right]_U.             \tag{15}
\end{aligned}
\]

The sum stops at \(h\), since \(r^k\) has site degree \(2k\).  Multiplying
the correction in (15) by the nonzero scalar \(s^{h-1}\) gives exactly
(4).  Hence

\[
 {\cal E}_{p,q}(K)=0
 \quad\Longleftrightarrow\quad
 H_U(y)={1\over s}K\mathbin{\lrcorner}H_B(A).          \tag{16}
\]

This proves both directions of the canonical claim.  Notice that
\({\cal E}_{p,q}\) is homogeneous of degree \(h\) in \(K\): both \(s\)
and \(r\) depend linearly on \(K\), and every summand in (4) has
\(K\)-degree \(h\).  Thus the target is projectively well defined without
choosing an affine normalization for \(K\).

If \(r^2=0\), then \(r^k=0\) for all \(k\ge2\), so (4) vanishes.  The
converse is neither asserted nor needed: top-support cancellation among the
higher cumulants is allowed.

At the first inductive boundary \(N=8\), one has \(h=3\), and

\[
 {\cal E}_{p,q}(K)
 ={s\,r^2x\over2}+{r^3\over6},
 \qquad
 6{\cal E}_{p,q}(K)=3sr^2x+r^3.                       \tag{17}
\]

For a pure pair cap this is, up to sign, the denominator-cleared cubic
recorded in the cap-condition notes.  Thus the uniform formula (4) agrees
with the already audited eight-to-six boundary rather than introducing a
new notion of cleanliness.

## 4. Proof of the descent theorem

Under (2), (5), and (16),

\[
                       H_U(y)
 =\sum_{c=0}^2{\kappa_c\over s}X_c^U.                 \tag{18}
\]

Choose one site \(u_0\in U\).  Since every \(\kappa_c\) and \(s\) is
nonzero, the diagonal map

\[
 D_{u_0}(e_c^{(u_0)})={s\over\kappa_c}e_c^{(u_0)}
 \qquad(0\le c\le2)                                   \tag{19}
\]

is invertible.  Apply \(D_{u_0}\) to the \(u_0\)-slot of every block of
\(y\) incident with \(u_0\), leaving every other endpoint unchanged.
Every perfect matching of \(U\) uses exactly one block incident with
\(u_0\).  Multilinearity of the matching tensor therefore applies
\(D_{u_0}\) exactly once to (18), giving

\[
 \sum_{c=0}^2{\kappa_c\over s}{s\over\kappa_c}X_c^U
 =\Delta_{U,3}.                                       \tag{20}
\]

This proves the aggregate statement.

To return to a finite decorated graph, expand each transformed block in
the endpoint basis:

\[
                     y_{ab}=\sum_{c,d=0}^2
                         y_{ab}(c,d)e_c^{(a)}e_d^{(b)}. \tag{21}
\]

For every nonzero coefficient in (21), introduce one source adjacent to
\(a,b\), give its two endpoint colours \(c,d\), and give it weight
\(y_{ab}(c,d)\).  There are at most

\[
                              9\binom{|U|}{2}           \tag{22}
\]

such sources.  Aggregation recovers \(y\), so its decorated matching tensor
is (20).  No symmetry between the two endpoint colours has been imposed.

All introduced endpoint colours lie in \(\{0,1,2\}\).  Conversely, for
each \(c\), the coefficient of \(X_c^U\) in (20) is one, so at least one
nonzero matching uses colour \(c\) at every site.  In particular colour
\(c\) occurs on a nonzero source.  After omitting zero coefficients, the
palette is therefore exactly \(\{0,1,2\}\).  This proves Theorem 1.1.

## 5. The conditional resolution corollary

**Corollary 5.1 (curvature-to-resolution interface).**  Suppose that for
every finite exact ternary aggregate source on every even set \(B\) with
\(|B|\ge8\), there are \(p,q,K\) satisfying (5).  Then no exact ternary
source exists on any even set of size at least six.

**Proof.**  If an exact ternary source existed, choose one of minimum even
order \(N\ge8\); order six is excluded by the proved arbitrary-complex
six-site theorem.  The assumed existence statement and Theorem 1.1 produce
an exact ternary source of order \(N-2\), contradicting minimality.
\(\square\)

If a monochromatic decorated graph has at least three palette colours,
project three selected colour axes identically at every site and send every
other colour axis to zero.  Its matching tensor becomes an exact ternary
target, with parallel sources, endpoint order, and complex coefficients
retained by aggregation.  Corollary 5.1 would therefore imply the required
palette upper bound two for every even \(N\ge6\).  Combined with the known
lower constructions and the proved orders two and four, it would resolve
the conjecture completely.

## 6. Exact scope and instructions for the existence theorem

1. Merely having \(s\ne0\) and all three \(\kappa_c\ne0\) does not make a
   cap clean.  The higher-cumulant error (4) is essential.
2. The cap identity (12) is always pure for an exact source, but purity of
   its top tensor does not imply pair-only closure on \(U\).
3. The existence theorem need only force the top-support equation (4), not
   the stronger algebra identity \(r^2=0\).
4. No representative modulo an annihilator occurs in (4): \(s,r,x\) are
   built from the original aggregate blocks and the physical covector
   \(K\).
5. Scaling \(K\) does not affect activity or cleanliness.  Both are
   projective conditions.
6. A proof based only on the dimension of the cap space or one top
   contraction cannot work: the registered prism root covers satisfy those
   relaxations.  The missing input must constrain (4) through transverse
   source-variable compatibility.

The dependency-free checker
[verify_clean_pair_cap_exact_descent_target.py](../computations/verify_clean_pair_cap_exact_descent_target.py)
audits the typed-perfect-matching expansion of (15), the homogeneous
denominator clearing in (4), the \(N=8\) cubic profile, diagonal
normalization, and the finite aggregate-to-decorated source count.  The
proof above is uniform; the checker is not a bounded existence search.
