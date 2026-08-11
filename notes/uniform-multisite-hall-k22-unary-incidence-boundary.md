# Unary incidence repairs goodness but leaves a double-flat `K2,2` shore

## Result

The unary follow-up to the strict Hall `K2,2` reduction is exact.

In the opposite orientation, retain both disjoint core matchings in each
diagonal hole family.  The natural overlaps on either shore are already
support-active and have all four deleted-star ranks equal to three.  The
second core matching restores the same-colour column lost when a selected
arm is cut; the other diagonal target supplies the other nonzero colour;
the direct pure-zero matching supplies colour zero.

Their two physical four-cycle minors are

\[
 \kappa_A=a_0d_3-d_0a_3,qquad
 \kappa_B=b_1c_2-c_1b_2.                               \tag{1}
\]

If either is nonzero, the strict rectangle reaches the active four-good,
nonflat overlap interface.  If both vanish, the two endpoint vectors are
proportional on each shore.  The complete crossed rows then expose the
exact unary obstruction: absent a cancellation mate in the same literal
word grade, they force

\[
                         H_{03}=H_{12}=0,              \tag{2}
\]

where `H_uv` is the pure-zero two-cofactor after deleting the shore edge
`uv`.  Equation (2) is compatible with the genuine unary top
`q^[3]=X0`.  Hence the unary row repairs goodness but does not by itself
kill the double-flat shore lock.

Checker:
`computations/verify_uniform_multisite_hall_k22_unary_incidence_boundary.py`.

## 1. The rank repair is intrinsic to the strict core

Use outer endpoints `P=6,S=7` and the five selected pure matchings

```text
Q0 : PS | 01 | 24 | 35,
Q1 : P0 | S1 | 23 | 45,     P3 | S2 | 01 | 45,
Q2 : P2 | S0 | 13 | 45,     P1 | S3 | 02 | 45.
```

For the natural shore-`A` overlap `P0,S0`, cutting `P0` loses the first
`Q1` column.  The second `Q1` matching supplies colour 1 through `P3` at
`P` and through its residual `01` edge at site `0`; `Q2` supplies colour
2 and `Q0` colour 0.  The same argument at `S0`, and on shore `B`, gives

```text
P0,S0 : (3,3,3,3),        P1,S1 : (3,3,3,3).          (3)
```

Each arm lies in a selected nonzero diagonal-target monomial, so its
deleted cofactor is nonzero.  Thus these are support-active good overlaps,
not the rank-two selected-packet boundary obtained by retaining only one
core edge per colour.

At the opposite core site, the four selected axis cells form the physical
minor (1).  Nonzero `kappa_A` or `kappa_B` therefore supplies exactly the
nonflat transition datum required at the curved-good interface.  This is a
landing statement; it does not claim the downstream curved-overlap theorem
has been reproved here.

## 2. The literal crossed rows

On shore `A={0,3}`, the selected `p1,s2` components produce four distinct
axis words.  Two of their coefficients are

\[
 a_0d_3H_{03},qquad a_3d_0H_{03}.                    \tag{4}
\]

On shore `B={1,2}`, the other two are

\[
 b_1c_2H_{12},qquad b_2c_1H_{12}.                    \tag{5}
\]

All eight core coefficients are nonzero in the strict family.  Therefore,
if no other source term enters the same output word, the crossed zero rows
force (2).  A same-word cancellation mate is not silently discarded: it
is precisely the next full-source branch and must be routed through a free
carrier, lock kernel, or selected-anchor correction.

This corrects a tempting but invalid simplification.  The two orientations
`03` and `30` occupy different residual output words on the axis chart;
they do **not** cancel as a two-term scalar row.

## 3. Unary top does not forbid the dark cofactors

The pure-zero residual support

```text
01, 24, 35
```

has exactly one perfect matching, so `q^[3]=1`.  After deleting `03`, the
remaining vertices are `1,2,4,5` and have no perfect matching.  After
deleting `12`, the remaining vertices are `0,3,4,5` and likewise have no
perfect matching.  Thus

```text
q^[3]=1,       H03=0,       H12=0.                    (6)
```

This is an exact common-`q` incidence guard, not a formal independent
assignment of cofactors.  It does not satisfy every full one-bad row, so it
is not a source counterexample.  It proves that Euler expansion of the
unary top alone cannot close (2).

## 4. Sharp remaining packet

The opposite strict rectangle is now reduced to:

1. a same-word cancellation mate leaves the selected-axis chart and must
   route to the already isolated free-carrier/lock mechanisms;
2. `kappa_A != 0` or `kappa_B != 0` lands on the active four-good curved
   interface; or
3. both shore vectors are proportional and the pure-zero two-cofactors
   `H03,H12` vanish.

The third case is the exact unary incidence obstruction.  The next row
must couple the unary matching used in (6) to one of the two shore
cofactors, or show that a cancellation mate necessarily creates a free
active carrier.  No further hole-family or support enumeration is needed
before that identity is found.

## Verification

Run

```text
python3 computations/verify_uniform_multisite_hall_k22_unary_incidence_boundary.py
python3 -O computations/verify_uniform_multisite_hall_k22_unary_incidence_boundary.py
python3 -I -S computations/verify_uniform_multisite_hall_k22_unary_incidence_boundary.py
```

Frozen ledger SHA-256:

```text
3b9bac27ddafe82e3fd315beb1307fa6144d4f7de0a7db2e5eb4dbbe8120e58c
```
