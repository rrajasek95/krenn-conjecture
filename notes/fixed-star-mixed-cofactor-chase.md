# Mixed common cofactors: exact Koszul bridges and the rerouting chase

This note treats the branch left open by
`notes/fixed-star-common-cofactor-rigidity.md`.  It gives three exact
conclusions.

1. Modding out the three diagonal target lines produces a short exact
   sequence.  A quotient relation need not be a genuine star perturbation.
2. Every irreducible two-center quotient relation has an explicit Koszul
   normal form.  Following its defect to the other center either gives a
   support-preserving star perturbation or a nonzero two-cross rerouting
   tensor in a different color at the original vertex.
3. Coefficientwise, every such nonzero defect closes in an even cycle or in
   two odd cycles joined by a path.  These are all possible finite closures.

An actual binary hafnian source realizes the even-cycle alternative.  At
the first center its derivative atoms are independent, but at the two
defect endpoints they become dependent.  Thus second-center compatibility
does kill that particular countermodule, while also showing that the first
star quotient alone cannot do so.  The unresolved three-color branch is a
fully rerouted circuit for which every clean second-center lift is nonzero.

Throughout, `B` has even cardinality at least six,

\[
 H_B(A)=\Delta_{B,3}=\sum_{c=0}^2e_c^{\otimes B},           \tag{1}
\]

and all endpoint orders are retained.

## 1. The quotient-star exact sequence

Fix `p`, put `J=B\setminus\{p\}` and

\[
 C_j=H_{B\setminus\{p,j\}}(A),\qquad
 W=\bigotimes_{v\in J}V_v,\qquad
 D=\operatorname{span}\{g_0,g_1,g_2\},quad
 g_c=e_c^{\otimes J}.                                      \tag{2}
\]

Define the common-cofactor map

\[
 F_p:\bigoplus_{j\in J}V_j\longrightarrow W,\qquad
 F_p((x_j)_j)=\sum_jx_j^{(j)}\otimes C_j.                  \tag{3}
\]

If `u_c` is the vector whose `j`-component is the endpoint-`p` row
\((e_c^*\otimes\operatorname{id})A_{pj}\), the three star equations are
simply

\[
                         F_p(u_c)=g_c.                     \tag{4}
\]

Let `pi:W -> W/D` and `bar F_p=pi F_p`.  Replace the domain in (3) by the
coordinate subspace `U_*` spanned by atoms which occur in at least one
nonzero incident matrix entry, and keep the same notation for the
restriction.  The vectors `u_c` lie in `U_*`, so (4) gives the short exact
sequence

\[
 0\longrightarrow\ker F_p\longrightarrow\ker\bar F_p
   \mathbin{\mathop{\longrightarrow}^{F_p}}D
   \longrightarrow0.                                      \tag{5}
\]

Indeed, the kernel of the displayed map is `ker F_p`, and (4) makes it
surjective.  Consequently

\[
                 \dim\ker\bar F_p=\dim\ker F_p+3.          \tag{6}
\]

The three row vectors `u_c` can therefore account for all quotient
relations even when some `C_j` is mixed.  Entry-minimality only excludes a
vector in `ker F_p` supported on the nonzero cells of one fixed row `u_c`;
such a vector would give an affine perturbation of a single star row and
delete a cell.  It does not turn an arbitrary element of
\(\ker\bar F_p\) into an element of \(\ker F_p\).

## 2. Exact normal form for a two-center quotient circuit

The smallest possible mixed relation can nevertheless be classified.
The statement works for any number of colors.

**Lemma 2.1 (two-center diagonal bridge).**  Let `j != k`, let
`R=J\setminus\{j,k\}` be nonempty, and suppose nonzero vectors `x in V_j`,
`y in V_k` and tensors `C,E` satisfy

\[
 x^{(j)}\otimes C+y^{(k)}\otimes E
       =\sum_r\delta_r e_r^{\otimes J}.                    \tag{7}
\]

At most two of the scalars `delta_r` are nonzero.  For every color in their
support, at least one of `x,y` is proportional to that color axis.

If the right side is the single term `delta_a g_a`, then, after possibly
interchanging `j,k`, one has `x=alpha e_a` and there is a tensor `Z` on
`R` such that

\[
 E=e_a^{(j)}\otimes Z,\qquad
 \alpha C=\delta_a e_a^{(k)}\otimes e_a^{\otimes R}
                 -y^{(k)}\otimes Z.                        \tag{8}
\]

