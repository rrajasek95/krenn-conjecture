# The local `U_C4` terminal embeds globally; one cross-grade orbit remains untyped

## Result

The exhaustive four-site functional of `020277c` embeds literally into the
canonical `h=3` fixed-window plus cap map.  On the raw three-matching cap
coordinates it is

\[
 \Psi_{\rm loc}={1\over12}
  \sum_{c,m}\delta_c(B_{c,m}-Eq_{c,m}),
 \qquad \delta=(1,1,-1,-1).                         \tag{1}
\]

Repeating each aggregated cap coordinate on all three `C4` occurrences
pulls (1) back to

\[
                    {1\over4}\delta\cdot(B-Eq),      \tag{2}
\]

the canonical terminal of the maximal named `h=3` cap packet.  This identity
holds on all 27 cap basis vectors, not only after projection to the eight
`B/Eq` rows.  Lifting all 25 named cap columns leaves the exhaustive local
rank equal to `126` in dimension `127`.

All collision/PP companions are **not** yet proved to preserve `B=Eq`.
Every currently typed companion does preserve the terminal, but the selected
`db01` comparison, the eighteen `dL01` placements, and the mixed
response-to-`AugP2` incidence have no constructed `B/Eq` projection.

The smallest explicit hypothesis promoting the local terminal is therefore

> For every column `g` in the one missing response-to-`AugP2`
> mapping-cylinder boundary orbit,
> \(\Psi_{\rm loc}(\pi_{\rm loc}g)=0\).

Since the local map has image exactly `ker(Psi_loc)`, this is equivalently a
factorization of every such local projection through the already exhaustive
four-site boundary map.  Under this one hypothesis, extend `Psi_loc` by zero
on every off-grade response, collision, and PP block.  The result is the
global terminal.  A first nonzero value instead identifies the physical
rank-raising exit.

Exact checker:
[`verify_h3_uc4_local_terminal_global_gluing_criterion.py`](../computations/verify_h3_uc4_local_terminal_global_gluing_criterion.py).

## 1. Canonical cap embedding

The local output has

```text
24  top B/Eq occurrences
36  direction B/Eq flags
48  tail-PP B/Eq flags
19  target/q/anchor/W/ores/ridge/eta/sigma rows
---
127 coordinates.
```

The canonical named cap output has 27 coordinates:

```text
B[4], Eq[4], target[4], W[4], ores[4],
M, ainc, q, P_f, ridge, eta, sigma.
```

Define the insertion `J` by

\[
 J(B_c)=\sum_{m=1}^3B_{c,m},\qquad
 J(Eq_c)=\sum_{m=1}^3Eq_{c,m},                       \tag{3}
\]

and map every external augmentation coordinate identically.  Then

\[
          \Psi_{\rm loc}\circ J
            ={1\over4}\delta\cdot(B-Eq).             \tag{4}
\]

The checker verifies (4) on the 27 standard basis vectors.  Thus there is no
normalization ambiguity between the raw three-occurrence theorem and the
aggregated cap theorem.

The local supermap has rank `126`.  Every named cap column is killed by
(4), and adjoining their lifts leaves rank `126`.  Because the local image
has codimension one, this also proves that every named lifted cap column is
already in the local boundary image.

## 2. Fixed-window normalization and the tied-lift failure

On the fixed window `2345`, put

\[
 A=Dq_{01}H,\qquad B=p_0s_1H,\qquad C=p_1s_0H,
 \qquad L=(2,-1,-1),                                 \tag{5}
\]

with `H=q23q45+q24q35+q25q34`.  Normalize the fixed-window detector so
that it reads one on `L H`.  Its values are

```text
L H                               1
18 endpoint/direction terms       2
```

The local functional has exactly the matching private-only values:

```text
balanced private top              1
private direction packet          2
```

Consequently a comparison boundary

\[
                  x_{\rm window}-y_{\rm local}       \tag{6}
\]

is killed for the top and direction packets if `y_local` is private-only.
The values are `1-1=0` and `2-2=0`.

The physical four-site response does not give that placement.  Its lift is
tied:

\[
                  (B,Eq)=(\delta,\delta),             \tag{7}
\]

and its product-rule direction packet is tied termwise.  Formula (1) reads
zero on both.  Hence the corresponding comparison debts are

```text
L H minus tied top                1
18 directions minus tied packet  2.
```

This is the precise reason that a perfect normalized h2 response still does
not glue the fixed-window obstruction into an absolute cap.  The missing
mixed incidence must be private/`Eq`-unequal.

This comparison statement is distinct from the terminal extension.  For a
pointed comparison joining the two nonzero block detectors, (6) must have
equal normalized values.  For the terminal obtained by extending
`Psi_loc` by zero off-grade, every new local projection must instead have
value zero.

## 3. Which collision and PP families are already dark

The following families have now been checked against (1).

