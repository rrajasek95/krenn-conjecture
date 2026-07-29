# The coordinate-plane mixed packet cannot carry the nine responses

## 1. Result

Let \(U=\{0,\ldots,5\}\), let

\[
 B_0=\{0,1\},\qquad B_1=\{2,3\},\qquad B_2=\{4,5\},
 \tag{1}
\]

and let \(e_0^{(u)},e_1^{(u)},e_2^{(u)}\) be independent target
vectors at every site. Put

\[
 W_u=\operatorname {span}\{e_j^{(u)}:j\ne i\}
       \quad (u\in B_i).                                      \tag{2}
\]

Work in the site-square-zero algebra

\[
 {\cal R}_U=\bigotimes_{u\in U}(\mathbb C\oplus V_u),
 \qquad V_uV_u=0,
\]

and suppose

\[
 q=\sum_{u<v}q_{uv},\qquad q_{uv}\in W_u\otimes W_v,
 \qquad F=q^{[2]}.                                           \tag{3}
\]

The endpoint-ordered blocks in (3) are completely arbitrary. Let
\(p_i,s_j\in\bigoplus_uV_u\) be arbitrary multi-site rows and put

\[
 X_i=\bigotimes_{u\in U}e_i^{(u)}.
\]

**Theorem 1.1 (coordinate-plane mixed-packet obstruction).** The nine
equations

\[
                    p_i s_jF=\delta_{ij}X_i
                    \qquad(0\le i,j\le2)                         \tag{4}
\]

have no solution under (1)--(3).

In particular the coordinate-plane boundary of the sitewise endpoint
filtration is empty. This is stronger than the common-power application:
the additional equation \(q^{[3]}=0\) is not used. The proof retains all
mixed-colour four-site terms, arbitrary \(2\times2\) edge blocks, both row
endpoint orders, and arbitrary complex cancellation.

## 2. The double quotient purifies an entire hole slice

We may first replace every \(V_u\) by the target three-space
\(T_u=\operatorname {span}(e_0^{(u)},e_1^{(u)},e_2^{(u)})\). Indeed,
choose a linear projection \(V_u\to T_u\) which fixes \(T_u\), extend it
by \(1\mapsto1\), and apply the resulting algebra endomorphism to (4).
It fixes \(q,F\), and all three targets. Thus no component of a row
outside the target frame can rescue the equations.

For \(u\in B_i\), let

\[
 \epsilon_u:T_u\longrightarrow\mathbb C,
 \qquad \ker\epsilon_u=W_u,\qquad
 \epsilon_u(e_i^{(u)})=1.                                  \tag{5}
\]

Write \(p_{r,u}\) and \(s_{r,u}\) for the site components of the rows and
define response-index vectors

\[
 a_u=(\epsilon_u(p_{0,u}),\epsilon_u(p_{1,u}),
                         \epsilon_u(p_{2,u}))^{\mathsf T},\qquad
 b_u=(\epsilon_u(s_{0,u}),\epsilon_u(s_{1,u}),
                         \epsilon_u(s_{2,u}))^{\mathsf T}.       \tag{6}
\]

Decompose the degree-four tensor by its missing pair:

\[
                  F=\sum_{P\in\binom U2}F_P,
 \qquad F_P\in\bigotimes_{u\notin P}W_u.                    \tag{7}
\]

For \(P=\{u,v\}\), retain both endpoint orders and set

\[
                     N_P=a_ub_v^{\mathsf T}+a_vb_u^{\mathsf T}.
                                                                    \tag{8}
\]

Apply \(\epsilon_u\otimes\epsilon_v\) to all nine equations (4), with
the response indices retained as a \(3\times3\) matrix. A summand
\(F_Q\) survives only if both quotient sites are missing from it, that is,
\(P\subseteq Q\). Since both are pairs, this means \(P=Q\). Consequently

\[
 N_P\otimes F_P=
 \begin{cases}
   E_{ii}\otimes E_i(B_i),&P=B_i,\\
   0,&P\text{ meets two different }B\text{-classes},
 \end{cases}                                                \tag{9}
\]

where

\[
 E_i(B_i)=\bigotimes_{u\notin B_i}e_i^{(u)}.
\]

