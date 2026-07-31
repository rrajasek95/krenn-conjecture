# The complementary scalar-unit pivot exports the obstruction to an essential pair

## 1. Outcome

Fix a good physical pair \(p,q\) in an exact ternary aggregate source,
write \(U=B\setminus\{p,q\}\), \(|U|=2h\), with \(h\geq3\), and suppose
its direct block is the intrinsic scalar unit

\[
                         A_{pq}=\alpha E_{aa},\qquad \alpha\ne0.       \tag{1}
\]

As in the full normal-jet ledger, let \(q\) be the internal quadratic on
\(U\), let \(p_i,s_j\) be the two endpoint-star rows, and put

\[
 R_{ij}=p_i s_j,\qquad G=\alpha q+R_{aa},\qquad
 \begin{aligned}
 U_a&=G^{[h]}-\alpha^{h-1}X_a,\\
 \Theta_a&=G^{[h-1]}-\alpha^{h-1}q^{[h-1]}.
 \end{aligned}                                                       \tag{2}
\]

Let \(\{a,b,c\}=\{0,1,2\}\).  There is an exact conditional pivot:

**Theorem 1.1 (complementary pivot).**  If

\[
 U_a=0,
 \qquad R_{ij}\Theta_a=0
       \quad\text{for every }i,j\in\{b,c\},                         \tag{3}
\]

then replacing

\[
 q\longmapsto q^\sharp=q+\alpha^{-1}R_{aa},
 \qquad p_a\longmapsto0,qquad s_a\longmapsto0                     \tag{4}
\]

and leaving every other block unchanged produces another exact ternary
source on the **same** vertex set.  At the transformed pair, both deleted
endpoint stars have rank exactly two with coordinate kernel \(a\), and the
direct block \(\alpha E_{aa}\) is mutually essential: \(q\) is an
essential neighbour of \(p\), and \(p\) is an essential neighbour of
\(q\).

Only the four complementary products in (3) are needed.  Products involving
the selected row or column may be arbitrary because those response rows are
removed by (4).

This is not yet an order descent.  If the original source has globally
minimum aggregate-entry support and

\[
                  m=|\operatorname{supp}p_a|,
                  \qquad n=|\operatorname{supp}s_a|,                 \tag{5}
\]

then minimality instead forces the exact support-escalation bound

\[
 \boxed{
 |\operatorname{supp}q^\sharp|-|\operatorname{supp}q|
       \ge m+n,
 \qquad mn\ge m+n.}                                                 \tag{6}
\]

In particular \(m,n\ge2\).  If \(m=n=2\), all four possible products
survive as four distinct internal aggregate entries, none already belongs
to the support of \(q\), and none cancels in the pivot.  Thus the smallest
possible surviving packet is a literal four-cell rectangle.

This equality packet also closes the first occupancy-selection gate.
Because a clean unary cap at a minimum-support good pair has
\(\Theta_a=R_{aa}H_a\ne0\), one of the four cells and one of its two
physical orientations satisfies

\[
                  \boxed{\kappa^{\rm or}H_{a,\mathrm{comp}}\ne0}.  \tag{6a}
\]

Here \(H_{a,\mathrm{comp}}\) is the literal coefficient of the carrier on
the complementary occupied sites and
\(\kappa^{\rm or}=\alpha q_{rs}(c,d)-BF\) or
\(\alpha q_{rs}(c,d)-EC\), with endpoint order retained.  Thus the
minimal \(2\)-by-\(2\) pivot packet cannot hide the carrier through a site
collision or a zero curvature coefficient.  The remaining filtered
restriction--insertion/transgression step is separate; nonzero detection
alone does not construct it.

The gain is a sharp fork.  A proof that one of the four products in (3) is
nonzero detects the normal jet.  If all four vanish, the obstruction can be
pivoted into a mutually essential rank-two pair and must pay the support
cost (6).  What is still missing is a global argument showing that these
essential-pair/support costs cannot coexist over the many good pairs.

## 2. Exact source identity

The complete nine physical rows at the selected pair are

\[
 \alpha\delta_{ia}\delta_{ja}q^{[h]}
       +R_{ij}q^{[h-1]}=\delta_{ij}X_i.                              \tag{7}
\]

Since \(q^\sharp=\alpha^{-1}G\), the unary equation in (3) gives

\[
                    (q^\sharp)^{[h]}=\alpha^{-1}X_a.                 \tag{8}
\]

At the adjacent power,

\[
 (q^\sharp)^{[h-1]}
   =\alpha^{-(h-1)}G^{[h-1]}
   =q^{[h-1]}+\alpha^{-(h-1)}\Theta_a.                              \tag{9}
\]

Hence (3) and the four rows of (7) indexed by \(i,j\in\{b,c\}\)
give

\[
                  R_{ij}(q^\sharp)^{[h-1]}
                           =\delta_{ij}X_i.                          \tag{10}
\]

Expand the matching tensor of the transformed source by the partners of
\(p,q\).  The direct edge supplies the selected colour and the four
remaining star responses supply the complementary block:

\[
\begin{aligned}
 H_B(A^\sharp)
  ={}&\alpha e_a^{(p)}e_a^{(q)}(q^\sharp)^{[h]}\\
    &+\sum_{i,j\in\{b,c\}}
       e_i^{(p)}e_j^{(q)}R_{ij}(q^\sharp)^{[h-1]}\\
  ={}&X_a^B+X_b^B+X_c^B.
\end{aligned}                                                       \tag{11}
\]

This proof uses a literal replacement of aggregate blocks.  It does not
cancel a matching power, select a summand from a complex sum, or claim that
the pivot is a hafnian Schur complement.

## 3. Exact essential-pair export

Goodness of \(p,q\) means that the two deleted endpoint-star maps are
injective.  Equivalently, each ordered triple

\[
                         (p_a,p_b,p_c),\qquad(s_a,s_b,s_c)            \tag{12}
\]

is linearly independent in its residual direct-sum space.  After (4), the
first star has image of dimension two and kernel exactly
\(\mathbb C e_a^*\); the same holds at the second endpoint.

More concretely, every transformed block from \(p\) to \(U\) has its
\(p\)-mode image in \(\operatorname{span}\{e_b,e_c\}\), and the nonzero
rows \(p_b,p_c\) make this image equal to that plane.  The block
\(A_{pq}=\alpha E_{aa}\) adds precisely the missing line
\(\mathbb C e_a\).  Thus deleting neighbour \(q\) makes the total endpoint
support proper, while restoring it gives all of \(V_p\).  This is exactly
essentiality of \(q\) at \(p\).  The transposed argument proves the other
orientation.

This explains why re-minimizing after the pivot does not immediately
contradict the good-pair theorem: the selected pair has deliberately moved
from the good graph into its sharply classified bad graph.

## 4. Minimum-support accounting

Count nonzero endpoint-ordered aggregate matrix entries.  The pivot leaves
the direct block and all rows other than \(p_a,s_a\) unchanged.  Therefore

\[
 |\operatorname{supp}A^\sharp|-|\operatorname{supp}A|
 =|\operatorname{supp}q^\sharp|-|\operatorname{supp}q|-m-n.         \tag{13}
\]

Global minimum support of \(A\), together with the exact source identity
(11), makes (13) nonnegative and proves the first inequality in (6).

In the site-square-zero algebra, every nonzero entry of
\(R_{aa}=p_as_a\) comes from an ordered choice of one supported entry of
\(p_a\) and one of \(s_a\).  Same-site products vanish and two orientations
may merge or cancel, so

\[
                         |\operatorname{supp}R_{aa}|\le mn.          \tag{14}
\]

For any two finite-support vectors \(z,w\), a new entry of \(z+w\) outside
\(\operatorname{supp}z\) must belong to \(\operatorname{supp}w\).  Hence

\[
 |\operatorname{supp}q^\sharp|-|\operatorname{supp}q|
       \le |\operatorname{supp}R_{aa}|\le mn.                      \tag{15}
\]

There is a useful sharper form of the same accounting.  Put

\[
 N=\operatorname{supp}q^\sharp\setminus\operatorname{supp}q,
 \qquad
 L=\operatorname{supp}q\setminus\operatorname{supp}q^\sharp .       \tag{15a}
\]

Then (13) says

\[
                    |N|-|L|\geq m+n,
 \qquad |N|\geq m+n.                                                \tag{15b}
\]

Every cell of \(N\) is a cell of \(R_{aa}\), has zero \(q\)-coefficient,
and has nonzero \(R_{aa}\)-coefficient.  At least one of its two ordered
star products is therefore nonzero.  In particular

\[
                  m+n\leq |N|
                      \leq|\operatorname{supp}R_{aa}|\leq mn,       \tag{15c}
\]

which proves (6).  If one of \(m,n\) were one, then \(mn<m+n\), a
contradiction.  When \(m=n=2\), every inequality in (15c) is equality.
Thus \(N=\operatorname{supp}R_{aa}\), and (15b) then gives
\(L=\varnothing\).  All four ordered products survive as four distinct new
cells.  This rules out a same-site loss, an orientation merger or
cancellation, overlap with \(\operatorname{supp}q\), and cancellation
against an old \(q\)-entry.  This proves the four-cell statement.

There is no purely local monotonicity theorem beyond this.  With three
supported coordinates of \(p_a\) and three of \(s_a\) on disjoint residual
sites, their product can have nine internal entries: the pivot deletes six
star entries and adds nine.  This support pattern is only a counting guard,
not an exact ternary source, but it prevents treating (4) itself as a
descent without using more full-source equations.

## 5. The four-cell packet detects an oriented carrier

Continue with \(m=n=2\).  Equality throughout (13)--(15) says more than
nonvanishing of \(R_{aa}\): each supported internal cell of \(R_{aa}\)
comes from exactly one ordered product of a \(p_a\)-entry and an
\(s_a\)-entry.  If both orientations contributed to the same cell, two of
the four ordered products would merge and
\(|\operatorname{supp}R_{aa}|<4\).  Moreover

