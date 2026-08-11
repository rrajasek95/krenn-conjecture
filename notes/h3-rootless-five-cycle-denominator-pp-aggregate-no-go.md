# Denominator-marked PP squares realize the cubic differences but miss the fifth aggregate

## Outcome

The selector-localized denominator/two-edge principal-parts inventory does
meet the first-Tor degrees isolated in 466bfd6, but only in the expected
rank-four way. On the five-cycle specialization:

* five of the fifteen denominator-marked PP squares have the selected
  internal cycle degree, one for each deleted site;
* pairing neighboring squares and multiplying each by its one missing cycle
  edge gives exactly the five cubic (P_3\sqcup K_2) S-pairs;
* those pairs cancel their response companions and have zero strict
  Bianchi/PP readouts; but
* their actual order-four diagonal Eq defects are

  \[
                    a-b, c-d, e-a, b-c, d-e,         \tag{1}
  \]

  so both the ridge and residual modules have rank four.

Selector localization does not change the internal cycle degree. Strict
chart Bianchi squares have signature ((0,0,0,0)), and the normalized
bar/curvature endpoint has equal (q)-augmentation and ordinary residue.
Therefore no combination in this inventory supplies the fifth aggregate
(sum_v\lambda_v), or a source-valid lower face of signature

\[
       (\operatorname{ainc},\widehat w,operatorname{tgt},
          \operatorname{ores})=(-1,0,0,0).              \tag{2}
\]

The minimal candidate of 466bfd6 is thus not hidden in the already committed
denominator/PP squares. The missing object remains a genuinely new
repeated-site relative lower face with nonzero aggregate value.

## 1. Which denominator squares reach the cycle degree

Retain the cycle cells

\[
 (a,b,c,d,e)=(q_{12},q_{23},q_{34},q_{45},q_{15}).     \tag{3}
\]

For (F_v=D\setminus\{v\}), exactly one of its three perfect matchings uses
only (3):

\[
\begin{array}{c|c}
v&N_v\\ \hline
1&23|45\\
2&15|34\\
3&12|45\\
4&15|23\\
5&12|34.
\end{array}                                             \tag{4}
\]

These are precisely the five monomials
((h_1,h_2,h_3,h_4,h_5)) from c4cac60. Each of the other ten denominator
squares contains an off-cycle marked direction. Fine multidegree is
nonnegative, so polynomial multiplication cannot remove that direction;
those ten squares cannot enter a cubic cycle degree.

Selector/adjugate transport does not change this conclusion. Its exact
forced shift is supported at the external sites (x,p,q); its internal
((a,b,c,d,e))-degree is zero. Thus it transports endpoint character while
leaving the split (5+10) in (4) unchanged.

## 2. The five cubic PP pairs

Use the cycle order ((1,3,5,2,4)). The first pair consists of

\[
                N_1=23|45,qquad N_3=12|45.             \tag{5}
\]

Multiplying the (v=1) PP square by (q_{12}=a), the (v=3) square by
(q_{23}=b), and subtracting puts both in degree

\[
                        q_{12}q_{23}q_{45}=abd.          \tag{6}
\]

Their response symbols cancel by (a h_1-b h_3=0). The other four
neighboring pairs give the remaining four rows of the odd-cycle first Tor.
Hence the denominator squares do not miss the cubic *differences*; they
realize their algebraic PP symbols exactly.

For the strict two-chart PP/Bianchi square, every coarse readout is zero.
For the actual physical order-four cube, however, diagonal descent leaves
the uncancelled pure Eq face

\[
                         (H_0-u)e_{\rm Eq}.              \tag{7}
\]

Consequently the pair in (6) leaves

\[
                    (a-b)(H_0-u)e_{\rm Eq}.             \tag{8}
\]


The five versions of (8) are exactly (1). Their coefficient matrix is the
oriented incidence matrix of a (5)-cycle and has rank four. It vanishes at
the active torus point

\[
                         a=b=c=d=e=1.                   \tag{9}
\]

Allowed selector, star-minor, and curvature localizations remain active at
a specialization with their independent units equal to one, so (9) proves
that the diagonal ideal remains proper after those localizations. Inverting
one of the differences in (1) would be a different, divisor-dependent
chart, not a consequence of selector localization.

## 3. Why Bianchi and bar corrections do not add the aggregate

Strict chart Bianchi comparisons redistribute chart representatives and
have zero total anchor incidence. They add no column to the internal
five-cycle incidence matrix.

The mixed normalized-bar/curvature bicomplex does produce a genuine lowered
endpoint and kills its target after the complete word change. Its committed
readout is nevertheless

\[
             (q\text{-augmentation},\operatorname{ores})
                       =(\kappa,\kappa),                \tag{10}
\]

while every bar edge has ((0,0)). Thus a combination with ordinary residue
zero also has (q)-augmentation zero. The desired invisible endpoint
((\kappa,0)) raises this readout rank from one to two; it is not supplied
by another shuffle or Bianchi path.

Together with (1), this leaves the all-ones covector
(sum_v\lambda_v). At (9), response cancellation for formal-tail weights
(gamma_v) requires (sum_vgamma_v=0), while anchor normalization in
(2) requires (sum_vgamma_v=1). The old cap rows retain the same primitive
separator: their rank is three in
((u\mathrm{Eq},w,\mathrm{tgt},\mathrm{ores})), and adjoining (2) raises it
to four.

## 4. Scope and next dependency

This is an exact negative theorem for the fifteen denominator-marked
two-edge PP squares, their selector-localized strict chart comparisons, and
the committed normalized bar/curvature correction, in the five-cycle
specialization. It neither assumes nor constructs a new underived Hasse
face.

The smallest remaining positive object must have a nonzero value under the
fifth aggregate, repeated-site (P_3\sqcup K_2) provenance, and signature
(2). Its differential must also be compatible with the unique degree-five
odd-cycle relation from 466bfd6. Declaring such a face is precisely the new
source-resolution input excluded from the present inventory.

## Verification

Run

~~~text
python3 computations/verify_h3_rootless_five_cycle_denominator_pp_aggregate_no_go.py
python3 -O computations/verify_h3_rootless_five_cycle_denominator_pp_aggregate_no_go.py
~~~

The checker pins the first-Tor gate and the exact Bianchi-selector,
order-four cube, and mixed bar-curvature audits. It enumerates all fifteen
denominator squares, proves the (5+10) fine-degree split, constructs all
five cubic PP pairs, verifies both rank-four incidence matrices, and replays
the selector, residue, and old-cap separators. Its frozen ledger digest is

~~~text
f245e206da5139e72e0e39cdf4b13dd78dcc4655f6ca73be7483ed9764cd1c64
~~~
