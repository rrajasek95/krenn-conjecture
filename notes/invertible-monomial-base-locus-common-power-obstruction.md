# The coordinate-monomial base locus has no matching-power lift

## 1. Outcome

The disjoint-pair abstract base-locus model in
[`invertible-monomial-nine-cap-classification.md`](invertible-monomial-nine-cap-classification.md)
cannot satisfy the common-power condition which it deliberately omits.
The first theorem below allows arbitrary nonzero target weights: partition
six sites into three pairs

\[
 U=P_0\mathbin{\dot\cup}P_1\mathbin{\dot\cup}P_2,
 \qquad |P_i|=2,
\]

and put

\[
 F_i=\bigotimes_{u\in U\setminus P_i}e_i^{(u)}.
\]

Here \(q^{[j]}\) denotes the unordered \(j\)-edge matching power (equal to
\(q^j/j!\) in characteristic zero).  For arbitrary nonzero scalars
\(\lambda_0,\lambda_1,\lambda_2\), there is no quadratic \(q\) in the
site-square-zero algebra on \(U\) such that

\[
                 q^{[2]}
                    =\lambda_0F_0+\lambda_1F_1+\lambda_2F_2,
 \qquad          q^{[3]}=0.                             \tag{1}
\]

The proof is field-independent when divided powers are interpreted as
unordered matching sums.  It uses neither genericity nor a support census.
The obstruction is the actual common-power relation: (1) first kills the
three within-pair blocks of \(q\); two nonzero pure four-site powers then
force their crossed product both to vanish and to share the same local
lines.  Those lines would have to be two distinct coordinate colors.

The full coordinate-monomial conclusion is stronger.  If the three missing
pairs are allowed to intersect but the actual nine products
\(p_i s_jF=\delta_{ij}\lambda_iX_i\) are retained, a short orientation
lemma leaves only one intersecting support type: a directed two-edge path
plus a disjoint edge.  Six four-site coefficient extractions exclude that
type from the common-power locus as well.

Consequently the eight-dimensional quotient-algebra countermodel from the
earlier note is sharp only before physical lifting.  It remains a valid
countermodel to the semisimple-quotient inference, but its complete
coordinate-monomial product table is not the annihilator quotient of a
six-site matching quadratic with the displayed three target lifts.

## 2. Square-free setup

For a finite site set \(S\), work in

\[
 \mathcal R_S=\bigotimes_{u\in S}(\mathbb F\oplus V_u),
 \qquad V_uV_u=0,
\]

over an arbitrary field \(\mathbb F\).  Products below are reordered into
the named site order.  The symbol \(q^{[j]}\) denotes the sum over unordered
\(j\)-edge matchings, so no division by \(j!\) is required.  The elementary
distinguished-edge identity is

\[
                         q q^{[2]}=3q^{[3]}.              \tag{2}
\]

Indeed, every three-edge matching on six sites occurs once for each choice
of its distinguished edge on the left.

We use one standard crossing-factor fact.

**Lemma 2.1 (crossing factorization).**  Let \(A,B,C,D\) be vector spaces
over \(\mathbb F\), and suppose nonzero tensors

\[
 X\in A\otimes B,\quad Y\in C\otimes D,\quad
 Z\in A\otimes D,\quad W\in C\otimes B
\]

satisfy, after the natural reordering into \(A\otimes C\otimes B\otimes D\),

\[
                         XY=ZW.                           \tag{3}
\]

Then all four tensors have matrix rank one.  Moreover their factors at
each named space lie on the same local line: for suitable nonzero
\(a,b,c,d\) and nonzero scalars,

\[
 X\in\mathbb F^*(a\otimes b),\quad
 Y\in\mathbb F^*(c\otimes d),\quad
 Z\in\mathbb F^*(a\otimes d),\quad
 W\in\mathbb F^*(c\otimes b).                            \tag{4}
\]

