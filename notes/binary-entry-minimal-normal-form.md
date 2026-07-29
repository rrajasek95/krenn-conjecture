# Entry-minimal binary restrictions: an exact normal form and its limit

Let \(B\) have even cardinality \(n=2m\), and attach an arbitrary complex
\(2\times2\) matrix \(A_{uv}\) to every unordered pair. Write

\[
 H_B(A)=\sum_{M\in\operatorname {PM}(B)}\bigotimes_{uv\in M}A_{uv}.
\tag{1}
\]

This note classifies the least possible *scalar-cell support* of an exact
binary realization.  It then records the extra conclusion available when
such a binary restriction occurs inside an exact three-color realization.
All arguments are coefficientwise only after a term has been proved unique;
no general termwise-vanishing assumption is made.

## 1. The sharp binary cell minimum

Count a nonzero aggregate matrix entry \(A_{uv}(i,j)\) as one cell. Parallel
sources have already been aggregated, so this count is intrinsic to the
matrices in (1).

**Theorem 1 (Hamilton normal form).**  If

\[
 H_B(A)=e_0^{\otimes B}+e_1^{\otimes B},                    \tag{2}
\]

then \(A\) has at least \(n\) nonzero cells. Equality holds if and only if
there are perfect matchings \(P_0,P_1\) whose occurrence union is one
alternating Hamilton cycle (a doubled edge is allowed when \(n=2\)), and

\[
 A_{uv}=\begin{cases}
 a_{uv}E_{00},&uv\in P_0\setminus P_1,\\
 b_{uv}E_{11},&uv\in P_1\setminus P_0,\\
 a_{uv}E_{00}+b_{uv}E_{11},&uv\in P_0\cap P_1,\\
 0,&\text{otherwise},
 \end{cases}                                                \tag{3}
\]

with every displayed scalar nonzero and

\[
                  \prod_{e\in P_0}a_e=
                  \prod_{e\in P_1}b_e=1.                  \tag{4}
\]

For \(n\ge4\), the Hamilton condition in particular makes \(P_0,P_1\)
edge-disjoint.

**Proof.** The all-zero coefficient in (2) is one, so at least one perfect
matching \(P_0\) has a nonzero product of \(00\)-cells. The all-one
coefficient similarly supplies \(P_1\) made of nonzero \(11\)-cells. These
are \(m+m=n\) distinct scalar cells, proving the lower bound.

At equality they exhaust the support.  Regard a shared underlying edge as
two differently colored parallel occurrences.  The 2-regular occurrence
multigraph \(P_0\cup P_1\) is a disjoint union of alternating even cycles.
If it had at least two components, choose the color-zero factor on a
nonempty proper collection of components and the color-one factor on the
others.  This gives a nonconstant coloring.  It has exactly one contributing
underlying perfect matching: at a vertex of color \(i\), the only compatible
nonzero cell is its incident \(P_i\)-cell. Its coefficient is therefore a
nonzero product, contradicting (2). Thus the occurrence union is connected,
which is exactly the Hamilton condition.  The two constant coefficients now
give (4).

Conversely, an even cycle has exactly its two alternating perfect matchings.
Equations (3)--(4) therefore give (2). \(\square\)

There is a small sharp gap above equality. If a realization of (2) has
exactly \(n+1\) cells, choose \(P_0,P_1\) as in the proof. If their union is
disconnected, a componentwise mixed coloring again has a base matching.  A
cancellation mate would have to differ on an alternating cycle and hence
use at least two cells outside the selected \(n\), impossible. If their
union is Hamilton, the one remaining cell cannot occur in a constant term:
a perfect matching distinct from \(P_i\) differs from it in at least two
edges.  Nor can it occur in a mixed coefficient with a cancellation mate.
After fixing its endpoint colors, every remaining vertex has at most its
unique compatible \(P_i\)-edge, so there is at most one matching containing
that cell.  Consequently the extra cell is tensor-inactive and can be
deleted.  In particular an inclusion-minimal exact binary support has either
\(n\) cells or at least \(n+2\).

The latter bound cannot be raised.  On six vertices take

\[
 P_0=01|23|45,\qquad P_1=05|12|34,
\]

