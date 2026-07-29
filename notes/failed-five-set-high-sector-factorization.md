# Failed five-set cuts give a degree-five common-power equation

> **Strengthening (2026-07-26).**  For ternary local spaces one may always
> choose the failed-cut witness in the kernel of the internal cofactor map,
> independently of the external shore.  Such a witness has
> \(\delta_U(\beta)\ne0\) and the stronger identity \(p_1(\beta)=0\), not
> merely \(q_C^sp_1(\beta)=0\).  See
> [the universal five-set cofactor annihilator](five-set-universal-cofactor-annihilator.md).
> The standalone countermodels below already allow \(p_1=0\), so the
> common-power conclusion remains noncontradictory; the live problem is the
> compatibility of the high-crossing quotient identities over overlapping
> five-sets.

## 1. Outcome

Let \(B=C\mathbin{\dot\cup}U\), where \(|U|=5\) and
\(|C|=2s+1\).  Split the source quadratic in the site-square-zero
algebra as

\[
                         q_B=q_C+q_X+q_U,                 \tag{1}
\]

where the three summands use edges internal to \(C\), crossing
\(C|U\), and internal to \(U\), respectively.  If
\(H_B(q_B)=\Delta_{B,3}\) and
\(\beta\in\ker F_1\) has
\(b=\delta_U(\beta)\ne0\), then

\[
 \boxed{\quad
 \Delta_C(b)
 =\frac{q_C^{s-2}}{(s-2)!}
       \left(\frac{q_Cp_3(\beta)}{s-1}+p_5(\beta)\right).
 \quad}                                                   \tag{2}
\]

Here \(p_3\) and \(p_5\) are explicit contractions of the crossing
quadratic, defined in (6) below.  Thus every failed five-set cut gives a
nonzero diagonal odd tensor in the image of multiplication by
\(q_C^{s-2}\) from degree five.

The common-power conclusion by itself is not an obstruction.  For
\(|C|=7,9,11\) there are exact integral examples with all three entries of
\(b\) nonzero.  They can moreover be chosen so that the graph of rank-three
blocks of \(q_C\) is connected and nonbipartite.  These examples realize
the actual contraction data: \(q_U=0\), \(\beta\in\ker F_1\),
\(p_3=0\), and \(p_5\) is obtained from \(q_X\) and the same \(\beta\).
They are not full GHZ sources.  Consequently any contradiction must use
global mixed-GHZ equations that are lost after this one contraction.

There is one genuine support consequence.  For every color \(r\) with
\(b_r\ne0\), the graph of nonzero scalar cells
\(q_{ij}(r,r)\) has a matching covering all but at most five vertices of
\(C\).  This is sharp for the examples.

The exact audit is
`computations/verify_failed_five_set_high_sector_factorization.py`.

## 2. Exact sector expansion and factorials

Write

\[
 \mathcal R_B=\bigotimes_{v\in B}(\mathbb C\oplus V_v),
 \qquad V_v^2=0.
\]

If \(|B|=2s+6\), its matching tensor is

\[
                         H_B(q_B)=\frac{q_B^{s+3}}{(s+3)!}. \tag{3}
\]

Because the three terms in (1) commute, the multinomial coefficient in
(3) cancels the factorials of their powers.  A term with \(j\) crossing
edges has exponents \((a,j,d)\) determined by

\[
                    2a+j=2s+1,\qquad j+2d=5.             \tag{4}
\]

Thus \(j\in\{1,3,5\}\), and the three crossing sectors are exactly

\[
\begin{aligned}
 T_1&=\frac{q_C^s}{s!}\;q_X\frac{q_U^2}{2!},\\
 T_3&=\frac{q_C^{s-1}}{(s-1)!}\;\frac{q_X^3}{3!}q_U,\\
 T_5&=\frac{q_C^{s-2}}{(s-2)!}\;\frac{q_X^5}{5!}.
\end{aligned}                                             \tag{5}
\]

For \(\beta\in V_U^*\), contract the component occupying all five sites
of \(U\), and define homogeneous elements of \(\mathcal R_C\) by

\[
\begin{aligned}
 p_1(\beta)&=\beta\mathbin{\lrcorner_U}
                \left(q_X\frac{q_U^2}{2!}\right)
                  \in(\mathcal R_C)_1,\\
 p_3(\beta)&=\beta\mathbin{\lrcorner_U}
                \left(\frac{q_X^3}{3!}q_U\right)
                  \in(\mathcal R_C)_3,\\
 p_5(\beta)&=\beta\mathbin{\lrcorner_U}
                \left(\frac{q_X^5}{5!}\right)
                  \in(\mathcal R_C)_5.
\end{aligned}                                             \tag{6}
\]

