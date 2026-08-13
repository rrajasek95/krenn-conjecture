# The root-even Eq coefficient is derived-exact but not yet physically dressed

The generic `C_+` orbit needs the reduced-Eq face

\[
 E(H_0-u)e_{\rm Eq},\qquad
 E=2D_{\rm root}\otimes v,quad
 D_{\rm root}=(-1,1,-1,1),\quad
 v={B_1+B_4\over2}.                                  \tag{1}
\]

This note identifies its strongest current construction and the first
complete-source obstruction.  The distinction between labelled residue and
its coarse aggregate is load-bearing.

Checker:
[`verify_h3_cplus_root_even_koszul_physical_dressing_gate.py`](../computations/verify_h3_cplus_root_even_koszul_physical_dressing_gate.py).

## 1. The canonical derived construction is immediate

Put `F=H0-u`.  The canonical relative Koszul class satisfies

\[
                 dC_K=-F e_{\rm Eq}.                  \tag{2}
\]

Therefore

\[
 \boxed{K^{\rm der}_+=-2D_{\rm root}\otimes v\otimes C_K}
 \quad\Longrightarrow\quad
 dK^{\rm der}_+=2D_{\rm root}F e_{\rm Eq}\otimes v. \tag{3}
\]

Thus (1) is not a missing polynomial or conormal identity.  It is an exact
coefficient of the canonical derived intersection.

Equation (3) is not yet a physical source column.  The pinned Koszul/Tate
audit requires a comparison to the complete physical homotopy fibre that
preserves labelled residue, word/fine/repeated grade, private boundary,
anchor/ridge, `W`, terminal data, and physical `q`.

## 2. The nearest physical old-column lift

Retain the four root words separately and, inside each, the six pure labels.
For every word-label vector `u`, the existing cap/response block gives

\[
 O_u=-B_u+\varrho_u,
 \qquad
 (\operatorname{lower},\operatorname{Eq},W,
   \operatorname{target},\operatorname{ores},\operatorname{ainc})(O_u)
 =(-u,-u,0,0,u,\sum u).                               \tag{4}
\]

Take `u=-E`.  Since `sum D_root=0`, (4) becomes

\[
 O_{-E}=(E,E,0,0,-E,0).                              \tag{5}
\]

This is an exact positive result:

- the desired Eq coefficient is obtained;
- `W` and target vanish coefficientwise;
- global anchor incidence vanishes;
- after forgetting the root word, the six-label ordinary residue also
  vanishes.

But the last cancellation is only coarse.  In the complete source-labelled
map the four root-word residue copies are independent, so the residue in
(5) is the nonzero vector `-E`.  This is the same phenomenon as the pinned
rho audit: an odd signed sum can have zero aggregate residue while retaining
a nonzero labelled residue.

## 3. Two primitive physical debts

The desired clean correction has signature

\[
                     (0,E,0,0,0,0).                  \tag{6}
\]

Every old cap/response column in (4) is annihilated, label by label, by

\[
 \lambda_j=\operatorname{lower}_j-\operatorname{Eq}_j,
 \qquad
 \mu_j=-\operatorname{Eq}_j+W_j+\operatorname{target}_j
       -\operatorname{ores}_j.                        \tag{7}
\]

For each of the eight nonzero entries of `E`, both covectors detect (6),
while both vanish on (5).  Hence the nearest physical lift necessarily
carries

\[
             \operatorname{lower/private}=+E,
 \qquad     \operatorname{ores}_{\rm word}=-E.       \tag{8}
\]

No combination of the checked old columns can erase either debt while
retaining the Eq face.  A coarse six-label quotient hides both `E` and
`-E`; that quotient is too small to prove physical source validity.

This also clarifies `W`: it is **not** the first obstruction for the Eq
correction.  It is already zero in (5).  The first obstruction is the
private/labelled augmentation in (8).

## 4. Actual omitted-orbit placement is still separate

The connected local `SL3`/Weyl orbit is a physical way to decorate a
correctly placed source column by the four root words.  It preserves the
matching label and repeated edge.  In the actual tau-plus omitted orbit the
available local source grades span

\[
                     \langle B_0,B_2,B_3,B_5\rangle, \tag{9}
\]

whereas (1) lies in the fixed plane `span(B1,B4)`.  The primitive fixed-plane
dual vanishes on (9) and reads one on `v`.  Therefore root decoration does
not create the missing `B1/B4` placement from the actual repeated-01/04
source grades.

The shortest exact remaining theorem is consequently one of these
equivalent augmented forms:

1. construct a source-labelled `K_Eq` comparison in the actual omitted
   01/04 word/fine/repeated grades with zero private and labelled-residue
   faces; or
2. construct the raw target-bearing `C_+` cell with hidden faces `-E` in
   lower/private and `+E` in word-resolved residue, so that adding (5)
   cancels them.

The canonical derived class (3), root Cartan equivariance, and coarse
residue cancellation do not prove either statement.  Conversely, either
statement would supply exactly the missing physical Eq correction; no
additional `W` repair is required at this stage.

## Scope

This theorem is for generic `beta != 0` and the h=3 `C_+` interface.  It
does not specialize the orbit to `beta=0`, construct `D0`, or compare final
terminal alternatives.  It only isolates the physical augmentation and
placement required by the first generic Eq residual.