If its support is the two colors `a,b`, then, after interchanging the
centers and absorbing nonzero scalars, `x=alpha e_a`, `y=beta e_b`, and

\[
\begin{aligned}
 \alpha C&=\delta_a e_a^{(k)}\otimes e_a^{\otimes R}
                         -e_b^{(k)}\otimes Z,\\
 \beta E&=\delta_b e_b^{(j)}\otimes e_b^{\otimes R}
                         +e_a^{(j)}\otimes Z.               \tag{9}
\end{aligned}
\]

The two appearances of `Z` are the exact Koszul transfer.

**Proof.**  Quotient \(V_j\) by \(\mathbb Cx\) and \(V_k\) by
\(\mathbb Cy\), and apply both quotients to (7).  The tensors
\(e_r^{\otimes R}\) are independent, so for every `r` with
\(\delta_r\ne0\), either \(e_r\in\mathbb Cx\) or
\(e_r\in\mathbb Cy\).
Each of the two lines contains at most one coordinate axis.  This proves
the support assertion.

In the one-color case assume `x=alpha e_a`.  Quotienting only at `j` now
shows that `E` has the factor `e_a` at `j`; write it as in (8), substitute,
and cancel that factor.  In the two-color case the two distinct axes must
be assigned one to each center.  Quotienting at each center in turn leaves
the indicated diagonal term plus an arbitrary tensor in the killed axis.
Substitution shows that the two arbitrary tensors are negatives of one
another, giving (9). \(\square\)

If two terms from one row equation form a circuit after quotienting by
`D`, their lift has the form (7).  A zero right side would be a genuine
dependence among derivative atoms in that row and is forbidden at an
entry-minimal point.  Thus every entry-minimal two-center circuit carries
one of the nonzero diagonal bridges (8)--(9).

## 3. Following a one-color bridge to the second center

There is a particularly transparent lift when a whole row has only two
active neighbours.  It identifies exactly what can prevent a second-center
entry-minimality contradiction.

**Proposition 3.1 (clean lift or two-cross rerouting).**  Suppose the source
is entry-minimal.  Fix a color `c` and suppose the complete row-`c` support
at `p` is

\[
 r_{j,c}=\alpha e_c^{(j)},\qquad
 r_{k,c}=y=\sum_l b_l e_l^{(k)},\qquad
 r_{v,c}=0\quad(v\notin\{j,k\}),                           \tag{10}
\]

where `alpha != 0`.  Then (4) and Lemma 2.1 give a tensor `Z` on
`U=B\setminus\{p,j,k\}` with

\[
 C_k=e_c^{(j)}\otimes Z,\qquad
 \alpha C_j=e_c^{(k)}\otimes e_c^{\otimes U}
                         -y^{(k)}\otimes Z.                 \tag{11}
\]

For a scalar cell on `uv`, write its unweighted full derivative tensor as

\[
 T_{uv}^{a,b}=e_a^{(u)}\otimes e_b^{(v)}
                 \otimes H_{B\setminus\{u,v\}}(A).         \tag{12}
\]

For every `l != c` with `b_l != 0`, the following variation is supported
only on currently nonzero cells incident with the second center `k`:

\[
 \mathcal V_{k,l}=
 b_lT_{pk}^{c,l}+
 \sum_{u\in U}\sum_s A_{ku}(l,s)T_{ku}^{l,s}.              \tag{13}
\]

It has zero endpoint-`p` color-`c` slice.  More precisely, it is exactly
the differently colored two-cross rerouting tensor

\[
 \mathcal V_{k,l}=e_l^{(k)}\otimes
 \sum_{d\ne c}e_d^{(p)}\otimes
 \sum_{\substack{u\in U,\ v\notin\{p,k,u\}\\s,t}}
 A_{ku}(l,s)A_{pv}(d,t)
 e_s^{(u)}\otimes e_t^{(v)}\otimes
 H_{B\setminus\{p,k,u,v\}}(A).                           \tag{14}
\]

Consequently either \(\mathcal V_{k,l}=0\), contradicting entry-minimality,
or there is a nonzero rerouting sector which changes the color at `p` from
`c` to some `d != c`.

**Proof.**  Expand `C_j` at its vertex `k`.  With
\(D_u=H_{B\setminus\{p,j,k,u\}}\), the color-`l` row of (11) is