The one-crossing flattening therefore satisfies

\[
                  F_1\beta=\frac{q_C^s}{s!}p_1(\beta).   \tag{7}
\]

For \(b=(b_0,b_1,b_2)=\delta_U(\beta)\), put

\[
                  \Delta_C(b)=\sum_{r=0}^2b_r
                         \prod_{c\in C}x_{c,r}.          \tag{8}
\]

If \(H_B(q_B)=\Delta_{B,3}\), contraction by \(\beta\) gives
\(\Delta_C(b)\).  When \(F_1\beta=0\), (5)--(6) leave

\[
 \Delta_C(b)=
   \frac{q_C^{s-1}}{(s-1)!}p_3(\beta)
   +\frac{q_C^{s-2}}{(s-2)!}p_5(\beta).                 \tag{9}
\]

Factoring \(q_C^{s-2}/(s-2)!\) from (9) proves (2), including the
factor \(1/(s-1)\).  Notice that (7) only says
\(q_C^sp_1=0\); it does not in general imply \(p_1=0\).

## 3. A support consequence that survives cancellation

Put \(k=s-2\) and

\[
                         z_5=\frac{q_Cp_3}{s-1}+p_5.
                                                                  \tag{10}
\]

For a color \(r\), let \(G_r(q_C)\) be the graph on \(C\) with edge
\(ij\) precisely when the \((r,r)\) cell of the block \((q_C)_{ij}\)
is nonzero.

**Lemma 3.1 (five-defect matching condition).**  If

\[
                  \frac{q_C^k}{k!}z_5=\Delta_C(b)        \tag{11}
\]

and \(b_r\ne0\), then \(G_r(q_C)\) has a matching of size \(k\).

**Proof.**  Take the coefficient of the all-\(r\) word in (11).  Splitting
\(z_5\) by its five-site support gives

\[
 b_r=\sum_{\substack{S\subset C\\|S|=5}}
       z_{5,S}(r^S)\,
       H_{C\setminus S}\bigl((q_{ij}(r,r))\bigr).       \tag{12}
\]

The sum is nonzero, so some scalar matching polynomial on
\(C\setminus S\) is nonzero.  At least one of its monomials is nonzero,
and its \(k\) edges form the required matching.  \(\square\)

This lemma can exclude (11) when one active diagonal-cell graph has
matching number less than \(s-2\).  It cannot be strengthened merely by
assuming a connected nonbipartite graph of full-rank blocks, as the next
construction shows.

## 4. Exact three-color routing countermodels

Fix \(1\le k\le5\), so \(|C|=2k+5\), and take disjoint sets

\[
 A=\{a_1,\ldots,a_k\},\quad
 D=\{d_1,\ldots,d_k\},\quad
 E'=\{e_1,\ldots,e_k\},\quad
 E=\{t_1,\ldots,t_{5-k}\}.                              \tag{13}
\]