put \(E_{11}\) with weight one on \(P_1\), put \(E_{00}\) with weights
\(1/2,1,1\) on \(01,23,45\), and add \(E_{00}\) with weights \(1,1/2\) on
\(02,13\). The only color-zero matchings are \(01|23|45\) and
\(02|13|45\), each of weight \(1/2\); the only color-one matching is \(P_1\),
and there is no mixed supported matching.  This is an exact active
\(n+2\)-cell realization. Thus the theorem is an equality classification,
not a rank-one statement for arbitrary active binary realizations; the
rank-two cancellation gadget in
`computations/verify_active_ranktwo_binary_gadget.py` supplies an even
stronger warning.

There is also a useful quantitative version when the two selected constant
factors are not Hamilton.

**Lemma 1.1 (four-cell cost of a disconnected selected pair).** Choose any
nonzero all-zero matching \(P_0\) and any nonzero all-one matching \(P_1\)
in an exact binary realization. If the occurrence union \(P_0\cup P_1\)
has at least two alternating-cycle components, then the binary support has
at least \(n+4\) cells.

**Proof.** Choose a nonempty proper collection of cycle components and use
\(P_0\) on those components and \(P_1\) on the others. This gives a mixed
coloring \(c\) with a unique monomial inside the selected \(n\) cells. A
cancellation mate differs from it on an alternating cycle, so at least two
of the mate-only cells lie outside the selected support. Apply the same
argument to the complementary coloring \(\bar c\). No scalar cell can be
compatible with both \(c\) and \(\bar c\), since both endpoint colors are
flipped. The two mates therefore require four distinct extra cells.
\(\square\)

Consequently, if a binary exact support has at most \(n+3\) cells, *every*
choice of one nonzero constant monomial of each color has Hamilton occurrence
union. This is a cancellation-aware statement: the number four comes from
two alternating-cycle mates, not from declaring either mixed coefficient
termwise zero.

## 2. A one-third-color defect lemma

Now let every \(A_{uv}\) be \(3\times3\) and suppose

\[
                         H_B(A)=\Delta_{B,3}.               \tag{5}
\]

Assume its principal restriction to colors \(0,1\) has exactly \(n\)
nonzero cells.  Theorem 1 supplies an alternating Hamilton cycle
\(C=P_0\cup P_1\). Let \(B=X\sqcup Y\) be the cycle bipartition.

**Lemma 2 (cross-shore decoupling).** For every \(x\in X,y\in Y\) and
\(i\in\{0,1\}\), both endpoint orientations mixing color \(2\) with color
\(i\) vanish:

\[
 A_{xy}(2,i)=A_{xy}(i,2)=0,                                \tag{6}
\]

where the displayed entries are interpreted in the natural endpoint order.
Equivalently, every cross-shore matrix is block diagonal for
\(\mathbf C^3=\operatorname {span}(e_0,e_1)\oplus\mathbf Ce_2\).

**Proof.** Fix an oriented cell, say color \(2\) at \(x\) and color \(i\)
at \(y\). Since \(x,y\) are in opposite shores, deleting them from \(C\)
leaves two even paths.  Each path has a unique perfect matching; call their
union \(K\). Color the endpoints of every edge of \(K\cap P_j\) by \(j\),
color \(x\) by \(2\), and color \(y\) by \(i\).

The proposed cell on \(xy\), together with \(K\), is a matching monomial.
It is the unique possible monomial of this coloring.  Indeed, among vertices
other than \(x\), all colors lie in \(\{0,1\}\), and Theorem 1 says that a
color-\(j\) vertex has only its \(P_j\)-edge available inside that binary
plane. More explicitly, the \(P_i\)-mate of the deleted vertex \(y\) is an
endpoint of one of the two paths and is matched by \(K\) along its other,
\(P_{1-i}\), edge; it consequently has color \(1-i\). Thus \(y\) has no
compatible binary edge and must be paired with the sole color-2 vertex
\(x\). Once \(xy\) is fixed, both paths are forced to use \(K\).

The coloring is nonconstant, so its coefficient in (5) is zero. The unique
monomial is the proposed cell times a product of nonzero Hamilton cells;
hence that cell is zero.  Reversing the endpoint colors proves the other
orientation. \(\square\)

This conclusion survives arbitrary complex entries and cancellations away
from the isolated fiber.  It says that if one binary restriction reaches its
cell minimum, all couplings of the third color to that binary plane are
confined to the two shores separately.