\[
 \sum_{u\in U}\sum_s A_{ku}(l,s)e_s^{(u)}\otimes D_u
 =\alpha^{-1}\delta_{lc}e_c^{\otimes U}
  -\alpha^{-1}b_lZ.                                        \tag{15}
\]

Now expand each full cofactor in the second sum of (13) at `p`.  In its
color-`c` slice, the removed vertex `k` makes the edge `pk` unavailable;
by (10), `p` is therefore forced onto `pj`.  That contributes the factor
\(\alpha e_c^{(p)}\otimes e_c^{(j)}\), and (15) shows that for
\(l\ne c\) the result is \(-b_lT_{pk}^{c,l}\).  This proves the asserted
cancellation of the color-`c` slice.

All remaining terms in the same cofactor expansions use a color
`d != c` at `p`; writing their second edge as `pv` gives (14).  If (13)
vanishes, it is a nontrivial dependence because `b_l != 0`.  Every varied
cell is incident with `k`, so no matching contains two varied cells and

\[
                 H_B(A+t\,\delta A)=H_B(A)+t\mathcal V_{k,l}
\]

exactly.  Choosing `t` to zero a cell contradicts entry-minimality.
\(\square\)

Thus the obstruction to lifting the first-star Koszul relation into a
genuine second-star perturbation is not mysterious: it is precisely the
two-cross tensor (14).  Repeating the chase changes colors and neighbors;
because there are finitely many decorated cells, any nonterminating chase
must close.

## 4. Exact classification of a closed coefficient chase

The closure can be described without choosing individual matching terms.
Fix any mixed coloring `z` of `B`.  On every underlying edge put

\[
 w_{uv}=A_{uv}(z_u,z_v),\qquad
 q_{uv}=H_{B\setminus\{u,v\}}(z|_{B\setminus\{u,v\}}),
 \qquad x_{uv}=w_{uv}q_{uv}.                               \tag{16}
\]

Expansion of the zero target coefficient at each vertex gives

\[
                    \sum_{u\ne v}x_{uv}=0
                    \qquad(v\in B).                       \tag{17}
\]

Fix \(l\ne c\) with \(b_l\ne0\), choose any nonzero coefficient of the
transfer tensor `Z` in (11), and extend its coloring by
\(z_p=z_j=c,z_k=l\).  The resulting full coloring is mixed, and

\[
 x_{pk}=b_lZ(z_U)\ne0,\qquad x_{pj}=-b_lZ(z_U),           \tag{18}
\]

and (17) forces the defect to leave both other endpoints.

**Lemma 4.1 (finite rerouting circuits).**  Over characteristic different
from two, every nonzero coordinate of a solution of (17) belongs to a
support-minimal solution whose graph is exactly one of:

1. an even cycle, with alternating nonzero coefficients; or
2. two odd cycles joined by a path, where the path may have length zero.

In the second case the coefficients alternate on each odd cycle and on the
joining path; the path magnitude is twice the cycle magnitude, up to the
endpoint signs.

**Proof.**  Choose a kernel vector containing the prescribed coordinate
with inclusion-minimal support.  It is a circuit of the matrix whose column
for `uv` has a one in rows `u,v`.  If its connected support is bipartite,
this matrix has rank `|V|-1`; minimal dependence makes the graph unicyclic,
and its cycle is even.  Pruning any tree edge would contradict the vertex
equations, so the circuit is exactly that cycle.

If the support is nonbipartite, the unsigned incidence matrix has full row
rank.  Minimal dependence therefore gives a connected graph with one more
edge than vertices.  An even cycle would already be a smaller circuit, so
both cycles are odd.  A theta graph always contains an even cycle; the only
remaining bicyclic graphs are two odd cycles joined by a path, including a
shared endpoint.  Solving (17) successively around the cycles and path gives
the stated alternating coefficients and the factor two. \(\square\)

There is also a tensor-level continuation which no longer assumes the
two-neighbour form (10).  At a vertex `v`, let `E_v` be the coordinate
space on all currently nonzero scalar cells incident with `v`, and let

\[
 \partial_v:E_v\longrightarrow\bigotimes_{u\in B}V_u
\]

send a unit coordinate to its unweighted derivative tensor (12).
Entry-minimality says exactly that `partial_v` is injective.  For each color
`r`, let `a_(v,r) in E_v` be the vector of the current entries having color
`r` at `v`.  The star equations say

\[
                         \partial_v a_{v,r}=e_r^{\otimes B}.             \tag{19}
\]