Thus \(C=A\sqcup D\sqcup E'\sqcup E\).  Define three matchings

\[
 M_0=\{a_id_i:1\le i\le k\},\quad
 M_1=\{a_ie_i:1\le i\le k\},\quad
 M_2=\{d_ie_i:1\le i\le k\},                           \tag{14}
\]

and their five-site complements

\[
 Z_0=E'\sqcup E,\qquad Z_1=D\sqcup E,\qquad
 Z_2=A\sqcup E.                                         \tag{15}
\]

Let

\[
 q_0=\sum_{i=1}^k
   \bigl(x_{a_i,0}x_{d_i,0}
        +x_{a_i,1}x_{e_i,1}
        +x_{d_i,2}x_{e_i,2}\bigr)                       \tag{16}
\]

and, for arbitrary \(b_0,b_1,b_2\), put

\[
                         p_5=\sum_{r=0}^2b_r
                              \prod_{v\in Z_r}x_{v,r}.  \tag{17}
\]

After multiplication by the \(r\)-th monomial in (17), every edge of
\(q_0\) outside \(M_r\) meets the occupied set \(Z_r\) and vanishes.
The only surviving product of \(k\) edges is \(M_r\).  Hence

\[
                  \boxed{\quad\frac{q_0^k}{k!}p_5
                         =\Delta_C(b).\quad}             \tag{18}
\]

For \(k\le3\), the common set \(E\) has at least two vertices.  Add to
\(q_0\) arbitrary blocks on all pairs having at least one endpoint in
\(E\), and call their sum \(h\).  Every monomial of \(p_5\) occupies all
of \(E\), so \(hp_5=0\).  Consequently

\[
             \frac{(q_0+h)^k}{k!}p_5
             =\frac{q_0^k}{k!}p_5=\Delta_C(b).           \tag{19}
\]

Taking every block of \(h\) to be the \(3\times3\) identity makes the
rank-three block graph connected and nonbipartite: it contains the clique
on \(E\), and every other vertex is adjacent to every vertex of \(E\).
This gives the advertised examples for \(|C|=7,9,11\).

These degree-five tensors also come from genuine five-shore contraction
data.  Let \(U=\{u_1,\ldots,u_5\}\), choose bijections
\(f_r:U\to Z_r\), and set

\[
 q_X=\sum_{r=0}^2\sum_{j=1}^5
                  x_{f_r(u_j),r}x_{u_j,r},qquad q_U=0.  \tag{20}
\]

Define \(\beta\) on the word basis of \(V_U\) by

\[
 \beta(x_{u_1,r}\cdots x_{u_5,r})=b_r,qquad
 \beta(\text{every mixed word})=0.                       \tag{21}
\]

For each constant \(r\)-word there is exactly one crossing perfect
matching, namely the graph of \(f_r\).  Equations (20)--(21) therefore
give

\[
 \delta_U(\beta)=b,qquad
 p_5(\beta)=p_5,qquad p_3(\beta)=p_1(\beta)=0.          \tag{22}
\]

In particular \(F_1\beta=0\), and (19) is exactly the high-sector
identity (2), not an arbitrary divisibility example.

For the audited rank-three cases \(k\le3\), the corresponding full source
is visibly not GHZ.  In the all-zero
matching, switch the crossing edge landing at any common vertex of \(E\)
from the color-zero bijection to the color-one bijection.  Its endpoints
are unchanged, so this is still a perfect matching, but its output word is
mixed.  All source coefficients in this construction are positive, hence
that mixed coefficient cannot cancel.

The restriction \(k\le5\) in this routing family is combinatorial: the
three pairwise-overlap parts in (13) use \(3k\) vertices, while
\(|C|=2k+5\).  This is not a proof that different constructions fail for
\(k>5\).

## 5. At seven sites divisibility is generically vacuous

There is an even sharper limitation when \(|C|=7\).  For the following
integral quadratic \(q\), the map

\[
              \mu_q:(\mathcal R_C)_5\longrightarrow
                    (\mathcal R_C)_7,qquad z\longmapsto qz          \tag{23}
\]

has full row rank \(3^7=2187\).  The checker performs exact bit row
reduction on the reduction of this integer matrix modulo two and obtains
rank \(2187\).  A maximal minor is therefore odd, hence nonzero over
\(\mathbb Q\) and \(\mathbb C\).  Since maximal rank is a Zariski-open
condition, (23) is surjective for generic \(q\).

In the table, a block is written as its three binary rows; omitted cells
inside a displayed block are zero.

\[
\begin{array}{c|c@{\qquad}c|c@{\qquad}c|c}
01&100/111/000&02&100/101/011&03&110/101/011\\
04&100/010/001&05&000/110/000&06&110/011/010\\
12&101/101/011&13&111/101/011&14&111/110/000\\
15&101/001/110&16&001/111/111&23&001/110/011\\
24&100/101/100&25&010/011/110&26&100/100/010\\
34&000/101/101&35&000/111/101&36&001/011/011\\
45&001/000/100&46&110/010/011&56&011/101/010
\end{array}                                               \tag{24}
\]

Thus at the first nontrivial size every seven-site tensor, not only the
three diagonal words, has the required degree-five quotient for generic
\(q_C\).  The special form (10) and the simultaneous equations from other
five-set cuts are indispensable.

## 6. Boundary of the result

Equation (2) is a necessary consequence of one failed cut in a hypothetical
GHZ source.  The examples in Section 4 satisfy that consequence together
with its actual \((q_X,q_U,\beta)\) provenance, but their full matching
tensors have mixed coefficients.  They therefore prove neither existence
nor nonexistence of the global source.  What they rule out is a standalone
common-power contradiction, even after imposing all three active colors
and the usual connected nonbipartite rank-three graph hypothesis.
