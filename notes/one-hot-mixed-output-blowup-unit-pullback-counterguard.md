# The mixed-output blow-up has no exceptional divisor on the one-hot source torus

Research counterguard only.  This note does not rule out a blow-up of the
full source scheme with additional source equations, construct a clean cap,
or prove Krenn's conjecture.

## 1. Outcome

Blowing up the mixed-output ideal does retain the **target** leading direction
of the audited Laurent boundary, but it retains no source-relative
exceptional invariant on the normalized one-hot chart.  The obstruction is
an exact uniform unit calculation.

Let (G=(B,E)) be a properly three-edge-coloured cubic graph, with colour
matchings (P_0,P_1,P_2), and let

\[
 U_G=\left\{(w_e)\in(\mathbb G_m)^E:
                    \prod_{e\in P_c}w_e=1\ (c=0,1,2)\right\}.       \tag{1}
\]

Write (H:U_G\to Y) for the matching-output map and let

\[
 I_{\rm mix}=(y_m:m\text{ is a nonconstant colour word})
                 \subset\mathcal O(Y).                    \tag{2}
\]

If (G) has at least one perfect matching besides the three colour
matchings, then

\[
 \boxed{\qquad H^*I_{\rm mix}=\mathcal O(U_G).\qquad}      \tag{3}
\]

Consequently

\[
 \operatorname {Bl}_{H^*I_{\rm mix}}U_G
       =\operatorname {Bl}_{(1)}U_G\cong U_G,              \tag{4}
\]

and its exceptional divisor is empty.  Thus the target blow-up does not
manufacture a source exceptional class on the chart: it only projectivizes
the already known mixed-output monomials.

For the one-hot Laurent boundary, the target exceptional point is a
one-parameter-subgroup limit of the lift of the finite all-unit output.  Any
target-torus-invariant rational function that is regular at that limit has
the same value there as on the finite orbit.  Hence the affine
target-stabilizer quotient still collapses.  A blow-up coordinate which sees
the limit must be a non-invariant covariant or a section with singular
normalization; it is not an invariant finite-source separator.

The result is stronger than the statement that a Rees lift has not yet been
constructed.  Equation (3) computes the relevant pulled-back ideal exactly:
on this entire source torus there is no center to blow up.

## 2. Unit-pullback lemma

The coordinate ring of (1) is

\[
 A_G=k[w_e^{\pm1}:e\in E]\Big/
       \left(\prod_{e\in P_c}w_e-1:c=0,1,2\right).         \tag{5}
\]

For a supported perfect matching (M), proper edge colouring makes its
colour word (m(M)) determine (M): at every vertex the colour in the word
selects the unique incident edge of that colour.  Therefore there is no
coefficient collision, and

\[
                         H^*y_{m(M)}=\prod_{e\in M}w_e.    \tag{6}
\]

Every factor in (6) is invertible in (5), so (6) is a unit, with inverse

\[
                         \prod_{e\in M}w_e^{-1}.           \tag{7}
\]

If (M) is not a colour matching, then (m(M)) is mixed and (6) is one of
the generators of (H^*I_{\rm mix}).  A single unit generator proves (3).
Unsupported mixed coordinates pull back to zero and do not alter the ideal.

The same argument applies if one blows up the full ideal of the GHZ point,
including the three pure-coordinate deviations: its pullback still contains
the mixed unit (6), hence is the unit ideal on (U_G).

The universal property of the blow-up gives a unique lift

\[
                         \widetilde H:U_G\longrightarrow
                            \operatorname {Bl}_{I_{\rm mix}}Y,      \tag{8}
\]

because (3) is invertible.  This should not be confused with a nontrivial
source modification.  The Rees algebra of the unit ideal is (A_G[s]), and

\[
                         \operatorname {Proj}A_G[s]\cong U_G,      \tag{9}
\]

which is (4).

## 3. The six-site counterexample in one line

For the triangular-prism seed, the only extra perfect matching is

\[
                         M=03\mid14\mid25,
\]

with word `012012`.  Its output coordinate on the one-hot torus is

\[
                         z=w_{03}w_{14}w_{25}\in A_G^\times.        \tag{10}
\]

Thus

\[
                         H^*I_{\rm mix}=(z)=A_G.           \tag{11}
\]

On the audited Laurent arc, (w_{03}=t) and the other two displayed
factors are one, so

\[
                         H(A(t))=\Delta+t\,e_{012012}.     \tag{12}
\]

The lift of (12) to the target blow-up has special point over \(\Delta\)
with exceptional direction

\[
                         [e_{012012}].                     \tag{13}
\]

Equations (11) and (13) exhibit the distinction sharply: the target blow-up
records a direction, while the source blow-up of the pulled-back ideal is
the unchanged torus and has no exceptional point at all.  The exceptional
point in (13) comes from the boundary of the Laurent source, not from a
finite source in (U_G).

## 4. Uniform exceptional direction

