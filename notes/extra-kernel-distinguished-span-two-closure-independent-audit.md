# Independent audit of the distinguished-span-two closure

## 1. Verdict

The theorem in
[`extra-kernel-distinguished-span-two-closure.md`](extra-kernel-distinguished-span-two-closure.md)
is **confirmed**.  Its hypothesis is only

\[
 \dim\operatorname {span}\{[K_{cd}]:c\ne d\}=2,        \tag{A1}
\]

not `dim E_q=2`.  The distinction is material: the common internal
quadratic may have unrelated extra Hessian-kernel classes.  I traced every
invoked proof after replacing its nominal two-dimensional codomain by the
distinguished image in (A1).  No step uses a complementary class in
`E_q`, so the replacement is valid.

The proof has four independent gates:

1. (A1) and dense rows give a row/column-avoiding relation four-plane.
2. If all rank-three edges are dead, the exact product geometry and the
   diagonal cap equations contradict each other.
3. A live edge is necessarily invertible at all four local star matrices;
   the singular fixed-line closures cover every possible physical rank.
4. Live propagation gives a literal zero-star boundary vertex unless the
   whole internal set is local-full, and the full pair equations exclude
   that case.

The final same-support bilinear construction works for every complex
`3 by 3` direct block.  Its normalization gives exactly a pure
three-cross selector, with no division by a possibly zero direct entry.

## 2. Hypothesis ledger

Let `W` be the internal even set, let `q` be its quadratic, and use

\[
 \mathcal H_q(p_cs_d)+a_{cd}Q=\delta_{cd}X_c,
 \qquad
 K_{cd}=p_cs_d+(a_{cd}/r)q.                            \tag{A2}
\]

The following ledger records where each assumption is consumed.

| hypothesis | first use | not used for |
|---|---|---|
| connected, spanning `G_3(q)` | propagation of vertex-gauge scalars | existence of `D_pq` |
| nonbipartite `G_3(q)` | killing the alternating vertex weights | selector normalization |
| all six rows supported at three or more sites | one-product injectivity and all-dead product closure | singular local classification |
| `dim D_pq=2` | four-dimensional kernel in `Z_0` | any claim about all of `E_q` |
| all nine equations (A2) | row/column independence, all-dead cap bound, local-full contradiction | fixed-line incidence algebra |
| characteristic zero / `C` | zero-sum gauge scalar and bilinear root choice | matching-sector split |

The proof does not assume endpoint symmetry, positivity, a simple source
graph, invertibility of the direct block, or injectivity of `II_q` or
`III_q`.

## 3. Re-derivation of the relation four-plane

Fix a second colour index `d`, and suppose the two classes
`u_cd,u_ed`, with `{c,e,d}={0,1,2}`, are dependent.  Expanding their
representatives gives

\[
            (\mu p_c+\nu p_e)s_d+bq\in\mathcal G_q.    \tag{A3}
\]

On a rank-three edge, the product block on the left has rank at most two.
Thus its gauge coefficient on that edge is zero.  Connectedness and an odd
cycle make all vertex weights constant, and the zero-sum gauge
normalization makes the constant zero.  Hence (A3) is the literal product
identity `(mu p_c+nu p_e)s_d=0`.  Multiplication by `s_d`, which reaches
at least three sites, is injective on linear elements in characteristic
different from two.  Therefore `mu p_c+nu p_e=0`.

Both coefficients are nonzero.  Otherwise one dense row would be zero.
Thus `p_e=t p_c`.  The diagonal/off-diagonal pair equations in columns
`c` and `e` then put both `X_c` and `X_e` in `C Q`; when `Q=0` they are
zero.  Either result is impossible.  This proves column independence;
transposition of the two deleted endpoints proves row independence.

Now define

\[
 f:Z_0\longrightarrow D_{pq},\qquad
 f(M)=\sum_{c\ne d}m_{cd}u_{cd}.                      \tag{A4}
\]

Surjectivity follows from the definition of `D_pq`, so (A1) gives
`dim ker f=4`.  Independence in each named row and column gives

\[
             \ker f\cap R_c=\ker f\cap C_d=0.         \tag{A5}
\]

This derivation never invokes `dim E_q`.  In particular, defining `f`
with codomain `E_q` gives the same linear map and the same kernel because
its image is exactly `D_pq`.  This resolves the sole apparent hypothesis
mismatch in the older corank-two notes, whose theorem statements named a
two-dimensional `E_q` even though their proofs use only (A4)--(A5).

