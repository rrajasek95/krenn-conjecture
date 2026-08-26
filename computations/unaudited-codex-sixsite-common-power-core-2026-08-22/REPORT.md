# Six-site common-power core: exact classification and fixed-label guard

Status: **exact bounded audit; negative for the scalar core; not a full-nine counterexample.**

## Outcome

The literal selected-row normalization is

\[
q^{[3]}+zq^{[2]}=0
\quad\Longleftrightarrow\quad
(q+3z)q^{[2]}=0,
\]

because \(q q^{[2]}=3q^{[3]}\).  The originally suggested
\((q+z)q^{[2]}=0\) is not source-faithful unless \(z\) has already been
rescaled by three.

Let

\[
\Phi_q:({\cal R}_W)_2\longrightarrow({\cal R}_W)_6,
\qquad u\longmapsto u q^{[2]}.
\]

For a fixed six-site quadratic \(q\), the isolated scalar core is exactly

\[
z\in \operatorname{Segre}\cap
   \left(-{q\over3}+\ker\Phi_q\right),
\qquad
r\in\Phi_q^{-1}(-\Delta),
\qquad r^{[3]}\ne0.                                      \tag{1}
\]

Thus the two common-power equations specify one kernel point and one affine
fibre point.  They do not remember that the kernel point is an
**off-diagonal** cell relative to the same ordered endpoint pairing whose
diagonal trace defines \(r=-\sum_iB_{ii}\).

An exact six-site guard realizes all of (1), and more:

\[
(q+3z)q^{[2]}=0,qquad rq^{[2]}=-\Delta,qquad
r^{[3]}=X_0\ne0,                                        \tag{2}
\]

with two injective endpoint triples, identity channel pairing,
\(r=-\sum_i p_i s_i\), and \(z=p_2s_2\).  Hence scalar common-power,
nonnilpotence, decomposability, and even an unlabeled shared rank-three
factorization are insufficient.

The defect is exact rather than cosmetic: among all complex channel
combinations

\[
Z(x)=\sum_{i,j}x_{ij}p_i s_j,
\]

the system \(Z(x)q^{[2]}=-q^{[3]}\) has the unique solution

\[
                              x=E_{22}.                 \tag{3}
\]

Its trace pairing is one.  A trace-preserving endpoint basis change sends
\(P\mapsto PG\), \(S\mapsto SG^{-\mathsf T}\); every off-diagonal cell
has coefficient vectors \(u,v\) with \(u^{\mathsf T}v=0\).  Equation (3)
has \(u^{\mathsf T}v=1\), so no such change can turn this canceller into an
off-diagonal cell while retaining the trace decomposition of \(r\).

## Source replay

The guard reuses the exact decorated six-site tables frozen in
[`verify_h3_scalar_zero_packet_six_site_nonreduction.py`](../verify_h3_scalar_zero_packet_six_site_nonreduction.py):

\[
\begin{aligned}
q^{[3]}&=e_{020200},\\
Rq^{[2]}&=X_0+X_1+X_2,\\
R^{[3]}&=-X_0,\\
(p_2s_2)q^{[2]}&=-e_{020200}.
\end{aligned}
\]

Putting \(z=p_2s_2\) and \(r=-R=-\sum_i p_i s_i\) gives (2).  The
endpoint forms are the source file's Gaussian-rational, pairwise-disjoint
triples, so both endpoint maps are injective.  No formal replacement of
\(q^{[2]}\) or \(q^{[3]}\) is used.

The checker builds all nine products, enumerates all 15 perfect matchings
on six sites and all \(3^6\) decorated words, and solves the canceller
system over \(\mathbb C\) by splitting it into 42 rational equations in 18
real/imaginary unknowns.  The coefficient rank is 18 and the unique answer
is (3).

## What the guard does and does not show

If the guard's \(z\) is kept in the \(22\) cell, then

\[
\left({q\over3}+z\right)q^{[2]}=0,
\]

whereas a literal diagonal full-nine row requires \(X_2\).  If it is
declared off-diagonal instead, the trace pairing used by
\(r=-\sum_iB_{ii}\) is lost, by (3).  Therefore the guard is faithful to
every displayed scalar equation but deliberately not to the fixed-label
full-nine packet.  It is not a Krenn counterexample.

The first extra datum that must be retained is consequently

\[
\boxed{
 a\ne b,\quad z=p_as_b\text{ in the same ordered endpoint bases in which }
 r=-\sum_iB_{ii}.}                                      \tag{4}
\]

For a positive proof, (4) is necessary but not presently known to be
sufficient.  The smallest source-level packet not defeated by the archived
guards also retains at least one **individually labelled diagonal target
row**

\[
B_{ii}q^{[2]}=X_i,
\]

through a one-bright/two-site coefficient cut.  Merely summing the three
rows to \(rq^{[2]}=-\Delta\) loses their labels.  The six off-diagonal
annihilator rows and their Segre hexagon alone are separately known to be
insufficient; see
[`selector-macaulay-double-jet-and-offdiagonal-hexagon.md`](../../notes/selector-macaulay-double-jet-and-offdiagonal-hexagon.md).

Accordingly the minimal honest next target is not another scalar identity.
It is a fixed-label coefficient-cut statement coupling one off-diagonal
cell \(B_{ab}\) to one diagonal anchor \(B_{ii}\), with their common
factors \(p_a,s_b,p_i,s_i\) still visible.

## Relation to existing routes

No archived file states the corrected pair (2) as one theorem.  Its two
pieces were already adjacent:

- [`endpoint-dark-shore-consecutive-power-jet.md`](../../notes/endpoint-dark-shore-consecutive-power-jet.md)
  freezes \(rq^{[2]}=-\alpha\Delta\), \(r^{[3]}\ne0\), and warns that the
  scalar contraction misses the uncontracted one-bright rows;
- [`h3-scalar-zero-packet-six-site-nonreduction.md`](../../notes/h3-scalar-zero-packet-six-site-nonreduction.md)
  supplies the exact \(q,R\) packet and all adjacent polarizations;
- [`selector-macaulay-double-jet-and-offdiagonal-hexagon.md`](../../notes/selector-macaulay-double-jet-and-offdiagonal-hexagon.md)
  gives the source-faithful normalized cells
  \(B_{ij}=p_is_j+(a_{ij}/3)q\) and proves that a diagonal anchor must enter
  before top-degree multiplication.

This audit joins those facts and identifies their exact fixed-label gap.

## Reproduction

Checker:
[`audit_common_power_core.py`](audit_common_power_core.py)

Pinned source SHA-256:

```text
20ec8fabda17ab915e9b071df00a06d72e985943a3672a5f0a9e02edff80badf
```

Run independently as:

```text
python3 audit_common_power_core.py --mode full
python3 -O audit_common_power_core.py --mode exhaustive
python3 -I -S audit_common_power_core.py --mode structural
```

All three pass with ledger digest

```text
a45ce1b648f7792848b1232dbcda425e878ac7629c2bba6b5e84f1242b61f90f
```