The second line is exact: at two sites with different omitted colours,
every \(X_i\) has a factor in one of the two planes and is killed.

The first line of (9) is a nonzero equality of decomposable tensors across
the bipartition

\[
 \operatorname {Mat}_{3\times3}\ \big|\
                  \bigotimes_{u\notin B_i}W_u.
\]

Uniqueness of the factors of a nonzero simple tensor gives nonzero scalars
\(\theta_i\) such that

\[
             N_{B_i}=\theta_iE_{ii},\qquad
             F_{B_i}=\theta_i^{-1}E_i(B_i).               \tag{10}
\]

Thus the quotient does not merely select the monochromatic coefficient of
\(F_{B_i}\): it forces the **entire** four-site hole slice, including every
mixed-colour cell, to be pure.

For a cross-class pair \(P\), (9) also gives the implication

\[
                         F_P\ne0\quad\Longrightarrow\quad N_P=0.
                                                                    \tag{11}
\]

No term of a cancelling sum has been selected in deriving (9)--(11).

## 3. Pure four-site cofactors force a connected zero-response graph

Form a graph \(G\) on \(U\) by joining sites in different \(B\)-classes
exactly when

\[
                              F_{\{u,v\}}\ne0.              \tag{12}
\]

We use the following exact four-site facts. They are proved in Sections
6.1--6.2 of
[the common-annihilator plane obstruction](common-annihilator-plane-obstruction.md),
and the focused checker below replays their complete symbolic and finite
certificates.

**Lemma 3.1 (pure-\(K_4\) apex).** Let four two-spaces carry an arbitrary
quadratic \(r\). If \(r^{[2]}\) is a nonzero pure four-tensor, then one
of the four sites is an apex: every incident block has the pure target
line as its endpoint factor there.

The proof differentiates \(r^{[2]}\). If \(r\ell=0\), the exact four
support normal forms show that every component of \(\ell\) is on the pure
target line. If there were no apex, the four transverse derivatives would
all have support two; their missing edges would form a perfect matching,
while the same support-two normal form makes the remaining cross edges both
rank two and rank at most one. This contradiction proves the lemma.

**Lemma 3.2 (zero-cofactor connectivity alternatives).** Assume the
three same-class cofactors in (10) are nonzero pure tensors.

1. The graph \(G\) has no isolated vertex.
2. If \(G\) is disconnected and has no isolated vertex, then its component
   sizes cannot be \(3+3\) or \(2+2+2\).

Here is the analytic proof of the first assertion. Suppose \(y\in B_0\)
is isolated and let \(x\) be its mate. On
\(D=B_1\cup B_2\), the first equation in (10) says that the restricted
quadratic has square \(\theta_0^{-1}e_0^{\otimes4}\). The four zero
cofactors obtained by deleting \(y\) and one site of \(D\) say, row by
row at \(x\), that the \(x\)-star is in the linear annihilator of this
quadratic. The extension-annihilator part of Lemma 3.1 forces every
endpoint of that star in \(D\) onto \(\mathbb C e_0\).

Now use the pure equation on \(B_0\cup B_2\) and quotient both \(B_2\)
planes by \(\mathbb C e_0\). Both cross matchings vanish, so the internal
block on \(B_0\) must be a nonzero multiple of
\(e_1\otimes e_1\). Repeating with \(B_0\cup B_1\) makes the same block a
nonzero multiple of \(e_2\otimes e_2\), a contradiction.

For completeness, the second assertion has a small exact branching
certificate. Normalize the pairs to \(01,23,45\), so the pure four-sets
are

\[
                         2345,\qquad0145,\qquad0123.       \tag{13}
\]

Choose one of the four target apices supplied by Lemma 3.1 in each set.
On a zero four-site cofactor, if two blocks at one vertex have endpoint
factor in the same line \(L\), quotienting by \(L\) gives the exact
disjunction

\[
 \boxed{\text{the third block has endpoint factor }L
        \quad\text{or}\quad\text{the opposite block is zero}.}   \tag{14}
\]

Two incompatible endpoint-line records make a block zero. A branch
closes when every matching of one of (13) contains a zero block or a
wrong target factor.

There are only \(4^3=64\) apex placements. For a transversal \(3+3\)
cut, the six zero four-sets are

