# The four-site source frontier reduces to four DQ/PS gluing types

## Outcome

The local rank-`126/127` theorem turns the named-family audit into an exact
decomposition for the canonical primitive cellular source grammar.

Every selected `h=3` primitive face is in exactly one of three classes:

1. it stays in the four-site response/target/PP/reinsertion operation fan;
2. it is block-diagonal or has the wrong word/fine/repeated grade, hence has
   zero projection to the selected private/reduced-`Eq` rows; or
3. it changes from an ordered `DQ` parent to a `PS` parent and has one of four
   cross-shore types.

The four types are

```text
g_02: DQ[a|b] -> PS[P0,S1]    g_03: DQ[a|b] -> PS[P1,S0]
g_12: DQ[b|a] -> PS[P0,S1]    g_13: DQ[b|a] -> PS[P1,S0].
```

They are the four edges of the formal `K2,2` primitive-`C4` shadow.  The two
face-complete pairings are

```text
tau_a = {g_02,g_13},       tau_b = {g_03,g_12},
```

and after identifying the ordered direct copies they become the two
root-labelled word sections `A/B` and `A/C`.

This gives a finite reduction, but not an unconditional full decorated source
census.  The missing assertion is that every higher source column is a linear
totalization of these primitive one-incidence cells.  No committed source
presentation proves that assertion.  A higher multi-parent generator would
be outside the present decomposition and could carry an independent balanced
private/reduced-`Eq` packet.

Exact checker:
[`verify_h3_four_site_full_source_exhaustiveness_decomposition_gate.py`](../computations/verify_h3_four_site_full_source_exhaustiveness_decomposition_gate.py).

## 1. What rank `126/127` now settles

The four-site local output retains

```text
24  top private/reduced-Eq matching occurrences
36  direction-factor private/reduced-Eq flags
48  tail-PP private/reduced-Eq flags
19  target/q/anchor/W/residue/ridge/eta/sigma coordinates
---
127 coordinates.
```

The projection-complete supermap grants the complete top incidence, every
individual restriction/reinsertion comparison, and the whole external
augmentation space.  Its rank is `126`.  Its unique left kernel is

\[
 \Psi_{\rm loc}={1\over12}
   \sum_{c,m}\delta_c
       \bigl(B_{c,m}^*-\operatorname{Eq}_{c,m}^*\bigr),
 \qquad \delta=(1,1,-1,-1).                           \tag{1}
\]

Therefore every physical four-site response derivative has equal private and
reduced-`Eq` occurrence incidence.  This includes:

- all matching differences and normalized target rows;
- every first-PP restriction and reinsertion;
- the selected six-term `db01` **response derivative**;
- the eighteen direction terms of `dL01`; and
- every tail deletion and all external augmented rows.

All of them have

\[
                       \chi=\delta\cdot(B-Eq)=0.       \tag{2}
\]

This resolves the older `db01` fork only inside the physical response
derivative grammar.  An independently adjoined absolute `db01` carrier is not
a response derivative; it is a cross-block gluing datum and is not classified
by (1).

## 2. Exhausting the operation-parent pairs

Order the selected parents as

```text
0  A_[a|b] = DQ[a|b]       direct shore
1  A_[b|a] = DQ[b|a]       direct shore
2  B       = PS[P0,S1]     endpoint shore
3  C       = PS[P1,S0]     endpoint shore.
```

For one primitive incidence there are only four possibilities.

- The parent is unchanged.  This is local.
- The incidence is `0<->1` or `2<->3`.  It stays on one shore and is generated
  by the tag-preserving action/swap part of the local fan.
- Its word/fine/repeated idempotent is not the selected one.  Its selected
  `B/Eq` projection is zero.
- It joins the two shores.  There are exactly `2*2=4` endpoint types, the four
  `g_ij` above.

These cases are disjoint and exhaustive for a primitive one-incidence cell.
A cellular differential with several faces is a linear sum of its primitive
incidences, so it adds no fifth quotient generator type.

The last sentence is a theorem for the primitive cellular grammar, not yet a
theorem about arbitrary generators in a hypothetical completed source
resolution.  This is the precise boundary between the finite decomposition
and full-source exhaustiveness.

## 3. The four top gluing edges are dark

Before the physical shore gauge a direct-to-endpoint boundary is oriented:

\[
                             e_i-e_j.
\]

Multiplication by the shore sign `diag(1,1,-1,-1)` sends it to the physical
signless incidence

\[
                             u_{ij}=e_i+e_j,
 \qquad i\in\{0,1\},\ j\in\{2,3\}.                  \tag{3}
\]

For all four edges,

