# Endpoint/matching Maschke contraction stops at the pointed occurrence graph

## Exact result

On the ninety literal occurrences of the selected `11:110000` response,
the coefficient projector is exactly a finite-group Reynolds projector:

\[
 \Pi_{\rm end}\Pi_{\rm match}
 ={(B+2)(B-2)(B-4)(A+I)\over240\cdot3}
 ={J_{90}\over90}.                                      \tag{1}
\]

Here the full site group `S6` acts transitively, and the stabilizer of a
marked occurrence has order eight.  Therefore the action-groupoid bar has
an explicit characteristic-zero primitive

\[
 H_f=-90\,{1\over720}\sum_{g\in S_6}[g\mid e_f],
 \qquad dH_f=90e_f-\mathbf1_{90}=c_f.                  \tag{2}
\]

This is a positive construction in the homotopy-orbit complex.  It is not a
boundary in the fixed pointed physical source presentation.  Canonical
transport of the retained endpoint label sends `g e_f` back by `g^-1`, so
both endpoints of every bar become `e_f` and the boundary becomes zero.
Forgetting the object tag without transporting its label produces (2), but
then the raw action bars span the full rank-89 augmentation ideal and impose
new occurrence equalities.

Checker:
[verify_h3_centered_occurrence_endpoint_matching_maschke_pointed_gate.py](../computations/verify_h3_centered_occurrence_endpoint_matching_maschke_pointed_gate.py).

## The presentation-preserving cone

Modulo the complete response row, the original occurrence presentation has
dimension `89`.  Adjoining raw `c_f` as a boundary lowers it to `88`.  The
smallest rank-preserving relative cone instead adjoins one graph coordinate
`u_f` and uses

\[
                         db_f=c_f-u_f.                 \tag{3}
\]

The extended quotient again has dimension `89`, but (3) makes `c_f`
homologous to `u_f`, not zero.  At the normalized pointed response one may
take `f=1`, one other occurrence `=-1`, and all others zero.  Then the
complete response is zero while

\[
                         c_f(x)=90.                    \tag{4}
\]

Thus pointedness forces `u_f(x)=90`.  Its first cotangent face is

\[
                        du_f=dc_f=90df-dR.             \tag{5}
\]

This is the same scaled-anchor datum isolated in the earlier occurrence
audit.  Killing `u_f` or (5) would be exactly the missing centered
occurrence comparison, not a consequence of Maschke semisimplicity.

The word stabilizer `S2 x S4` makes the distinction even sharper.  Its
marked orbit has size six, so its bars can contract only the
marked-within-six component.  They cannot reach the orbit-marginal part of
`c_f` on the other 84 occurrences.  The full `S6` action reaches it only by
moving among word/presentation objects.

## First literal principal-parts face

Let `b01` be the three-matching fibre with endpoints `(0,1)`.  Exact
coefficient identities give

\[
 (A+I)c_f=3c_{01},\qquad c_{01}=30b_{01}-R.            \tag{6}
\]

The first vertical face is therefore

\[
 dc_{01}=30db_{01}-dR,
 \qquad db_{01}={dR+dc_{01}\over30}.                  \tag{7}
\]

In coordinates `(db01, sum of the other 29 endpoint fibres, all-D)`, the
available complete face and normalized all-D endpoint are

```text
dR      = (1,1,0),
all-D   = (0,0,1),
db01    = (1,0,0).
```

The first two have rank two; adjoining `db01` raises it to three.  The
primitive dual is `(1,-1,0)`, and the genuine missing centered face is
`dc01=(29,-1,0)`.  This recovers the selected-face obstruction from
`e2384ea` without using normalized `GL3`.

Residual matching flips do not remove (7).  They fix `c_f`, `c01`, `b01`,
and the aggregate six-term `db01`.  Over characteristic zero, their
nontrivial three-dimensional termwise character module is indeed
Maschke-contractible, but the invariant aggregate face remains.  This is
exactly the distinction recorded by `15d0c12`.

## Augmented readouts and the first obstruction

The proper faces occur in this order.

1. In the orbit-relative action groupoid, the GHZ target readout is zero
   because literal site permutations preserve the target.
2. The first pointed proper face is the graph/anchor conormal (5).  After
   matching, its literal selected `q`/first-PP face is (7).
3. Returning every moved word to the fixed `110000` object by signed
   Weyl/Cartan paths is extra structure.  It produces the known 18-term
   endpoint target normal `N_f`; a common target cone cancels that target
   but leaves the rank-two protected curvatures `C2,C3` of `fa1a397`.
4. Cap and shifted-ridge transport is later and differently typed:
   `01211222 / t*q_(v,N) / repeated P3+K2`.  The first conditional cap
   shadow is the primitive `(Q,ores)=(-1,-1)` cell.  No action-groupoid bar
   maps (5) or (7) into that grade.

Hence neither `435e8cd` nor `fa1a397` is contradicted.  The former is the
same retained-label-versus-raw-fold obstruction at one endpoint edge.  The
latter starts only after granting the pointed graph/PP lift and choosing a
fixed-word target-normal splitting.

## Shortest remaining theorem

Construct a pointed, termwise PP-natural endpoint/matching comparison whose
relative graph coordinate realizes (5), whose matching face realizes (7),
and whose fixed-word lift carries the target-normal, cap/ridge, physical-q,
anchor, and eta/sigma rows.  Maschke contraction then supplies all
nontrivial finite-group character directions automatically; it does not
supply the invariant graph coordinate or its selected first-PP face.

This result is exact for the canonical h=3 packet over characteristic zero.
It proves the orbit-relative primitive and a minimal pointed no-go, not the
missing physical comparison cell.

Run normally, optimized, and isolated/no-site.  The frozen ledger digest is
recorded by the checker.
