# The fixed-old arbitrary-cross problem starts at four cells

## Outcome

The permanent-image result and the permanent-zero lower-degree result do
not, by themselves, close arbitrary cross additions to the anchored N=10
forced-pair lift.  They close the two endpoint cases

\[
 \pi(X,Y)=0
 \quad\hbox{and}\quad
 \Phi(\pi(X,Y))=0,                                      \tag{1}
\]

but ordinary cylinder membership can absorb visible nonzero permanent data
in the evaluated span of constant, linear, and quadratic cofactor columns.

There is nevertheless a stronger exact finite theorem.  On fixed cut 2,
even after all 144 linear cross-cofactor directions are granted
independently,

1. no single nonzero swap-symmetrized permanent class can complete the
   cylinder; and
2. no two nonzero permanent classes sharing a literal cross coordinate can
   complete it while preserving the three pure anchors.

Together with the arbitrary-support permanent-zero theorem, this excludes
**every cross addition supported on at most three nonzero coordinates**.
Such a source cannot preserve cut 2, hence cannot preserve the fixed triple
2,3,4 or produce a fixed-three-plus-candidate four-cut model.

The exact unresolved frontier starts at four cross coordinates.  It is a
coupled nonlinear determinantal problem.  A final universal-rank audit shows
that all 2,268 quadratic cofactor directions together absorb the cut-2
residual, so there is no source-independent quotient functional which
annihilates every such direction while detecting that residual.  This is a
stopping decision for linear enumeration, not a counterexample to Krenn's
conjecture.

## 1. Exact evaluated equations

Keep the certified anchored N=8 source fixed and adjoin the isolated
diagonal pair 8,9.  Write the old-to-new cross weights as

\[
 X_{v\alpha;\beta}=a_{v8;\alpha\beta},\qquad
 Y_{v\alpha;\delta}=a_{v9;\alpha\delta}.                \tag{2}
\]

For distinct old endpoints (v,w), the visible permanent coordinate is

\[
 \pi_{vw}^{\alpha\gamma;\beta\delta}
 =X_{v\alpha;\beta}Y_{w\gamma;\delta}
  +X_{w\gamma;\beta}Y_{v\alpha;\delta}.                \tag{3}
\]

There are 144 cross coordinates and 2,268 coordinates (3).  Exact matching
degree gives, on a cut (z),

\[
 \begin{aligned}
 C_z(X,Y)&=C_z^{(0)}+
       \sum_e x_eL_{z,e}+\sum_p\pi_p(X,Y)Q_{z,p},\\
 R_z(X,Y)&=R_z^{(0)}+\sum_p\pi_p(X,Y)D_{z,p}.           \tag{4}
 \end{aligned}
\]

Here (C_z) is the literal matrix of 21 labelled cofactor columns, and
(R_z) is the table of boundary residual rows of
(H_{10}-\Delta_{10,3}).  There are no higher cross degrees.

The complete-cylinder equations are the evaluated rank conditions

\[
       \operatorname{rank}[C_z(X,Y)\mid R_z(X,Y)]
             =\operatorname{rank}C_z(X,Y).              \tag{5}
\]

The three pure anchors add

\[
       \sum_p\pi_p(X,Y)(D_p)_{0^{10}}=0,quad
       \sum_p\pi_p(X,Y)(D_p)_{1^{10}}=0,quad
       \sum_p\pi_p(X,Y)(D_p)_{2^{10}}=0.               \tag{6}
\]

Equations (3), (5), and (6), for (z=2,3,4) and one of (0,1,5), are the
precise remaining fixed-old-source variety.  Neither of the two earlier
kernel theorems implies (5).

## 2. The universal linear quotient

On cut 2 let

\[
 {cal U}^{\rm lin}_2=\operatorname{span}
   \{C_2^{(0)},L_{2,e}:e\text{ any cross coordinate}\}. \tag{7}
\]

The checker constructs all derivatives by literal perfect-matchings and
finds

\[
                         \dim{\cal U}^{\rm lin}_2=126.  \tag{8}
\]

The forced-pair residual has only one nonzero boundary normal form modulo
(7): at word 111 it is

\[
                              e_{1089}+e_{1097}.         \tag{9}
\]

This recovers the cut-2 part of the permanent-zero theorem.  More
importantly, (7) is used below as a deliberately oversized lower-degree
space: actual linear contributions share 21 evaluated columns, whereas
(7) allows every derivative column independently.

## 3. One nonzero permanent class

Thirteen of the 2,268 permanent classes change at least one pure anchor.
A source with only one such nonzero class violates (6) immediately.  The
remaining 2,255 classes preserve all three anchors individually.

For each anchor-preserving class (p), form the still larger space

\[
             {cal V}_p={\cal U}^{\rm lin}_2+
                 \operatorname{span}\{Q_{2,p;h,i}:h,i\}.             \tag{10}
\]

If (pi_p=t\ne0), a necessary condition for the actual cylinder is

