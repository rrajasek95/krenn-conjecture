# An exact unrestricted polarized counterexample on eight sites

## Outcome

The isolated polarized matching-power equation remains possible after the
six-site boundary.  There are integral quadratics \(q,z\) in the
site-square-zero algebra on eight ternary sites for which

\[
                     \boxed{\quad z\,{q^3\over3!}
                            =\Delta_{8,3}.\quad}          \tag{1}
\]

Only twelve unit same-colour cells are used, and exactly three decorated
matching terms are supported.  Thus a proposed uniform lemma excluding
\(zq^{m-1}/(m-1)!\) for every \(m\ge4\) is false already at \(m=4\).

This is not a Krenn counterexample: (1) is a polarized derivative, not the
ordinary fourth matching power \(q^4/4!\).  In fact this particular model
provably does **not** have the two-deletion factorization
\(z=a q+4ps\), for any \(a,p,s\).  Thus it separates the unrestricted
polarized equation sharply from the shared pair-cap condition.  The latter,
or compatibility among several cap rows, remains essential.

The exact audit is
[verify_polarized_eight_site_unrestricted_counterexample.py](../computations/verify_polarized_eight_site_unrestricted_counterexample.py).

## 1. The twelve cells

On vertices \(0,\ldots,7\), take the three perfect matchings

\[
\begin{aligned}
 P_0&=01\mid23\mid45\mid67,\\
 P_1&=01\mid24\mid36\mid57,\\
 P_2&=02\mid14\mid37\mid56.                              \tag{2}
\end{aligned}
\]

Designate

\[
                         d_0=01,\qquad d_1=24,\qquad d_2=37. \tag{3}
\]

For every \(r\), put a unit \(E_{rr}\) cell in \(z\) on \(d_r\), and put
a unit \(E_{rr}\) cell in \(q\) on every edge of
\(P_r\setminus\{d_r\}\).  Explicitly,

\[
\begin{array}{c|c|c}
r&z& q\\ \hline
0&01&23,45,67\\
1&24&01,36,57\\
2&37&02,14,56.
\end{array}                                               \tag{4}
\]

The underlying pair \(01\) carries two different cells: the colour-zero
cell belongs to \(z\), while the colour-one cell belongs to \(q\).  They
remain distinct endpoint-colour entries throughout.

## 2. Exact matching proof

A term of \(zq^3/3!\) chooses one distinguished \(z\)-edge and three
pairwise-disjoint \(q\)-edges.  The factorial divides the six orders of the
three \(q\)-edges, so each decorated choice has coefficient one.

After choosing \(d_0=01\), the \(q\)-graph on the remaining sites has the
unique perfect matching

\[
                              23\mid45\mid67.             \tag{5}
\]

After choosing \(d_1=24\), the pair \(01\) is forced and the remaining
four sites have the unique matching \(36\mid57\).  Hence the full remaining
matching is

\[
                              01\mid36\mid57.             \tag{6}
\]

After choosing \(d_2=37\), vertex \(2\) forces \(02\), vertex \(1\) then
forces \(14\), and the last edge is \(56\).  Thus the unique remaining
matching is

\[
                              02\mid14\mid56.             \tag{7}
\]

Every edge in (5), (6), or (7) has the same colour as its selected
\(z\)-edge.  Consequently the only three terms are the all-zero, all-one,
and all-two words, each with coefficient one.  This proves (1) over
\(\mathbb Z\), hence over \(\mathbb C\).

## 3. Consequence for the global route

The separation from the pair-cap equation is witnessed by one constant
minor.  Use row modes

\[
                         (0,0),\ (2,1),\ (3,2)
\]

and column modes

\[
                         (1,0),\ (4,1),\ (7,2).
\]

For every scalar \(a\), the corresponding cross matrix of \(z-aq\) is

\[
                              I_3.                        \tag{8}
\]

Indeed, its diagonal entries are the three distinguished cells in (3),
and every other selected cell of both \(z\) and \(q\) is zero.  On the
other hand, if \(p,s\) are linear elements, the same cross matrix of
\(ps\) is

\[
                 P_{\rm row}S_{\rm col}^{\mathsf T}
                   +S_{\rm row}P_{\rm col}^{\mathsf T}, \tag{9}
\]

a sum of two rank-one matrices.  It has rank at most two, whereas (8) has
rank three.  Therefore \(z-aq\ne4ps\) for all choices of the parameters.

The six-site pair-cap example already showed that an isolated polarized
equation can survive at the first boundary.  Equations (2)--(7) show that
the unrestricted polarized escape is not confined to six sites.  Therefore
the invertible-pair adjugate equation cannot be closed by a theorem about
\(zq^{m-1}\) alone.  A useful continuation has to retain at least one of:

1. the literal form \(z=a q+4ps\) at this boundary;
2. two or more colour-pair rows sharing the same two stars; or
3. overlap between adjugate identities from distinct physical pairs.

No ordinary matching-power realization and no all-even descent is claimed.
