# Bottom/top torus collision and the sharp twelve-site boundary

## Outcome

For three selected one-factors with pairwise Hamilton unions, every extra
perfect matching is automatically a genuinely ternary singleton.  If it
uses `e_r` edges of colour `r`, then scaling colour `r` places that singleton
in degree `2e_r`.  Since `e_0+e_1+e_2=m`, some colour detects it by degree at
most

\[
                         2\left\lfloor\frac m3\right\rfloor. \tag{1}
\]

The first degree is not uniformly two.  At `n=12`, there is an exact
unit-weight triple whose three binary faces are Hamilton and whose five
extra matchings all have colour-edge counts `(2,2,2)`.  Under the torus
scaling of *any* colour, its output has terms only in degrees

\[
                              0,\quad4,\quad12.            \tag{2}
\]

Thus the low layers `1,2,3` and the reversed top layers `1,...,7` vanish
simultaneously for all three endpoint choices.  Degree four consists of
five distinct singleton genuinely ternary fibres.

This is sharp for a purely coefficient-counting collision.  Assuming exact
binary faces, requiring the low layers through degree `floor(n/3)` for all
three colour scalings is already equivalent to requiring every mixed
coefficient to vanish.  At `n=12`, adding degree four is therefore the full
ternary problem, not a smaller input from which a six-site contraction
follows formally.

## 1. Where a pairwise-Hamilton triple must first fail

Let `P_0,P_1,P_2` be three colour-decorated perfect matchings on `2m` sites,
and suppose every pairwise occurrence union is one alternating Hamilton
cycle.  Put only the unit diagonal colour-`r` cell on every edge of `P_r`.

The standard three-one-factors lemma gives a fourth perfect matching `M` in

\[
                         \Gamma=P_0\cup P_1\cup P_2.      \tag{3}
\]

It cannot use only two factor colours: the union of the corresponding two
factors is a Hamilton cycle and has only its two alternating perfect
matchings.  Hence every nonselected matching in `Gamma` uses all three
colours.

Moreover, its induced vertex colouring determines it uniquely.  At a site
coloured `r`, exactly one occurrence in (3) uses the local colour-`r` port,
namely its incident `P_r` edge.  A compatible matching is therefore forced
at every site.  We obtain the following elementary but useful statement.

**Lemma 1.1 (first singleton layer).**  Every pairwise-Hamilton triple on
`2m>=6` sites has a genuinely ternary singleton fibre.  If an extra matching
`M` has

\[
                         e_r=|M\cap P_r|,                 \tag{4}
\]

then `e_r>=1`, `e_0+e_1+e_2=m`, and the singleton occurs in degree `2e_r`
under colour-`r` torus scaling.  For some choice of scaled colour its degree
is bounded by (1).

This bound uses only the pigeonhole principle after the occurrence-level
uniqueness argument.  It does not say that a preassigned colour has
`e_r=1`.  The path family in
`torus-osculation-top-half-countermodel.md` has such a degree-two singleton;
the example below proves that simultaneous degree two is not forced.

## 2. A balanced twelve-site triple

On sites `0,...,11`, take

\[
\begin{aligned}
P_0={}&01|23|45|67|89|(10,11),\\
P_1={}&(0,11)|12|34|56|78|(9,10),\\
P_2={}&02|17|35|(4,10)|68|(9,11).                        \tag{5}
\end{aligned}
\]

The factors are edge-disjoint.  The complete perfect-matching list of their
union consists of the three rows in (5) and

\[
\begin{aligned}
M_1={}&01|23|(4,10)|56|78|(9,11),\\
M_2={}&02|17|34|56|89|(10,11),\\
M_3={}&(0,11)|12|35|(4,10)|67|89,\\
M_4={}&(0,11)|17|23|45|68|(9,10),\\
M_5={}&(0,11)|17|23|(4,10)|56|89.                        \tag{6}
\end{aligned}
\]

Expanding successively at the lowest unmatched vertex gives exactly these
eight rows; the checker repeats that recursion independently.  Every pair
of factors in (5) is therefore a Hamilton cycle: its union is connected and
the list (5)--(6) contains no other matching using only those two colours.

