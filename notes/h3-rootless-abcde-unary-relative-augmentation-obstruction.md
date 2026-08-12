# The literal (abcde) unary column has the wrong target/anchor readout

## Exact source occurrence

Put

\[
 (a,b,c,d,e)=(q_{12}^{12},q_{23}^{21},q_{34}^{11},
               q_{45}^{12},q_{15}^{12}).
\]

The monomial (abcde) exists in the complete source inventory, but it is
not a literal hafnian matching coefficient.  Its physical site profile is

\[
                         (0,2,2,2,2,2,0,0),             \tag{1}
\]

so it repeats every odd site.  Its actual source label is the pure unary
full-nine row (0^8), multiplied by the polynomial monomial (abcde).
On the normalized (C_5) torus its coefficient is one, but (1), the source
row label, and all physical readouts remain present.

The complete degree-five enumeration contains 4,266 labelled full-nine
columns and has rank 4,266.  The full-cycle pure label has exactly five
owners, one from each cubic (P_3\sqcup K_2) component.  Natural Tate
compatibility on those owners is

\[
                         \gamma_0+\cdots+\gamma_4=0.   \tag{2}
\]

Thus every compatible Schur/(C_5)/Tate relation has zero coefficient on
the primitive pure label after summing its owners.  An arbitrary top
full-nine correction is unique by injectivity and cancels its source label,
anchor incidence, and target term by term.

## First readout obstruction

Retain a row for the lower presentation label (abcde), and order the
coarse rows as

\[
       (\operatorname{low}_{abcde},\operatorname{ainc},W,
          \operatorname{tgt},\operatorname{ores}).
\]

After suppressing the common unit (abcde), the literal pure unary column
is

\[
                         R=(1,-1,0,1,0).                \tag{3}
\]

The desired relative lower augmentation from the matching-cell gate is

\[
                         U=(1,0,0,0,0).                 \tag{4}
\]

The old target cap and split-residue columns are

\[
             T=(0,0,-Y,1,0),\qquad
             \rho=(0,0,1,0,1).                        \tag{5}
\]

The primitive covector

\[
                 \boxed{\operatorname{low}_{abcde}
                         +\operatorname{ainc}}          \tag{6}
\]

kills (3), both columns in (5), every chart difference, and every compatible
Tate/top correction, but takes value one on (4).  Hence cancelling the
target in (3) with the cap cannot help: the anchor incidence remains
(-1).  Cancelling that incidence with another pure-row column also
cancels the same injective lower source label.

This is the first exact readout obstruction to constructing (U) from the
existing direct unary normalization.  The equality (abcde=1) on the
torus is only coefficient localization; it does not turn (3) into (4).

## Consequence and scope

The cyclic comparison package therefore needs a genuinely relative
degree-(abcde) lower face with nonzero presentation augmentation and

\[
             (\operatorname{ainc},W,
                \operatorname{tgt},\operatorname{ores})=(0,0,0,0).
\]

No literal unary/Schur/(C_5)/Tate column in the complete audited top
degree has this signature.  This is a complete no-go for that polynomial
source module and old cap block, not for a newly adjoined relative source
generator.

Run:

```text
python3 computations/verify_h3_rootless_abcde_unary_relative_augmentation_obstruction.py
python3 -O computations/verify_h3_rootless_abcde_unary_relative_augmentation_obstruction.py
python3 -I -S computations/verify_h3_rootless_abcde_unary_relative_augmentation_obstruction.py
```

Frozen ledger SHA-256:

```text
d5c72fa4a62fbfd224b0c33bc557dd0c83d04f15e1b23a9bb329ec301e669c00
```
