# The five degree-four `h_v` cells are central-`Eq` and dark, not the mixed landing

## Verdict

The five canonical degree-four Koszul-with-`Eq` cells are **not** a physical
unbalanced reduced-`Eq` landing for the missing response-to-cap mapping
cylinder.

Their derived fillers satisfy

\[
 d n_v=h_vYw,qquad
 \operatorname{target}(n_v)=\operatorname{ores}(n_v)=0,              \tag{1}
\]

but projection to the underived physical differential leaves

\[
                         h_v(H_0-u)e_{\rm Eq}.                         \tag{2}
\]

The row `e_Eq` in (2) is the central scalar conormal.  It is not one of the
four operation-corner-resolved reduced-`Eq` occurrence rows seen by

\[
 \Psi_{\rm loc}={1\over12}\sum_{c,m}\delta_c
        (B_{c,m}-Eq_{c,m}),
 \qquad \delta=(1,1,-1,-1).                             \tag{3}
\]

Moreover, the raw reset coefficient has squarefree `2K2` site grade and no
`DQ/PS` operation parent or `A/B` versus `A/C` root label.  The mixed
naturality cell requires repeated `P3+K2` grade and all those labels.  Hence
the strict literal projection of all five cells to (3) is zero.

Even granting the strongest operation-blind placement

\[
              e_{\rm Eq}\longmapsto(1,1,1,1)_{Eq}                    \tag{4}
\]

does not help, because `delta dot (1,1,1,1)=0`.  Granting arbitrary values
in every target, physical-`q`, anchor, `W`, ordinary-residue, ridge, eta and
sigma row also cannot help: `Psi_loc` has coefficient zero on the entire
19-dimensional external augmentation space.

The exact first possible nonzero value after a new corner-resolving lift is

\[
       \boxed{\Psi_{\rm loc}(\operatorname{reset}_v)
              =-{h_v\over4}\,\delta\cdot e_v,}                       \tag{5}
\]

where `e_v` is the not-yet-constructed corner reduced-`Eq` vector.  Thus the
degree-four reset supplies a promising coefficient for the missing
`K_Eq`/cross-word theorem, but does not itself construct or force its
augmentation.

Exact checker:
[`verify_h3_degree4_hv_psiloc_augmented_landing_gate.py`](../computations/verify_h3_degree4_hv_psiloc_augmented_landing_gate.py).

## 1. The five cells

At the mixed internal word `12112`, the five quadratic denominator
hafnians are

\[
\begin{aligned}
h_1&=x_{23}x_{45}+x_{24}x_{35}+x_{25}x_{34},\\
h_2&=x_{13}x_{45}+x_{14}x_{35}+x_{15}x_{34},\\
h_3&=x_{12}x_{45}+x_{14}x_{25}+x_{15}x_{24},\\
h_4&=x_{12}x_{35}+x_{13}x_{25}+x_{15}x_{23},\\
h_5&=x_{12}x_{34}+x_{13}x_{24}+x_{14}x_{23}.
\end{aligned}                                                        \tag{6}
\]

Their fifteen quadratic monomials are pairwise distinct.  The degree-four
mixed/pure Koszul cell is

\[
                    K_m=H_mr_0-(H_0-u)r_m,
             \qquad m=01211222.                                      \tag{7}
\]

The complete derived Hasse totalization cancels every Boolean product-rule
face and produces (1).  This is a genuine positive derived construction.
It is not yet an underived source cell: the q-zero diagonal leaves the monic
commutator `(H0-u)e_Eq`, and the committed audit records

```text
underived_source_descent = false.
```

The q-zero contraction of `h_v` to one therefore does not turn (2) into a
physical primitive landing.  It isolates the precise comparison which is
still missing.

## 2. Literal operation and grade projection

The selected local terminal has four physical parents:

```text
0  DQ[a|b]
1  DQ[b|a]
2  PS[P0,S1]
3  PS[P1,S0].
```

Its only possible primitive cross-profile cells are the four direct-to-PS
incidences.  They are then grouped into the two root-labelled sections
`A/B` and `A/C`.

The reset residual (2) has none of this data:

| datum | reset cell | mixed naturality landing |
|---|---|---|
| full word | `01211222` | `01211222` |
| operation parent | central Hasse/Koszul | one `DQ/PS` corner |
| root label | none | `A/B` or `A/C` |
| raw site grade | squarefree `2K2` | repeated `P3+K2` |
| `Eq` row | scalar central `e_Eq` | corner-resolved `Eq_0,...,Eq_3` |

The equal full word is real, but insufficient.  A source idempotent includes
the operation, root, fine and repeated labels as well.  With those retained,
the Hom block from the reset residual to the selected corner `B/Eq` packet
is zero until a physical `K_Eq` comparison is constructed.

This is stronger than saying that no convenient formula has been found.  It
is the strict typed projection:

```text
Pi_local(reset_v) = 0,   Psi_loc(reset_v) = 0,   v=1,...,5.
```

## 3. Diagonal and tied controls

