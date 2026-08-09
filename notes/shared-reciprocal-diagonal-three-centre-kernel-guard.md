# Diagonal kernel circuits have a simplex form, but genuine triangles exist

## 1. Result

Colour parity and the complete-simplex complex give an exact normal form
for every three-centre kernel relation.  They do **not**, by themselves,
force a two-centre subbridge.

> **Coordinate-line simplex lemma.**  Fix a line `ke_t` at each of three
> sites.  Every relation
>
> \[
> e_t^{(0)}K_0+e_t^{(1)}K_1+e_t^{(2)}K_2=0
> \]
>
> is the boundary of pair tensors `Z_01,Z_02,Z_12`:
>
> \[
> \begin{aligned}
> K_0&=e_t^{(1)}Z_{01}+e_t^{(2)}Z_{02},\\
> K_1&=-e_t^{(0)}Z_{01}+e_t^{(2)}Z_{12},\\
> K_2&=-e_t^{(0)}Z_{02}-e_t^{(1)}Z_{12}.
> \end{aligned}                                           \tag{1}
> \]

For five ternary sites, the three terms, three pair potentials, and one
triangle potential have dimensions and boundary ranks

```text
dimensions: 243, 81, 9
ranks:      171, 72, 9.
```

Thus the first kernel is exactly the edge image and the second kernel is
exactly the triangle image.

There is nevertheless an exact rational colour-diagonal quadratic whose
target-axis columns on sites `0,1,2` form a minimal three-centre circuit,
while the full local image blocks of every proper pair are independent.
Consequently no parity/Koszul argument can replace a large circuit by a
two-centre bridge without using the two known pure cofactor images or an
equivalent extra source equation.

## 2. Why colour parity reduces to coordinate lines

Every four-site matching of a colour-diagonal quadratic has even
multiplicity in each colour.  Inserting local colour `d` moves it into the
parity sector `e_d` in `(Z/2)^3`.  The three inserted-colour sectors are
disjoint.  Hence a kernel row decomposes coefficientwise into three
coordinate-line kernel rows.

If a minimal circuit contributes a target-colour entry to the selected
pure product, its target component is itself a kernel relation.  If this
component had smaller support, it would give an earlier kernel circuit.
Otherwise it has the same support and the simplex lemma applies.  This is
the exact higher-centre extension of the parity split used to straighten a
two-centre bridge; what changes is that the simplex boundary can now have a
genuine triangular cancellation.

## 3. The rational three-centre guard

Use sites `0,...,4`, target colour `2`, and non-target colour `0`.  The only
non-target cell is

```text
q_34(0,0) = 1.
```

The target cells are

```text
q_01=q_02=q_12=1,
q_13=1, q_24=1, q_03=2, q_04=3,
```

and every unlisted cell is zero.  Let `F_x=e_2^(x) K_x`.  Literal matching
expansion gives only two full words on the three active sites:

\[
 \begin{array}{c|cc}
       &22222&22200\\ \hline
 F_0   &1&1\\
 F_1   &2&1\\
 F_2   &3&1.
 \end{array}                                             \tag{2}
\]

Therefore

\[
                         F_0-2F_1+F_2=0.                 \tag{3}
\]

Each pair of columns in (2) is independent.  More strongly, for every
pair among sites `0,1,2`, the six columns obtained by inserting all three
local colours have rank six.  Thus (3) is a minimal three-centre relation
and no arbitrary-vector two-centre subbridge is hidden in a proper subset.

The two scalar provenance equations are transparent.  The non-target
chord sees the target triangle row

\[
                         1-2+1=0,                         \tag{4}
\]

while the all-target hafnians give

\[
                         1-2\cdot2+3=0.                   \tag{5}
\]

Every active cofactor has zero coefficient on a four-word containing no
target colour, as required by isolating a target insertion in a kernel
relation.

## 4. A literal triangular potential

For the all-target word, the three component coefficients of (3) are
`(1,-4,3)`; for the chord word they are `(1,-2,1)`.  Both triples sum to
zero.  In the orientation of (1), the edge flows

```text
word 22222:  z_01=5, z_02=-4, z_12=1,
word 22200:  z_01=3, z_02=-2, z_12=1
```

have precisely those boundaries.  All six edge coefficients are nonzero.
The checker constructs the tensors rather than only checking the two
scalar sums, and verifies that their complete simplex boundary is (3).

This also shows why the phrase “Koszul exactness” does not imply a smaller
kernel relation.  Exactness supplies edge *potentials* for a three-term
relation; an individual edge potential is not a two-term relation between
the original cofactors.

## 5. What extra hypothesis closes the guard

This guard deliberately has no two distinct pure tensors in the cofactor
image.  That is the missing rigidity, not a defect in matching provenance.
Indeed, let `S` be the support of a target-axis circuit with `|S|>=3`.
Looking at a four-word with no target colour isolates each `x in S`, so

\[
                         K_x^{\mathrm{binary}}=0
                         \qquad(x\in S).                 \tag{6}
\]

Only the at most two holes outside `S` can then lift the two non-target
pure tensors.  If both pure tensors exist, decomposing each outside
cofactor by the colour at the other hole forces one cofactor to be pure in
the first colour and the other to be pure in the second.  Nonzero matching
terms in those two cofactors contain disjoint differently-coloured edges;
their unique mixed word contradicts either (6) or one of the two purity
statements.

Thus the counterguard is compatible with—and confirms the need for—the
large-kernel exclusion using both known pure images.  It rules out only the
shorter claim that parity and simplex provenance alone force a two-centre
bridge.

## 6. Reproduction

```sh
python3 computations/verify_shared_reciprocal_diagonal_three_centre_kernel_guard.py
python3 -O computations/verify_shared_reciprocal_diagonal_three_centre_kernel_guard.py
```

The checker pins the two-centre parity theorem, verifies both simplex
complexes and the parity split, reconstructs every matching coefficient in
(2), proves all proper pair-block ranks are six, and checks the displayed
three-edge Koszul boundary.
