# Exact K4 vertex-expansion equations and the `K_(3,2)` obstruction

## Outcome

Replace one vertex of the standard four-site qutrit GHZ construction by an
odd set `C` and retain the other three K4 vertices as terminals
`u_0,u_1,u_2`.  Suppose the proposed gadget is required to have

1. an exact one-cross copy signature in each color, and
2. zero total three-cross sector.

For `|C|=5`, the three one-cross identities are **exactly equivalent** to
the still-open arbitrary-matrix six-site problem: merging the terminals
produces `H_6=Delta_(6,3)`, and conversely splitting the columns at one
vertex of any six-site realization produces the three copy signatures.
Thus terminal merger is a sharp characterization, not by itself an
obstruction.

The extra equation `T_3=0` is the only genuinely new constraint in the full
copy-then-cancel ansatz.  Contracting its three terminal slots gives a
compact five-party quartic equation recorded below.  Numerical searches of
both the full and contracted systems find only the familiar two-color
finite basin and a divergent three-color border, but this does not prove
the full ansatz impossible.

There is, however, an exact unconditional obstruction to the six-edge
`K_(3,2)` support used by the original search.  After terminal merger its
support is `K_(3,3)`; contracting one shore would equate a `3 by 3` vector
permanent with ternary GHZ, which is impossible.

## 1. Exact aggregate equations

Let

\[
 C=\{0,1,2,3,4\},\qquad U=\{u_0,u_1,u_2\},
 \qquad V_v\cong\mathbb C^3.                              \tag{1}
\]

Put arbitrary aggregate matrices

\[
 X_{ab}\in V_a\otimes V_b\quad(a,b\in C),\qquad
 B^{(r)}_c\in V_c\otimes V_{u_r}\quad(c\in C).           \tag{2}
\]

No rank, symmetry, support, or coordinate condition is imposed.  For
`c in C`, write

\[
 P_c=H_{C\setminus\{c\}}(X)\in
       \bigotimes_{a\in C\setminus\{c\}}V_a.             \tag{3}
\]

Restoring the missing slot `c`, the sector in which exactly one edge crosses
from `C` to `U` and ends at `u_r` is

\[
 K_r=\sum_{c\in C}P_c\otimes B^{(r)}_c
       \in \left(\bigotimes_{a\in C}V_a\right)\otimes V_{u_r}.
                                                                    \tag{4}
\]

There are `5*3=15` matching terms in each `K_r`.  An exact color-copy
signature is the tensor identity

\[
 \boxed{K_r=e_r^{\otimes C}\otimes e_r^{(u_r)}}
 \qquad(r=0,1,2).                                         \tag{5}
\]

The total three-cross sector is

\[
 T_3=\sum_{\substack{c_0,c_1,c_2\in C\\\text{distinct}}}
 X_{de}\otimes B^{(0)}_{c_0}\otimes B^{(1)}_{c_1}
                  \otimes B^{(2)}_{c_2},                 \tag{6}
\]

where `{d,e}=C\setminus\{c_0,c_1,c_2\}` and all eight tensor slots are
restored to their natural order.  Equation (6) has `5*4*3=60` terms.  The
copy-then-cancel ansatz asks additionally for

\[
                              T_3=0.                       \tag{7}
\]

To see that these are precisely the K4 expansion equations, put
`E_(rr)=e_r tensor e_r` on the old terminal edge joining the two terminals
other than `u_r`.  Every perfect matching of `C disjoint-union U` crosses
the odd cut `C|U` either once or three times.  Hence

\[
 H_{C\sqcup U}=
 \sum_{r=0}^2 K_r\otimes E_{rr}^{(U\setminus\{u_r\})}+T_3. \tag{8}
\]

Equations (5) and (7) make (8) exactly `Delta_(8,3)`.

## 2. Terminal merger is exactly the six-site problem

Linearity in the star of one vertex gives both directions.

**Lemma 2.1 (terminal merger).**  Let `C` have odd cardinality, keep one
common family of internal matrices `X`, and suppose three boundary families
`B^(r)` satisfy (5).  Identify the three terminal spaces with one new color
space `V_star` and define