The same proof gives a quantitative defect statement before equality. Fix
selected constant matchings \(P_0,P_1\) whose union is Hamilton, and let
\(E\) be all other cells in the principal \(0,1\) restriction. For opposite
cycle shores \(x,y\), form the one-color-2 coloring used in the proof. Its
coefficient equation has the form

\[
 A_{xy}(2,i)\,\mu_{xy}+F_{xy,i}=0,                          \tag{7}
\]

where \(\mu_{xy}\ne0\) is the product of the forced path-matching cells and
every monomial of \(F_{xy,i}\) contains at least one cell of \(E\). Indeed,
if a second matching also uses \(xy\), any deviation from the two selected
path matchings uses a cell of \(E\). If it sends the sole color-2 vertex
elsewhere, the binary vertex \(y\), which is isolated in the selected
compatible graph, can be covered only by a cell of \(E\). Thus cross-shore
third-color coupling is algebraically paid for by binary excess. Lemma 2 is
the sharp \(E=\varnothing\) case.

## 3. The absolute three-color support floor

There is one setting in which source minimality really does force minimal
binary restrictions. Let \(n=2m\). Selecting one nonzero constant matching
\(P_i\) for each of the three colors uses \(3m\) distinct cells. The
three-one-factors lemma supplies a fourth, mixed matching in their decorated
union. Its cancellation mate differs on an alternating cycle, and every
mate-only edge is outside the selected cells. Thus every exact three-color
realization has at least

\[
                              3m+2                         \tag{8}
\]

nonzero cells.

**Proposition 3 (two-extra rectangle normal form).** Suppose equality holds
in (8). Then, after permuting colors, the two cells outside the selected
\(P_0,P_1,P_2\) are off-diagonal \(a,b\)-cells with \(a\ne b\). More
precisely, there are selected edges

\[
 uu'\in P_a,\qquad vv'\in P_b                              \tag{9}
\]

such that the extra occurrences are \(uv\) and \(u'v'\) (or the crossed
pair \(uv',u'v\)), with the endpoint colors prescribed by \(a,b\).
Consequently the two principal restrictions involving the unused third
color have exactly \(n\) cells and hence are in the Hamilton normal form of
Theorem 1.

**Proof.** Use a target-preserving diagonal one-parameter subgroup
\(A_{uv}(r,s)\mapsto t^{h_{u,r}+h_{v,s}}A_{uv}(r,s)\). Impose zero weight
on every selected cell:

\[
                         h_{u,i}+h_{v,i}=0
                 \quad(uv\in P_i).                         \tag{10}
\]

These equations already imply \(\sum_vh_{v,i}=0\) for every color, so the
subgroup fixes the target. At the two endpoints of each \(P_i\)-edge write
the potentials as \(x_{e,i}\) and \(-x_{e,i}\). The weight of any
unselected cell is therefore a nonzero signed sum of two of the independent
variables \(x_{e,i}\).

If the two extra weight functionals did not positively span zero, the
strict theorem of alternatives would give a choice of \(h\) for which both
weights are nonnegative and one is positive. Taking \(t\downarrow0\) would
retain every selected cell, delete at least one extra cell, and leave an
exact target, contradicting the lower bound (8). Hence the two signed
two-coordinate functionals are negative scalar multiples. Their
coefficients all have absolute value one, so they are exact negatives. They
therefore involve the same two selected-edge variables at opposite
endpoints. This is precisely the rectangle (9).