\[
                    R_2^{(0)}+tD_{2,p}\in{\cal V}_p.   \tag{11}
\]

All entries are rational, so reducing (11) modulo (10) gives exact affine
linear equations in the one scalar (t).  Every one of the 2,255 systems
is inconsistent for nonzero (t).  The enlarged-space rank census is

| rank | number of classes |
|---:|---:|
| 126 | 1467 |
| 127 | 18 |
| 128 | 116 |
| 129 | 132 |
| 130 | 54 |
| 131 | 198 |
| 132 | 198 |
| 133 | 9 |
| 134 | 27 |
| 135 | 36 |

Because the actual evaluated column span is contained in (10), failure of
(11) is a source-level exclusion, not a coefficient sample.

## 4. Two sharing classes and the three-cell theorem

A source supported on three cross coordinates has either zero permanent
data or a (1+2) distribution across new vertices 8 and 9.  In the latter
case it creates at most two nonzero permanent classes, and those classes
share the coordinate on the singleton side.  Endpoint swap means that a
permanent class has two literal orientations; the checker retains both
when classifying sharing.

There are 231,336 unordered sharing-class systems among all 2,268 classes.
For every pair (p,q), including the 13 anchor-changing classes, the checker
forms

\[
 {cal V}_{p,q}={\cal U}^{\rm lin}_2+
      \operatorname{span}\{Q_{2,p;h,i},Q_{2,q;h,i}:h,i\}             \tag{12}
\]

and solves exactly for (s,t\ne0):

\[
 \begin{cases}
 R_2^{(0)}+sD_{2,p}+tD_{2,q}\in{\cal V}_{p,q},\\
 s(D_p)_{c^{10}}+t(D_q)_{c^{10}}=0,&c=0,1,2.
 \end{cases}                                                        \tag{13}
\]

No system has a solution with both scalars nonzero.  Cases with one scalar
zero reduce to the preceding one-class audit.  Hence a nonzero-grade source
on at most three cells fails cut 2.  A zero-grade source of any support was
already excluded by the universal linear quotient.  Therefore

\[
 \boxed{\text{Every fixed-old cross source with support at most three is
 excluded.}}                                                       \tag{14}
\]

This conclusion is over arbitrary rational or complex weights: the exact
linear systems have rational coefficients, and their inconsistency remains
inconsistency after extending the field to (mathbb C).

## 5. Why arbitrary support remains open

Let

\[
 {cal U}^{\rm quad}_2={\cal U}^{\rm lin}_2+
       \operatorname{span}\{Q_{2,p;h,i}:p=1,\ldots,2268,\ h,i\}.     \tag{15}
\]

Exact reduction gives

\[
                         \dim{\cal U}^{\rm quad}_2=1224,             \tag{16}
\]

and every row of (R_2^{(0)}) belongs to (15).  Thus the universal
quadratic superspace erases the witness (9).  This does not exhibit an
actual source: it independently chooses thousands of coefficient
directions which an actual 21-column evaluated matrix cannot choose
independently.  It proves the narrower but strategically important fact
that another linear quotient functional on the same ordinary data cannot
settle the arbitrary-support case.

The smallest unresolved source has at least four nonzero cross coordinates.
For a four-coordinate support with (X)-coordinates (i,j) and
(Y)-coordinates (k,l), the ordered products lie on the rank-one quadric

\[
 (X_iY_k)(X_jY_l)-(X_iY_l)(X_jY_k)=0,                  \tag{17}
\]

before endpoint-swap recombination by (3).  A (1+3) support gives three
sharing products; a (2+2) support gives the four rectangle products in
(17).  These are the first support strata not covered by (14).  The next
admissible calculation is therefore the exact intersection of these
rank-one support strata with (5)--(6), first on cut 2 and then on the fixed
triple plus a candidate.  Enumerating coefficient grids or further
independent linear-grade spans should stop here.

## 6. Scope

The theorem fixes the certified anchored N=8 old source and the isolated
diagonal pair used in the N=10 lift.  It permits arbitrary coloured cross
coordinates incident to vertices 8 or 9, but it does not permit simultaneous
changes to old source cells.  It is a cut-2 exclusion, which is sufficient
for the fixed-three question because cut 2 is mandatory.

The result is not an N=8 counterexample, an N=10 counterexample, or a proof
of Krenn's conjecture.  It sharpens the contraction route to a precise
nonlinear four-cell frontier and records why the two preceding theorems do
not close arbitrary cross additions.

## Reproduction

    python3 computations/verify_n10_fixed_old_arbitrary_cross_frontier.py
    python3 -O computations/verify_n10_fixed_old_arbitrary_cross_frontier.py
    python3 -I computations/verify_n10_fixed_old_arbitrary_cross_frontier.py
    python3 -S computations/verify_n10_fixed_old_arbitrary_cross_frontier.py

The checker uses exact rational perfect-matching tensors, labelled cofactor
columns, sparse quotient bases, and exact one- and two-parameter elimination.
