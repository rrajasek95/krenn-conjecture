# Mixed-word reset reaches the odd class but not the source chain lift

Research reduction only.  This note does not construct the relative-Rees
generator \(n_0\), prove a nonzero filtered \(d_2\), close the unified overlap
theorem, or prove Krenn's conjecture.

## 1. Outcome

The residual-word gap isolated in
[the multi-label target-Koszul no-go](h3-multilabel-target-koszul-crossword-no-go.md)
has a smaller literal test than a new target Koszul complex.  On the five odd
sites, coefficient extraction at a word \(m\), followed by ordered reinsertion
of the pure word **00000**, is the rank-one operator

\[
 {\sf P}_m=\iota_{00000}\epsilon_m,
 \qquad {\sf P}_m(e_m)=Y_0,
 \qquad {\sf P}_m(e_w)=0\quad(w\ne m).                 \tag{1}
\]

This is an actual coefficient-exposure/reinsertion map, not an abstract arrow
between word tags.  Because each relevant \(m\) is mixed,
\({\sf P}_m(\Delta)=0\).  The first question is whether (1) descends through
the physical odd quotient

\[
 C_q={{\cal R}_{5}(D_x)\over {\cal R}_{1}(D_x)q^{[2]}}. \tag{2}
\]

The exact answer on the two rational eight-site packets is:

\[
\begin{array}{c|c|c}
\text{packet}&m&{\sf P}_m:C_q\to C_q\\ \hline
\text{direct-free}&12112,12212&\text{well defined}\\
\text{tilted}&02012&\text{well defined}\\
\text{tilted}&22012&\text{not well defined}.
\end{array}                                             \tag{3}
\]

Moreover \([Y_0]=[00000]\ne0\) in both quotients.  Thus the bare word change
is **not** the obstruction: three of the four exact tags already admit a
literal cross-quotient reset.

On the calibrated non-source packets, the descended resets have exactly the
desired numerical normalization:

\[
\begin{aligned}
 {1\over4}{\sf P}_{12112}
   \bigl({\cal F}_{22}^{x=0}\bigr)
   &={1\over4}Y_0=-\kappa_{\rm df}Y_0,\\
 5{\sf P}_{02012}
   \bigl({\cal F}_{22}^{x=0}\bigr)
   &={5\over2}Y_0=-\kappa_{\rm tilt}Y_0.               \tag{4}
\end{aligned}
\]

Here \({\cal F}_{ij}=H_{ij}-\delta_{ij}X_i\) is the full-nine EqSystem
residual, \(\kappa_{\rm df}=-1/4\), and
\(\kappa_{\rm tilt}=-5/2\).  Formula (4) is not \(n_0\).  Its inputs are
precisely the nonzero full-EqSystem failures of the two guards.  In a true
source, \({\cal F}_{ij}=0\), so every strict map (1) gives zero.  Coefficient
reset therefore transports the guard defect to the right odd word but does
not manufacture the filtration-lowering source cell required by the
target-augmented \(d_2\).

The direct-free packet also gives an exact zero-indeterminacy obstruction.
Both \({\sf P}_{12112}\) and \({\sf P}_{12212}\) descend, but

\[
 ({\sf P}_{12112}-{\sf P}_{12212})[12112]=[00000]\ne0. \tag{5}
\]

They happen to agree after evaluation on the particular guard because its
two mixed coefficients both equal one.  They are distinct quotient maps, so
that numerical agreement is not a source-independent readout theorem.

Consequently the next missing object is now sharper than a cross-word map.
It is a **one-higher source syzygy** lifting one of the descended resets to
the relative EqSystem/cap complex.  Its filtration-lowering commutator must
cancel \(\kappa Y_0w\), and differences of two lifts must have zero odd
readout.  No existing coefficient row supplies that chain lift.

## 2. The literal reset and its quotient criterion

Let \(D_x=\{1,2,3,4,5\}\) in the site order of the committed eight-site
packets.  The top occupied piece has basis

\[
                 e_w=\prod_{v\in D_x}e_{w_v}^{(v)},
                 \qquad w\in\{0,1,2\}^{5}.             \tag{6}
\]

Extraction and ordered reinsertion are

\[
 \epsilon_m(e_w)=\delta_{mw},
 \qquad \iota_{00000}(1)=e_{00000}.                    \tag{7}
\]

This uses the same named-slot extraction and reinsertion primitives as the
ordered five-exposed reconstruction, but it is not that inverse
reconstruction: it deliberately chooses a new colour basis vector at every
reinserted slot.  The choice of pure output is therefore extra data, and (5)
records part of its indeterminacy.

The operator \({\sf P}_m\) descends through (2) exactly when

\[
 \epsilon_m\bigl({\cal R}_1q^{[2]}\bigr)=0,             \tag{8}
\]

because its image is the line spanned by \(Y_0\), and the checker proves
\(Y_0\notin{\cal R}_1q^{[2]}\).  On basis linear forms, (8) is the finite
literal test

\[
 [e_m]\bigl(e_a^{(v)}q^{[2]}\bigr)=0
 \quad(v\in D_x,\ a=0,1,2).                            \tag{9}
\]

