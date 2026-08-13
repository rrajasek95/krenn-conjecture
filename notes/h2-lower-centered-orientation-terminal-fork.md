# The two lower centered debts have one physical orientation fork

## Result

The two marked restrictions of the (h=3) centered occurrence class are
literal order-two physical packets:

```text
delete 23: word 0112, residual q45:12, reinsert q23:21,
delete 45: word 0121, residual q23:21, reinsert q45:12.
```

Both restore the mixed tail `q23:21*q45:12` in word `01211222` and labelled
repeated grade `P3+K2`.  Each lower packet has twelve ordered response
occurrences and its marked class has the exact endpoint-parity split

\[
 c_2=12e_+-\mathbf1_{12}
    =6(e_+-e_-)+\left(6(e_++e_-)-\mathbf1_{12}\right)
    =c_2^-+c_2^+.                                      \tag{1}
\]

This gives the sharp physical fork.

1. If the odd readout is realized by a literal nonzero same-tail
   offdiagonal response/curvature cell, the existing bidirectional
   private-site identity supplies a source-provenant distinct-head active
   fan.  The complete-support theorem then gives four-good or a literal
   pure-colour coloop.  A nonzero *abstract occurrence coordinate* is not
   enough for this implication.
2. If the odd readout is dark, then only (c_2^+) remains.  It is not a
   common-(H_0) class: it lies in the five-dimensional augmentation-zero
   part of the six unordered endpoint-hole rows.
3. Coefficientwise one endpoint-adjacency factor suffices:

   \[
   c_2^+=(B-4I)w,
   \qquad w=-{1\over24}(B+6I)c_2^+.                   \tag{2}
   \]

   Physically, however, the known target-safe Cartan prism is endpoint-odd.
   The signless/even prism needed for (2) has target defect
   (2(w_{m Weyl}-1)\Delta).  After a hypothetical target-normal
   correction, its first still-unfilled Hasse face is the one-endpoint
   Cartan product-rule cross term.  Thus (2) is the smallest construction
   target, not a completed boundary.

The checker is
[verify_h2_lower_centered_orientation_terminal_fork.py](../computations/verify_h2_lower_centered_orientation_terminal_fork.py).

## 1. The literal twelve-occurrence packets

On four sites an occurrence consists of ordered response endpoint sites
((p,s)) and the forced residual edge on the other two sites.  There are
(4\cdot3=12) occurrences.  In both marked cuts the selected orientation is
((p,s)=(0,1)), and its transpose is ((1,0)).  The marked residual edges
are respectively `45:12` and `23:21`.

Deleting `23` from the six-site residual word `012112` leaves the sites
`0,1,4,5` and word `0112`.  Deleting `45` leaves `0,1,2,3` and word `0121`.
Reinsertion restores `012112`; the common spectator `q67:22` restores the
declared eight-site cap word and repeated grade.  Thus the parity fork is in
the actual lower physical words, not a free four-site occurrence model.

Endpoint transposition preserves the four-site word as a site-colouring but
exchanges the ordered endpoint decorations `01` and `10`.  A physical chain
must therefore retain the endpoint role and fine label; the coefficient
involution alone does not do this.

## 2. Odd brightness is a physical landing only after typing

Let

\[
                         \chi^-=e_+^*-e_-^* .          \tag{3}
\]

Then

\[
 \chi^-(\mathbf1)=0,
 \qquad \chi^-(c_2^-)=12,
 \qquad \chi^-(c_2^+)=0.                              \tag{4}
\]

Suppose a complete augmented comparison identifies this odd coordinate
with the literal same-tail physical offdiagonal cell.  The target-augmented
private-site row and its transpose give the two distinct-head fans at the
two endpoints.  The complete pure matching supports then imply

```text
physical odd cell -> bidirectional active fan -> four-good or pure coloop.
```

This is stronger and more precise than calling any nonzero occurrence
functional terminal.  The private-site theorem consumes an actual decorated
cell and complete source rows.  Until the lower word/fine comparison supplies
that cell, (4) is only a coefficient detector.

## 3. Odd-dark leaves a five-dimensional even class

Pair the twelve occurrences by endpoint reversal and let

\[
 b_h=e_{h,+}+e_{h,-}
\]

for the six unordered endpoint holes (h).  The complete response row is

\[
                         H_0=\sum_hb_h.                \tag{5}
\]

For the marked hole (h_0),

\[
                         c_2^+=6b_{h_0}-\sum_hb_h.     \tag{6}
\]

Thus the swap-even hole module has rank six, its common line has rank one,
and its augmentation-zero quotient has rank five.  Choose a comparison hole
(h_1\ne h_0) and put (+1) on both orientations over (h_0), (-1) on
both orientations over (h_1), and zero elsewhere.  This primitive integral
covector kills (H_0) and every odd vector, but reads (12) on (6).

