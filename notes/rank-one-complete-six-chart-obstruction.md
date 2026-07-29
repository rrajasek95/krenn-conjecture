# The six-site rank-one arc chart is impossible

## 1. Result

Let \(G\) be a simple support graph on six sites and put
\(A_{uv}=x_{u|v}\otimes x_{v|u}\ne0\) on every edge of \(G\).  Suppose
that the coordinate incidences are mutual: for each
\(c\in\{0,1,2\}\), the edges carrying \(e_c\) at one endpoint carry
\(e_c\) at the other endpoint and form a perfect matching \(M_c\).
Suppose also that the factors at both endpoints of every remaining
supported edge have all three coordinates nonzero.

**Theorem 1.1.** Such a source cannot satisfy

\[
                         H_6(A)=\Delta_{6,3}.             \tag{1}
\]

The proof is support-theoretic except for one complete-support cubic orbit,
where it uses only four exact mixed coefficient equations.  All scalar
weights and all full-support endpoint vectors remain arbitrary nonzero
complex numbers, and arbitrary edges outside the three forced matchings may
be absent.

This closes the entire six-site all-rank-one, all-pair-Hessian-rigid
residual in
`rank-three-separator-collapse.md`. Indeed, its endpoint-line injectivity
and projective-arc lemmas, together with the slice-cover anchors and the
unique-anchor theorem, imply precisely the hypotheses above; Section 5
records the deduction.

## 2. The two cubic unions

The three matchings \(M_0,M_1,M_2\) are pairwise edge-disjoint. Their
union is therefore a simple cubic graph on six vertices. Up to vertex and
colour permutation it is either \(K_{3,3}\) or the triangular prism.

For the \(K_{3,3}\) orbit take

\[
\begin{aligned}
 M_0&=01|23|45,\\
 M_1&=02|14|35,\\
 M_2&=05|13|24.
\end{aligned}                                             \tag{2}
\]

and label its complementary edges

\[
 D_K=(d_0,\ldots,d_5)=(03,04,12,15,25,34).               \tag{3}
\]

For the prism orbit take

\[
\begin{aligned}
 M_0&=01|23|45,\\
 M_1&=02|14|35,\\
 M_2&=03|15|24,
\end{aligned}                                             \tag{4}
\]

with complementary six-cycle

\[
 D_P=(d_0,\ldots,d_5)=(04,05,12,13,25,34).                \tag{5}
\]

In either case every source support has the form

\[
                    E(G)=M_0\cup M_1\cup M_2\cup D',
                    \qquad D'\subseteq D_K\text{ or }D_P. \tag{6}
\]