Each `M_j` uses exactly two edges from each `P_r`.  Its induced colouring has
four sites of each colour, and port uniqueness shows that the five induced
colourings are distinct singleton fibres.  If `E` is the sum of their five
coordinate tensors, the complete unit-weight output is

\[
                            H(q)=X_0+X_1+X_2+E.           \tag{7}
\]

Now scale any fixed colour `r` by `t` at every site and denote the resulting
source by `q_r(t)`.  Since each source cell in this diagonal example has two
equal endpoint colours, (7) becomes exactly

\[
 H(q_r(t))=X_s+X_u+t^{12}X_r+t^4E,
 \qquad\{r,s,u\}=\{0,1,2\}.                              \tag{8}
\]

Equivalently, at the reversed pure endpoint,

\[
 H(c_r+s^2a_r)=X_r+s^8E+s^{12}(X_s+X_u).                \tag{9}
\]

Thus (8) passes the bottom equations in degrees one through three and all
top equations corresponding to original degrees five through eleven.  In
the reversed convention it has contact order eight, two orders beyond the
middle `m=6`.  The sole collision is the five-dimensional coordinate
sector in degree four.

This support has no hidden literal descent.  Its underlying cubic graph is
3-vertex-connected, has no nontrivial tight odd shore, and every six-site
cut has at least four support edges.  No proper six-set is closed under all
three selected factors.  Hence neither an induced six-site restriction nor
a tight-cut contraction explains the degree-four errors.

The model is not a Krenn counterexample: every term of `E` is nonzero.  Its
role is to show exactly how far simultaneous bottom/top osculation can go
before it encounters genuinely ternary information.

## 3. Why the next simultaneous layer is already the full problem

For a tensor `T` on `n` sites, let `T_d^{(r)}` be the sum of its coordinate
components whose words use colour `r` at exactly `d` sites.  These are
direct coordinate subspaces, so `T_d^{(r)}=0` means every such coefficient
is zero.

**Lemma 3.1 (three-colour layer covering).**  Suppose all three principal
binary faces of `T` are diagonal equality.  Then `T` is ternary diagonal
equality if and only if

\[
        T_d^{(r)}=0
        \quad\text{for every }r\in\{0,1,2\}
        \text{ and }1\leq d\leq\left\lfloor\frac n3\right\rfloor, \tag{10}
\]

together with the three normalized constant coefficients.

**Proof.**  Necessity is immediate.  Conversely, a nonconstant word using
only two colours lies in a principal binary face and has coefficient zero.
A word using all three colours has positive colour counts summing to `n`,
so one of them is at most `floor(n/3)`.  Its coefficient belongs to one of
the zero spaces in (10).  Thus every mixed coefficient vanishes. `QED`

At `n=12`, condition (10) ends at degree four.  The model (5) is sharp:
all its genuinely ternary errors have count vector `(4,4,4)`, so no layer
of degree at most three can see them, while degree four sees all five.

This also identifies the logical status of a proposed six-site contraction.
Vanishing strictly below the collision degree does not force one, by
(5)--(9) and the support audits above.  Vanishing through degree four for
all three scalings is, by Lemma 3.1, already the complete twelve-site
ternary realization hypothesis.  Deriving a six-site realization from it
would require a new matching-source contraction theorem; it is not a
consequence of torus-layer coverage.  Using (10) itself as that theorem
would simply restate the original mixed coefficient system.

For one selected matching term, its zero coefficient does force an external
same-colouring mate and an alternating cancellation cycle.  Nothing in the
degree count bounds that cycle by six sites.  This is the same occurrence
versus support distinction as in the selected-triple rewrite: localization
requires a tight interface or another genuine structural input.

The dependency-free audit is
`computations/verify_torus_osculation_bottom_top_collision.py`.  It verifies
the eight-matchings list, all three Hamilton binary faces, the exact degree
spectrum (2) under every colour scaling, 3-vertex-connectivity, absence of
nontrivial tight odd shores, and the lower bound four on every six-site cut.