For the direct-free packet, all fifteen coefficients in (9) vanish for both
**12112** and **12212**.  The denominator has rank seven.  For the tilted
packet, the denominator has rank eight and all fifteen coefficients vanish
for **02012**.  For **22012** there are exactly two failures:

\[
 [22012]\bigl(e_2^{(2)}q^{[2]}\bigr)=1,
 \qquad
 [22012]\bigl(e_1^{(4)}q^{[2]}\bigr)=1.                \tag{10}
\]

Thus any construction using the tilted **22012** row additionally needs two
denominator homotopies.  The **02012** row avoids that earlier obstruction.

## 3. Exact action on the missing rows

Fix residual site \(x=0\) at colour zero.  The complete enumeration of all
\(9\cdot3^6=6561\) pq coefficients gives the mixed part

\[
\begin{array}{c|c|c|c}
\text{packet}&\text{six-site word}&(i,j)&{\cal F}_{ij}\\ \hline
\text{direct-free}&012112&(2,2)&1\\
&012212&(2,1)&1\\
&012212&(2,2)&1\\ \hline
\text{tilted}&002012&(2,2)&1/2\\
&022012&(0,2)&-3/2\\
&022012&(2,0)&1/2\\
&022012&(2,2)&-1/4.
\end{array}                                             \tag{11}
\]

Every target entry in (11) is zero.  Deleting the fixed first site gives the
four tags in (3).  Applying the descended maps to (11) proves (4), with no
division by a star, direct entry, trace, or matching power.  The scalar
normalization only divides by the displayed nonzero **guard residual**.
That last phrase is essential: the normalization is unavailable on the
actual source locus, where all entries of (11) vanish.

This distinguishes two statements which the word-tag model could not
separate:

1. a literal map from a mixed coefficient line to the pure odd quotient
   exists; but
2. a physical secondary source cell with that associated-grade symbol has
   not been constructed.

The first is settled positively by (1)--(4).  The second is the live proof
obligation.

## 4. Why this is not the generator \(n_0\)

Write \(r_{ij}^{x=0}\) for a formal tensor-valued EqSystem row generator,
with

\[
                    d_{\rm Eq}r_{ij}^{x=0}
                       ={\cal F}_{ij}^{x=0}.             \tag{12}
\]

A strict lift of \({\sf P}_m\) through (12) has boundary
\({\sf P}_m({\cal F}_{ij}^{x=0})\).  After base change to a genuine source,
that boundary is zero.  The desired filtered construction instead needs a
new relative generator whose lower boundary is

\[
                         d_0n_0=\kappa Y_0w,             \tag{13}
\]

while its associated-grade response is \(-\kappa Y_0\).  Hence a successful
lift must contain a filtration-lowering homotopy term not present in (1).
Schematically, on the selected mixed row it must satisfy a commutator
identity of the form

\[
 d_{\rm cap}{\sf H}_m+{\sf H}_m d_{\rm Eq}
       =-\kappa\,\iota_{00000}\epsilon_m               \tag{14}
\]

in the relative source resolution, with the cap-relation coordinate \(w\)
restored on the left.  Formula (14) is a typed request for an actual
one-higher syzygy; it is not asserted to exist.

The smallest possible associated-grade symbols are forced by (4):

\[
 \operatorname {gr}(n_0)=
 \begin{cases}
  \frac14{\sf P}_{12112}r_{22}^{x=0},&\text{direct-free},\\
  5{\sf P}_{02012}r_{22}^{x=0},&\text{tilted}.
 \end{cases}                                            \tag{15}
\]

The missing literal operation is the lower term \({\sf H}_m\) in (14).
Equivalently, it is a first syzygy comparing the curvature-normal Euler row
with the reset mixed EqSystem row before evaluation.  Another coefficient
row, ordinary target wedge, or strict extraction/reinsertion cannot replace
it: all such strict maps factor through \({\cal F}=0\).

Zero indeterminacy is a separate part of the same obligation.  Equation (5)
shows that it is false for arbitrary descended resets.  A source theorem must
prove

\[
 \operatorname {res}_0({\sf H}_m-{\sf H}'_m)=0          \tag{16}
\]

for any two physical lifts satisfying (14).  Agreement on the rational guard
does not prove (16).

## 5. Verification and scope

The dependency-free checker
[verify_h3_mixed_word_reset_cross_quotient_chain_lift_no_go.py](../computations/verify_h3_mixed_word_reset_cross_quotient_chain_lift_no_go.py)
reconstructs both eight-site cell tables, independently enumerates all 6561
pq equations, rebuilds \({\cal R}_1q^{[2]}\), proves \([00000]\ne0\), checks
the exact quotient-descent witnesses (9)--(10), verifies every value and
target in (11), and checks the normalizations (4).  It uses exact rational
arithmetic and no third-party packages.

The result is deliberately narrow.  It proves neither nonexistence of the
syzygy (14) nor a physical \(n_0\).  It does prove that the next search should
target a source-resolution/relative-Rees first syzygy, not another word-space
or target-Koszul operation: literal reset already crosses the word gap, while
strict reset cannot cross the source-chain gap.
