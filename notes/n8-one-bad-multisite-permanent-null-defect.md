# The exact multisite defect of the one-bad permanent-null cap

## Outcome

The direct cap from `7ccff7c` has a complete closed-form extension to
arbitrary multisite stars, but its higher defect does not vanish formally.
Write

\[
 a=p_1,\quad b=p_2,\quad c=s_1,\quad d=s_2,
 \qquad R=ac+ad-bc+bd.
\]

The coefficient matrix is

\[
 K=\begin{pmatrix}1&1\\-1&1\end{pmatrix},
 \qquad \operatorname{perm}K=0,
\]

and

\[
                         R=a(c+d)+b(d-c).                 \tag{1}
\]

In the site-square-zero source algebra the full repeated-row/column defect is

\[
 \boxed{
 R^{[2]}={1\over2}a^2(c+d)^2+ab(d^2-c^2)
             +{1\over2}b^2(d-c)^2 .}                    \tag{2}
\]

The coefficient of `abcd` is zero: this is exactly the permanent
cancellation.  Every one of the eight surviving monomial classes in (2)
repeats a row label or a column label.  The cubic term is

\[
 \boxed{
 \begin{aligned}
 R^{[3]}={}&{1\over6}a^3(c+d)^3
 +{1\over2}a^2b(c+d)^2(d-c)\\
 &+{1\over2}ab^2(c+d)(d-c)^2
 +{1\over6}b^3(d-c)^3 .
 \end{aligned}}                                         \tag{3}
\]

Consequently the complete cap identity under the four response equations is

\[
 (q+R)^{[3]}=X_0+X_1+X_2+
                 \underbrace{R^{[2]}q+R^{[3]}}_{\text{multisite defect}}.
                                                               \tag{4}
\]

Equations (2)--(3) sharpen the fixed-port hypothesis of `7ccff7c`.  It is
enough that

\[
 p_1^{[2]}=p_2^{[2]}=s_1^{[2]}=s_2^{[2]}=0.             \tag{5}
\]

For a global one-form in the site-square-zero algebra, its square vanishes
exactly when it is supported at at most one physical site.  The four sites
need not be distinct: a collision kills additional products.  The nonzero
diagonal responses already force the `p_i` and `s_i` support sites to differ
for each `i`.  Thus the clean concentration target is four square-zero star
rows, not four preassigned distinct literal ports.  For arbitrary endpoint
stars, permanent zero by itself gives no further cancellation.

## An exact common-provenance response guard

There is a smallest useful source-row guard to any argument which attempts
to kill (2) using only the complete response tensor and the two-star
dependent-line theorem.  On sites `0,...,5`, take

```text
q = 24:11 + 35:11 + 05:22 + 14:22,

a=p1 = e1@0 + e1@5,       b=p2 = e2@2,
c=s1 = e1@1,              d=s2 = e2@3.
```

Literal perfect-matching expansion gives all four binary response rows:

\[
 acq^{[2]}=X_1,\qquad adq^{[2]}=0,
 \qquad bcq^{[2]}=0,\qquad bdq^{[2]}=X_2.              \tag{6}
\]

Thus `Rq^[2]=X1+X2`.  Sorting the full top expansion by insertion count gives

```text
q^[3]       = 0,
R q^[2]     = X1 + X2,
R^[2] q     = 2 * [111211],
R^[3]       = 0.
```

The coefficient `2` is a literal sum of two source matchings, not an
output-only artifact.  The packet also realizes the two-star conclusion:
the `p` pair has target-line sites of colours `1` and `2`, and so does the
`s` pair.  Those line sites do not annihilate the repeated `p1` term.

## The defect is not automatically the curved doubly-good gate

Adjoin deleted endpoints `P,Q` and regard `a,b` as the `P` star and `c,d`
as the `Q` star.  The same literal cells define an eight-site partial source
whose complete tensor is exactly

\[
                              X_1+X_2.                  \tag{7}
\]

Thus this is a source-faithful incidence test, although it still lacks the
one-bad `X0` anchor.  The five physical star arms have activity

```text
P0  active       P5  inactive       P2  active
Q1  active       Q3  active.
```

Their two endpoint deleted-star ranks are respectively

```text
P0: (2,1)    P5: (2,2)    P2: (1,1)
Q1: (1,1)    Q3: (1,1).
```

In particular, none is a doubly-good `(3,3)` arm.  More sharply, the two
literal source matchings contributing `2*[111211]` are

```text
(P0,Q1),(P5,Q3),q24,
(P0,Q3),(P5,Q1),q24.
```

Both use the inactive arm `P5`; the shared `P0/P5` fan is the flat common
factor `E11/E11`.  Therefore a nonzero second fundamental form of the
response plane is **not**, without further hypotheses, the curved
doubly-good/other-ruling OO gate.  Activity and goodness are exactly the
missing upgrade.

## Why this does not defeat minimum support

The extra component `e1@5` of `p1` is invisible in every row of (5).
Deleting it preserves all four responses and removes `R^[2]q`.  Hence this
guard is excluded by a genuine minimum-entry normalization.  It proves two
precise negative statements, and no more:

1. the full response equations plus the two-star dependent-line conclusion
   do not formally kill the multisite cap defect;
2. maximum-anchor/minimum-support is load-bearing, rather than cosmetic, in
   any concentration argument.

It does **not** satisfy the unary equation `q^[3]=X0`, is not a full one-bad
packet, and is not a Krenn counterexample.  The exact theorem gap is now
narrower: prove that every minimum-support full one-bad packet has the four
self-square identities (5), or show that a coupled nonzero self-square
contains active doubly-good arms and forces the adjacent-cubic/curved-overlap
descent.
Neither conclusion follows from the current two-star theorem, which only
locates dependent target lines and does not identify them with all support
of the global stars.

## Reproduction

```sh
uv run python computations/verify_n8_one_bad_multisite_permanent_null_defect.py
PYTHONOPTIMIZE=1 uv run python computations/verify_n8_one_bad_multisite_permanent_null_defect.py
```

The checker verifies (2)--(3) as formal rational polynomial identities,
reconstructs every decorated source matching in (5), separates the four cap
sectors, audits the minimum-support deletion, and pins the fixed-port theorem
and the two-star/channel-synchronization inputs.
