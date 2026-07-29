# An exact eight-site model inside the shared pair-cap ansatz

## 1. Outcome

The literal eight-site pair-cap equation is consistent.  There are rational
quadratics \(q,z\), rational linear forms \(p,s\), and \(a=1/4\) in the
site-square-zero algebra on eight ternary sites such that

\[
             \boxed{\quad z=a q+4ps,\qquad
                    zq^{[3]}=\Delta_{8,3}.\quad}         \tag{1}
\]

Here \(q^{[j]}=q^j/j!\) is the unordered \(j\)-edge matching power.  The
forms \(p,s\) are genuinely global: the same two forms produce all blocks
of \(ps\), with both endpoint orders retained.

This is not a Krenn counterexample.  The ordinary fourth matching power of
\(q\) has two mixed words, and \(z\ne q\).  Nor is an extension to all caps
of one larger source asserted.  The model proves sharply that one isolated
identity of the full form in (1), even with exact rational coefficients,
cannot be the missing eight-site obstruction.  A positive cap descent must
extract a nonlinear source-variable consequence from the complete shared-row
system.  Merely rewriting that complete tensor system at an overlapping
physical pair does not add equations, as the later exchange theorem records.

## 2. The twelve cells of \(q\)

Number the sites \(0,\ldots,7\), and take the three perfect matchings

\[
\begin{aligned}
 P_0&=01\mid23\mid45\mid67,\\
 P_1&=07\mid12\mid34\mid56,\\
 P_2&=04\mid17\mid26\mid35.                             \tag{2}
\end{aligned}
\]

Put a unit monochromatic color-\(i\) cell on every edge of \(P_i\), and no
other cell in \(q\):

\[
                         q=\sum_{i=0}^2\sum_{uv\in P_i}
                              e_i^{(u)}e_i^{(v)}.         \tag{3}
\]

The twelve physical edges in (2) are distinct.  Their union has exactly
five perfect matchings.  Three are \(P_0,P_1,P_2\); the other two decorated
matchings are

\[
\begin{aligned}
 M_A&=04_2\mid12_1\mid35_2\mid67_0,\\
 M_B&=04_2\mid17_2\mid23_0\mid56_1,                     \tag{4}
\end{aligned}
\]

where a subscript records the common color of that cell.  Denote the
corresponding mixed basis words, in site order, by the same letters:

\[
\begin{aligned}
 M_A&=e_{21122200},\\
 M_B&=e_{22002112}.                                     \tag{5}
\end{aligned}
\]

Every cell has coefficient one, so the complete fourth matching power is

\[
                  q^{[4]}=X_0+X_1+X_2+M_A+M_B,
 \qquad X_i=e_i^{\otimes8}.                             \tag{6}
\]

There is no cancellation or support inference in (6): it is the literal
five-matching enumeration.

## 3. A two-cell global product cap

Use only the color-two modes of \(p,s\), and set

\[
\begin{aligned}
 p&=e_2^{(0)}+e_2^{(2)}-\tfrac18e_2^{(4)}-\tfrac18e_2^{(6)},\\
 s&=e_2^{(0)}-e_2^{(2)}-\tfrac18e_2^{(4)}+\tfrac18e_2^{(6)}.
                                                               \tag{7}
\end{aligned}
\]

At the four active modes, the pairs of coefficients \((p,s)\) are

\[
 x_0=(1,1),\quad x_2=(1,-1),\quad
 x_4=(-1/8,-1/8),\quad x_6=(-1/8,1/8).                 \tag{8}
\]

For distinct sites \(u,v\), the block coefficient of \(ps\) is the
hyperbolic Gram product

\[
             \beta(x_u,x_v)=p_us_v+s_up_v.              \tag{9}
\]

The lines spanned by \(x_0,x_4\) and by \(x_2,x_6\) are orthogonal.  Direct
calculation gives

\[
 (ps)_{04}(2,2)=-\tfrac14,qquad
 (ps)_{26}(2,2)= \tfrac14,                              \tag{10}
\]

and every other cell of \(ps\) is zero.  In particular, all four possible
cross terms between the two lines vanish exactly; (10) is not a shorthand
which discards endpoint-order terms.

Put