Consequently odd-dark does **not** make the lower debt a common response
constant.  Nor does a fixed-endpoint (q)-only K4 switch help: with (p,s)
fixed, the residual set has two sites and only one residual matching, so its
matching-difference rank is zero.  A full K4 perfect-matching/Bianchi row
uses two (q)-edges and changes the source-operation block.

The even covector is presently a source-presentation detector, not a
physical Fredholm separator.  Terminal promotion would require it to extend
over the complete protected map, including the physical-(q) columns.

## 4. One coefficient operator, one physical obstruction

Let (B) move one ordered endpoint through the forced residual edge and
pair the displaced old endpoint with the residual mate.  It has degree four.
On the even endpoint module its spectrum is

\[
                             4,0,-2,                   \tag{7}
\]

where the (4)-eigenspace is the common line.  Hence

\[
               \Pi_{H_0}={B(B+2I)\over24}             \tag{8}
\]

and (8) kills (c_2^+).  Factoring (1-\Pi_{H_0}) gives (2).  The displayed
preimage (w) is rational, and (12w) is integral on all twelve occurrence
coordinates.  So characteristic zero introduces no coefficient obstruction.
One equivariant (B-4I) family supplies all five even standard directions;
five unrelated construction theorems are unnecessary.

The coefficient adjacency is the top symbol of a one-endpoint
Cartan/matching prism.  The pinned physical source theorem constructs the
target-safe combination

\[
                         (1-s)H_{w_{\rm Weyl}},        \tag{9}
\]

which is endpoint-odd.  The even combination required here is

\[
                         (1+s)H_{w_{\rm Weyl}},        \tag{10}
\]

and its target boundary is

\[
              (1+s)(w_{\rm Weyl}-1)\Delta
                    =2(w_{\rm Weyl}-1)\Delta.         \tag{11}
\]

Thus the old odd Cartan theorem cannot be reused as the even filler.  In the
smallest augmented rows, cancelling (11) still needs the already isolated
primitive source-normal attachment.  Furthermore a source lift of (B)
obeys the Hasse product rule: besides its desired endpoint-change top it has
the one-endpoint Cartan cross term.  A physical (B-4I) theorem must fill
that face in the literal lower word and preserve target, Eq, residue, anchor,
physical (q), (W), eta, and sigma.

## 5. Why the E14 units do not fill the lower class

There is a genuine coefficient core alignment with E14, but the known unit
theorems terminalize two- or three-new-cell support only after it has been
placed in the canonical E14 chart.  The present source word is `01211222`,
whereas the E14 unary/G11 base word is `000101`.

There is also a tail mismatch.  The physical lower/cap tail is

\[
                    a_{24}^{21}a_{35}^{12},           \tag{12}
\]

while the E14 curvature response uses

\[
                    a_{24}^{11}a_{35}^{11}.           \tag{13}
\]

The only complete E14 response row hitting the two endpoint orientations is
signless, with coefficients `(1,1)`.  It is killed by the odd detector (3),
and importing it into the even branch still requires the cross-word and
tail-transport map.  Therefore neither the K4 inventory nor the E14 unit
theorems construct the physical (B-4I) lift in `0112` or `0121`.

## Shortest remaining theorem

It is enough to construct one cut-covariant physical family (G_2) whose
two marked proper faces are the (B-4I) endpoint-difference family in
`0112/q23:21` and `0121/q45:12`, whose reinsertion has the common mixed tail
in `01211222/P3+K2`, and whose target-normal and one-endpoint Hasse faces are
physical boundaries.  Then:

- odd-bright faces route to the existing active-fan landing;
- odd-dark faces are filled by (2); and
- the remaining common component is the already isolated (H_0) line.

Failure of that family is measured first by the signless target defect (11),
then by the one-endpoint product-rule face or the primitive even covector.
This is one physical source theorem shared by both cuts.

## Scope and verification

The checker proves the literal cut words and decorations, twelve-occurrence
parity split, primitive odd/even detectors, rank-five even quotient, zero
fixed-endpoint K4 matching-difference rank, and the rational/integral
(B-4I) factorization.  It pins the active-fan and E14 scope statements.  It
does not claim that an abstract occurrence projection is physical, construct
the signless Cartan correction, promote the even covector to a terminal, or
close the normalized pure-colour coloop branch by itself.

Run:

```text
python3 computations/verify_h2_lower_centered_orientation_terminal_fork.py
python3 -O computations/verify_h2_lower_centered_orientation_terminal_fork.py
python3 -I -S computations/verify_h2_lower_centered_orientation_terminal_fork.py
```

Frozen ledger SHA-256:

```text
62603383e8aeaf8b691c8f28fea5df80f206d555b3dfc4cd53c6a46a5d4251b9
```