\[
             A_{c\star}=\sum_{r=0}^2 B^{(r)}_c
             \in V_c\otimes V_\star.                      \tag{9}
\]

Then

\[
                       H_{C\sqcup\{\star\}}(X,A)
                         =\Delta_{|C|+1,3}.                \tag{10}
\]

**Proof.**  Every perfect matching of `C union {star}` contains a unique
edge `c star`.  Expanding by that edge and using (3) gives

\[
\begin{aligned}
 H_{C\sqcup\{\star\}}(X,A)
 &=\sum_{c\in C}P_c\otimes A_{c\star}\\
 &=\sum_{c\in C}P_c\otimes\sum_{r=0}^2B^{(r)}_c\\
 &=\sum_{r=0}^2K_r
  =\sum_{r=0}^2e_r^{\otimes(C\sqcup\{\star\})}.
\end{aligned}                                             \tag{11}
\]

This is (10).  No statement about the three-cross tensor was used. `QED`

The converse is equally important.

**Lemma 2.2 (terminal-column split).**  Suppose arbitrary matrices `X` and
`A_(c star)` satisfy

\[
                         H_{C\sqcup\{\star\}}(X,A)
                            =\Delta_{|C|+1,3}.             \tag{12}
\]

Let `pi_r` be the coordinate projection on `V_star` with
`pi_r(e_s)=delta_(rs)e_r`, and set

\[
              B_c^{(r)}=(id_{V_c}\otimes\pi_r)A_{c\star}.\tag{13}
\]

After replacing `V_star` by the identified copy `V_(u_r)`, these boundary
families obey (5), and `sum_r B_c^(r)=A_(c star)`.

**Proof.**  The matching tensor is linear in all matrices incident with
`star`.  Applying `id tensor pi_r` to (12) therefore gives

\[
 \sum_cP_c\otimes B_c^{(r)}
   =(id\otimes\pi_r)\Delta_{|C|+1,3}
   =e_r^{\otimes C}\otimes e_r.                           \tag{14}
\]

The sum assertion is `sum_r pi_r=id`. `QED`

**Corollary 2.3 (exact equivalence).**  For `|C|=5`, equations (5) have a
solution if and only if arbitrary aggregate matrices on six vertices can
satisfy `H_6=Delta_(6,3)`.

This is why the merger observation cannot be cited as an unconditional
complex obstruction: the arbitrary six-site radical problem is one of the
open cores of the conjecture.  More generally, an exact copy gadget on an
odd `C` already contains a realization at the smaller even order `|C|+1`;
a vertex-expansion bootstrap cannot jump over that order.

There is also an exact parametrization of the freedom in the boundary
families.  Let

\[
 \mathcal L_X((D_c)_c)=\sum_cP_c\otimes D_c              \tag{15}
\]

be the boundary map.  Given a solution of (5), merge it to `A=sum_rB^(r)`
and let `S_r(A)` be the column split (13).  Then

\[
 B^{(r)}=S_r(A)+Z_r,qquad
 Z_r\in\ker\mathcal L_X,qquad \sum_rZ_r=0.              \tag{16}
\]

Conversely every choice in (16) preserves the three copy identities.  Thus
the full problem is precisely: find a six-site solution and three
zero-sum boundary syzygies for which the cubic expression (6) vanishes.

## 3. A necessary contracted `T_3` equation

For each color, contract its own boundary family against its target
terminal covector:

\[
 b_{c,r}=(id_{V_c}\otimes e_r^*)B_c^{(r)}\in V_c.        \tag{17}
\]

Contracting (5) gives three five-party identities

\[
             \boxed{\sum_{c\in C}P_c\otimes b_{c,r}
                         =e_r^{\otimes C}}
             \qquad(r=0,1,2).                            \tag{18}
\]

Contracting (7) at terminal colors `(0,1,2)` gives the quartic condition

\[
 \boxed{
 Q_X(b^0,b^1,b^2)=
 \sum_{\substack{c_0,c_1,c_2\in C\\\mathrm{distinct}}}
 X_{de}\otimes b_{c_0,0}\otimes b_{c_1,1}
             \otimes b_{c_2,2}=0,}                     \tag{19}
\]