Every present edge of \(D'\) has full support at both endpoints.

## 3. Every sparse case has a singleton fibre

For a set \(I\subseteq\{0,\ldots,5\}\), write
\(D_I=\{d_i:i\in I\}\).  The following tables classify \(I\) under all
vertex permutations and colour permutations preserving the three displayed
matchings.  The orbit-size column sums to \(64\) in the \(K_{3,3}\) table
and to \(63\) in the prism table.  In each row the displayed mixed word has
exactly the displayed compatible perfect matching in
\(M_0\cup M_1\cup M_2\cup D_I\).

For the \(K_{3,3}\) factorization (2):

| \(I\) | orbit size | mixed word | unique matching |
|---|---:|---|---|
| \(\varnothing\) | 1 | 002121 | 01\|24\|35 |
| 0 | 6 | 002121 | 01\|24\|35 |
| 01 | 6 | 002121 | 01\|24\|35 |
| 02 | 9 | 000100 | 03\|12\|45 |
| 012 | 18 | 000100 | 03\|12\|45 |
| 234 | 2 | 002121 | 01\|24\|35 |
| 0123 | 9 | 000001 | 04\|15\|23 |
| 0234 | 6 | 000100 | 03\|12\|45 |
| 01234 | 6 | 000001 | 04\|15\|23 |
| 012345 | 1 | 000102 | 01\|25\|34 |

For the prism factorization (4):

| \(I\) | orbit size | mixed word | unique matching |
|---|---:|---|---|
| \(\varnothing\) | 1 | 002121 | 01\|24\|35 |
| 0 | 6 | 002121 | 01\|24\|35 |
| 01 | 6 | 002121 | 01\|24\|35 |
| 02 | 3 | 000101 | 04\|12\|35 |
| 12 | 6 | 002121 | 01\|24\|35 |
| 012 | 12 | 000101 | 04\|12\|35 |
| 014 | 6 | 002121 | 01\|24\|35 |
| 034 | 2 | 000001 | 04\|13\|25 |
| 0123 | 3 | 000101 | 04\|12\|35 |
| 0124 | 6 | 000101 | 04\|12\|35 |
| 0134 | 6 | 000001 | 04\|13\|25 |
| 01234 | 6 | 000001 | 04\|13\|25 |

Every factor in a displayed matching is nonzero: a coordinate edge is used
in its prescribed colour, while every used \(D_I\)-edge has all coordinates
nonzero.  Thus every table row gives a nonzero singleton monomial in a mixed
target coefficient, contradicting (1).  The only unlisted support is the
complete prism, \(D'=D_P\).

## 4. A four-fibre rectangle kills the complete prism

The two alternating perfect matchings of \(D_P\) are

\[
              P=04|13|25,\qquad Q=05|12|34.              \tag{7}
\]

For a colouring \(a\), let \(z_a(P)\) and \(z_a(Q)\) be their nonzero
matching monomials and put

\[
                         R(a)={z_a(P)\over z_a(Q)}.        \tag{8}
\]

Because every edge of \(D_P\) is rank one, this ratio separates over the
vertices. More explicitly, if \(P(v)\) and \(Q(v)\) denote the two
incident cycle edges selected at \(v\), then for nonzero local factors

\[
 R(a)=\prod_{v=0}^5
 {x_{v|P(v)}(a_v)\over x_{v|Q(v)}(a_v)}.                 \tag{9}
\]

Consider the four mixed colourings

\[
\begin{aligned}
 t&=000001,& b&=010001,\\
 d&=100000,& e&=110000.
\end{aligned}                                             \tag{10}
\]

At every vertex, the two colours appearing in \((t,e)\) are the same
multiset as those appearing in \((b,d)\). Formula (9) therefore gives the
exact rectangle identity

\[
                         R(t)R(e)=R(b)R(d).               \tag{11}
\]

Direct compatibility, using (4)--(6), gives

\[
 \operatorname {PM}(b)=\operatorname {PM}(d)
 =\operatorname {PM}(e)=\{P,Q\}.                         \tag{12}
\]

All three are mixed target fibres. Their equations are binomials with
nonzero terms, so

\[
                         R(b)=R(d)=R(e)=-1.               \tag{13}
\]

Equations (11)--(13) force \(R(t)=-1\). The complete \(t\)-fibre is

\[
                \operatorname {PM}(t)=
                 \{01|25|34,\ P,\ Q\}.                  \tag{14}
\]

Thus the \(P\)- and \(Q\)-terms cancel. The remaining term
\(01|25|34\) is nonzero: \(01\in M_0\) is a nonzero pure coordinate
edge and \(25,34\in D_P\) have full support. Hence the mixed coefficient
at \(t\) is nonzero, the final contradiction. This proves Theorem 1.1.

## 5. Consequence of the all-pair rigid normal form

Assume now that every aggregate block on six sites has rank at most one,
every nonzero block has its rank-one factorization, every
pair-deleted Hessian is gauge-rigid, and \(H_6(A)=\Delta_{6,3}\).
Lemmas 6.11--6.12 of the separator-collapse note show that the nonzero
endpoint lines at any site are distinct and any three are independent.
For each centre and colour, the slice-cover contraction supplies an
incoming edge whose factor at the opposite endpoint is the corresponding
coordinate vector.  Thus there are at least \(6\cdot3=18\) directed anchor
incidences.  Endpoint-line injectivity permits at most one outgoing
incidence of a fixed colour at each of the six sites, hence at most eighteen
in total.  Equality follows: each site has exactly one incoming and one
outgoing incidence of each colour.

For a fixed colour \(c\), direct the unique local \(e_c\)-edge away from
its coordinate endpoint. Every site has one outgoing incidence, and the
anchor theorem gives every site at least one incoming incidence. Hence
these incidences form a permutation. At a site the incoming incidence is
unique, so Theorem 4.1 of
`rankone-incidence-contraction-obstructions.md` makes that edge mutual
\(e_c\otimes e_c\). The permutation is therefore a fixed-point-free
involution, namely a perfect matching \(M_c\).

The three matchings are edge-disjoint. Every remaining endpoint line is
noncoordinate; the projective-arc lemma makes all three of its coordinates
nonzero. Theorem 1.1 now applies. Consequently:

**Corollary 5.1.** No exact six-site source all of whose aggregate blocks
have rank at most one can have all fifteen pair-deleted Hessians
gauge-rigid.

## 6. Exact audit

`computations/verify_rank_one_complete_six_chart.py` enumerates all fifteen
perfect matchings and all eighty labelled triples of pairwise edge-disjoint
matchings. It verifies that every triple is a vertex/colour relabelling of
exactly one of (2) or (4), enumerates the support automorphism groups,
checks that the two tables are disjoint and cover all \(64+63\) singleton
supports, verifies every displayed unique fibre, and checks all four
complete-prism fibres (10)--(14) and the vertexwise multiset identity behind
(11).
