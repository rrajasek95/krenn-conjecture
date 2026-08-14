# The support-15 edge-37 rank strata

Research result on the unique support-15 terminal from
[`n8-support15-clean-terminal-census.md`](n8-support15-clean-terminal-census.md).
It does not finish the terminal: it reduces the coefficient problem to two
sharp coordinate strata and exhibits their first full mixed-row failure.

## Outcome

At edge `37`, the complete clean error has `r^[3]=0` and its remaining
nine-component quadratic is

\[
 F=a_0\otimes b_1+a_1\otimes b_0.                     \tag{1}
\]

The exact-source anchor theorem at the degree-four endpoint leaves five
anchor placements.  Three put both response blocks in anchor form and reduce
to the already solved scalar `2x2` permanent.  The other two have exactly one
anchor response block and one unrestricted block `M`.

Every one-anchor rank stratum has a target-active zero except possibly

1. all three relevant anchor vectors are coordinate vectors and `M` is
   invertible; or
2. the same coordinate stratum, `rank(M)=2`, and its left kernel is exactly
   the direct-colour coordinate line.

On both exceptions an exact saturation identity proves that `F=0` forces a
diagonal activity coordinate to vanish.  Thus the local obstruction is real
and source-anchor-compatible.  It is not yet full-source-compatible: an
explicit pure-normalized extension over the whole 15-edge graph has eleven
unique mixed fibres, the first at word `00000101`.

The exact checker is
[`verify_n8_support15_edge37_anchor_rank_strata.py`](../computations/verify_n8_support15_edge37_anchor_rank_strata.py).

## 1. Tensor-rank classification

For vectors `a_0,a_1` and `b_0,b_1`, a sum of two pure tensors satisfies

\[
                    a_0\otimes b_1+a_1\otimes b_0=0    \tag{2}
\]

only in the following cases:

* `a_0=a_1=0`;
* `b_0=b_1=0`; or
* both pairs span lines, say `a_i=alpha_i a` and
  `b_i=beta_i b`, with
  `alpha_0 beta_1+alpha_1 beta_0=0`.

Indeed, if `a_0,a_1` are independent, applying the two dual coordinate
functionals to (2) gives `b_0=b_1=0`; the other side is symmetric.  If
neither pair is independent and neither side vanishes, both span lines and
the scalar relation follows.  The checker exhausts all `3^8=6561` choices
of four two-vectors with entries in `{-1,0,1}`, including every zero-vector
degeneration, as an exact sign calibration.

At edge `37`, write the cubic endpoint anchors on `72,75` as

\[
                   A_{72}=u_0\otimes e_a,
                   \qquad A_{75}=u_1\otimes e_b.       \tag{3}
\]

For an arbitrary cap `K`, put

\[
 a_i=u_i^TKM_0,\qquad b_i=u_i^TKM_1.                  \tag{4}
\]

Then (1) is literal, up to the fixed coordinate factors at sites `2,5` and
the nonzero residual multiplier `A_46`.

For a rank-one cap `K=xy^T`, (1) becomes

\[
 F=2(u_0\cdot x)(u_1\cdot x)
       (y^TM_0)\otimes(y^TM_1).                       \tag{5}
\]

Thus an active rank-one zero exists whenever one of the following holds,
with the chosen vector also avoiding the direct-scalar hyperplane:

* `ker(u_i)` meets the all-coordinate torus;
* a left kernel of `M_j` meets that torus.

A hyperplane `ker(u_i)` meets the torus precisely when `u_i` is not a
coordinate vector.  This is the first positive rank stratum.

## 2. Exact-source anchor placement

At the degree-four endpoint `3`, the four incident roles are

```text
direct=37,  M0=30,  M1=31,  shared=35.
```

At least three are anchors, so there are only five placements: all four are
anchors, or exactly one of the four is not.  If `direct` is not an anchor,
the other three are; in particular both `M0,M1` are anchors.  If `direct`
is an anchor and both `M0,M1` are anchors, the same conclusion holds.  These
are three of the five placements.

Two anchored response blocks fix coordinate colours on both residual shores,
so (1) is the scalar pulled-back permanent

\[
 (u_0^TKv_0)(u_1^TKv_1)+(u_0^TKv_1)(u_1^TKv_0),       \tag{6}
\]

