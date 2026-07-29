# Cancellation-aware propagation of a missing star row

## 1. Outcome

The missing-row branch of the all-even pair trichotomy is not inert once the
actual mixed two-deletion equations are retained.  Fix deleted vertices
`p,q`, suppose the internal source Hessian is gauge-rigid, and let `G_3` be
the graph of rank-three internal blocks.  If a color row from `p` vanishes
at one internal site, then along every `G_3` boundary edge it has only two
possible continuations:

* the same row vanishes at the neighboring site; or
* all two off-color rows from `q` vanish at the original site.

On a connected `G_3`, this gives an exact dichotomy.  Either a boundary
site becomes a support hole or an active coordinate anchor into `q`, or the
zero row propagates through every internal site.  In the latter case the
row at `p` has a unique direct `(c,c)` cell on `pq`, and the complementary
matching tensor is a nonzero pure color-`c` tensor.  Thus one obtains a
clean one-color selector, not merely another support zero.

This is cancellation-aware: it is derived from the complete off-diagonal
pair equations and the rank-three/gauge quotient, not from individual
matching monomials.  The positive `K_8` model of
[`all-pair-missing-row-countermodel.md`](all-pair-missing-row-countermodel.md)
violates exactly the required mixed equation.  Embedded binary cancellation
examples lie outside the rank-three hypothesis, so they do not contradict
the lemma.

## 2. Oriented pair equations

Use the notation of
[`source-hessian-bipartite-rankdrop.md`](source-hessian-bipartite-rankdrop.md).
In particular, all blocks are oriented toward their named first endpoint:

\[
 A_{p\mid i}\in V_p\otimes V_i,
 \qquad A_{q\mid i}\in V_q\otimes V_i,
 \qquad A_{p\mid q}\in V_p\otimes V_q.                  \tag{1}
\]

On the even internal set `W=B\setminus{p,q}`, write

\[
 p_c=\sum_{i\in W}p_{c,i},\quad
 p_{c,i}=(e_c^*\otimes\operatorname{id})A_{p\mid i},
 \qquad
 s_d=\sum_{i\in W}s_{d,i},\quad
 s_{d,i}=(e_d^*\otimes\operatorname{id})A_{q\mid i}.    \tag{2}
\]

Let `q_0` be the internal quadratic, put

\[
 Q={q_0^r\over r!},\qquad
 \mathcal H_{q_0}(Z)={Zq_0^{r-1}\over(r-1)!},
 \qquad |W|=2r,                                          \tag{3}
\]

and let `a_cd=A_(p|q)(c,d)`.  The exact two-deletion equations are

\[
 \boxed{\quad
 \mathcal H_{q_0}(p_cs_d)+a_{cd}Q
       =\delta_{cd}X_c,
 \qquad X_c=\bigotimes_{i\in W}e_c^{(i)}.
 \quad}                                                   \tag{4}
\]

Assume `q_0` is gauge-rigid.  As proved in Lemma 3.1 of the cited note,
the off-diagonal equations in (4) imply, for every `c != d` and every
`ij in G_3(q_0)`,

\[
 p_{c,i}\otimes s_{d,j}+s_{d,i}\otimes p_{c,j}=0.         \tag{5}
\]

The rank comparison producing (5) is exact: before it vanishes, its left
side is a sum of two simple tensors and hence has rank at most two, while a
nonzero scalar multiple of the internal block has rank three.

## 3. Boundary propagation

For a fixed deleted endpoint `p` and color `c`, define the literal zero set

\[
                   Z_c(p)=\{i\in W:p_{c,i}=0\}.           \tag{6}
\]

No quotient or support convention is hidden in (6): it means all three
entries of that endpoint row are zero.

**Lemma 3.1 (zero-row boundary propagation).**  Suppose `q_0` is
gauge-rigid and (4) holds.  If

\[
 i\in Z_c(p),\qquad ij\in G_3(q_0),\qquad j\notin Z_c(p),\tag{7}
\]

then

\[
                         s_{d,i}=0\qquad(d\ne c).         \tag{8}
\]

Equivalently, the opposite deleted-star block has the form

\[
                         A_{q\mid i}=e_c\otimes v_i       \tag{9}
\]

for some `v_i in V_i`, including the possibility `v_i=0`.

**Proof.**  Put `p_(c,i)=0` in (5).  For every `d != c` it becomes

\[
                         s_{d,i}\otimes p_{c,j}=0.        \tag{10}
\]

The second factor is nonzero by (7), and a simple tensor over a field is
zero only when one factor is zero.  Hence (8).  Formula (9) is exactly the
row-wise restatement.  \(\square\)

If `v_i !=0`, reversing the endpoint order in (9) gives

\[
                         A_{i\mid q}=v_i\otimes e_c.      \tag{11}
\]

Thus `iq` is a directed color-`c` anchor into `q`.  In an entry-minimal
source its complementary tensor is nonzero, so it is tensor-active.  If
`v_i=0`, (9) is an actual zero underlying block.  This is where activity is
used: the two alternatives are an active anchor or a literal support hole,
not an inactive nonzero decoration.

## 4. Connected propagation or a pure selector

**Theorem 4.1 (anchor/hole or clean selector).**  Suppose
`H_B(A)=Delta_(B,3)`, the source is entry-minimal, `q_0` is gauge-rigid,
and `G_3(q_0)` is connected.  If `Z_c(p)` is nonempty, exactly one of the
following conclusions holds.

