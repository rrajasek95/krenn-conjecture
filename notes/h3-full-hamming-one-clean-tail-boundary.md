# The full-nine Hamming-one rows do not force the clean tail at \(h=3\)

## Outcome

There is a rational one-chart packet with good shared stars and literal Segre
responses for which every pure and Hamming-one coefficient in all nine output
rows is correct, while

\[
 \chi
 =2\alpha\,(u^{\{2\}})^T K_Qv^{\{2\}}
   +6\,(u^{\{3\}})^TJ_3v^{\{3\}}
 =-4.
\]

Thus the complete Hamming-one/full-nine row system, by itself, cannot imply the
desired cancellation.  The first rows detecting this packet are at Hamming
distance two.  This is an exact boundary for the one-chart
Hamming-distance-\(\leq1\) strategy; it is not an all-word source and makes no
claim against a second-chart or overlap argument that genuinely supplies the
missing Hamming-two information.

## Exact packet

Use sites \(x=0,\ldots,5\), physical colours \(c=0,1,2\), and variables
\(z_x^c\).  Put

\[
 q=\sum_{c=0}^2
 \bigl(z_0^cz_1^c+z_2^cz_3^c+z_4^cz_5^c\bigr)
 +z_0^1z_1^0,
 \qquad d=E_{00}+E_{01}.
\]

The two shared star triples are

\[
\begin{aligned}
 p_0&=z_0^0+z_1^0+z_1^1+z_2^2+z_4^2,
 &p_1&=z_0^1,
 &p_2&=z_3^2,\\
 s_0&=-z_0^1-z_3^2,
 &s_1&=-z_0^0-z_0^1+z_1^1+z_3^2-2z_5^2,
 &s_2&=z_2^2.
\end{aligned}
\]

In particular, the term \(z_1^1\) in \(p_0\) is essential.  Both global
coefficient matrices of the triples \((p_0,p_1,p_2)\) and
\((s_0,s_1,s_2)\) have rank three.  Since the response block is literally
\((p_i s_j)_{i,j}\), every Segre rectangle

\[
 (p_i s_j)(p_k s_\ell)=(p_i s_\ell)(p_k s_j)
\]

holds as a polynomial identity.

## All 351 admitted coefficients

For a physical word \(w\in\{0,1,2\}^6\), write the row coefficient as

\[
 F_{ij}(w)
 =d_{ij}[z^w]q^{[3]}+[z^w](p_i s_jq^{[2]}).
\]

On the three pure words, the response matrices are respectively

\[
 -E_{01},\qquad E_{11}-E_{00}-E_{01},\qquad
 E_{22}-E_{00}-E_{01}.
\]

The direct matrix is \(d\) on each pure word, so their sums are
\(E_{00},E_{11},E_{22}\), as required.

There are only two Hamming-one words on which either summand is nonzero:

\[
 (\text{base},\text{defect},\text{site})=(0,1,0),\qquad(1,0,1).
\]

For each one, the direct matrix is \(d\) and the response matrix is \(-d\).
For the other 34 Hamming-one words both matrices vanish separately.  Hence all

\[
 3\cdot9+3\cdot2\cdot6\cdot9=27+324=351
\]

pure and Hamming-one row coefficients are exact.

## The uncancelled clean tail

Select output row \((i,j)=(0,1)\), pure colour \(c=2\), and
\(\alpha=d_{01}=1\).  The pure internal matching is
\(Q=01\mid23\mid45\), while

\[
 u=(0,0,1,0,1,0),\qquad
 v=(0,0,0,1,0,-2).
\]

The expansion by number of response edges has exact layers

\[
 (Q_0,Q_1,Q_2,Q_3)=(1,-1,-4,0).
\]

Thus the admitted top equation is \(Q_0+Q_1=0\), but the remaining tail is
\(Q_2+Q_3=-4\).  Equivalently,

\[
 (u^{\{2\}})^TK_Qv^{\{2\}}=-2,
 \qquad (u^{\{3\}})^TJ_3v^{\{3\}}=0,
\]

so the normalization in the displayed formula gives
\(\chi=2(-2)+6(0)=-4\).

The complete ledger over all \(3^6\) physical words and nine rows has 59
nonzero residual coefficients.  Its minimum Hamming distance from a pure word
is two; for example

\[
 F_{01}(1,0,2,2,2,2)=-1.
\]

This is the first omitted layer, not a hidden normalization error.

## Why the tagged-polar repair stops

Ordinary Hamming-one tagging marks an endpoint of the two internal \(Q\)-edges
in the first-response layer.  In this packet the six site values are

\[
 (-1,-1,-2,-2,1,1),
\]

whose sum is \(-4=4Q_1\).  It therefore reproduces the already known
first-response equation with the four-endpoint multiplicity; it does not
produce the second-response compound \(K_Q\).

The marked normal-incidence identity needed for that compound inserts the
response incidence

\[
 \beta_x(y)=u_xv_y+v_xu_y
\]

into the repeated-star functional.  Its site values here are

\[
 (0,0,-4,-4,-4,-4),
\]

and sum to \(-16=4Q_2\), exactly exposing the missing nonzero tail.  But this
is a different input from the physical \(q\)-incidence supplied by an ordinary
tagged source row.  For example, at site 2,

\[
 \beta_2=z_3^2-2z_5^2,
\]

whereas the pure physical incidence of \(q\) at that site is supported only at
site 3.  Hence \(\beta_2\) has no local physical-incidence lift.  The cubic
response layer is already zero in the packet, so adding a cubic source term
cannot cancel the missing \(-4\).

This is consistent with the general marked identities in
[`h3-hamming-one-normal-incidence-compound-transgression.md`](h3-hamming-one-normal-incidence-compound-transgression.md):
they identify the correct normal functional, but an additional theorem is
needed to place every \(\beta_x\) in the image of the available tagged source
incidences.

A source-faithful derivation would also suffice.  If
\(\delta q=R\), \(\delta R=0\), and \(\delta T=0\), then differentiating
\(\alpha Q_0+Q_1=T\) through all orders triangularly kills the tail.  This
packet has no such sitewise colour derivation: its internal quadratic has site
support only on \(01,23,45\), while its selected response has nonzero edges
\(23,25,34,45\).  A colour derivation cannot create the new site edges 25 and
34.  The Hamming-one rows therefore do not force the integrability needed by
the derivation argument.  See
[`unipotent-response-transgression-clean-tail.md`](unipotent-response-transgression-clean-tail.md)
for that sufficient mechanism.

## Reproduction

The exact rational verifier is
[`verify_h3_full_hamming_one_clean_tail_boundary.py`](../computations/verify_h3_full_hamming_one_clean_tail_boundary.py).
It exhausts the 351 admitted coefficients, the full failure ledger, both
global ranks, every Segre rectangle, the response layers and normalization,
and three targeted mutation guards.