| family | local `B/Eq` status | `Psi_loc` |
|---|---|---:|
| 121 named response/intermediate columns before gluing | different literal grade, zero projection | 0 |
| 24 internal chart/root switches | signless cross-shore edge | 0 |
| 24 shore-gauged one-hole/collision repairs | the same signless edge | 0 |
| symmetric collision top and typed first-PP flags | collision/vertical direct summands | 0 in the current direct sum |
| 30 distinct `C2+/C4/P2` packets | old, centered, or outside selected block | 0 |
| 18 local h2 direction flags | tied `B=Eq` | 0 |
| 24 local tail PP flags | tied `B=Eq` | 0 |
| named target, `q`, anchor, `W`, residue, ridge, eta, sigma | external rows | 0 |

The collision conclusion is deliberately limited.  “Zero in the current
direct sum” does not construct a physical cross-grade comparison.  It says
that the family is dark until such a comparison is added.

In particular, an absolute one-hole landing can close its local first-PP
anti-diagonal without filling the global balanced quotient.  After the
physical shore gauge its oriented `e_A-e_endpoint` face becomes the
signless `e_A+e_endpoint` edge, which (1) kills.

## 4. Exact global families not covered

The present source still lacks the following linked data.

1. Both operation-profile-changing fixed-window families

   ```text
   (A+B)H_2345,  (A+C)H_2345,
   ```

   and their `H-r` restriction/reinsertion companions.  A single switch is
   insufficient; both fill the fixed-window `L` quotient coefficientwise.

2. The selected six-term `db01` private/`Eq` comparison.  Its deciding
   scalar

   \[
       m_{db01}=\delta\cdot(B-Eq)(\Pi_{B/Eq}(db01))   \tag{8}
   \]

   remains uncomputed.  The normalized all-`D` endpoint is a different
   vertical/horizontal summand and does not determine (8).

3. The eighteen endpoint/direction placements of `dL01`, with primitive
   profile

   ```text
   (2,2,-1,-1,-1,-1).
   ```

4. The word/fine diagonal

   ```text
   11:110000  ->  01211222.
   ```

   The words differ at six augmented sites, all six selected `P3+K2` fine
   degrees change, and the cap word is not in the existing response `D4`
   cube.

5. The primitive mixed private/reduced-`Eq` mapping-square incidence after
   that word arrow.  This is the first independent post-word row and the
   only part of the missing family that can change (1).

6. The whole boundary orbit of the same physical source cell: six selected
   `P3+K2` faces, six sibling `3K2` faces, reduced-`Eq` cap-label descent,
   and the shifted

   \[
                     \gamma=-d\Omega,
            \qquad -d(q_{xv}^{01})                   \tag{9}
   \]

   ridge connection.

7. Downstream, the word-`0102` occurrence-local private section and its
   `dq23` reinsertion with physical `q`, `W`, and labelled-ridge readouts.

Items 2--6 are not independent arbitrary guesses: they are the faces of the
one missing response-to-`AugP2` relative PP mapping-cylinder/Tate family.
Item 7 is its required downstream labelled descent.  No current theorem
identifies these rows with the already dark companions.

## 5. Smallest gluing hypothesis

Let `G_cross` be precisely the omitted physical mapping-cylinder boundary
orbit above, including its downstream restriction/reinsertion faces.  For a
column `g` define

\[
 \chi(g)={1\over12}\sum_{c,m}\delta_c
       \bigl(B_{c,m}(g)-Eq_{c,m}(g)\bigr).            \tag{10}
\]

The required hypothesis is

\[
                         \chi(g)=0
             \qquad\hbox{for every }g\in G_{cross}.  \tag{11}
\]

No target, `q`, anchor, `W`, ordinary-residue, or ridge coefficient appears
in (10).  Those rows have already been granted completely in the local
supermap.

Because the local map has rank `126/127`, (11) is equivalent to

\[
            \pi_{\rm loc}(G_{cross})
                    \subseteq\operatorname{im}(d_{\rm loc}).           \tag{12}
\]

Thus (11) is not merely necessary.  It is sufficient for the zero extension
of `Psi_loc` to kill the exhaustive global map.  Conversely, the first
column with `chi != 0` fills the unique local quotient projection-wise and
is the exact physical exit whose remaining faces must be repaired.

The sharp current answer is therefore:

```text
canonical cap embedding                 CONSTRUCTED
all typed collision/PP companions       B-Eq DARK
all physical collision/PP companions    NOT YET CLASSIFIED
one missing cross-grade orbit has chi=0 SMALLEST TERMINAL HYPOTHESIS
one member has chi!=0                   PHYSICAL FILLER/EXIT ARM
```

## Verification

Run in normal, optimized, and isolated/no-site modes:

```text
python3 computations/verify_h3_uc4_local_terminal_global_gluing_criterion.py
python3 -O computations/verify_h3_uc4_local_terminal_global_gluing_criterion.py
python3 -I -S computations/verify_h3_uc4_local_terminal_global_gluing_criterion.py
```

Frozen ledger SHA-256:

```text
6da9fe6018feadabdc78a42b36223b7e0c176a31729f0e917c1b5599a628155e
```

## Scope

This is an exact rational embedding, normalization, rank, and finite-family
criterion for canonical `h=3`.  It does not construct the missing
response-to-cap mapping cylinder, assert that its private/`Eq` incidence is
tied, or call the word-`0102` occurrence detector an accepted terminal
before its augmented readouts exist.
