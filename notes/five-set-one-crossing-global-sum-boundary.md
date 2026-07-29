# Global five-set sector sums and the cube obstruction

## 1. Outcome

Let `B` have `2m` vertices and, for every five-set `U subset B`, let
`T_(j,U)` be the part of a matching tensor whose matching has exactly
`j` edges across `U | (B setminus U)`.  Only `j=1,3,5` occur.  There is
an exact global identity which couples all five-set cuts:

\[
 \boxed{
 \sum_{|U|=5}T_{j,U}=\kappa_j H_B(A),\qquad
 \kappa_j=2^j{m\choose j}{m-j\choose(5-j)/2}.}          \tag{1}
\]

Thus for an exact ternary source each of the three sector sums is already
a scalar multiple of the GHZ tensor, separately:

\[
                     \sum_{|U|=5}T_{j,U}=\kappa_j\Delta_{B,3}.      \tag{2}
\]

This is a genuinely global mixed-coefficient identity absent from a
single-cut analysis.  There is also a local Johnson-graph refinement:
relative to any fixed five-set, its three- and five-crossing sectors are
exact linear combinations of one-crossing sectors on five-sets at distance
one and two.  In particular, the whole matching tensor can be reconstructed
from that radius-two family.  However, these identities, exact target
support, and the formal perfect-matching sector structure still do **not**
force one five-set to satisfy

\[
                         \ker F_{1,U}\subseteq\ker\delta_U.         \tag{3}
\]

An exact abstract countermodel is supplied by the three coordinate
one-factors of the eight-vertex cube.  If their three constant-colour
matching atoms are retained and the other six cube matchings are assigned
coefficient zero independently, the resulting tensor is exactly
`Delta_(8,3)`, while (3) fails on all 56 five-sets.  This assignment is
not induced by products of edge entries: the six omitted mixed matchings
are precisely the obstruction.  Therefore any proof of a successful
five-set must use edgewise factorization and the simultaneous cancellation
of actual mixed matchings, not only the global sector sums.

## 2. Proof of the global sector identities

Fix one perfect matching `M` on `B`.  A five-set crossed by exactly `j`
edges of `M` is obtained by

1. choosing its `j` split matching edges;
2. choosing which endpoint of each split edge lies in `U`; and
3. choosing `(5-j)/2` of the remaining matching edges wholly inside `U`.

The number of choices is exactly `kappa_j` in (1), independently of `M`.
Summing the sector projectors over all five-sets therefore multiplies
every decorated matching atom by the same scalar.  Linearity proves (1),
including arbitrary parallel cells and complex cancellation.  Equation
(2) follows on substituting `H_B(A)=Delta_(B,3)`.

For reference,

\[
 \kappa_1=2m{m-1\choose2},\qquad
 \kappa_3=8{m\choose3}(m-3),\qquad
 \kappa_5=32{m\choose5}.                               \tag{4}
\]

Their sum is `{2m choose 5}`, as it must be because every matching crosses
an odd five-set cut in exactly one of the three possible sizes.

## 3. The first localized identity

The same count can retain a fixed vertex or edge.  For example,

\[
 \sum_{\substack{|U|=5\\x\in U}}T_{1,U}
             =5{m-1\choose2}H_B(A).                    \tag{5}
\]

Fix two vertices `x,y`, and let `H_B^(xy)(A)` denote the contribution of
the perfect matchings which contain the edge `xy`; explicitly it is the
restored tensor `A_xy tensor H_(B setminus {x,y})(A)`.  If `xy` belongs
to a fixed matching, there are

\[
                         b=2(m-1)(m-2)                  \tag{6}
\]

five-sets containing `x,y` which it crosses once.  If `x,y` have distinct
partners, there are

\[
                         a=4(m-2).                      \tag{7}
\]

Indeed, either both partners also lie in `U` and the fifth vertex is the
endpoint of one crossing edge, or exactly one partner lies in `U` and one
further matching edge lies wholly in `U`.  Hence