Suppose one forgets the operation/root labels but retains symmetry.  The
strongest natural placement of the central Eq row is the diagonal (4).
Repeating it over the three matching occurrences gives

\[
 \Psi_{\rm loc}(0,\mathbf1_{Eq})
   =-{3\over12}\delta\cdot\mathbf1=0.                \tag{8}
\]

A tied diagonal placement in both private and `Eq` is likewise zero.  The
checker freezes the controls

```text
literal off-grade zero              Psi_loc =  0
Eq diagonal (1,1,1,1)              Psi_loc =  0
tied B=Eq diagonal                  Psi_loc =  0
Eq-only balanced delta              Psi_loc = -1.
```

Thus the candidate is not secretly bright after operation-blind averaging.
The bright control requires the nonconstant corner vector `delta`, exactly
the datum the missing mixed naturality theorem would have to produce.

For a general corner vector `e=(e0,e1,e2,e3)`, occurrence insertion gives

\[
              \Psi_{\rm loc}(0,e)=-{1\over4}\delta\cdot e.            \tag{9}
\]

Multiplying by the actual reset coefficient yields (5).

## 4. Full augmented external rows

The exhaustive local output contains the 19 external coordinates

```text
target[4], W[4], ores[4],
M, ainc, q, P_f, ridge, eta, sigma.
```

The local rank is `126` in dimension `127` after the entire external basis
has been granted.  The unique terminal (3) is identically zero on all 19
rows.  The checker additionally inserts a vector with an arbitrary nonzero
coefficient in every external row and verifies

```text
Psi_loc(arbitrary external decoration) = 0,
rank(local map + decoration)            = 126.
```

Therefore missing `W`, physical `q`, anchor, labelled residue or ridge data
remain essential to source validity, but none can change the terminal
classification.  Only a corner-resolved private/reduced-`Eq` projection can
make the cell bright.

Equation (1) already proves target and ordinary residue zero in the derived
presentation.  It does not assign the other augmented rows under the missing
underived comparison.  The full external grant shows that this uncertainty
is irrelevant to (3), without pretending that those physical faces have
been constructed.

## 5. Why the five coefficients do not force a primitive landing

The five polynomials (6) form a height-five complete intersection in the ten
internal edge variables.  Their first syzygies are generated by the ten
Koszul relations

\[
                         h_i e_j-h_j e_i.                             \tag{10}
\]

Every coefficient in (10) lies in the ideal `(h1,...,h5)`.  Consequently no
denominator-only combination has a primitive unit face coefficient.

If a future corner-resolving lift assigns `e_v` to face `v`, its five values
are still the polynomial quantities in (5).  The complete-intersection
theorem prevents the five `h_v` alone from forcing these into `1` over the
unlocalized source ring.  Localization at one `h_v` would create a different
branch and does not construct the required global polynomial cell.

The physical cap calculation which reduces five transported faces to one
aggregate uses additional endpoint-odd Cartan paths after a source-valid
`2K2 -> P3+K2` transport.  It cannot be cited before that transport.

## 6. Exact remaining physical theorem

The candidate becomes relevant only through one new physical object:

> Construct a source-labelled `K_Eq(beta)`/cross-word comparison which maps
> the central conormal `e_Eq` into a corner-resolved repeated-grade `Eq`
> packet and totalizes every Hasse product-rule face.

The same object must retain:

- word `01211222` and the incident response-to-cap word arrow;
- the repeated `P3+K2` fine degree;
- the `DQ/PS` parent and `A/B` or `A/C` root label;
- private and reduced-`Eq` matching occurrences;
- target, `W`, physical `q`, anchor and ordinary/labelled residue;
- shifted ridge and `-d(q_xv^01)` connection; and
- eta and sigma.

Once it exists, (5) is the exact test.  A nonzero `delta dot e_v` gives an
unbalanced `Eq` direction, but it remains `h_v`-weighted until the same
source construction supplies a primitive cap landing.  A diagonal or tied
comparison remains dark and preserves the terminal.

The shortest current classification is therefore

```text
derived h_v filler                    CONSTRUCTED
underived physical descent            NOT CONSTRUCTED
literal operation/corner projection   ZERO/OFF-GRADE
operation-blind diagonal placement    PSI_LOC ZERO
external augmented decoration         PSI_LOC ZERO
physical unbalanced Eq landing        NOT CONSTRUCTED
```

## Verification

Run in all three modes:

```text
python3 computations/verify_h3_degree4_hv_psiloc_augmented_landing_gate.py
python3 -O computations/verify_h3_degree4_hv_psiloc_augmented_landing_gate.py
python3 -I -S computations/verify_h3_degree4_hv_psiloc_augmented_landing_gate.py
```

Frozen ledger SHA-256:

```text
c24027f49e9a0ed3b617ad3e8879bb40e8adf39ed8b7a3b13b16a9e550912110
```

## Scope

This is an exact rational projection and augmentation theorem for the five
canonical `h=3` reset cells and the exhaustive four-site local terminal.  It
does not construct the missing underived `K_Eq` comparison, assert a value
for its corner vector, or identify a localized `h_v` inverse with a global
source unit.