**Proof.**  Across the bipartition \((A\otimes B)|(C\otimes D)\), the
left side of (3) has matrix rank one.  The crossing reshuffle of the right
side has rank \(\operatorname{rank}(Z)\operatorname{rank}(W)\).  Hence
\(Z,W\) both have rank one.  Across
\((A\otimes D)|(C\otimes B)\), the same argument gives rank one for
\(X,Y\).  Equality of two nonzero completely decomposable tensors then
gives (4) by uniqueness of their factor lines. \(\square\)

## 3. The common-power obstruction

Write

\[
 P_0=A=\{a_0,a_1\},\qquad
 P_1=B=\{b_0,b_1\},\qquad
 P_2=C=\{c_0,c_1\}.
\]

**Theorem 3.1 (disjoint-pair common-power obstruction).**  Under the setup
of Section 1, equation (1) has no solution.

**Proof.**  Assume (1).  Multiplying its degree-four equation by \(q\), then using
(2) and the degree-six equation, gives

\[
             q(\lambda_0F_0+\lambda_1F_1+\lambda_2F_2)=0. \tag{5}
\]

Only the block \(q_{P_i}\) can multiply \(F_i\) without repeating a
site.  Furthermore the three full-support tensors \(q_{P_i}F_i\) have
disjoint color supports: for \(i\ne j\), the third pair
\(U\setminus(P_i\cup P_j)\) is colored \(i\) in one tensor and \(j\) in
the other.  Since every \(\lambda_i\) is nonzero, equation (5) therefore
implies separately

\[
                         q_{P_0}=q_{P_1}=q_{P_2}=0.       \tag{6}
\]

Thus

\[
                         q=q_{AB}+q_{AC}+q_{BC}.          \tag{7}
\]

The component of \(q^{[2]}\) on \(A\cup B\) is now just
\(q_{AB}^{[2]}\), and similarly for the other two pair-unions.  Hence

\[
 q_{AB}^{[2]}=\lambda_2F_2,\qquad
 q_{AC}^{[2]}=\lambda_1F_1.                              \tag{8}
\]

On a four-set containing both sites of \(A\), one site of \(B\), and one
site of \(C\), the target in (1) is zero.  A matching using a
\(q_{BC}\) block would have to pair it with the within-\(A\) block, which
is zero by (6).  The only surviving terms therefore give

\[
                         q_{AB}q_{AC}=0.                  \tag{9}
\]

Write the four blocks of these two quadratics as

\[
 X_{ij}\in V_{a_i}\otimes V_{b_j},\qquad
 Y_{ik}\in V_{a_i}\otimes V_{c_k}
 \quad(0\le i,j,k\le1).                                  \tag{10}
\]

The two equations in (8) say

\[
\begin{aligned}
 X_{00}X_{11}+X_{01}X_{10}&=\lambda_2F_2,\\
 Y_{00}Y_{11}+Y_{01}Y_{10}&=\lambda_1F_1.                \tag{11}
\end{aligned}
\]

At least one summand in each nonzero line of (11) is nonzero.  Relabeling
the two sites inside \(B\) and \(C\), if necessary, we may assume

\[
                         X_{00},X_{11},Y_{00},Y_{11}\ne0.\tag{12}
\]

The \(\{a_0,a_1,b_j,c_k\}\)-component of (9) is

\[
                         X_{0j}Y_{1k}+X_{1j}Y_{0k}=0.    \tag{13}
\]

For \((j,k)=(0,1)\), the first product in (13) is nonzero by
(12), so the second is also nonzero.  For \((j,k)=(1,0)\), the second
product is nonzero, so the first is also nonzero.  Consequently every one
of the eight blocks in (10) is nonzero.

Apply Lemma 2.1 to (13), absorbing its minus sign into one factor.  Varying
\(j,k\) shows that there are fixed nonzero local vectors

\[
 a_i\in V_{a_i},\qquad b_j\in V_{b_j},\qquad c_k\in V_{c_k}
\]

and nonzero scalars \(x_{ij},y_{ik}\) such that

\[
                         X_{ij}=x_{ij}a_i b_j,\qquad
                         Y_{ik}=y_{ik}a_i c_k.            \tag{14}
\]