\[
 \boxed{
 \sum_{\substack{|U|=5\\x,y\in U}}T_{1,U}
   =4(m-2)H_B(A)+2(m-2)(m-3)H_B^{(xy)}(A).}             \tag{8}
\]

Unlike (1), (8) begins to recover the actual edge-factorized source.  More
highly localized sums distinguish further incidence types of a matching.
They are a possible route beyond the negative result below, but a rank or
kernel inclusion does not follow from their linear span alone.

## 4. Johnson-shell transport of the high sectors

Fix a five-set `U` and define its overlap-shell sums

\[
 S_{h,U}=\sum_{\substack{|V|=5\\|V\cap U|=h}}T_{1,V}
 \qquad(0\leq h\leq5).                                  \tag{9}
\]

For one perfect matching `M`, suppose that exactly `k` of its edges cross
`U`, where `k` is one of `1,3,5`.  Relative to `U`, the matching has `k`
crossing edges, `(5-k)/2` internal `U`-edges, and
`(2m-5-k)/2` internal complement edges.  The number `N_(h,k)` of five-sets
`V` in the `h`-overlap shell which `M` crosses once is the coefficient

\[
 \begin{split}
 N_{h,k}=[x^hy^{5-h}z]\,&(1+xy+z(x+y))^k
       (1+x^2+2xz)^{(5-k)/2}\\
      &\mathbin{}\cdot(1+y^2+2yz)^{(2m-5-k)/2}.           \tag{10}
 \end{split}
\]

Here `x` records a selected endpoint originally in `U`, `y` records one
outside `U`, and `z` records a matching edge split by `V`.  Consequently
the first two nontrivial shells give

\[
 \begin{array}{c|ccc}
 &k=1&k=3&k=5\\ \hline
 h=4&2m-1&6&0\\
 h=3&10(m-3)&9m-21&30.
 \end{array}                                             \tag{11}
\]

The count is independent of the matching itself.  Applying it to every
decorated matching atom and using linearity gives the exact tensor
identities

\[
 \boxed{S_{4,U}=(2m-1)T_{1,U}+6T_{3,U},}                 \tag{12}
\]

\[
 \boxed{S_{3,U}=10(m-3)T_{1,U}+(9m-21)T_{3,U}+30T_{5,U}.}\tag{13}
\]

Thus the high sectors are not independent contamination.  They are
transported from nearby one-crossing sectors:

\[
 T_{3,U}=\frac{S_{4,U}-(2m-1)T_{1,U}}6,                 \tag{14}
\]

\[
 T_{5,U}=\frac{S_{3,U}-10(m-3)T_{1,U}-(9m-21)T_{3,U}}{30}.
                                                                  \tag{15}
\]

Adding the sectors gives a particularly compact local reconstruction
valid for every matching tensor:

\[
 \boxed{
 H_B(A)=\frac{6m^2-57m+137}{60}T_{1,U}
       +\frac{17-3m}{60}S_{4,U}
       +\frac1{30}S_{3,U}.}                             \tag{16}
\]

For an exact source, the left side of (16) is `Delta_(B,3)`.  At eight
vertices (`m=4`) this specializes to

\[
 \Delta_{B,3}=\frac1{12}(T_{1,U}+S_{4,U})
                         +\frac1{30}S_{3,U}.             \tag{17}
\]

This is stronger than the unrestricted sum (1): every target tensor is
already in the span of the one-crossing sectors in a radius-two ball about
*each* five-set.

## 5. Why shell transport does not by itself give the kernel inclusion

The row-space test in (3) uses the flattening across one fixed shore `U`.
Although (16) reconstructs the target from `T_(1,V)` for nearby `V`, a
neighboring tensor `T_(1,V)` is not being flattened across its own shore
after it is inserted into the `U | (B setminus U)` equation.  Its row space
therefore need not lie in `row(F_(1,U))`.  Equivalently, a witness in
`ker(F_(1,U))` kills only the center term in (16), not the shell terms.

