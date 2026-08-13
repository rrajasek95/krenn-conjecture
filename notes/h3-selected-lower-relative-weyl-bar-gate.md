# The Weyl bar cancels the private face formally; physical descent is occurrence-local

## Exact universal correction

Write `Z0,Z1` for the two 341-term fine components of the endpoint-
recoloured, tail-antisymmetric order-six cycle.  The simultaneous signed
Weyl action `tau` at sites 2 and 5 satisfies

\[
                         \tau Z_0=-Z_1.                 \tag{1}
\]

Therefore the canonical group-bar edge on `Z0` has

\[
 d[\tau\mid Z_0]=\tau Z_0-Z_0=-(Z_1+Z_0).              \tag{2}
\]

This is not just a shadow identity.  On source products `A0^2,A1^2`, in
the selected `37:11` singleton face, the two components are exactly

\[
 -{4\over3}\,\bar\xi,
 \qquad
 +{4\over3}\,\xi,                                    \tag{3}
\]

where

\[
\begin{aligned}
 \xi&=q_{01}^{01}q_{27}^{21}q_{34}^{11}q_{35}^{12}q_{67}^{22},\\
 \bar\xi&=q_{01}^{01}q_{27}^{11}q_{34}^{11}q_{35}^{11}q_{67}^{22}.
\end{aligned}
\]

Thus (2) cancels the private pair coefficientwise.  The two-root Weyl
target defect on the GHZ tensor is invariant under the residual-site swap
`s=(0 1)`.  Consequently the odd bar `(1-s)[tau|Z0]` has target zero and
cancels

\[
 {4\over3}(\xi-\bar\xi-s\xi+s\bar\xi).                 \tag{4}
\]

The normalized bar augmentation is also zero.  The universal
Cartan/Spencer problem is therefore solved exactly.

## Why the old physical bars do not supply this edge

All four monomials in (4) have the repeated-site profile

```text
(1,1,1,2,1,1,1,2),
```

so sites 3 and 7 are the doubled pair.  In each of the four exact fine
degrees there are only two compatible complete-row endpoints.  They use
the two multipliers `q_37^11,q_37^12`.  Hence all eight 90-term endpoints,
every normalized tail-Weyl difference between them, and both endpoint-odd
Cartan rectangles contain a physical `37` edge in every monomial.  None of
the four private monomials in (4) contains that edge.

There is a tempting two-term Hasse bridge.  Put

\[
 m=q_{01}^{01}q_{27}^{21}q_{34}^{11}.
\]

Then the four-site hafnian face is

\[
 m(q_{35}^{12}q_{67}^{22}
   +q_{36}^{12}q_{57}^{22}
   +q_{37}^{12}q_{56}^{22}).                            \tag{5}
\]

All three coefficients in (5) are plus one: it is the nonzero four-site
hafnian, not a signed `C4` source identity.  The middle term is removed by
the direct-free specialization `q_36=0`.
The first is \(\xi\); the last, call it \(L_\xi\), is one occurrence in
the `01211221` row times `q_37^12`.  Crucially, (5) is a nonzero Hasse-face
polynomial \(\xi+L_\xi\), not the equation \(\xi=-L_\xi\) in the
coefficient ring.  It is a source boundary only after the corresponding
principal-parts/Hasse cell is included.

The tail-Weyl difference makes the distinction exact:

\[
 H_\xi-H_{\bar\xi}
   =(\xi-\bar\xi)+(L_\xi-L_{\bar\xi}).                  \tag{6}
\]

The selected complete-row Weyl bar contains
\(L_\xi-L_{\bar\xi}\), but also its other complete-row companions.
Subtracting the whole bar therefore does not leave just
\(\xi-\bar\xi\).  The formal 341-edge bar does not specialize to the
single four-site face without this companion cancellation.

The exact finite image calculation, now including all four transported
copies of (5), is

```text
complete endpoints                                      8
normalized tail-bar boundaries                          4
endpoint-odd bar boundaries                             2
rank(endpoints)                                          8
rank(endpoints + every bar boundary)                     8
rank(after four Hasse-face bridges)                      12
rank(after adjoining the private packet (4))            13
```

The symmetry-compatible covector begins with

\[
 {3\over16}
 (e_\xi^*-e_{\bar\xi}^*-e_{s\xi}^*+e_{s\bar\xi}^*)    \tag{7}
\]

and is extended in each fine grade by the negative weight on (L) and the
positive weight on a private pivot of its `q37:12` complete column.  This
extended covector vanishes on every complete endpoint, normalized/odd bar,
and all four Hasse faces, while evaluating to one on (4).

There is no contradiction with the separate 343-term first-flat operator
solution: that affine representative kills every singleton face inside the
bounded coefficient-operator module while retaining `D2=-delta`.  It still
has no constructed map to the literal complete-row repeated grade.  The
formal group bar and the affine first-flat adjustment are two source-side
ways to remove the singleton; neither supplies the occurrence-local
physical comparison or its augmented readouts.

This explains the apparent tension between the universal Weyl prism and
the literal discrepancy.  The universal bar uses an edge based at each
operator occurrence.  A complete physical bar acts on a 90-term row as a
whole and retains the forced matching edge.  Complete-row covariance proves
that the latter exists; it does not localize it to the private occurrence
needed by (3).

## Remaining cell

The smallest positive datum is now precise: lift the 341-edge formal group
bar to an occurrence-local principal-parts/Weyl-bar cell in the displayed
word/fine/repeated grades.  Its differential must contain (4), and its
physical `D/W/anchor/eta/sigma` rows must be defined.  Endpoint oddization
then gives target zero automatically.

The finite no-go is exhaustive for complete-row normalized Weyl bars in
these grades.  It does not exclude a higher PP/Hasse relative generator;
that generator is exactly the missing occurrence-local lift.

## Verification

```bash
python3 computations/verify_h3_selected_lower_relative_weyl_bar_gate.py
python3 -O computations/verify_h3_selected_lower_relative_weyl_bar_gate.py
python3 -I -S computations/verify_h3_selected_lower_relative_weyl_bar_gate.py
```
