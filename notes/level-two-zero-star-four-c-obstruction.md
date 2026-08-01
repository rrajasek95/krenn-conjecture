# The four-\(c\) rows exclude a cofactor-open zero-star block

Research evidence only. Krenn's conjecture remains open,
**SP-CLEAN-BRIDGE** is untouched, and no certified dependency changes.

## 1. Outcome

Fix a level-two block with rare colour \(c\) at \(p,q\), complementary
colours \(a,b\), residual set \(R\), binary residual packet \(M\), and

\[
 P_x=(A_{px}[c,a],A_{px}[c,b]),\qquad
 Q_x=(A_{qx}[c,a],A_{qx}[c,b]),\qquad
 z=A_{pq}[c,c].                                      \tag{1}
\]

> **Zero-star four-\(c\) theorem.** Suppose
> \[
>                         P=Q=0,\qquad z=0.           \tag{2}
> \]
> If, for every pair \(r\ne x\) in \(R\), the four-site binary matching
> tensor of \(M\) on \(R\setminus\{r,x\}\) is not identically zero, then the
> full eight-vertex equations are inconsistent.

No differential-rank, slope, or support assumption is needed for this
statement. It converts the old selected-block zero-star guard into a sharp
boundary condition: any full solution realizing (2) must have an identically
zero four-site binary cofactor.

Combined with the preceding
[one-sided overlap theorem](level-two-one-sided-overlap-collapse.md), it gives
a stronger generic conclusion:

> **Rank-\(55\) one-sided corollary.** Suppose \(Q=0,z=0\),
> \(\operatorname{rank}d\Psi_M=55\), and every live deletion graph
> \(R\setminus\{r\}\) is connected and nonbipartite. Then the full
> eight-vertex equations are inconsistent.

The nonzero-slope and cofactor-open assumptions in the preceding theorem are
automatic under these rank and graph hypotheses, as proved in Section 4.
Endpoint transposition gives the same result with \(P,Q\) exchanged.

## 2. The mixed four-\(c\) equations

Put

\[
       \alpha_r=A_{qr}[c,c],\qquad
       \beta_r=A_{pr}[c,c],\qquad
       S_{rx}=\alpha_r\beta_x+\alpha_x\beta_r.        \tag{3}
\]

Fix \(r<x\) in \(R\). Colour \(p,q,r,x\) by \(c\), and colour the other
four residual vertices by \(a,b\). Under (2), neither rare endpoint can meet
a binary residual vertex or the other endpoint. Thus the only possible
endpoint edges are

\[
                  (qr,px)\quad\hbox{or}\quad(qx,pr). \tag{4}
\]

Removing those two edges leaves the same binary four-site cofactor in both
cases. If

\[
 C_{rx}(w)=
 \operatorname{haf}\bigl(M|_{R\setminus\{r,x\}};w\bigr),
\]

the mixed target coefficient is therefore

\[
                         S_{rx}C_{rx}(w)=0            \tag{5}
\]

for all sixteen binary words \(w\). Cofactor openness supplies one word with
\(C_{rx}(w)\ne0\), so

\[
                         S_{rx}=0                    \tag{6}
\]

for every residual pair.

## 3. Those are exactly the pure-\(c\) coefficients

Write \(\gamma_{rx}=A_{rx}[c,c]\) for the residual diagonal-\(c\) graph, and
let \(D_{rx}\) be its four-site matching cofactor after deleting \(r,x\).
Expansion of the pure-\(c\) eight-site coefficient first separates matchings
using \(pq\) from those sending \(p,q\) to two distinct residual vertices:

\[
 H(c^8)
  =z\,\operatorname{haf}(\gamma)
   +\sum_{r<x}S_{rx}D_{rx}.                          \tag{7}
\]

Equations (2) and (6) make the right side zero. The target coefficient of
the pure-\(c\) word is \(1\), a contradiction. Notice that no classification
of the supports of \(\alpha,\beta\), and no nonvanishing property of the
diagonal packet \(\gamma\), enters the argument.

## 4. Rank \(55\) makes the open hypotheses automatic

Assume now that \(\operatorname{rank}d\Psi_M=55\) and every deletion live
graph is connected and nonbipartite. The five trace-zero vertex scalings

\[
 K^\mu_{xy}=(\mu_x+\mu_y)M_{xy},\qquad
 \sum_{x\in R}\mu_x=0,                               \tag{8}
\]

are independent: a zero scaling gives \(\mu_x+\mu_y=0\) on a connected
nonbipartite live graph, hence \(\mu=0\). Since \(d\Psi_M\) has 60 columns,
rank \(55\) says that (8) is its entire kernel.

First, \(\Psi(M)\ne0\). Otherwise Euler's identity

\[
                         d\Psi_M(M)=3\Psi(M)          \tag{9}
\]

puts \(M\) in the kernel. Equality with a scaling (8) gives
\(\mu_x+\mu_y=1\) on every live edge. Connectivity and an odd cycle force
all six \(\mu_x=1/2\), contradicting \(\sum\mu_x=0\).

Second, every four-site binary cofactor is nonzero. If the tensor
\(C_{rx}\) vanished identically, all four differential columns belonging to
the \(2\times2\) block \(M_{rx}\) would be zero. Hence every variation
supported on that block would lie in the kernel. But a scaling (8) supported
only on \(rx\) vanishes on the connected nonbipartite deletion graph
\(R\setminus\{r\}\), which forces \(\mu=0\). The four-dimensional edge-block
space therefore has zero intersection with the scaling kernel, a
contradiction.

The prior one-sided theorem may consequently be applied without separately
assuming a live slope or live cofactors. It first forces \(P=0\); the
zero-star four-\(c\) theorem then gives the contradiction claimed in the
rank-\(55\) corollary.

## 5. Exact audit

The extended checker
[verify_level_two_one_sided_overlap_collapse.py](../computations/verify_level_two_one_sided_overlap_collapse.py)
uses named formal variables for all twelve \(\alpha,\beta\) cells and all
fifteen \(\gamma\) cells. By literal enumeration of the 105 eight-site
perfect matchings it verifies:

* every mixed four-\(c\) polynomial is exactly \(S_{rx}C_{rx}(w)\); and
* the pure-\(c\) polynomial is exactly (7), monomial by monomial.

For the integral rank-\(55\) witness, the same checker verifies independent
gauge dimension \(5\), differential rank \(55\), connected nonbipartite
deletions, nonzero slope on all 64 words, and nonzero cofactors on all
\(15\cdot16=240\) coordinates. It is standard-library only and remains live
under normal, optimized, and isolated Python.

## 6. Revised frontier

The generic one-sided rank-\(55\) locus is now closed, including its
zero-star specialization. The unresolved level-two work splits into:

1. genuinely two-sided generic-kernel packets not covered by the earlier
   invertible/dead rank-drop theorem; and
2. boundary packets where the differential rank drops, a deletion graph is
   disconnected or bipartite, or a four-site cofactor vanishes.

In particular, another generic selected-block witness with \(P=Q=z=0\) is
not a global obstruction: its very genericity makes the four-\(c\)
contradiction apply. A useful next boundary target is to quantify the rank
drop forced by a vanishing four-site cofactor without assuming the deletion
graph remains connected and nonbipartite.
