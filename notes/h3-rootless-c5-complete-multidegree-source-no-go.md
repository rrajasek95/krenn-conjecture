# The complete full-nine C5 multidegrees have no primitive Tate anchor

Exact bounded membership theorem.  This closes the polynomial full-nine
source-combination question posed by the augmented-pentagon interface.  It
does not exclude a genuinely new higher source-resolution generator and does
not prove Krenn's conjecture.

## Outcome

In each of the five repeated-site \(P_3\sqcup K_2\) fine degrees, enumerate
every literal full-nine output row and every polynomial edge-monomial
multiplier of the complementary degree.  There are exactly

\[
       32\text{ words},\qquad 288\text{ labelled columns}              \tag{1}
\]

per degree.  Every column has at least 42 literal matching monomials owned
by no other column (at least 45 in four of the five degrees).  Hence each
complete one-chart boundary map is injective of rank 288.  The doubled
two-chart kernel consists only of the 288 pairwise chart differences, whose
anchor, target, normalized boundary, and ordinary residue all vanish.

The common degree-five component is also finite and complete:

\[
       32\text{ words},\qquad 4266\text{ labelled columns}.            \tag{2}
\]

Every one of these columns has at least 24 private matching monomials, so
its boundary map is injective of rank 4266.

Multiplication by the natural Tate coefficients

\[
                    ce,\ be,\ bd,\ ad,\ ac                         \tag{3}
\]

maps the five cubic components (1440 columns total) onto 1201 distinct
degree-five row/multiplier labels.  The exact kernel therefore has dimension
239.  It is the direct sum of the coefficient-sum-zero spaces inside the
fibres of this label map.  The owner multiplicities are

\[
 980\times1,\quad205\times2,\quad15\times3,\quad1\times5.             \tag{4}
\]

On pure output rows there are 16 image labels, with multiplicities

\[
                     5\times1,\quad10\times2,\quad1\times5.          \tag{5}
\]

The unique five-owner label is the literal full-cycle multiplier
\(abcde\).  Its five owners are precisely the cycle-supported pure-row
columns in the five cubic degrees.  Thus Tate compatibility imposes

\[
                         \gamma_0+\cdots+\gamma_4=0                  \tag{6}
\]

on the only five columns which could give the normalized pentagon anchor.
More strongly, every vector in the entire 239-dimensional Tate kernel has
coefficient sum zero separately on every pure label.  Therefore

\[
 (\operatorname {ainc},\widehat w,\operatorname {tgt},
   \operatorname {ores})=(0,0,0,0)                                  \tag{7}
\]

on the whole compatible kernel.  In particular it cannot contain the
required \((-1,0,0,0)\).

Allowing an arbitrary polynomial full-nine correction in the complete top
degree does not change the conclusion.  Its boundary map is injective, so
the unique correction cancelling a natural Tate image is its coefficientwise
negative in the free row/multiplier module.  It cancels pure-anchor incidence
and physical target term by term.  There is no hidden top syzygy with which
to alter that readout.

## 1. The five complete cubic components

Use

\[
 (a,b,c,d,e)=(q_{12}^{12},q_{23}^{21},q_{34}^{11},
               q_{45}^{12},q_{15}^{12})
\]

and the five pairs

\[
 (1,3;a,b),\ (3,5;c,d),\ (5,2;e,a),\
 (2,4;b,c),\ (4,1;d,e).                              \tag{8}
\]

For example, the first target degree is
\(\lambda_1+\deg a=\lambda_3+\deg b\).  At the five odd sites it contains
one zero and one selected mixed slot, except that the repeated site contains
two copies of its mixed slot.  A compatible global row chooses one occupied
slot at each physical site, giving \(2^5=32\) words.  The deficit always has
site profile \((2,1,1,1,1)\) and six coloured stubs.  Exhaustively pairing
those stubs without physical loops gives six multipliers for 16 words and
twelve for the other 16:

\[
                         16\cdot6+16\cdot12=288.        \tag{9}
\]

This enumerates polynomial monomials, not only matching multipliers;
repeated cells and repeated physical sites are retained whenever the stub
degree permits them.  Each multiplier is then applied to all 90 surviving
monomials of the direct-free full-nine row.  Literal private monomials prove
the ranks without modular or generic inference.

Each cubic component contains six pure-row multipliers.  Exactly one uses
only the five cycle cells.  In the first component it is \(abd\); the other
four are \(acd,ace,bce,bde\), in cyclic order.  These are the five candidate
primitive anchor columns tested in (6).

## 2. The complete top and the natural Tate map

Adding the corresponding coefficient from (3) puts all five cubic degrees
in one weight-18 fine degree.  The same word-and-coloured-stub construction
gives all 4266 top columns; it is not restricted to images of the cubic
pieces.  The per-word multiplier counts are

\[
 1\times22,\ 5\times40,\ 10\times74,\ 10\times140,
 5\times272,\ 1\times544.                              \tag{10}
\]

The 1440 natural images use 1201 of these columns.  Since multiplication
does not change the output-row label, the map is the literal set map

\[
 (w,m)\longmapsto(w,m\,t_i),                           \tag{11}
\]

where \(t_i\) is the appropriate monomial in (3).  Its kernel is therefore
exactly the sum-zero space on each fibre.  Equations (4)--(6) are a complete
integer description, not merely a rank calculation over a field.

The two-chart presentation introduces no extra source combination.  The
two copies of every global full-nine column are equal, so the complete
kernel is generated by their pairwise differences.  Their labelled pure
targets and anchor incidences cancel with the same sign.

## 3. Exact scope and consequence

The no-go is complete for:

1. all polynomial multiples of all labelled direct-free full-nine rows in
   the five cubic repeated-site degrees;
2. both identical chart copies and all strict chart differences;
3. the natural degree-five Tate multiplication maps; and
4. all polynomial full-nine corrections in the complete common top degree.

It proves that the primitive anchor requested by `5f490c6` is not hidden in
an omitted row or multiplier of those degrees.  It strengthens `752e79f`:
the negative result is no longer based on the one 448-row dark-plane
identity, but on the entire literal multigraded source module.

No localization is needed for this conclusion.  The private pivots have
coefficient one, so the displayed finite boundary maps remain injective
after arbitrary scalar extension or localization.  Likewise the Tate
kernel is an integral coefficient-sum-zero lattice and is unchanged by
base change.  This base-change statement concerns the columns of the two
audited fine degrees.  It does not import new Laurent columns translated
from unaudited higher polynomial degrees; the theorem asked for and proved
here is polynomial source membership in the cubic and natural top degrees.

The result deliberately stops here rather than becoming a global Macaulay
search.  A positive proof still requires a new relative/Tate generator whose
differential is not a polynomial combination of the old full-nine rows and
whose pure-anchor incidence is not accompanied by the same labelled target.

## Verification

Run

```text
python3 computations/verify_h3_rootless_c5_complete_multidegree_source_no_go.py
python3 -O computations/verify_h3_rootless_c5_complete_multidegree_source_no_go.py
```

The checker pins the complete first-fine-degree enumerator, the augmented
pentagon interface, and the previous Tate-anchor obstruction.  It enumerates
all cubic and top words/multipliers, constructs all literal full-nine
boundaries, verifies private-monomial rank certificates, reconstructs the
natural Tate fibre map, and checks the complete pure-label augmentation.
