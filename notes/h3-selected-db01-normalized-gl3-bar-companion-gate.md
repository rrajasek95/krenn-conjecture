# The normalized all-D endpoint is not the selected `db01` companion

## Result

The normalized local-`GL3` bar does not construct the first selected
six-term face isolated by `1cc1f81`, even when its all-D endpoint is retained
as a principal companion rather than killed.

There is a real near-hit.  On the only compatible four-site face—deletion
`v=1`, residual sites `2,3,4,5`—the all-D endpoint and

\[
 b_{01}=p_0s_1(q_{23}^{00}q_{45}^{00}
              +q_{24}^{00}q_{35}^{00}
              +q_{25}^{00}q_{34}^{00})
\]

have the same three uncoloured K4 matching shapes after granting the all-D
endpoint the multiplier `p0*s1`.  But that agreement forgets exactly the
load-bearing data.  The all-D terms have face tag `2112`, pure-output tag
`Y00000`, and horizontal bar degree zero.  The selected `b01` terms have
pure `q:00` colours in response head/word `11:110000`.  Its first physical
principal-parts face is the six-term one-form

\[
 db_{01}=p_0s_1\sum_{ab|cd}
              (dq_{ab}^{00}q_{cd}^{00}+q_{ab}^{00}dq_{cd}^{00}). \tag{1}
\]

Thus squarefreeness and coarse matching shape agree, but fine colour,
source/output role, and vertical PP degree do not.

Checker:

```text
computations/verify_h3_selected_db01_normalized_gl3_bar_companion_gate.py
```

Frozen ledger digest:

```text
7f8fd35050f39a56dad2b3562d0b06e1e1fa3bbb0d60e4b2cd66a62439c1679c
```

## The exact face comparison

For face tag `2112`, the all-D matching coefficients are

```text
q23:21 q45:12,
q24:21 q35:12,
q25:22 q34:11.
```

Even after adjoining `p0*s1`, this support is disjoint from the three pure
`q:00` monomials of `b01`.  Erasing every colour suffix maps both triples to
the same uncoloured perfect matchings.  That erasure is not a morphism of the
word/fine complex and also drops the pure-output basis tag.  It explains why
the normalized bar looks coefficientwise promising without giving a
physical source map.

Taking first principal parts makes the mismatch sharper: (1) has six
distinct `dq`-labelled terms, while the all-D endpoint has three degree-zero
terms and no `dq` label.  Applying the normalized bar to (1) would give

\[
 d_{bar}H(db_{01})=L(db_{01})-D(db_{01}),              \tag{2}
\]

not a boundary equal to `db01`.  Horizontal bar degree and vertical PP
degree are independent.

## Retaining a companion does not identify the companion

The presentation-safe selected graph has

\[
 z_{01}-b_{01}=0,
 \qquad d z_{01}-d b_{01}                              \tag{3}
\]

as its first PP column.  In coordinates

```text
(db01, dz01, all-D output endpoint),
```

the literal graph column, retained bar endpoint, and desired selected face
are

```text
(-1,+1,0), (0,0,+1), (+1,0,0).
```

The first two have rank two and adjoining the desired face raises rank to
three.  The primitive covector `(1,1,0)` kills both available objects and
reads one on `db01`.

This is the precise effect of retaining the principal companion: it removes
the demand that a *correctly typed* companion vanish.  It does not permit an
all-D output endpoint to be renamed `dz01-db01`.  A two-cell identifying
those objects would be exactly the source-labelled selected comparison that
the construction is trying to prove.

The fibre-preserving centered presentation gives the same rank test.  In
coordinates `(db01, sum of the other 29 PP fibres, all-D)`, the complete
response face and retained bar endpoint are `(1,1,0)` and `(0,0,1)`.
The desired selected face `(1,0,0)` raises rank from two to three and is
detected by `(1,-1,0)`.  What would split it is the genuine centered face

```text
dc01=(29,-1,0),  db01=(dR+dc01)/30,
```

not all-D.  Hence the obstruction applies equally to the graph-coordinate
and centered-section formulations.

The augmentation statement is consistent with this obstruction.  The
normalized bar assigns augmentation one to all-D and all-L and zero to bar
edges.  The PP zero section kills `db01` and `dz01`.  These are maps on
different summands; equating them would silently collapse the output and
cotangent presentations.

## Frontier and scope

The first missing proper face remains a literal selected `db01`/graph PP
cell at canonical grade `g`.  D4 and the cap grade
`01211222 / P3+K2` occur only after that face and were not used to manufacture
membership here.  Once a genuine selected cell is supplied, the previously
isolated D4/cap/Cartan attachment is still the next face.

This is a sharp obstruction to reusing the standard normalized bar.  It is
not a no-go for an enlarged Spencer/bar totalization carrying a new vertical
comparison between the all-D output and the selected response graph.

Run normally, optimized, and isolated/no-site.  Expected output:

```text
all-D vs b01: COARSE 3-MATCHING NEAR-HIT ONLY
all-D vs db01/graph PP face: LITERAL NO
first obstruction: fine colour + module role + vertical PP degree
D4/cap grade: NOT INVOKED BEFORE FIRST FACE
```