This is not merely a gap in the argument.  The cube atom model below obeys
(12)--(17) atom by atom, while (3) fails for every five-set.  Hence all
Johnson-shell identities, even the local reconstruction of the full target,
are insufficient in the freely weighted matching-atom model.  To turn
shell transport into a successful cut one must use the common edge factors
which couple the same decorated edges across different matchings.  In the
cube support those factors necessarily also create the six mixed perfect
matchings omitted by the abstract model.

## 6. Exact cube countermodel before edge factorization

Label the cube vertices by the binary triples, identified with
`0,...,7`.  Its coordinate one-factors are

\[
 M_r=\{\{x,x\mathbin\oplus2^r\}:x_r=0\},
 \qquad r=0,1,2.                                      \tag{18}
\]

In the vector space having independently weighted decorated perfect
matching atoms, retain only `M_r`, decorate every endpoint of `M_r` by
colour `r`, and give it coefficient one.  The image in the ordinary
colour tensor space is exactly

\[
                         \sum_{r=0}^2e_r^{\otimes8}.    \tag{19}
\]

Let `U` be a five-set and put `C=B setminus U`, so `|C|=3`.  The matching
`M_r` crosses the cut once exactly when `C` contains an edge of `M_r`.
Thus all three constant right rows belong to the one-crossing flattening
only if the three vertices of `C` contain one edge from each coordinate
matching.  The three edges would form a triangle in the cube.  The cube is
bipartite, so this never occurs.  More explicitly, among its 56 triples,

\[
 \begin{array}{c|ccc}
 \#\{r:M_r\text{ crosses once}\}&0&1&2\\ \hline
 \#C&8&24&24.
 \end{array}                                           \tag{20}
\]

For this atom assignment `row(F_(1,U))` is exactly the span of the
constant `U`-words for the colours counted in (20).  It is always a
proper subspace of the three constant rows of `delta_U`, proving failure
of (3) on every cut.

The union of the three coordinate one-factors has nine perfect matchings:
the three in (18) and six mixed ones.  The exact edge-factorization defect
can be written as three binomials.  Put an independent nonzero weight on
the colour-`r,r` cell of each edge in `M_r`, and let `c_w` be the resulting
coefficient of the eight-letter colour word `w`.  The nine supported words
are

\[
 \begin{gathered}
 00000000,\quad11111111,\quad22222222,\\
 00001111,\quad11110000,\quad
 00220022,\quad22002200,\quad
 12121212,\quad21212121.
 \end{gathered}                                          \tag{21}
\]

The two mixed matchings in each colour pair together use every edge of the
two corresponding coordinate one-factors exactly once.  Hence their
monomials obey

\[
 \begin{aligned}
 c_{00001111}c_{11110000}&=c_{00000000}c_{11111111},\\
 c_{00220022}c_{22002200}&=c_{00000000}c_{22222222},\\
 c_{12121212}c_{21212121}&=c_{11111111}c_{22222222}.
 \end{aligned}                                           \tag{22}
\]

The abstract assignment (19) sets every left factor in (22) to zero and
every right side to one.  It therefore violates edge factorization in the
smallest possible, explicitly toric way.  In a full source, other
matchings may contribute to the same six mixed coefficients and cancel
these monomials; controlling those simultaneous cancellation fibres is the
remaining nonlinear input.

## 7. Exact audit

[`verify_five_set_one_crossing_global_sum_boundary.py`](../computations/verify_five_set_one_crossing_global_sum_boundary.py)
checks the counts in (1), (5), (8), and (11)--(17) by exhaustive
matching-subset enumeration for several symbolic sizes, enumerates all nine
cube perfect matchings, verifies the all-cut histogram (20), and confirms
that the shell reconstruction holds on every cube cut despite the all-cut
kernel failure.  It also checks the three exponent-vector identities (22).
