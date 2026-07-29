# Hamiltonian cubic cores can have complete, phase-consistent cycle covers

## 1. Outcome

The proposed pure-graph continuation of the five-factor singleton bound is
false, even in its strongest natural small-core form.  There are five
pairwise edge-disjoint coordinate one-factors

\[
                         P_0,P_1,P_2,S,T                  \tag{1}
\]

on eight vertices such that:

1. \(U=P_0\cup P_1\cup P_2\) is connected and cubic, and every
   \(P_i\cup P_j\) is a Hamilton cycle;
2. the only perfect matchings of \(U\) are the three pure factors and two
   mixed matchings \(R_S,R_T\);
3. every edge of \(S\) and \(T\) is decorated bichromatically, so the
   three pure fibres are exact singletons of coefficient one;
4. the fibres of the two pure-core mixed words are exactly
   \(\{R_S,S\}\) and \(\{R_T,T\}\);
5. one negative edge in each extra factor cancels both binomials, and their
   two Laurent rows are linearly independent.

Thus two extra one-factors can supply a compatible alternating cycle for
*every* mixed perfect matching of a Hamiltonian three-factor cubic core.
Neither switching, cycle-cover double counting, nor binomial phase
consistency forces an uncovered core matching.  The obstruction is merely
moved to other words: the complete mixed-fibre histogram of this module is

\[
                       \{1:24,\ 2:2\}.                    \tag{2}
\]

There is already a one-binomial version on six vertices, the smallest
possible order for five edge-disjoint one-factors.  An exact small-order
classification goes further: after normalizing one pair of pure factors to
an alternating Hamilton cycle, every colored core orbit at orders six and
eight and every possible underlying pair \(S,T\) is exhausted.  The audit,
which uses only matching enumeration, a finite three-valued backtrack, and
GF(2) elimination, is
`computations/verify_hamiltonian_cubic_cycle_cover_countermodels.py`.

## 2. Exact port-cycle characterization

The right finite object is a port multigraph.  For each colour \(i\) and
vertex \(v\), let \(p_i(v)\) be the \(P_i\)-edge incident with \(v\).
Make the \(3n/2\) pure edges the nodes of a multigraph \(\Lambda\), retaining
the two physical endpoint ports on every node.  If an extra edge \(uv\) is
decorated by endpoint colours \((a,b)\), insert a link in \(\Lambda\) from
the \(u\)-port of node \(p_a(u)\) to the \(v\)-port of node \(p_b(v)\).

For \(R\in\operatorname {PM}(U)\), regard the \(n/2\) pure edges of \(R\)
as a node set in \(\Lambda\).  The compatibility identity from
`notes/five-coordinate-factor-singleton-debt.md` becomes

\[
 e=uv\in X_R
 \quad\Longleftrightarrow\quad
 p_a(u),p_b(v)\in R.                                    \tag{3}
\]

Hence the compatible extra edges are precisely the links of the induced
port multigraph \(\Lambda[R]\).  Not every ordinary cycle in this induced
multigraph lifts to an alternating cycle: at each pure-edge node, the two
cycle links must use its two *opposite* physical ports.  Call such a cycle
port-valid.  Then

\[
 R\cup X_R\text{ has an }R\text{-alternating cycle}
 \quad\Longleftrightarrow\quad
 \Lambda[R]\text{ has a port-valid cycle}.              \tag{4}
\]

This is an exact characterization, including asymmetric endpoint
decorations.  It also supplies a cycle-cofactor incidence bound.  If \(Q\)
is a port-valid cycle and \(D(Q)\) is its set of pure-edge nodes, its mixed
cover is

\[
 \mathcal C_{\rm mix}(Q)=
 \{R\in\mathcal R_{\rm mix}:D(Q)\subseteq R\}.           \tag{5}
\]

When the edges in \(D(Q)\) are pairwise vertex-disjoint, its size is the
explicit cofactor

\[
 \kappa_{\rm mix}(Q)=
 \#\operatorname {PM}\bigl(U[V\setminus V(D(Q))]\bigr)
 -\sum_{i=0}^2 {\bf1}_{D(Q)\subseteq P_i};               \tag{6}
\]

otherwise it is zero.  Combining (4) over all port-valid cycles gives the
exact canonical singleton count

\[
 s_U=\left|\mathcal R_{\rm mix}\setminus
          \bigcup_Q\mathcal C_{\rm mix}(Q)\right|,       \tag{7}
\]

and consequently the uniform union bound

\[
 s_{\rm mix}\geq s_U
 \geq |\mathcal R_{\rm mix}|-\sum_Q\kappa_{\rm mix}(Q). \tag{8}
\]

Formula (8) refines the edge-incidence estimate by charging complete
port-valid cycles rather than individual compatible edges.  The examples
below make (7) zero with equality: their valid cycles partition the mixed
core matchings.  Therefore no universally positive lower bound can depend
only on the Hamiltonian-pair hypothesis and this port-cycle incidence data.

## 3. The eight-site two-cycle cover

Put

\[
\begin{array}{c|l}
P_0&01|23|45|67,\\
P_1&12|34|56|07,\\
P_2&02|14|36|57,\\
S  &03|15|26|47,\\
T  &04|16|25|37.
\end{array}                                               \tag{9}
\]

The three pure pair-unions have Hamilton orders

\[
\begin{array}{c|l}
P_0\cup P_1&0,1,2,3,4,5,6,7,0,\\
P_0\cup P_2&0,1,4,5,7,6,3,2,0,\\
P_1\cup P_2&0,7,5,6,3,4,1,2,0.
\end{array}                                               \tag{10}
\]

Direct matching enumeration gives only two non-pure matchings in \(U\):