It remains to exclude \(a=b\). In that case the two extra diagonal cells,
together with the selected \(P_a\)-edges \(uu',vv'\), are the two
alternating sides of a monochromatic four-cycle. The selected-factor
cancellation theorem supplies a mixed matching \(M\) and a mate \(M'\).
At equality in (8), every edge of \(M'\setminus M\) is one of the two
extras, so \(M\triangle M'\) is exactly this four-cycle. Since the extras
give color \(a\) to all four vertices, uniqueness of the selected
color-\(a\) port forces the two \(M\)-edges on the cycle to be
\(uu',vv'\).

The ratio of the two mixed monomials is therefore exactly the ratio between
the two all-\(a\) perfect matchings obtained by switching that four-cycle:
all edges outside the cycle are shared and cancel from the ratio. The mixed
coefficient equation makes this ratio \(-1\). But these are the only two
all-\(a\) matchings in a support with just the selected cells and the two
extras, so the all-\(a\) coefficient is then zero, contradicting its target
value one. Thus \(a\ne b\). An off-diagonal \(a,b\)-cell belongs only to
the principal \(a,b\) restriction, proving the last assertion.
\(\square\)

In particular, a putative source for which all three principal binary
restrictions strictly exceed \(n\) cells must have at least \(3m+3\) cells.
This does not prove that an arbitrary source-minimum attains the floor (8);
binary-inactive cells can be globally active in genuinely ternary fibers.
It does isolate the only two-extra chart and shows that two minimal binary
restrictions are unavoidable there.

The rectangle can be excluded uniformly at half of the even orders.

**Corollary 3.1.** Equality in (8) is impossible when \(4\mid n\).

**Proof.** Keep the notation of Proposition 3, with unused color \(c\), and
let \(\chi_{rs}\) denote the bipartition of the Hamilton cycle
\(P_r\cup P_s\). Lemma 2 applied to the two minimal restrictions \(a,c\)
and \(b,c\) says that the endpoints of each extra \(a,b\)-cell lie in the
same \(\chi_{ac}\)-shore and the same \(\chi_{bc}\)-shore. Since
\(vv'\in P_b\) crosses \(\chi_{bc}\), the two rectangle relations imply
that \(uu'\in P_a\) also crosses \(\chi_{bc}\).

In fact \(uu'\) must be the *only* \(P_a\)-edge crossing \(\chi_{bc}\).
If another such edge \(xx'\) existed, regard it as an opposite-parity chord
of the Hamilton cycle \(P_b\cup P_c\). Deleting \(x,x'\) leaves two even
paths, whose unique perfect matchings together with \(xx'\) give a
nonconstant matching monomial made from the selected cells. It does not use
\(uu'\). Consequently the colors at \(u,u'\) are supplied by \(P_b\)- or
\(P_c\)-edges, not color \(a\), so neither extra rectangle cell is compatible
with this coloring. Selected-port uniqueness makes the monomial a singleton,
contrary to exactness.

The two shores of \(\chi_{bc}\) both have \(m=n/2\) vertices. Any perfect
matching has a number of cross-shore edges congruent to \(m\) modulo two,
because the vertices left in either shore are paired internally. Thus
\(P_a\) cannot have exactly one cross-shore edge when \(m\) is even. This
contradicts the preceding paragraph. \(\square\)

For \(n\equiv2\pmod4\), the same proof shows that the distinguished
\(P_a\)-edge and \(P_b\)-edge must respectively be the unique cross chords
of \(P_b\cup P_c\) and \(P_a\cup P_c\). The following elementary cycle
lemma handles the two resulting holes.

**Lemma 3.2 (two-hole reflection lemma).** Let \(m\) be odd. Around a
\(2m\)-cycle write the vertices

\[
 E_0,O_0,E_1,O_1,\ldots,E_{m-1},O_{m-1},
\]

and let

\[
 B=\{E_jO_j\},\qquad C=\{O_jE_{j+1}\},                     \tag{11}
\]

with indices modulo \(m\). Let \(A\) be a perfect matching such that
\(A\cup B\) and \(A\cup C\) are Hamilton cycles. Suppose \(A\) has exactly
one \(E\)-to-\(O\) edge, and no \(E\)-to-\(E\) edge of \(A\) interlaces an
\(O\)-to-\(O\) edge of \(A\). Then, after an even rotation of the displayed
\(2m\)-cycle,

\[
 A=\{\{0,m\}\}\ \cup\
   \bigl\{\{-k,k\}:1\le k\le m-1\bigr\},                  \tag{12}
\]

where the labels in (12) are in \(\mathbf Z/(2m)\). Thus \(A\) is the
reflection \(x\mapsto-x\), with its two fixed vertices \(0,m\) paired to
one another.

**Proof.** Contract the \(B\)-edges and identify their blocks with
\(\mathbf Z/m\). Write \(\mathcal E\) for the matching induced by the
\(E\)-to-\(E\) edges of \(A\), and \(\mathcal O\) for the matching induced
by its \(O\)-to-\(O\) edges. If the unique cross edge is \(E_pO_q\), then
\(\mathcal E\) misses \(p\), \(\mathcal O\) misses \(q\), and Hamiltonicity
of \(A\cup B\) says

\[
 \mathcal E\cup\mathcal O
   \text{ is a Hamilton path from }p\text{ to }q.          \tag{13}
\]

Traverse the path (13), starting at \(p\). Its edges alternate
\(\mathcal O,\mathcal E,\mathcal O,\mathcal E,\ldots\). Write its block
order as \(x_0,x_1,\ldots,x_{m-1}\), so \(x_0=p\), \(x_{m-1}=q\), and
\(x_{k-1}x_k\) is an \(\mathcal O\)-edge for odd \(k\) and an
\(\mathcal E\)-edge for even \(k\).

We first record the exact local consequence of noninterlacing. If
\(O_aO_b\) and \(E_bE_c\) do not interlace, then, starting at block \(b\),
the clockwise block order is

\[
                              b,a,c.                       \tag{14}
\]

Indeed, rotate so that \(b=0\) and represent \(c\) by an integer with
\(0<c<m\). The clockwise arc from \(E_0\) to \(E_c\) contains \(O_0\).
For the two chords not to interlace it must also contain \(O_a\), whence
\(0<a<c\). Similarly, if \(E_aE_b\) and \(O_bO_c\) do not interlace, the
clockwise block order starting at \(b\) is \(b,c,a\).

Apply these two observations to each consecutive pair of path edges. For
odd \(k\), the order starting at \(x_k\) is
\(x_k,x_{k-1},x_{k+1}\); for even \(k\), it is
\(x_k,x_{k+1},x_{k-1}\). Define the *active arc* after \(x_k\) to be the
open clockwise arc

\[
 \Gamma_k=\begin{cases}
 (x_{k-1},x_k),&k\text{ odd},\\
 (x_k,x_{k-1}),&k\text{ even}.
 \end{cases}
\]

The local orders say exactly that \(x_{k+1}\in\Gamma_k\) and that
\(\Gamma_{k+1}\) is one of the two subarcs into which \(x_{k+1}\) cuts
\(\Gamma_k\). Iterating, the active arcs are nested, \(\Gamma_k\) contains
no already exposed vertex in its interior, and every later path vertex lies
in \(\Gamma_k\). Thus the subarc discarded when passing from
\(\Gamma_k\) to \(\Gamma_{k+1}\) contains neither an earlier nor a later
path vertex. It contains no block at all, because (13) is Hamiltonian. The
complementary arc from \(x_1\) to \(x_0\) is empty for the same reason.
Thus \(x_1\) is the immediate predecessor of \(x_0\);
at every subsequent step the newly discarded subarc is empty, alternately
forcing the immediate successor of the right endpoint and the immediate
predecessor of the left endpoint. Hence

\[
 p,\ p-1,\ p+1,\ p-2,\ p+2,\ldots,
 p-\frac{m-1}{2},\ p+\frac{m-1}{2}.                       \tag{15}
\]

In particular \(q=p+(m-1)/2\). Notice that the hypotheses involving
\(A\cup C\) were not needed for this stronger local classification.

Undoing the \(B\)-contraction, the consecutive pairs in (15) are precisely
the same-parity pairs symmetric about the two vertices
\(E_p\) and \(O_q\). Since

\[
 \operatorname{pos}(O_q)-\operatorname{pos}(E_p)
   =2(q-p)+1=m,
\]

the cross edge joins antipodal fixed vertices and all other pairs are the
reflection pairs (12). Rotating positions by \(-2p\) is an even rotation,
so it preserves each of the named matchings \(B,C\). \(\square\)

**Theorem 3.3 (the two-extra floor is unattainable).** For every even
\(n\ge6\), an exact three-color realization has at least

\[
                              \frac{3n}{2}+3               \tag{16}
\]

nonzero scalar cells.

**Proof.** Corollary 3.1 handles \(4\mid n\), so put \(n=2m\) with \(m\)
odd and suppose equality held in the weaker floor (8). Proposition 3 gives
the off-diagonal rectangle between \(uu'\in P_a\) and \(vv'\in P_b\).

First, the endpoints of either extra edge must lie in the same shore of
all three Hamilton cycles \(P_a\cup P_b\), \(P_a\cup P_c\), and
\(P_b\cup P_c\). The last two statements are Lemma 2. For
\(P_a\cup P_b\), Hamiltonicity of the selected pair follows from Lemma 1.1,
because its binary restriction has only \(n+2\) cells. An opposite-shore
extra chord, together with the two
residual even paths, gives a binary mixed monomial. At the other two
rectangle endpoints the residual path matching swaps colors \(a,b\), so
the second extra cell is incompatible. The monomial is therefore a
singleton, proving the first statement.

As in Corollary 3.1, \(uu'\) is the unique \(P_a\)-edge crossing the
bipartition of \(P_b\cup P_c\); symmetrically, \(vv'\) is the unique
\(P_b\)-edge crossing the bipartition of \(P_a\cup P_c\).

If a same-shore \(P_a\)-chord and a same-shore \(P_a\)-chord in the
opposite shore interlace around \(P_b\cup P_c\), the two chords and the
four intervening even paths form a selected perfect matching which avoids
\(uu'\). Its coloring is mixed, and at \(u,u'\) it uses only colors
\(b,c\), so neither extra cell is compatible. Selected-port uniqueness
makes this another forbidden singleton. Hence the noninterlacing
hypothesis of Lemma 3.2 holds with
\((A,B,C)=(P_a,P_b,P_c)\).

Normalize its reflection form as in (12). A direct traversal of the
Hamilton cycle \(P_a\cup P_c\), starting with \(\chi_{ac}(0)=0\), gives

\[
 \chi_{ac}(x)=
 \begin{cases}
  0,&x=0,\\
  x+1\pmod2,&1\le x\le m-1,\\
  x\pmod2,&m\le x\le2m-1.
 \end{cases}                                                \tag{17}
\]
Equivalently, among the \(m\) edges
\(P_b=\{\{2j,2j+1\}:0\le j<m\}\), exactly the two edges with
\(j=0\) and \(j=(m-1)/2\) stay within a \(\chi_{ac}\)-shore; the remaining
\(m-2\) cross it. For \(m\ge5\), this contradicts the already proved
uniqueness of the crossing \(P_b\)-edge.

It remains \(m=3\). In the normalization (12),
\[
\begin{aligned}
P_a&=03|15|24,&P_b&=01|23|45,&P_c&=12|34|05.
\end{aligned}
\]
The unique \(P_b\)-edge crossing \(\chi_{ac}\) is \(45\). The sign triples
\((\chi_{ab},\chi_{ac},\chi_{bc})\) at the endpoints of the distinguished
edges \(03\) and \(45\) are
\[
0:(0,0,0),\quad 3:(1,1,1),\quad
4:(1,0,0),\quad 5:(0,1,1).
\]
No endpoint pairing between \(03\) and \(45\) has equal sign triples at
both ends, contradicting the same-shore requirement for the two extra
cells. This finishes the final case. \(\square\)

The finite audits
`computations/verify_two_hole_reflection.py` and
`computations/search_two_extra_rectangle_uniform.py` independently check,
respectively, the reflection classification through (m=9) and the
rectangle/singleton classification at (n=6,8,10).

Theorem 3.3 concerns only the absolute minimum-cell floor. It does **not**
show that an order-minimal counterexample would attain that floor: choosing
minimum order and then minimum support makes every remaining cell essential,
but supplies no upper bound of \(3n/2+2\) on the support. A counting argument
alone therefore does not promote Theorem 3.3 to all realizations. What it
does prove is that any source-minimal counterexample has at least three
cells beyond one selected constant factor per color.

## 4. Why three binary restrictions alone do not contradict one another

The literal statement that three exact principal binary restrictions cannot
coexist is false, even when all three attain Theorem 1 with equality.  On six
vertices take

\[
\begin{aligned}
P_0&=01|23|45,\\
P_1&=05|12|34,\\
P_2&=03|15|24,
\end{aligned}                                              \tag{11}
\]

and put \(E_{ii}\) with weight one on the edges of \(P_i\), zero elsewhere.
Every pair \(P_i\cup P_j\) is an alternating Hamilton cycle. Hence every
principal two-color restriction is exactly the corresponding binary GHZ
tensor, by Theorem 1.

The full three-color tensor is nevertheless not GHZ.  Besides the three
selected factors, their union has the fourth perfect matching

\[
                         03|12|45,                          \tag{12}
\]

whose unique decorated coloring is

\[
                         (2,1,1,2,0,0).                    \tag{13}
\]

Its coefficient is one.  It is invisible in every principal binary
restriction because it uses all three colors.

Thus binary normal forms can constrain a putative exact realization (Lemma
2), but compatibility of all three binary targets is not itself the missing
contradiction.  Any successful continuation must use a coefficient involving
all three colors, or an invariant retaining that coefficient.  The fourth
matching (12) is exactly where that genuinely ternary information first
appears.