\[
                        \delta\cdot u_{ij}=1-1=0.      \tag{4}
\]

Consequently

```text
(B,Eq)=(u_ij,0)      chi=0,
(B,Eq)=(u_ij,u_ij)   chi=0.
```

This matters: merely constructing a physical `DQ<->PS` mate edge does not
fill the balanced quotient.  The four edges have rank three and their
centered cokernel remains `delta`.  A square two-cell can close their edge
cycle but does not automatically cone the vertex `H0` class.

## 4. Word/fine placement leaves two labelled sections

The response and cap objects have words

```text
response  11:110000
cap       01211222.
```

They differ at six augmented sites and in all six selected `P3+K2` fine
degrees.  The cap word is not a vertex of the response `D4` cube.  Hence the
old response and cap inventories are block-diagonal in the relative two-word
quotient.

Rootwise naturality leaves exactly two labelled word arrows:

```text
w_AB  for the A/B return, carrying g_02 and g_12 faces;
w_AC  for the A/C return, carrying g_03 and g_13 faces.
```

The old cross-word rank is zero.  A paired diagonal section has rank one;
the two root-labelled arrows have rank two.  Neither is present in the
committed physical source.

Thus the finite gluing frontier is

```text
four operation mate types
    -> two root-labelled word sections
    -> two root-labelled mixed reduced-Eq naturality cells
    -> two shifted labelled ridges.
```

The shifted ridge rows have zero `B/Eq` projection.  The deciding augmented
step is the mixed reduced-`Eq` naturality lift.

## 5. Exact first unclassified `chi`

Let `kappa_AB` be the first root-labelled mixed naturality lift; the `A/C`
copy is independent.  Its known private top is one of the physical signless
edges `u` in (3).  Write its not-yet-constructed reduced-`Eq` occurrence
vector as

\[
                         e_\kappa=(e_0,e_1,e_2,e_3).   \tag{5}
\]

Then its exact selected projection and scalar are

\[
 \boxed{
  \Pi_{B/Eq}(\kappa)=(u,e_\kappa),\qquad
  \chi(\kappa)=-\delta\cdot e_\kappa,qquad
  \Psi(\kappa)=-{1\over4}\delta\cdot e_\kappa .}    \tag{6}
\]

Equation (6) is exact because the known private edge has zero `delta`
augmentation.  It gives the sharp controls

```text
e_kappa = u          chi =  0   tied/signless lift
e_kappa = delta      chi = -4   normalized Psi = -1
e_kappa = 0          chi =  0   private signless top alone
```

For the physical `z` orientation the two roots have the same sign, so

\[
 \chi(\kappa_{AB}+\kappa_{AC})
       =\chi(\kappa_{AB})+\chi(\kappa_{AC}).           \tag{7}
\]

They cannot cancel merely by forgetting the root label.

There is no justified numeric value for (6) today.  The committed source
constructs neither word section nor the mixed reduced-`Eq` occurrence map.
Declaring zero assumes the desired tied naturality theorem; declaring a
nonzero number assumes the desired bright filler.  The exact current verdict
is therefore a symbolic scalar, not `0` and not `4`.

## 6. Resulting proof fork

Under the primitive-cell census hypothesis, the full selected terminal test
has only two remaining scalars:

```text
chi(kappa_AB)=chi(kappa_AC)=0
    -> every primitive full-source column is killed by Psi;

one scalar is nonzero
    -> the unique B/Eq quotient is filled projection-wise;
       repair that same cell's remaining word/q/anchor/W/ridge faces.
```

Without the census hypothesis there is one additional terminal alternative:
a higher multi-parent source generator, not decomposable into primitive
incidences, may carry a balanced `B/Eq` packet.  Proving that no such column
exists is the exact global exhaustiveness theorem still missing.

## Scope

This is an exact canonical `h=3` theorem over the rationals for:

- the complete four-site local response/target/PP/reinsertion category;
- the partition of primitive operation-parent incidences;
- the four formal `DQ/PS` mate types and two root-labelled word sections; and
- the deciding private-minus-`Eq` formula on the first mixed lift.

It is not an unconditional construction of the full decorated source
resolution.  The missing global input is precisely the primitive-cell census
or an explicit list of its higher generators.

Run:

```text
python3 computations/verify_h3_four_site_full_source_exhaustiveness_decomposition_gate.py
python3 -O computations/verify_h3_four_site_full_source_exhaustiveness_decomposition_gate.py
python3 -I -S computations/verify_h3_four_site_full_source_exhaustiveness_decomposition_gate.py
```

Frozen ledger SHA-256:

```text
596c31bc593ac6ce36ab629f4e68b81658e432f66de434ed9913c208aff07440
```