\[
\begin{array}{c|c|c}
 &\text{matching}&\text{pure-edge word}\\ \hline
R_S&07|14|23|56&s=12002111,\\
R_T&07|12|36|45&t=11120021.
\end{array}                                               \tag{11}
\]

Decorate \(S\) by the endpoint word \(s\), and decorate \(T\) by \(t\).
Every edge of its assigned extra factor has differently coloured
endpoints.  Thus no extra edge is compatible with a constant word, and
the three pure fibres remain \(\{P_0\},\{P_1\},\{P_2\}\).

At word \(s\), every \(S\)-edge and no \(T\)-edge is compatible.  At word
\(t\), every \(T\)-edge and no \(S\)-edge is compatible.  Moreover

\[
\begin{array}{c|l}
R_S\cup S&0,3,2,6,5,1,4,7,0,\\
R_T\cup T&0,4,5,2,1,6,3,7,0
\end{array}                                               \tag{12}
\]

are Hamilton alternating cycles.  Therefore the full compatible supports
are exactly those two cycles, proving

\[
                         F(s)=\{R_S,S\},\qquad
                         F(t)=\{R_T,T\}.                  \tag{13}
\]

Give edges \(03\in S\) and \(04\in T\) weight \(-1\), and every other
edge weight \(1\).  The two fibres in (13) cancel.  Their oriented Laurent
rows are

\[
                         \chi_{R_S}-\chi_S,\qquad
                         \chi_{R_T}-\chi_T.               \tag{14}
\]

They are linearly independent because the first row has private support on
every \(S\)-edge and the second on every \(T\)-edge.  Thus all binomial
phase constraints in the complete source are consistent; in fact (13) are
its only binomial fibres.  The remaining twenty-four mixed fibres are
singletons, giving (2).

In the port graph, (12) gives two spanning port-valid cycles.  Each has
\(D(Q)\) equal to a full perfect matching, so its cofactor (6) is one.
Their cover sets are \(\{R_S\}\) and \(\{R_T\}\), respectively.  They
exactly partition \(\mathcal R_{\rm mix}\), showing directly why the union
bound (8) is sharp and zero here.

## 4. The minimal six-site module

At order six take

\[
\begin{array}{c|l}
P_0&01|23|45,\\
P_1&12|34|05,\\
P_2&02|14|35,\\
S  &03|15|24,\\
T  &04|13|25.
\end{array}                                               \tag{15}
\]

The pure union is the triangular prism.  Besides its three displayed
factors it has the sole perfect matching

\[
 R=05|14|23,\qquad c_R=120021.                            \tag{16}
\]

Decorate \(S,T\) by the respective endpoint words

\[
                       000122,\qquad 021010.               \tag{17}
\]

Every extra edge is again bichromatic.  At (16), precisely the extra edges
\(24\in S\) and \(13\in T\) are compatible.  They form an alternating
four-cycle with \(14,23\in R\), while \(05\) is common to both terms.
Thus

\[
                  F(c_R)=\{05|14|23,\ 05|13|24\}.         \tag{18}
\]

Putting weight \(-1\) on \(24\) cancels (18); all pure fibres are
singleton of coefficient one.  The complete mixed histogram is
\(\{1:10,2:1\}\).

This order is minimal because five edge-disjoint one-factors require
degree at least five.  At six vertices the five factors fill \(K_6\).  The
extra pair has union \(C_6\), and its complement is necessarily the
triangular prism above.  The other three-factor cubic graph, \(K_{3,3}\),
has complement \(C_3\sqcup C_3\) and cannot contain even one perfect
matching, so it cannot be extended by \(S,T\).

## 5. Exact small-order exhaustion

For completeness, normalize \(P_0\cup P_1\) to the standard alternating
cycle and quotient the third factor by the dihedral symmetry of that
cycle, including the induced swap of colours zero and one.  For every
remaining core orbit, enumerate all unordered pairs of disjoint perfect
matchings in the complement.  Call a decoration a **strong phased cover**
when:

1. every extra edge is bichromatic;
2. every mixed \(R\in\operatorname {PM}(U)\) has exactly one compatible
   port-valid cycle, so its fibre is an exact binomial; and
3. the equations requiring the product of the extra-edge signs around
   every selected cycle to be \(-1\) are consistent over \(\mathbf F_2\).

The exhaustive counts are

\[
\begin{array}{c|c|c|c|c|c}
n&P_2\text{ representative}&|\mathcal R_{\rm mix}|&
 \#\{S,T\}&\#\text{ strong covers}&\#\text{ phased covers}\\ \hline
6&02|14|35&1&1&1&1\\
6&03|14|25&3&0&0&0\\ \hline
8&02|14|36|57&2&39&39&39\\
8&02|15|36|47&3&36& 6& 6\\
8&02|15|37|46&2&39&39&39
\end{array}                                               \tag{19}
\]

The audit obtains (19) without a black-box SAT solver.  For each mixed
matching it enumerates all alternating cycles in \(R\cup S\cup T\), then
enumerates the selected cycle.  Selected cycles force endpoint colours;
all other cycles become finite forbidden patterns in sixteen ternary
variables.  Unit propagation plus exhaustive branching decides those
patterns.  A separate exact GF(2) elimination checks the sign equations,
and direct matching enumeration verifies the displayed weighted modules.

The table rules out the hoped-for small-order counting contradiction quite
decisively: in two of the three eight-site core orbits, *every* possible
underlying pair of extra factors admits a strong phased cover.  What a full
proof must control is therefore not coverage of the pure-core matchings,
but the new singleton words created by the covering factors, or an
algebraic identity coupling those words back to the covered binomials.
