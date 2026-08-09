# The two-edge common-triple module contains the curvature--anchor class

## 1. Outcome

The strict one-edge no-go in
[`oo-common-triple-one-edge-syzygy-cokernel.md`](oo-common-triple-one-edge-syzygy-cokernel.md)
is sharp.  At the next coefficient order, the literal source-labelled
two-chart module contains curvature times the missing third diagonal
anchor with integral coefficients.

Normalize the two outgoing rank-one heads to `0` on `pq` and `1` on `pr`.
For every common tail colour (a) and fourth-site colour (ell), put

\[
 \kappa_{a\ell}
 =A_{pq}(a,0)A_{rs}(1,\ell)
  -A_{pr}(a,1)A_{qs}(0,\ell).                              \tag{1}
\]

After the common-triple cut, retain literal second
coefficient/reinsertion columns

\[
                ef\,\partial_e\partial_f H_w              \tag{2}
\]

and both labelled `22` diagonal-anchor rows.  Here (e,f) are disjoint
physical edges, one passes through the remaining site `s`, and

\[
                     w=(a,0,1,\ell,2,2,2,2).               \tag{3}
\]

The fixed-`s` module has 216 labelled columns, rank 73, and cokernel
dimension 35 in its 108-dimensional literal source-plus-target feature
space.  Adjoining (kappa_{a\ell}X_2^D) does not raise the rank: the target
is already in the image.  An exact four-column identity is

\[
 \boxed{
 M^{pq}_{pq\mid rs}-M^{pr}_{pr\mid qs}
 -D^{pq}_{pq\mid rs}+D^{pr}_{pr\mid qs}
   =\kappa_{a\ell}X_2^D .}                                \tag{4}
\]

Every coefficient in (4) is (+1) or (-1), and its source matching
terms cancel term by term.  This is not an abstract row identity: all
columns are expanded in labelled physical matching monomials and retain
their `pq`/`pr` provenance.

Equation (4) proves that coefficient order two is the first possible order
in this common-triple module.  It does not by itself prove the OO overlap
lemma.  The remaining issue is no longer a rank or incidence search: it is
to promote the second coefficient/reinsertion operation to a descended
source chain, including its Leibniz/principal-parts correction terms.  An
ordinary derivative of equations at one source point is not automatically
an ideal consequence.

## 2. Literal rows and fine-degree filter

Use sites

\[
 p=0,\quad q=1,\quad r=2,\quad s=3,
 \qquad D=\{4,5,6,7\}.                                    \tag{5}
\]

At (3), the compatible common-triple mixed rows are

\[
\begin{array}{c|cc}
a&pq&pr\\ \hline
0&00\text{ diagonal}&01\text{ off-diagonal}\\
1&10\text{ off-diagonal}&11\text{ diagonal}\\
2&20\text{ off-diagonal}&21\text{ off-diagonal}.
\end{array}                                                \tag{6}
\]

All 18 full-nine row labels are audited.  The other 16 mixed coefficients
have a different endpoint fine degree.  The two compatible coefficients in
(6) have zero GHZ target because their `q,r` colours are `0,1`.

The target-bearing rows are separately the two source-labelled `22`
diagonal anchors.  Cutting the four endpoint sites leaves the literal
four-site equation

\[
                         H_D^{(2)}-X_2^D=0,                 \tag{7}
\]

where (H_D^{(2)}) is the three-term pure-2 hafnian on (D).  The
fine-degree of (1) permits exactly the three two-edge matchings on
\({p,q,r,s}\):

\[
                     pq\mid rs,\qquad pr\mid qs,
                     \qquad ps\mid qr.                    \tag{8}
\]

Thus (7), multiplied by one of (8), gives the only diagonal-anchor columns
in the required two-edge degree.  Anchors `00` and `11` have the wrong
colour on every site of (D).  This is how the diagonal rows enter the
module; they are neither omitted nor replaced by free target symbols.

## 3. The second coefficient columns

For a disjoint physical two-edge partial matching (m=\{e,f\}), define

\[
                         M_m=m\,\partial_e\partial_f H_w.  \tag{9}
\]

Every (M_m) has exactly three terms, one for each perfect matching of the
four uncovered sites.  There are 105 nonzero (m)'s containing an edge
through `s`.  This exhausts the fixed-`s` order-two coefficient module:
two edges meeting each other are site-square-zero, while a disjoint pair
has the unique physical colours prescribed by (3).

The `pq` and `pr` copies of (9) are retained as different domain columns.
Their source images agree because both charts partition the same global
hafnian.  Their sector placements at the three endpoint matchings are