\[
                         a=\tfrac14,qquad z=\tfrac14q+4ps. \tag{11}

\]

Thus \(z\) has the same twelve-cell support as \(q\).  Its coefficients
are \(1/4\) except

\[
                         z_{04}(2,2)=-\tfrac34,qquad
                         z_{26}(2,2)= \tfrac54.          \tag{12}
\]

## 4. Exact cancellation of the two mixed matchings

Let \(F_{uv}\) be the component of \(q^{[3]}\) on the six sites outside
\(u,v\).  On the complement of \(04\), there are exactly three supported
decorated matchings:

\[
 12_1\mid35_2\mid67_0,qquad
 17_2\mid23_0\mid56_1,qquad
 17_2\mid26_2\mid35_2.                                  \tag{13}
\]

After adjoining the color-two cell on \(04\), these give respectively
\(M_A,M_B,X_2\).  On the complement of \(26\), the sole supported matching
is

\[
                         04_2\mid17_2\mid35_2,           \tag{14}
\]

which gives \(X_2\).  Equations (10), (13), and (14) therefore imply

\[
\begin{aligned}
 psq^{[3]}
   &=-\tfrac14(M_A+M_B+X_2)+\tfrac14X_2\\
   &=-\tfrac14(M_A+M_B).                                 \tag{15}
\end{aligned}
\]

The distinguished-edge identity \(q q^{[3]}=4q^{[4]}\), followed by
(6), (11), and (15), now gives

\[
\begin{aligned}
 zq^{[3]}
   &=\tfrac14q q^{[3]}+4psq^{[3]}\\
   &=q^{[4]}-(M_A+M_B)\\
   &=X_0+X_1+X_2=\Delta_{8,3}.                           \tag{16}
\end{aligned}
\]

There is no hidden factorial here: the checker computes
\(zq^{[3]}=zq^3/3!\) directly.  Equivalently,
\(q q^{[3]}=4q^{[4]}\), exactly as used above.  This proves (1) over
\(\mathbb Q\), hence over \(\mathbb C\).

## 5. The same \(q\) cannot satisfy all nine cap equations

The construction above solves one aggregate equation.  It does not supply
the direct \(3\times3\) cap matrix and all nine products formed from three
shared \(p\)-rows and three shared \(s\)-rows.  In fact, for this fixed
\(q\), such data do not exist.

Up to relabeling, this is the already registered Laurent border core from
[the pair-suspension obstruction](n8-border-pair-suspension-obstruction.md).
One exact isomorphism sends our colors \(0,1,2\) to its colors \(1,2,0\)
and our sites \(0,\ldots,7\) respectively to
\(3,0,1,5,6,7,4,2\).  Proposition 5.1 below is therefore an independent,
compact relabeling of that full-nine obstruction, not a new global route.
The new point of the present note is the explicit isolated aggregate
countermodel (1) on the same isomorphism class of core.

Suppose, toward a contradiction, that scalars \(a_{ij}\) and linear forms
\(p_i,s_j\), \(0\leq i,j<3\), satisfy

\[
       (a_{ij}q+4p_i s_j)q^{[3]}=\delta_{ij}X_i
       \qquad(0\leq i,j<3).                            \tag{17}
\]

Put \(Q=q^{[4]}\), \(F=q^{[3]}\), and \(C=(a_{ij})\).  Since
\(qF=4Q\), division by four rewrites (17) as

\[
       a_{ij}Q+p_i s_jF=\tfrac14\delta_{ij}X_i.         \tag{18}
\]

For a color mode \(x=(u,\alpha)\), package the three row coefficients as

\[
 P_x=(p_{0,x},p_{1,x},p_{2,x})^{\mathsf T},\qquad
 S_x=(s_{0,x},s_{1,x},s_{2,x})^{\mathsf T},
\]

and for two modes on distinct sites define the full response matrix

\[
 R_{xy}=\Phi(x,y):=P_xS_y^{\mathsf T}+P_yS_x^{\mathsf T}. \tag{19}
\]

Thus all nine equations in (18) are one matrix-valued coefficient identity.
There are \(28\cdot9=252\) possible quadratic cells \(xy\).  Call the
twelve cells occurring in (3) active and the other 240 inactive.