The endpoint orientation is also correct.  The block of `p_cs_d` on
`ij` is

\[
 p_{c,i}s_{d,j}^{\mathsf T}+s_{d,i}p_{c,j}^{\mathsf T}.
\]

Summing with coefficients `m_cd` gives

\[
 P_iMS_j^{\mathsf T}+S_iM^{\mathsf T}P_j^{\mathsf T},              \tag{A6}
\]

so no transpose or minus sign from the unrelated alternating-pencil
normalization has entered.

## 4. Dead/live exhaustion

Put `mathscr D=ker f`.  A relation in `mathscr D` is a vertex gauge after
adding its scalar multiple of `q`.  On a rank-three edge its physical
image therefore lies in the invertible line `C q_ij`.

### All edges dead

If every rank-three edge is dead, the same connected odd-cycle argument
used above kills both its scalar `q` coefficient and its vertex gauge.
Thus all four relations are literal relations among the six products
`p_cs_d`.  Row/column independence makes their product span exactly two.

I checked the scope of the three all-dead dependencies separately:

* the gauge-removal and cap-dimension sections of
  [`all-dead-corank-two-product-reduction.md`](all-dead-corank-two-product-reduction.md)
  use only the relation four-plane, six dense rows, and (A2);
* the ordinary-lift classification in
  [`all-dead-corank-two-product-geometry.md`](all-dead-corank-two-product-geometry.md)
  starts from the exact two-dimensional product span and (A5), not from
  the ambient Hessian quotient; and
* [`aligned-two-plane-boundary-closure.md`](aligned-two-plane-boundary-closure.md)
  handles both regular site partitions and all singular normalization
  patterns.

The `Q=0` branch is explicit: the diagonal products must map to three
independent targets, so their span modulo the two-space has dimension at
least three.  If `Q` is nonzero and lies in the target three-space, the
required quotient dimension drops by exactly one and is still too large
for the classified product geometry.  Thus no position of `Q` is omitted.

Consequently a rank-three edge is live.

### A live edge

For a live edge, let `L:Z_0 -> Mat_3` be (A6).  Since `mathscr D` has
codimension two and `L(mathscr D)` is a line,

\[
                             \operatorname {rank}L\le3.              \tag{A7}
\]

The evaluation/compression reduction gives only two outer-rank patterns:
all four outer matrices have rank three, or all four have rank two.  To
check that the second pattern is completely closed, enumerate the
physical ranks allowed by (A7):

* rank zero contradicts live;
* at rank one, `im L=Cq_ij`, but every coordinate generator of `L` is a
  sum of two rank-one matrices and hence singular; some generator must be
  nonzero, contradicting invertibility of `q_ij`;
* rank two is exactly
  [`rank-two-singular-fixed-line-obstruction.md`](rank-two-singular-fixed-line-obstruction.md);
* rank three is exactly
  [`rank-three-singular-fixed-line-obstruction.md`](rank-three-singular-fixed-line-obstruction.md).

The last two arguments first force both two-by-two kernel compressions to
one fixed nonzero rank-one line.  Their complete incidence lists include
all optional-zero degenerations.  The surviving crossed-kernel normal
form has identically singular physical image, so it cannot contain
`q_ij`.  There is no generic-rank assumption left over.  Hence all four
outer matrices at a live edge are invertible.

This audit does not invoke Section 7 of
[`singular-relation-block-reduction.md`](singular-relation-block-reduction.md),
the cubic `III_q`, or the projective matching
`u_cd parallel u_dc`.  Those are unnecessary routes to a common kernel.

## 5. Independent propagation check

At one live edge, normalize the two `P` matrices.  The live part of the
relation-space classification gives

\[
 \mathscr D=T_\Delta^{-1}(\mathbb C H),\qquad
 T_\Delta(M)=M\Delta+\Delta M^{\mathsf T},             \tag{A8}
\]

with `Delta` invertible diagonal and `H` invertible symmetric
zero-diagonal.  The ratio `d_d/d_c` is read from the restrictions of
`mathscr D^perp` to the opposite positions `cd,dc`; row/column avoidance
ensures that these restrictions are nonzero.  Therefore all live edges
have the same three-plane `ker T_Delta`.