1. `Z_c(p)` is a nonempty proper subset of `W`, and there is a boundary
   site `i in Z_c(p)` for which `A_(q|i)` has the form (9).  It is either
   zero or is a tensor-active directed color-`c` anchor from `i` into `q`.
2. `Z_c(p)=W`, and the complete color-`c` row at `p` consists of one cell:
   
   \[
    A_{p\mid q}(c,d)=0\ (d\ne c),\qquad
    A_{p\mid q}(c,c)\ne0,                                \tag{12}
   \]
   
   while the complementary tensor is pure,
   
   \[
        H_W(A)=Q=A_{p\mid q}(c,c)^{-1}X_c.               \tag{13}
   \]

Conclusion 2 is a clean color-`c` selector: the sole cell in (12) is
tensor-active and its full cofactor is the nonzero tensor (13).

**Proof.**  If `Z_c(p)` is a nonempty proper subset of the vertex set of
the connected graph `G_3(q_0)`, it has a boundary edge `ij` as in (7).
Lemma 3.1 gives conclusion 1.

Otherwise `Z_c(p)=W`, so `p_c=0`.  The `(c,d)` equations in (4) reduce to

\[
                         a_{cd}Q=\delta_{cd}X_c.          \tag{14}
\]

The diagonal equation shows `a_cc !=0` and gives (13).  Hence `Q!=0`, and
the off-diagonal equations give `a_cd=0` for every `d != c`.  Together
with `p_(c,i)=0` on all internal sites, this is (12).  The nonzero direct
cell has the nonzero full cofactor `Q`, so it is active independently of
minimality.  \(\square\)

The two conclusions concern respectively a proper zero set and the full
zero set, so they are mutually exclusive.  A coordinate anchor may of
course exist elsewhere also in the selector branch; it is not the boundary
witness asserted in conclusion 1.

**Corollary 4.2 (two colors cannot propagate cleanly).**  Under the same
hypotheses, suppose `Z_c(p)` and `Z_e(p)` are nonempty for two distinct
colors.  If neither zero set has a boundary anchor/hole of its own color,
then both equal `W`, and (13) would make the same nonzero tensor `Q`
proportional to the independent tensors `X_c` and `X_e`, a contradiction.
Thus at least one of the two colors forces the additional opposite-star
zero rows in conclusion 1.

## 5. Iterative form and exact scope

Lemma 3.1 can be used as a breadth-first propagation rule.  Start with a
literal zero `p_(c,i)=0`.  Across a rank-three edge, either add the neighbor
to `Z_c(p)`, or record that the original site has both off-color `q` rows
zero.  On a connected rank-three graph this process terminates only at the
active-anchor/support-hole boundary or at the pure selector (12)--(13).

The hypotheses cannot be dropped silently.

* Without gauge rigidity, the off-diagonal product can lie in an extra
  Hessian-kernel direction rather than vanish blockwise.
* Without a rank-three internal edge, a rank-two product can equal a
  nonzero multiple of the internal block.  In particular every ordinary
  binary cancellation source embedded in three colors has all block ranks
  at most two, so `G_3` is empty.
* Without the mixed equation, the rank-one block in (10) need not vanish.
  Section 6 audits this failure exactly in the positive `K_8` model.

The theorem produces a one-color clean selector, not yet a nondegenerate
three-color pair cap.  The required overlap is now supplied by
[`zero-row-globalization-rankgraph.md`](zero-row-globalization-rankgraph.md):
in a 2-connected global rank-three graph, a boundary site has a second
rank-three neighbor, and deleting that neighbor makes the forced anchor
simultaneously rank at most one and rank three.  Thus gauge rigidity for
every pair and 3-connectivity of the global rank-three graph are jointly
impossible.

## 6. Exact adversarial audit

Take the normalized positive model of
[`all-pair-missing-row-countermodel.md`](all-pair-missing-row-countermodel.md)
and delete `p=0,q=1`.  Its internal six-site Hessian has exact modular rank
`130/135`, equal to the five-dimensional gauge upper bound.  Its rank-three
graph has edges

\[
                    25,\ 34,\ 36,\ 45                  \tag{15}
\]

and an isolated vertex `7`, so the global connected hypothesis fails.
Nevertheless the local boundary test already detects the missing mixed
equation.  With

\[
                 i=3,\quad j=6,\quad c=1,\quad d=0,       \tag{16}
\]

one has

\[
 p_{1,3}=0,\qquad
 p_{1,6}={1\over53}e_1,
 \qquad s_{0,3}=e_0,\qquad \operatorname{rank}(q_0)_{36}=3.\tag{17}
\]

Thus the left side of (5) at `36` is the nonzero block

\[
                         {1\over53}e_0\otimes e_1.        \tag{18}
\]

Correspondingly, the actual mixed output coefficient with colors

\[
                         (1,0,0,0,0,0,0,0)               \tag{19}
\]

is

\[
                              {20\over53}\ne0.            \tag{20}

\]

So the countermodel does not evade propagation by a subtle cancellation:
it fails the precise off-diagonal tensor equation used in the proof.

[`verify_zero_row_pair_propagation.py`](../computations/verify_zero_row_pair_propagation.py)
checks (15)--(20), the internal gauge-rigidity certificate, endpoint
orientation, and the rank-three/product-rank comparison exactly.