### Singleton exposure

Consider the linear matching map

\[
 H_q:\ (R_{xy})\longmapsto \sum_{xy}R_{xy}\,xy\,q^{[3]}. \tag{20}
\]

An exact row census has the following three properties.

1. \(H_q\) has 363 nonzero coloring rows.
2. Of these, 358 are singleton rows: only one of the 252 cell columns is
   nonzero in that row, and its coefficient is one.
3. The columns exposed by those singleton rows are exactly the 240
   inactive cells; no active cell is exposed.

Every singleton word lies outside the five-word support (6), and hence
outside the target support as well.  Taking that word's coefficient in
(18) therefore gives \(R_{xy}=0\) for its unique column.  Consequently

\[
                         R_{xy}=0
       \quad\text{for every inactive cell }xy.          \tag{21}
\]

The census is exhaustive, not probabilistic: the companion checker
constructs every row from all 105 perfect matchings and all \(3^8\)
colorings.

### The twelve remaining blocks have one rank-one direction

We need only the elementary zero-pair classification for (19).  If
\(\Phi(x,y)=0\) and both mode points are nonzero, then either both are
\(P\)-pure, both are \(S\)-pure, or both are mixed and

\[
                    (P_y,S_y)=\lambda(P_x,-S_x)         \tag{22}
\]

for some \(\lambda\ne0\).  Indeed, a sum of two nonzero rank-one matrices
can vanish only when their left factors and their right factors are
respectively proportional; the pure cases follow directly.

Take two nonzero active blocks.  Their physical edges are distinct.  If
the edges are disjoint, all four cross-mode cells are inactive and hence
zero by (21).  A pure endpoint would force the second active block to
vanish, so the endpoints are mixed antipodal pairs by (22).  Both active
blocks are therefore proportional to the same rank-one matrix.

If the physical edges meet at one site, write the blocks as
\(\Phi(x,y)\) and \(\Phi(z,w)\), where \(x,z\) are the two modes at the
common site.  The other three corners

\[
                       \Phi(x,w)=\Phi(y,z)=\Phi(y,w)=0  \tag{23}
\]

are inactive.  If \(y\) were pure, then \(z,w\) would have the same pure
type and \(\Phi(z,w)\) would vanish.  Hence \(y\) is mixed; (22) makes
\(z,w\) proportional antipodes of \(y\), and then makes \(x\) proportional
to \(y\).  Again the two active blocks are proportional rank-one matrices.

Now take the coefficient of each pure word \(X_c\) in (18).  The unique
color-\(c\) complement matching gives

\[
             C+\sum_{e\in P_c}R_e=\tfrac14E_{cc},
             \qquad c=0,1,2.                           \tag{24}
\]

The three sums in (24) are pairwise distinct, so at least two active blocks
are nonzero.  The preceding pairwise argument then puts every nonzero
active block on one common rank-one line \(\mathbb F L\).  Thus
\(\sum_{e\in P_c}R_e=\lambda_cL\).  Subtracting the cases \(c=0,1\) in
(24) gives

\[
             \tfrac14(E_{00}-E_{11})=(\lambda_0-\lambda_1)L, \tag{25}
\]

which is impossible: the left side has rank two and the right side has
rank at most one.  This proves:

**Proposition 5.1.**  The quadratic \(q\) in (3) admits the isolated
countermodel (1), but admits no solution of the nine shared-row cap
equations (17).

## 6. The first overlapping physical-pair system

For future candidates, the next compatibility layer can be written without
performing another polarization from scratch.  Let a ten-site quadratic
have sites \(\{r,t,0,\ldots,7\}\), and suppose deletion of \(\{r,t\}\)
gives the decomposition

\[
 h=q+\sum_i e_i^{(r)}p_i+\sum_j e_j^{(t)}s_j
       +\sum_{i,j}a_{ij}e_i^{(r)}e_j^{(t)}.             \tag{26}
\]

