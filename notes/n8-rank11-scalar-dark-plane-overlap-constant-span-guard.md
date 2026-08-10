# Degree-zero and degree-one source multipliers do not force the dark-plane overlap caps

Research evidence only.  This is a scope guard for the pair-exchange
mechanism in
[`n8-rank11-scalar-dark-plane-second-chart-active-clean.md`](n8-rank11-scalar-dark-plane-second-chart-active-clean.md).
It is not a source point, an ideal-membership calculation, or a proof of
`SP-CLEAN-BRIDGE`.

## 1. Universal internal deformation

Keep the endpoint stars and direct block of the fixed-dark rational normal
form, but replace its internal six-site quadratic by all 135 independent
decorated cells

\[
                   q_{uv}(a,b),\qquad 0\leq u<v<6,quad 0\leq a,b<3.
\]

Expand all nine original full-pair equations coefficientwise.  After zero
coefficients are removed, they give 4,737 scalar polynomial rows with 63,183
terms.  Their constant-coefficient row span over \(\mathbb Q\) has exact rank
1,579.

On the restored eight-site array, retain the two overlapping cap directions
found by the fixed guard,

\[
              (uv,K)=(17,E_{02}+I),\qquad(27,E_{01}+I),
\]

but now compute their homogeneous clean errors for the arbitrary internal
quadratic.  The first has 339 nonzero output coefficients and 10,845 terms;
the second has 489 coefficients and 24,588 terms.

## 2. Exact span verdict

Sparse Gaussian elimination over \(\mathbb Q\) gives

\[
\begin{array}{c|c|c}
\text{cap}&\text{coefficients in the constant source-row span}&
             \text{surviving remainder sizes}\\ \hline
17&54/339&3\ldots227\\
27&48/489&3\ldots348.
\end{array}
\]

Thus 726 of the 828 clean-error coefficients survive.  In particular, the
successful caps of the rational guard are not polynomial identities obtained
by taking a fixed scalar linear combination of the original full-nine rows
after the internal cells are freed.

This is deliberately only a constant-span statement.  The diagonal source
rows are inhomogeneous, so source-dependent polynomial multipliers can feed
their target constants into the required degree and create higher filtered
tails.  The calculation neither excludes such a multiplier nor tests full
ideal membership.

## 3. Exact first-syzygy obstruction

The first overlap cap has a sharper coefficient.  Order its residual sites as
\((0,2,3,4,5,6)\).  At output word \(000122\), its complete clean-error
coefficient is

\[
\begin{aligned}
 24\bigl(&2q_{01}(0,1)q_{13}(1,0)
          +q_{01}(0,1)q_{13}(2,0)\\
         &+q_{01}(0,2)q_{13}(1,0)\bigr).                 \tag{1}
\end{aligned}
\]

Each monomial in (1) reuses physical site 1.  Conversely, every quadratic
monomial in every original full-pair coefficient is a product of two
disjoint internal edges: the checker finds 30,375 occurrences, 3,645 unique,
and no exception.  The source coefficients contain no linear monomial.

Let \(m_r(q)f_r(q)\) be an arbitrary polynomial source combination with
\(\deg m_r\leq1\).  Its degree-two part can only come from a constant
multiplier times the quadratic part of \(f_r\), or a linear multiplier times
a linear part of \(f_r\).  The latter is zero and the former is supported on
disjoint edges.  Therefore the projection to repeated-site quadratics kills
the entire degree-at-most-one source module and is nonzero on (1).

This remains true even if all quartic tails of the linear multiples cancel.
Hence a source-faithful identity producing this overlap cap must use a
multiplier of q-degree at least two, or impose entry-minimal support before
the universal internal deformation is formed.  The degree-two anchor
multipliers are exactly where the known filtered/Macaulay obstruction begins.

## 4. Proof consequence

The positive fixed-guard calculation remains useful: it exhibits literal
activity conversion by changing physical pairs.  The present audit shows
what cannot be used to promote it.  A uniform proof must employ at least one
of the following genuinely source-relative operations:

1. a degree-at-least-two use of the common cross-permanent/mixed-carrier
   identity;
2. a filtered two-chart comparison whose higher tails cancel through the
   labelled overlap; or
3. entry minimality to force the support-concentrated response pattern before
   the cap is formed.

Another static row sum, separate released-site comparison, or contraction of
the inactive clean plane cannot provide the missing theorem.

## 5. Exact audit

[`verify_n8_rank11_scalar_dark_plane_overlap_constant_span_guard.py`](../computations/verify_n8_rank11_scalar_dark_plane_overlap_constant_span_guard.py)
uses standard-library exact `Fraction` arithmetic.  It reconstructs the
fixed stars from the all-pair checker, builds all 135 internal variables,
expands the nine source tensors and both clean errors, and performs sparse
row reduction over \(\mathbb Q\).  Its deterministic ledger digest is

```text
770d44910eafc2b7ed8d6d5bd71bc1d0b6ef99a3f5f9430108e063491bc11e03
```