again with `{d,e}` the complementary pair and all five slots restored.
Equations (18)--(19) use ten arbitrary internal matrices and fifteen local
vectors, or `135` complex scalar variables before gauge.  They are a
necessary subsystem of the full `225`-variable equations (5)--(7).  If the
boundary families have only their target terminal columns, (19) is also
equivalent to the full tensor equation `T_3=0`.

## 4. Exact obstruction to the original `K_(3,2)` search

The script `computations/search_vertex_expansion_gadget.py` designates three
vertices of `C` as color interfaces and two as internal vertices.  It keeps
only the six interface--internal matrices.  Its equation

\[
 H_{C\setminus\{r\}}=e_r^{\otimes4}                       \tag{20}
\]

combined with a coordinate edge `E_(rr)` from interface `r` to `u_r` is
exactly (5).  Because there is no edge between the two internal vertices,
the three-cross sector vanishes termwise.

After merging the terminals, the six-site support has bipartition

\[
 L=\{0,1,2\},\qquad R=\{3,4,\star\},                      \tag{21}
\]

and contains precisely all nine edges of `K_(3,3)`: the six searched
interface--internal edges and the three coordinate edges `r star`.

**Theorem 4.1.**  The system searched by
`computations/search_vertex_expansion_gadget.py` has no finite complex
solution.

**Proof.**  If it had a solution, terminal merger would give
`H_(K_(3,3))=Delta_(6,3)`.  Contract the three `L` slots against covectors
whose three coordinates are all nonzero.  Since the graph has no edges
inside either shore, its six perfect matchings become a `3 by 3` vector
permanent on the three remaining spaces.  The contracted target is

\[
 \sum_{r=0}^2\left(\prod_{i\in L}x_i(e_r)\right)e_r^{\otimes R}.\tag{22}
\]

a three-term diagonal tensor with every coefficient nonzero.  The
vector-permanent obstruction in `notes/determinant-split-route.md` proves
that these tensors cannot be equal. `QED`

This proof keeps all six searched edge matrices arbitrary and asymmetric;
only the three fixed interface edges are coordinate, exactly as in the
script.

## 5. Numerical diagnostics for the full equations

The full optimizer
`computations/search_full_vertex_expansion_gadget.py` retains all ten
internal and all fifteen boundary matrices.  Its analytic-gradient audit
passes to about `1e-9` relative error.  Four generic simultaneous starts
converged to squared residual `1`, with two copy sectors exact to numerical
precision, the third of squared error `1`, and negligible three-cross
error.  When the three-cross penalty is removed, attempts to improve all
three copies run to a border: one representative reached total copy error
`0.00516` only at edge norm `375.5`, while `||T_3||^2` grew to
`5.36e17`.

The smaller necessary-system optimizer
`computations/search_reduced_vertex_expansion_gadget.py` implements
(18)--(19) with an independently checked analytic adjoint.  Its first two
generic starts likewise converged to squared residual `1`: two equations in
(18) were exact to about `1e-10` or better, the third had squared error
`1`, and (19) was below `1e-15`.  These are discovery diagnostics only.
They support neither an exact obstruction nor a counterexample.

## 6. Sharp limitation

The full arbitrary-matrix copy-then-cancel system (5)--(7) remains open.
The exact progress is:

1. its one-cross half is equivalent to the six-site problem;
2. its new content is isolated in the boundary-syzygy cubic (6);
3. every solution must satisfy the much smaller equations (18)--(19); and
4. the original automatic-cancellation `K_(3,2)` support is impossible.

None of this rules out a more general eight-site realization in which the
one-cross sector itself is not equal to the three GHZ terms and cancels
against `T_3`.  Closing (18)--(19) independently of the open six-site
radical problem would close the proposed full vertex-substitution route.

The exact smoke audit
`computations/verify_vertex_expansion_merger.py` checks (8), (11), and the
matching counts `45+60=105` coefficientwise over the integers for arbitrary
deterministic matrices.