Let \(\nu_e\in\mathbb Z\) be the normalized boundary valuations.  For every
mixed perfect matching put

\[
                         d_M=\sum_{e\in M}\nu_e,
                         \qquad d=\min_M d_M>0.            \tag{14}
\]

For nonzero (t), the target blow-up coordinate is

\[
             [H^*y_{m(M)}]_M=[t^{d_M}]_M.                 \tag{15}
\]

Choose a matching (M_0) with (d_{M_0}=d).  On its affine blow-up chart,
the ratios are

\[
 {H^*y_{m(M)}\over H^*y_{m(M_0)}}
   =\prod_{e\in E}w_e^{\,1_{e\in M}-1_{e\in M_0}},      \tag{16}
\]

again Laurent units on (U_G), and their orders on the arc are

\[
                         d_M-d\geq0.                      \tag{17}
\]

Therefore the exceptional special point is

\[
 \xi_\nu=\left[\sum_{M:d_M=d}e_{m(M)}\right]
                    \in\mathbb P(N_{V(I_{\rm mix})/Y,\Delta}).     \tag{18}
\]

The coefficient of every displayed direction is one because the finite
all-unit source has coefficient one on every supported matching word.

The exact expansion through eighteen vertices gives

\[
\begin{array}{c|rrrrrrr}
|B|&6&8&10&12&14&16&18\\ \hline
\#\text{ mixed coordinates}&1&2&3&5&7&9&13\\
\#\text{ minimum directions in }\xi_\nu&1&2&3&4&5&6&7.
\end{array}                                               \tag{19}
\]

In every case (d=1).  These extra projective coordinates make the target
blow-up geometrically nontrivial, but (3)--(4) show that they do not define a
source exceptional divisor.

## 5. Why the torus quotient still identifies the limit

The mixed ideal (2) is stable under the target-fixing port torus

\[
 T_\Delta=\{(\lambda_{v,c}):\prod_v\lambda_{v,c}=1\},    \tag{20}
\]

so its action lifts to the target blow-up.  The integral cocharacter
realizing the edge valuations gives, by equivariance,

\[
 \widetilde H(A(t))=h(t)\widetilde H(A_*),
             \qquad \lim_{t\to0}h(t)\widetilde H(A_*)=\xi_\nu.     \tag{21}
\]

Thus (18) lies in the orbit closure of the finite lifted output.  Any
regular (T_\Delta)-invariant defined on both points has equal values on
them.  More generally, any invariant rational function regular at
\(\xi_\nu\) is constant along the punctured orbit and takes that same
constant at its limit.

There is also a source-side proof.  The normalized source torus (U_G) is a
single (T_\Delta)-orbit: orient each colour edge and put its inverse weight
at one endpoint.  Hence

\[
                         k(U_G)^{T_\Delta}=k.              \tag{22}
\]

Every expression in the blow-up ratios (16) which is invariant after
pullback is therefore constant.  A semi-invariant homogeneous coordinate
can see the normal weight (d_M-d), but its normalization is exactly the
non-invariant gauge data erased by the quotient.

This is the appropriate scope of “the blow-up still collapses.”  The
unquotiented target blow-up certainly distinguishes \(\xi_\nu\) as a
projective normal direction.  It does not turn that target direction into a
regular invariant of a finite source.

## 6. Exact preimages and properness

An exact source (B) satisfies (H(B)=\Delta\), so all generators of

\(I_{\rm mix}\) vanish at (B).  The point (B) alone does not choose a
point of the exceptional fiber

\[
 \pi^{-1}(\Delta)
       =\mathbb P(N_{V(I_{\rm mix})/Y,\Delta});           \tag{23}
\]

a lift requires a deformation or a principalization of the pulled-back
ideal near (B).  By contrast, the Laurent arc chooses (18) even though it
has no finite source limit on (U_G).  Properness of the **target** blow-up
can preserve the point (18), but cannot change (4) or create an exact source.

Consequently a successful blow-up route must add source-faithful data not
present on this chart—for example a nontrivial center on a larger source
compactification and a proof that its exceptional fiber is incompatible
with (23).  The naive mixed-output blow-up plus the target-stabilizer quotient
does not supply such data.

## 7. Exact verification

The dependency-free checker
[`verify_one_hot_mixed_blowup_unit_pullback_counterguard.py`](../computations/verify_one_hot_mixed_blowup_unit_pullback_counterguard.py)
reconstructs the all-even expansion through eighteen vertices, enumerates
every supported matching word, writes each mixed coefficient and every
blow-up ratio as an explicit Laurent exponent vector with its inverse,
checks the integral target-fixing cocharacter, freezes the exceptional
directions (19), and independently verifies that the normalized source
torus has one-orbit action rank.  Its combined exact ledger digest is

```text
9b62adb3c4a5f7a64ac18c95df903f6d19ea1554caa22fc7d73d8ada090442fa
```