\[
 1245,1234,0345,0134,0235,0125.                         \tag{15}
\]

The six apex orbits have sizes \(12,12,12,12,4,12\); the corresponding
proof trees have respectively

\[
 (38,11),(127,15),(31,12),(27,10),(29,10),(59,12)       \tag{16}
\]

as (leaf count, maximum depth). All leaves close. The nontransversal
\(3+3\) cut has the eight zero sets

\[
 1245,1235,1234,0245,0235,0234,0135,0134,               \tag{17}
\]

and a \(2+2+2\) split has the nine zero sets

\[
 1245,1235,1234,0345,0245,0234,0135,0134,0125.          \tag{18}
\]

The same recursion closes all 64 placements for (17) and (18). Rule
(14) is a tensor-product quotient over a field, so this finite certificate
does not assume support positivity or forbid complex cancellation.

## 4. The response matrices finish every graph pattern

By (10), no site can have \(a_u=b_u=0\): its same-class matrix would then
vanish. On every edge of \(G\), (11) says

\[
                         a_ub_v^{\mathsf T}+a_vb_u^{\mathsf T}=0.
                                                                    \tag{19}
\]

Suppose first that \(G\) has components of sizes \(2+4\). The two-site
component joins different classes, so the four-site component contains
both sites of some class \(B_c\). It is connected. If \(a_u=0\) at one
of its sites, then \(b_u\ne0\), and (19) propagates \(a=0\) through the
component, contrary to \(N_{B_c}\ne0\). Thus all its \(a\)'s are nonzero;
symmetrically all its \(b\)'s are nonzero. Equality of the two nonzero
rank-one summands in (19) makes all \(a\)'s on the component proportional
and all \(b\)'s proportional. Since
\(N_{B_c}=\theta_cE_{cc}\), both common lines are
\(\mathbb C f_c\), where \(f_0,f_1,f_2\) is the response-index basis.

For either other class \(d\), one endpoint of \(B_d\) lies in the
four-component. Hence

\[
                 N_{B_d}=f_cx^{\mathsf T}+yf_c^{\mathsf T}          \tag{20}
\]

up to nonzero scalar factors. Its \((d,d)\) entry is zero, contradicting
\(N_{B_d}=\theta_dE_{dd}\). Thus \(2+4\) is impossible.

If \(G\) were disconnected, Lemma 3.2 and the absence of singleton
components leave only \(2+4,3+3,2+2+2\), all now excluded. Therefore
\(G\) is connected.

If some \(a_u=0\), equation (19) propagates \(a=0\) through all of \(G\),
again making every \(N_{B_i}\) zero. Thus every \(a_u\) is nonzero, and
similarly every \(b_u\) is nonzero. Along every edge, (19) makes the two
\(a\)-lines equal and the two \(b\)-lines equal. Connectivity therefore
puts all six \(a_u\)'s on one line and all six \(b_u\)'s on one line.
All three same-class matrices \(N_{B_i}\) are consequently proportional
to one fixed rank-one matrix. This contradicts (10), because

\[
                              E_{00},E_{11},E_{22}          \tag{21}
\]

are pairwise nonproportional. Theorem 1.1 follows.

## 5. Sharpness and exact checker

The three pure cofactors and \(q^{[3]}=0\) alone are consistent. Put one
site of every \(B_i\) in each of two triples. Within either triple, join
the two sites of classes \(i,j\) by the pure line of the third colour, and
put every other block equal to zero. The support is two disjoint
triangles, so \(q^{[3]}=0\). Deleting \(B_i\) leaves exactly the two
opposite edges, both in colour \(i\), and hence gives
\(F_{B_i}=E_i(B_i)\). Its nonzero cross-class cofactor graph is a
six-cycle. Thus the response matrices and their zero equations are an
essential part of the obstruction.

Run

~~~sh
uv run python computations/verify_coordinate_plane_mixed_packet_obstruction.py
~~~

The checker audits the double-quotient incidence and target-survival table,
replays the four exact extension-annihilator normal forms and the pure-
\(K_4\) apex theorem, exhausts the three disconnected apex-propagation
certificates, enumerates every disconnected no-isolated cross-class graph,
checks the \(2+4\) response-matrix contradiction, and reconstructs the
sharp two-triangle model coefficient by coefficient.