Every member of this three-plane has zero physical block on every
rank-three edge, live or dead.  Connected odd-cycle gauge removal makes
the full quadratic relation literal.  At an invertible endpoint it reads

\[
             N(\Delta^{-1}S_k^{\mathsf T}-P_k^{\mathsf T})=0
                    \quad\text{for every skew }N.      \tag{A9}
\]

Taking the three elementary skew matrices shows column by column that
the parenthesis vanishes.  Hence `S_k=P_k Delta` at every internal site.
One complementary relation then gives

\[
                         P_iHP_j^{\mathsf T}
                          =(\beta_i+\beta_j)q_{ij}.     \tag{A10}
\]

Let `U={i:det P_i != 0}`.  It is nonempty and in fact contains a live
edge.  Equation (A10) makes every pair in `U` a live rank-three edge.  On
a rank-three edge from `U` to its complement, the right side could have
rank three only if its scalar were nonzero, while the left side has rank
below three.  The scalar is therefore zero; invertibility at the `U`
endpoint then forces the other `P` matrix, and hence its `S` matrix, to
vanish.

If `U` is proper, graph connectedness supplies such a crossing edge and
the desired zero site.  If `U` is all of `W`, normalization gives one
common symmetric block `q_ij=w_ijH`.  The off-diagonal equations annihilate
the zero-diagonal symmetric colour subspace modulo `C Q`.  Under `SO(H)`,
that subspace contains the invariant line and a nonzero vector in the
irreducible trace-free five-space, so it generates all of `Sym^2 C^3`.
The diagonal equations would then put three independent targets on one
line.  This is impossible.  Thus the zero site is forced.

## 6. Direct-block and selector audit

It remains to verify a step not present in the older propagation theorem:
an arbitrary direct matrix admits the required covectors.

If `A_hh=0`, the singleton choice `xi=eta=e_h` works.  Otherwise every
diagonal entry is nonzero.  On any two-coordinate principal block write

\[
 A_S=\begin{pmatrix}a&b\\c&d\end{pmatrix},\qquad ad\ne0.
\]

For `xi=(1,t)` and `eta=(1,u)`, the bilinear value is

\[
                       a+ct+(b+dt)u.                   \tag{A11}
\]

Over `C`, choose nonzero `t` outside the roots of the two nonzero affine
polynomials `a+ct` and `b+dt`, then take
`u=-(a+ct)/(b+dt)`.  Both coordinates of both vectors are nonzero and
(A11) vanishes.  This proves the same-support assertion for every matrix,
including zero, singular, monomial, and invertible matrices.

At the zero site, `P_i=S_i=0` is equivalent to the literal aggregate
equalities `A_pi=A_qi=0`; it is not merely a vanished selected row.  Let
`h` belong to the common support and set

\[
                 \theta=(\xi_h\eta_h)^{-1}e_h^*.
\]

Then `(xi tensor eta tensor theta)(e_c tensor e_c tensor e_c)` is
`delta_hc`.  The three one-crossing terms correspond to the three shore
edges.  The two terms using `pi` and `qi` vanish literally, and the term
using `pq` has scalar `xi^T A_pq eta=0`.  Thus the entire one-crossing
sector, not merely its target projection, is killed.  Since a perfect
matching crosses a three-vertex cut one or three times, contracting the
full target leaves exactly `e_h^(tensor Y)` in the three-crossing sector.
This confirms every assertion in the selector corollary.

## 7. Scope and computational audit

The result converts, but does not by itself contradict, the dense
distinguished-span-two E1 branch.  The remaining E1 cases are a row of
site support at most two and distinguished span at least three.
Disconnected, nonspanning, or bipartite rank-three graphs lie outside the
theorem's connected-spanning-nonbipartite hypothesis and still require
separate treatment inside E1; they are not an additional live taxonomy.

The next equation packet must retain all 27 contractions on the common
complement of the selected triple.  The selector is only one product-
covector combination of that packet; an abstract response table would
forget the shared `q` powers and the three physical star families.

Running

```text
python3 computations/verify_extra_kernel_distinguished_span_two_closure.py
```

checks the bilinear construction over every `3 by 3` matrix with entries
in `{-1,0,1}`, the target normalization and one-cross coefficient, and
the one/three crossing partition of all perfect matchings at orders six
and eight.  The seven pre-existing exact relation-space verifiers also
pass independently; they are evidence for their coordinate ledgers, while
the uniform implications above are the proof.