**Proposition 4.2 (entry-minimal fiber-web chase).**  Let `z` be mixed,
let `K` be one of the circuits in Lemma 4.1, and let `(h_e)_(e in K)` be
its nonzero circuit coefficients.  For a vertex `v` of `K`, define a local
variation by

\[
 (\delta_v)_e=\frac{h_e}{q_e(z)}\quad(e\in K, e\ni v),
 \qquad (\delta_v)_e=0\quad\hbox{on every other cell at }v.              \tag{20}
\]

Every denominator is nonzero.  The `z`-coefficient of
`partial_v(delta_v)` is zero, and exactly one of the following holds.

1. **Diagonal closure.**  There are scalars `beta_r` such that

   \[
       \partial_v(\delta_v)=\sum_r\beta_re_r^{\otimes B},\qquad
       \delta_v=\sum_r\beta_ra_{v,r}.                                  \tag{21}
   \]

   In fact only `beta_(z_v)` can be nonzero.  Thus the circuit cells at
   `v` exhaust the entire active color-`z_v` row and (20) is its unique
   pure-row scaling.
2. **Mixed rerouting.**  The tensor `partial_v(delta_v)` has a nonzero
   mixed coefficient at some coloring `z'`.  At least one of the same
   scalar cells has a nonzero cofactor at `z'`, and the zero coefficient
   equation for `z'` supplies another circuit containing that cell.

The zero tensor cannot occur in either case.  Repeated mixed rerouting must
eventually revisit a previous coloring/cell/circuit state and hence gives a
finite fiber-web cycle.

**Proof.**  Circuit minimality and (16) make every `q_e(z)` in (20)
nonzero.  At the coloring `z`, the derivative tensor of `e` has coefficient
`q_e(z)`, so the relevant coefficient of the image of (20) is
`sum_(e ni v)h_e=0` by the circuit equation.

If the image lies in the diagonal space, write it as the first expression
in (21).  Equation (19) supplies the second displayed vector as another
preimage.  Injectivity of `partial_v` makes the two preimages equal.  The
coordinate supports of the different local-color rows are disjoint, while
(20) uses only cells whose color at `v` is `z_v`; hence all other `beta_r`
vanish.  The equality of preimages also proves the exhaustion assertion.

If the image is not diagonal, some mixed coefficient `z'` is nonzero.
One summand in that coefficient has both a nonzero variation coefficient
and a nonzero cofactor.  It is the same currently nonzero scalar cell, and
its endpoint colors agree with `z'`.  Applying (16)--(17) to `z'` and then
Lemma 4.1 gives the next circuit.  Finally, a zero image would lie in the
first case with all `beta_r=0`, forcing the nonzero vector `delta_v` to be
zero.  There are only finitely many colorings, cells, and circuit supports,
so an indefinitely repeated transition closes. \(\square\)

Diagonal closure is already restrictive.  Since the row in (21) produces
the all-`z_v` target coefficient, at least one circuit edge incident with
`v` must have color `z_v` at its other endpoint as well.  Thus every vertex
of a completely diagonal circuit closure has a same-colored circuit
neighbour.  Nonconstant color blocks of length at least two on an even
cycle still satisfy this condition, so it is not yet a contradiction.

For the two-neighbour row (10), the circuit containing `pk` must also
contain `pj`, because these are the only two nonzero coordinates at row
`(p,c)`.  Hence the graph-theoretic circuit is exactly the finite closure
of the defect chase beginning with `j-p-k`.

Pure-row coefficient equations, without a genuinely three-color input, do
not exclude the even-cycle alternative.  The next section gives an actual
two-color common-edge source in which it occurs.
What entry-minimality excludes is a **clean** closure with
\(\mathcal V_{k,l}=0\).  A surviving three-color source must realize a fully
rerouted cycle or odd handcuff: at every chased endpoint, (14) is nonzero
and is carried by another color at the original vertex.

## 5. An actual mixed-cofactor Koszul module

Use colors `0,1` on vertices `0,...,5` and the edge matrices

\[
\begin{array}{c|c}
01&e_0e_0\\
23&e_0e_0+e_1e_1\\
02&-e_0e_1\\
13&e_0e_1\\
45&e_0e_0\\
05,12,34&e_1e_1.
\end{array}                                                  \tag{22}
\]

The three supported matchings give exactly \(\Delta_{6,2}\), and every
underlying edge has a nonzero full cofactor.  At `p=0`, put