The crucial point is that the same line \(\mathbb F a_i\) occurs in both
families at each site of \(A\).

Substitution in (11) gives

\[
\begin{aligned}
 (x_{00}x_{11}+x_{01}x_{10})a_0a_1b_0b_1&=\lambda_2F_2,\\
 (y_{00}y_{11}+y_{01}y_{10})a_0a_1c_0c_1&=\lambda_1F_1. \tag{15}
\end{aligned}
\]

Both scalar parentheses are nonzero.  Uniqueness of the local factor
lines of a nonzero decomposable tensor makes

\[
             \mathbb F a_0=\mathbb F e_2^{(a_0)}
             =\mathbb F e_1^{(a_0)},                    \tag{16}
\]

and likewise at \(a_1\).  The two coordinate axes are distinct, so (16)
is impossible.  This proves the theorem. \(\square\)

## 4. The full coordinate-monomial product table

Section 4 of
[`invertible-monomial-nine-cap-classification.md`](invertible-monomial-nine-cap-classification.md)
uses precisely

\[
 P_i=\{u_i,v_i\},\qquad
 F=F_0+F_1+F_2,\qquad
 p_i=e_i^{(u_i)},\qquad s_i=e_i^{(v_i)}.                 \tag{17}
\]

Multiplication by the abstract \(F\) gives

\[
                         p_i s_jF=\delta_{ij}X_i,         \tag{18}
\]

which satisfies the quotient-level nine-cap table on the base locus.
For a physical lift at the first six-site common-power boundary one would
need exactly

\[
                         F=q^{[2]},\qquad q^{[3]}=0.      \tag{19}
\]

The theorem excludes (19), so the displayed formal escape is closed by the
omitted source-specific condition.  We now remove the disjointness
assumption while retaining the product table which makes this a nine-cap
submodel.

Let \(P_i=(u_i,v_i)\) be ordered pairs of distinct sites, put

\[
 F=\sum_i\lambda_i
       \bigotimes_{u\notin P_i}e_i^{(u)},
 \qquad p_i=e_i^{(u_i)},\qquad s_i=e_i^{(v_i)},          \tag{20}
\]

where every \(\lambda_i\ne0\), and impose the full product table

\[
                         p_i s_jF=\delta_{ij}\lambda_iX_i
 \quad(0\le i,j\le2).                                   \tag{21}
\]

### 4.1 The product table leaves two support types

**Lemma 4.1 (oriented missing-pair classification).**  Under (20)--(21),
the three underlying pairs are distinct.  Up to permuting colors and sites,
exactly one of the following occurs.

1. They are three disjoint pairs.
2. They are
   \[
                         P_0=(a,b),\qquad P_1=(b,c),
                         \qquad P_2=(d,e),               \tag{22}
   \]
   with \(a,b,c,d,e\) distinct.  The orientation of the disjoint pair is
   arbitrary.

**Proof.**  In the diagonal product \(p_i s_iF\), the \(F_i\) term gives
the required \(\lambda_iX_i\).  If an underlying pair \(P_k\), \(k\ne i\),
equaled \(P_i\), its nonzero term would give the distinct mixed word having
color \(i\) on \(P_i\) and color \(k\) on the complement.  Hence the three
pairs are distinct.

For \(i\ne j\), if \(u_i\ne v_j\) and
\(\{u_i,v_j\}=P_k\), the unique surviving \(F_k\) term in
\(p_i s_jF\) is nonzero, contradicting its required value zero.  Thus

\[
 u_i\ne v_j\quad\Longrightarrow\quad
                         \{u_i,v_j\}\notin\{P_0,P_1,P_2\}. \tag{23}
\]

Suppose two pairs meet at a site.  They cannot both point out of that site:
then (23) applied to their two indices reproduces the second pair.  They
cannot both point into it for the symmetric reason.  They therefore form a
directed path, say \((a,b),(b,c)\).