\[
           \operatorname{supp}R_{aa}\cap\operatorname{supp}q
                              =\varnothing.                    \tag{16a}
\]

The new-cell conclusion in fact gives a small general fork.  At a decorated
residual cell \(e=((r,c),(s,d))\), ordered with \(r<s\), write

\[
 \begin{array}{lll}
 B=(p_a)_{r,c},&F=(s_a)_{s,d},&q_e=q_{rs}(c,d),\\
 E=(p_a)_{s,d},&C=(s_a)_{r,c}.&
 \end{array}                                                       \tag{16b}
\]

Thus \((R_{aa})_e=BF+EC\), with the endpoint order retained.  Multiplication
by the cell monomial automatically restricts the other factor away from
the physical sites \(r,s\).  Consequently the contribution of this cell to
\(R_{aa}H_a\) is

\[
 (BF+EC)e_c^{(r)}e_d^{(s)}
       \left.H_a\right|_{U\setminus\{r,s\}} .                    \tag{16c}
\]

For every new cell \(e\in N\), one has \(q_e=0\), and at least one of

\[
              \kappa_e^\rightarrow=\alpha q_e-BF,
       \qquad \kappa_e^\leftarrow=\alpha q_e-EC                 \tag{16d}
\]

is nonzero.  Hence either some new cell has a nonzero restricted carrier
coefficient and already gives a literal nonzero
\(\kappa_e^{\rm or}H_{a,\mathrm{comp}}\), or every new-cell contribution
annihilates \(H_a\) and \(R_{aa}H_a\) is supported entirely through cells
of \(R_{aa}\) which overlap \(\operatorname{supp}q\).  This is the exact
scope of the support argument for general \(m,n\).

On the \(m=n=2\) branch, (16a) makes the second alternative impossible if
\(R_{aa}H_a\ne0\).  Cleanliness and minimum-support goodness give precisely
\(\Theta_a=R_{aa}H_a\ne0\).  Choose a nonzero decorated coefficient of
this product.  In its coefficient expansion, at least one summand

\[
                   (R_{aa})_{rs}(c,d)\,
                     (H_a)_{\mathrm{comp}}                       \tag{16e}
\]

is nonzero.  By unique orientation, its first factor is exactly one of
\(BF,EC\), while the other oriented star product at that cell is zero.
Equation (16a) also gives \(q_{rs}(c,d)=0\).  For the unique surviving
orientation, therefore,

\[
 \kappa^{\rm or}
    =\alpha q_{rs}(c,d)-(R_{aa})_{rs}^{\rm or}
    =-(R_{aa})_{rs}^{\rm or}\ne0.                            \tag{16f}
\]

Multiplying (16f) by the nonzero complementary carrier coefficient in
(16e) proves (6a).  After the four physical sites \(p,q,r,s\) are fixed,
\((H_a)_{\mathrm{comp}}\) is literally a coefficient of
\(H_a|_{U\setminus\{r,s\}}\).  Thus (6a) is exactly a coefficient of the
physical oriented four-cut carrier layer, before an ordinary odd quotient
or common-power cancellation; it is not an inference from the complete
formal product \(K^{\rm or}H_a\).  It supplies exactly the
occupancy/curvature detection which the general carrier-torsion guard lacks
on this smallest support packet.

The conclusion is deliberately not promoted to a clean-point theorem.
Current ordered five-site reconstruction sends the literal comparison to
zero, and a secondary filtered lift still needs an existence and
zero-indeterminacy theorem.  The result here ensures that such a theorem
would receive a nonzero physical carrier on the \(m=n=2\) branch.

## 6. Exact scope

The pivot theorem is conditional on the clean unary equation and four literal
complementary annihilations.  Existing four-cut results do not yet supply
those complete products: an exposed coefficient can vanish through site
collision or evaluated cancellation while \(R_{ij}\Theta_a\) survives.

Conversely, the theorem needs neither cancellation of the carrier \(H_a\)
nor the stronger eight-row condition \(R_{ij}\Theta_a=0\) for every
\((i,j)\ne(a,a)\).  It therefore identifies a smaller positive target than
carrier faithfulness:

\[
 \boxed{
 \text{either detect one complementary }R_{ij}\Theta_a,
 \text{ or control the essential-pair pivot globally}.}            \tag{16}
\]

The dependency-free checker
[`verify_scalar_unit_complementary_pivot_essential_pair.py`](../computations/verify_scalar_unit_complementary_pivot_essential_pair.py)
audits the divided-power scaling, the four-row reconstruction, the
rank-two/essential endpoint ledger, and the support bounds, including the
new-cell fork, exhaustive two-by-two support rigidity, both endpoint orders
in the restricted four-cut carrier, the nonmonotone nine-for-six guard, and
six adversarial mutations.  The result is a research reduction, not a proof
of a clean cap, an order descent, or the conjecture.