\[
 Z=e_1^{(3)}\otimes e_0^{(4)}\otimes e_0^{(5)}.
\]

The actual complementary hafnians are

\[
 C_1=e_0^{\otimes\{2,3,4,5\}}+e_1^{(2)}\otimes Z,
 \qquad C_2=e_0^{(1)}\otimes Z,qquad
 C_5=e_1^{\otimes\{1,2,3,4\}}.                            \tag{23}
\]

Thus the two rows at `p` are

\[
 e_0^{(1)}C_1-e_1^{(2)}C_2=e_0^{\otimes5},qquad
 e_1^{(5)}C_5=e_1^{\otimes5}.                              \tag{24}
\]

The two derivative atoms in the first equation are independent: one is
`g_0+z` and the other is `z`.  Modulo the diagonal space their classes are
equal, so (5) is saturated with no actual first-star kernel.

At the second center `2`, color `1`, the derivative atoms of the cells on
`23` and `02` are identical and their weights are `+1,-1`.  The three
nonzero incident atoms therefore have rank two.  The same dependence is
visible at center `3`.  Deleting the two canceling cells leaves the two
standard monochromatic matchings and the same binary target.  The defect
chase is the even four-cycle

\[
                         0-1-3-2-0.                        \tag{25}
\]

Hence this exact source preserves the common internal edges, all
second-center hafnian identities, and local irredundancy at the original
mixed star.  It fails entry-minimality precisely at the later centers.

The audit
[`computations/verify_mixed_cofactor_koszul_star.py`](../computations/verify_mixed_cofactor_koszul_star.py)
computes (23)--(24), verifies independence at `p=0`, and computes the exact
derivative rank at every vertex-color port.  It supplements the full tensor
and activity audit in
[`computations/verify_active_ranktwo_binary_gadget.py`](../computations/verify_active_ranktwo_binary_gadget.py).

## 6. The fixed-star six-site cap and the three-separator rule

There is an exact way for a fully rerouted component to produce a six-site
quotient.  Fix `p`, choose four further vertices `Q`, and put

\[
                     R=B\setminus(\{p\}\cup Q).
\]

The six bags `{p}`, the four singleton bags in `Q`, and the odd bag `R`
form a six-odd-bag partition.  Every singleton automatically has one
crossing matching edge.  The bad sector is therefore exactly the sector
with three or five edges across `delta(R)`.

This sector has the following common-cofactor expansion.  For \(q\in Q\),
let \(C_q^{[s]}\) be the part of \(C_q\) whose internal matching has `s`
edges from \(Q\setminus\{q\}\) into `R`.  For \(x\in R\), let
\(C_x^{[s]}\) be the part with `s` edges from `Q` into
\(R\setminus\{x\}\).  Then, with all slots restored,

\[
 T_{\rm bad}=
 \sum_{q\in Q}A_{pq}\otimes C_q^{[3]}
 +\sum_{x\in R}A_{px}\otimes\bigl(C_x^{[2]}+C_x^{[4]}\bigr).\tag{26}
\]

Indeed, an edge `pq` contributes no crossing endpoint at `R`, so the
remaining number is odd and bad exactly when it is three.  An edge `px`
with \(x\in R\) contributes one, so the internal number is even and bad
exactly when it is two or four.

Let

\[
 D_R=\operatorname{span}\{e_0^{\otimes R},e_1^{\otimes R},
                           e_2^{\otimes R}\}.
\]

The six-bag quotient theorem gives the exact necessary condition

\[
                 D_R\cap\operatorname{LS}_R(T_{\rm bad})\ne0           \tag{27}
\]

for every choice of `p,Q`.  If the intersection vanished, a map on the
big bag could fix its three diagonal vectors and kill the full bad tensor;
the one-cross sector would then be an ordinary six-site hafnian equal to
\(\Delta_{6,3}\), contrary to the proved six-site obstruction.

At order eight, `|R|=3`, the five-cross sector and `C_x^[4]` are absent.
Thus (26) is precisely the total **three-cross defect tensor** at a
three-vertex separator, and (27) says that every such defect must carry a
nonzero diagonal Schmidt direction.  This is the uniform separator test
which any minimally augmented double vertex-expansion must pass.  Proving
that a fully rerouted Koszul circuit violates (27) for one choice of four
chased vertices would complete the desired mixed-star-to-six-site reduction;
the present argument does not yet force that last disjointness.