\[
\begin{array}{c|cc}
m&pq&pr\\ \hline
pq\mid rs&\text{direct}&\text{two-star}\\
pr\mid qs&\text{two-star}&\text{direct}\\
ps\mid qr&\text{two-star}&\text{two-star}.
\end{array}                                                \tag{10}
\]

This is the matching-by-matching common-triple connection/normal
provenance.  Identifying the sectors before checking (10) would erase the
chart transition needed in (4).

For (m) in (8), define the diagonal column

\[
                         D_m=m(H_D^{(2)}-X_2^D).            \tag{11}
\]

Both labelled chart copies of (11) are retained.  Equations (9)--(11), not
independently declared direct/two-star pieces, are the generators of the
calculation.

## 4. The integral identity

Put

\[
                       m_+=pq\mid rs,qquad m_-=pr\mid qs.
\]

Because the complement of either partial matching is exactly (D), literal
matching expansion gives

\[
                         M_{m_+}=m_+H_D^{(2)},qquad
                         M_{m_-}=m_-H_D^{(2)}.              \tag{12}
\]

Using one mixed column and one diagonal column from each chart,

\[
\begin{aligned}
 &M^{pq}_{m_+}-M^{pr}_{m_-}
  -D^{pq}_{m_+}+D^{pr}_{m_-}\\
 &\quad=m_+H_D^{(2)}-m_-H_D^{(2)}
       -m_+(H_D^{(2)}-X_2^D)
       +m_-(H_D^{(2)}-X_2^D)\\
 &\quad=(m_+-m_-)X_2^D
       =\kappa_{a\ell}X_2^D,
\end{aligned}                                             \tag{13}
\]

which proves (4).  The equality is integral and source-termwise; no field
division, generic rank assumption, or sector projection occurs.

## 5. Exact rank and cokernel

Use 105 fixed-word matching monomials and the three endpoint-matching
copies of (X_2^D) as the 108 feature rows.  Exact rational elimination,
repeated for all nine choices of \((a,\ell)\), gives

\[
\begin{array}{l|r|r|r|r}
\text{module}&\text{columns}&\text{rank}&\text{kernel}&\text{cokernel}\\ \hline
\text{fixed-}s\text{ mixed, one chart}&105&70&35&35\\
\text{fixed-}s\text{ mixed, two charts}&210&70&140&35\\
\text{fixed-}s\text{ mixed + two labelled anchors}&216&73&143&35.
\end{array}                                                \tag{14}
\]

For the mixed-only module, adjoining the formal curvature--anchor target
raises rank from 70 to 71.  After the six diagonal columns (11) are added,
the rank is 73 both before and after adjoining the target.  This independently
checks membership in addition to the explicit identity (13).

As a larger counterguard, admit every disjoint two-edge partial matching,
not only those through `s`.  There are 210 per chart.  The mixed source rank
is 91.  Adding the six labelled diagonal columns gives

\[
             426\text{ columns},\qquad
             \operatorname {rank}=94,qquad
             \dim\operatorname {coker}=14,                 \tag{15}
\]

and the target-augmented rank remains 94.  Hence (4) is not an artifact of
discarding another residual edge.

## 6. Minimality and the remaining proof obligation

At coefficient order one, the exact block has rank seven and the
curvature--anchor vector raises it to eight.  Even the all-28-edge
enlargement misses the target, with an explicit integral cokernel covector.
At order two, (13) supplies the target.  Therefore

\[
 \boxed{\text{minimal strict coefficient/reinsertion order}=2.} \tag{16}
\]

No larger Macaulay or matching-incidence search is warranted for this
question.  The next proof task is a descent theorem for (13).  Concretely,
one needs a principal-parts, Rees, Hasse--Schmidt, or equivalent chain cell
whose associated coefficient is (9), and whose product-rule tails glue
between the two chart sectors in (10).  The diagonal columns (11) are
ordinary physical full-nine rows; the nontrivial issue is the source-valid
realization of the second coefficient operation on the mixed rows.

If that realization has zero indeterminacy, (13) gives
\(kappa_{a\ell}X_2^D=0\).  On the selected curvature-open stratum this is
the desired contradiction.  Until the descent/Leibniz correction is proved,
(13) is an exact associated coefficient identity rather than a completed
OO exclusion theorem.

## 7. Reproduction

Run

```text
python3 computations/verify_oo_common_triple_two_edge_anchor_identity.py
python3 -O computations/verify_oo_common_triple_two_edge_anchor_identity.py
```

The dependency-free checker expands all 105 physical matchings, all 18
full-nine labels, both chart copies, the 105 fixed-`s` and 210 unrestricted
two-edge partial matchings, the six literal diagonal columns, the exact
ranks in (14)--(15), and the four-column identity (13).  The frozen ledger
digest is

```text
cc2f54e38019ad5fbff97384185e7132a245edd3716d740f054b21ef4630950d
```