which has a target-active zero by the complete rank-case argument at support
14.

In either remaining placement, exactly one response block is not an anchor.
Assume by symmetry

\[
                  M_0=w\otimes e_d,\qquad M_1=M.       \tag{7}
\]

Put `x_i=u_i^TK`.  Removing the fixed `e_d` factor turns (1) into

\[
 F=\big((x_0w)x_1+(x_1w)x_0\big)M.                    \tag{8}
\]

If an external `u_i` is noncoordinate, (5) supplies an active zero through
`ker(u_i)`.  In the one-anchor placement the direct edge is itself an anchor,
so its near vector is the third coordinate vector; it cannot be proportional
to this noncoordinate `u_i`, and the direct scalar can be avoided.  If `w`
is noncoordinate, choose the rank-one right vector in `ker(w)` instead.
If a left kernel of `M` meets the torus, use that kernel in (5).

It remains to take

\[
                 u_0=e_0,\quad u_1=e_1,
                 \quad w=e_0                         \tag{9}
\]

up to exchanging the two external colours.  Write the first two rows of
`K` as

\[
                  x_0=(a,b,c),\qquad x_1=(d,e,f).
\]

The row before multiplication by `M` in (8) is

\[
                         g=(2ad,ae+bd,af+cd).           \tag{10}
\]

The active conditions include `ae != 0`; the third diagonal and direct
scalar can be chosen independently.

The attainable projective `g` are exactly all points except `[0:0:1]`.
If `g_0 != 0`, choose nonzero `a,e`, solve `d=g_0/(2a)`, and then solve for
`b,c,f`.  If `g_0=0` and `g_1 !=0`, take `d=0` and `e=g_1/a`.  Consequently:

* if `rank(M)<=1`, its left kernel has dimension at least two and contains
  an attainable `g`, so an active zero exists;
* if `rank(M)=2`, an active zero exists unless
  `ker_left(M)=span(e_2)`; and
* if `rank(M)=3`, an active zero does not exist.

In the last two exceptional cases, `FM=0` forces `g_0=g_1=0`.  The exact
projective Nullstellensatz/saturation certificate is

\[
 2(ae)^2=2(ae)(ae+bd)-(be)(2ad).                       \tag{11}
\]

Thus `g_0=g_1=0` forces `(ae)^2=0`, contradicting activity.  Equation (11)
is checked as a formal polynomial identity.

## 3. A source-anchor-compatible guard and its first mixed failure

The exceptional stratum is not an artefact of incompatible local anchors.
Put the identity matrix on the sole declared non-anchor edge `13`.  Put one
unit diagonal coordinate cell, with the indicated colour, on every other
support edge:

```text
colour 0: 03 16 24 27 45
colour 1: 01 02 35 46 57
colour 2: 04 12 37 56
nonanchor identity: 13.
```

Every cubic vertex sees the three distinct anchor colours.  Every
degree-four vertex also sees all three colours among its coordinate anchor
edges.  At `37`, the data are precisely (9), `M_0=e_0e_0^T`, `M_1=I`, and
the direct cell has colour two; hence the invertible exceptional stratum and
certificate (11) apply.

The three pure target coefficients are already exactly one, each with its
unique matching:

```text
colour 0: 03|16|27|45
colour 1: 02|13|46|57
colour 2: 04|12|37|56.
```

So pure normalization and all forced anchor placements do not remove the
local obstruction.  The complete mixed system does: there are eleven mixed
words with a unique supported matching.  The lexicographically first is

\[
 00000101,qquad 03\mid16\mid24\mid57,                 \tag{12}
\]

with coefficient one instead of the required zero.

This guard is deliberately not an exact source.  It identifies the first
missing theorem precisely: prove that every arbitrary-coefficient realization
of the two exceptional coordinate strata retains an uncancellable complete
mixed fibre, or show that mixed-row cancellation deforms it into one of the
positive rank strata above.

## 4. Reproduction

```sh
python3 computations/verify_n8_support15_edge37_anchor_rank_strata.py
python3 -O computations/verify_n8_support15_edge37_anchor_rank_strata.py
python3 -I -S computations/verify_n8_support15_edge37_anchor_rank_strata.py
```

The frozen ledger digest is
`c439c1690057b817a7290c9f6d424ca3c0ada704ccfffd1a998fb97d72dfdc8f`.