Delete instead the overlapping pair \(\{r,0\}\).  Its eight-site boundary
is \(U'_0=\{t,1,\ldots,7\}\).  Write
\(p_i=\sum_{v,\beta}p_{i,v,\beta}e_\beta^{(v)}\) and
\(s_j=\sum_{v,\beta}s_{j,v,\beta}e_\beta^{(v)}\).  The new internal
quadratic, direct matrix, and two star families are forced by the old data:

\[
\begin{aligned}
 q^{(0)}
   &=q|_{\{1,\ldots,7\}}
     +\sum_{v=1}^7\sum_{j,\beta}
        s_{j,v,\beta}e_j^{(t)}e_\beta^{(v)},\\
 b_{i\alpha}&=p_{i,0,\alpha},\\
 \widetilde p_i
   &=\sum_j a_{ij}e_j^{(t)}
     +\sum_{v=1}^7\sum_\beta p_{i,v,\beta}e_\beta^{(v)},\\
 \widetilde s_\alpha
   &=\sum_j s_{j,0,\alpha}e_j^{(t)}
     +\sum_{v=1}^7\bigl(e_\alpha^{(0)\,*}\mathbin{\lrcorner}
                         q_{0v}\bigr).
                                                               \tag{27}
\end{aligned}
\]

Here the contraction in the last line retains the endpoint ordering of
\(q_{0v}\).  The second cap is therefore not independent: it must satisfy

\[
 (b_{i\alpha}q^{(0)}
       +4\widetilde p_i\widetilde s_\alpha)(q^{(0)})^{[3]}
   =4\delta_{i\alpha}X_i^{U'_0}                        \tag{28}
\]

for all \(i,\alpha\).  Indeed,
\(q^{(0)}(q^{(0)})^{[3]}=4(q^{(0)})^{[4]}\).  Equivalently,
after division by four,

\[
 b_{i\alpha}(q^{(0)})^{[4]}
  +\widetilde p_i\widetilde s_\alpha(q^{(0)})^{[3]}
   =\delta_{i\alpha}X_i^{U'_0}.                         \tag{29}
\]

Equations (27)--(29) are the exact change of pair chart.  They are moot for
the present \(q\), which already fails Proposition 5.1.  More generally,
the [pair-slice exchange theorem](ten-site-overlapping-pair-exchange-redundancy.md)
and its independent
[audit](ten-site-overlapping-pair-exchange-redundancy-independent-audit.md)
show that a *complete* first nine-row tensor system already contains the
complete overlapping system: both list the same top-tensor residual
polynomials under reindexing.  The formulas remain useful for elimination
or localization in a second source-variable chart, but they are not an
additional filter unless the first system was projected or weakened.

## 7. Scope and next attack

The mechanism in Sections 2--4 is small and instructive.  The ordinary
matching power has two mixed defects sharing the cell \(04_2\).  One
product-cap cell on \(04\) cancels both defects but also removes one copy
of \(X_2\); the cell on \(26\) restores it.  The four mode vectors in (8)
make every unintended global \(ps\) block vanish.

Consequently neither the bare equation
\(zq^{[3]}=\Delta_{8,3}\), nor that equation together with
\(z=aq+4ps\), is a uniform obstruction.  Proposition 5.1 shows that the
full shared-row \(3\times3\) system is already strictly stronger for this
example.  The exchange theorem cited above corrects the original proposed
second-filter interpretation.  A reasonable next attack is therefore:

1. classify or search eight-site quadratics \(q\) for which the
   singleton-row exposure of \(H_q\) leaves enough response cells to solve
   all nine equations;
2. use (27) to rewrite the same full residual ideal in overlapping
   source-variable charts; and
3. derive a genuinely new elimination, saturation, or incidence consequence
   of that exchange, rather than counting (28) as new equations.

The standalone checker
[verify_polarized_eight_site_shared_pair_cap_countermodel.py](../computations/verify_polarized_eight_site_shared_pair_cap_countermodel.py)
enumerates all 105 perfect matchings and all \(3^8=6561\) coloring
coefficients over \(\mathbb Q\).  It constructs \(ps\) with both endpoint
orders, verifies all five words of \(q^{[4]}\), audits both cofactors
(13)--(14), checks (16) coefficientwise, performs the 363-row singleton
census, and audits every pair of the twelve surviving physical cells used
in the rank-one-line argument.  It also verifies the factor-four
normalization relating the raw overlapping-pair coefficient equation (29)
to its polarized form (28).