A third edge at \(b\) would have to point both into and out of \(b\), so is
impossible.  If the third edge joins \(a\) to \(c\), its forced orientation
completes a directed triangle, but \(\{u_0,v_1\}=\{a,c\}\) violates
(23).  If it joins \(a\) to a new vertex \(d\), it must point \(d\to a\);
then \(\{u_1,v_2\}=\{a,b\}=P_0\), again violating (23).  The case of an
edge at \(c\) is symmetric.  Thus the third edge is disjoint, giving (22).
If no two pairs meet, they form the first case. \(\square\)

### 4.2 The sole intersecting type is not a common power

Assume the second case (22), and let \(f\) be the sixth site.  Suppose in
addition to (20)--(21) that

\[
                         F=q^{[2]},\qquad q^{[3]}=0.      \tag{24}
\]

As in (5)--(6), the identity \(qF=3q^{[3]}=0\), together with the distinct
color support outside the union of any two missing pairs, gives

\[
                         q_{ab}=q_{bc}=q_{de}=0.          \tag{25}
\]

The \(U\setminus P_2=\{a,b,c,f\}\) component of \(q^{[2]}\) has only one
possibly nonzero matching, so

\[
                         q_{ac}q_{bf}=\lambda_2F_2\ne0.  \tag{26}
\]

In particular \(q_{ac}\) and \(q_{bf}\) are nonzero.  Now use four-site
supports absent from (20).  On \(\{a,b,c,d\}\), (25) leaves only
\(q_{ac}q_{bd}\); hence \(q_{bd}=0\).  The support
\(\{a,b,c,e\}\) similarly gives \(q_{be}=0\).  Then the zero components
on \(\{a,b,d,f\}\) and \(\{a,b,e,f\}\), using the nonzero block
\(q_{bf}\), give

\[
                         q_{ad}=q_{ae}=0.                 \tag{27}
\]

Finally the zero components on \(\{b,c,d,f\}\) and
\(\{b,c,e,f\}\) give

\[
                         q_{cd}=q_{ce}=0.                 \tag{28}
\]

But the required \(F_0\) component lives on \(\{c,d,e,f\}\).  Its three
matching products are

\[
                         q_{cd}q_{ef}+q_{ce}q_{df}
                                      +q_{cf}q_{de},      \tag{29}
\]

which is zero by (25) and (28), contradicting
\(\lambda_0F_0\ne0\).

Combining this argument with the disjoint-pair theorem and Lemma 4.1 gives
the exact closure.

**Theorem 4.2 (coordinate-monomial common-power obstruction).**  No six-site
quadratic \(q\), no three ordered missing pairs, and no nonzero
\(\lambda_i\) satisfy (20), (21), and (24).

## 5. Scope and the next shared-power problem

The result does **not** close either the full cyclic or the full diagonal
direct-block orbit, nor does it exclude a general solution of the nine
pair-slice equations.  It closes the coordinate-monomial base-locus
submodel in which all six star rows are one-site coordinate vectors and
their common Hessian multiplier has exactly the three displayed monomial
lifts.  In a general base-locus solution, the target lifts may be sums of
many four-site tensors and the star rows may have support at several sites.
The next bounded common-power problem is to allow one of those two
generalizations while retaining all nine products and \(F=q^{[2]}\), not
to enumerate more disjoint supports.

The product table in (21) is essential and must not be dropped.  For
example, take all three missing pairs equal to one pair \(P\), and on its
four-site complement put the standard ternary \(K_4\) source, with one
unit same-color perfect matching in each color.  With the other two sites
isolated, its quadratic satisfies exactly

\[
                         q^{[2]}=F_0+F_1+F_2,\qquad
                         q^{[3]}=0,                       \tag{30}
\]

so the common-power equations alone have an exact repeated-pair
countermodel.  It fails (21): multiplying by \(p_i s_i\) retains, besides
\(X_i\), the two mixed tensors having color \(i\) on \(P\) and another
color on its complement.  Thus the next calculation must retain all nine
products, not merely classify the powers in isolation.
