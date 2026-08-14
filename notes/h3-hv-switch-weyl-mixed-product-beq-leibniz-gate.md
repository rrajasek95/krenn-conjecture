# The reset--switch product has a bright shadow but no physical corner column

## Outcome

Combining the five central degree-four reset cells with the source-provenant
switch--Weyl carrier reveals a genuine coefficient-level effect which neither
factorwise darkness audit sees.  In the three-chart basis

```text
A = direct DQ chart,  B = PS01,  C = PS10,
```

the retained switch is

\[
                       T=(-2,1,1).                    \tag{1}
\]

The normalized even split of the aggregate direct chart into the two
oriented DQ corners is

\[
 J(a,b,c)=(a/2,a/2,b,c).                              \tag{2}
\]

For `delta=(1,1,-1,-1)`, equations (1)--(2) give

\[
                         J(T)=-\delta.                 \tag{3}
\]

Therefore an Eq-only placement of the central reset conormal, decorated by
`T`, would be bright:

\[
 \Psi_{\rm loc}(B=0,Eq=-\delta)=1,
 \qquad
 \Psi_{\rm loc}(\operatorname{reset}_v)=h_v.         \tag{4}
\]

This is a useful positive coefficient shadow.  It is not a constructed
physical column.  If `N_v` is the odd reset carrier and `X=T H_W`, the full
Leibniz differential is

\[
 d(N_vX)=(dN_v)T H_W-N_v(dT)H_W-N_vT(W-1).           \tag{5}
\]

The last two summands in (5) are mandatory.  They carry 180 `dT` face
families over the five reset cells and five root/`W` families.  All terms
remain in tensor products of the central squarefree-`2K2` reset grade with
response `C2+/C4/P2` or root/Weyl grades.  The signed Weyl and rational root
projectors preserve the missing operation, word/fine, and repeated-edge
idempotents.  Hence the strict projection of (5) to the corner-resolved
`t*q_(v,N)` repeated-`P3+K2` private/`Eq` packet is zero/off-grade.

Even after a tensor-to-corner comparison is granted, the source boundary
does not determine whether the landing is (4) or the tied dark packet

\[
             (B,Eq)=(-\delta,-\delta),
             \qquad \Psi_{\rm loc}=0.                 \tag{6}
\]

Both are compatible with `d^2=0`; the quotient value is still
`chi=4 lambda`, with `lambda` arbitrary.  Finally, the formal bright value in
(4) is `h_v`-weighted.  The five `h_v` form a height-five complete
intersection and provide no denominator-only primitive unit aggregate.

Exact checker:
[`verify_h3_hv_switch_weyl_mixed_product_beq_leibniz_gate.py`](../computations/verify_h3_hv_switch_weyl_mixed_product_beq_leibniz_gate.py).

## 1. The exact coefficient shadow

The chart-complete endpoint-even line and its retained switch orientation are

\[
                 (2,-1,-1),\qquad (-2,1,1).           \tag{7}
\]

The coefficient `2` on the direct chart means that its two oriented DQ roots
each occur with coefficient one.  Thus the augmentation-preserving split (2)
is the correct coefficient shadow:

\[
 J(2,-1,-1)=\delta,
 \qquad J(-2,1,1)=-\delta.                            \tag{8}
\]

This split can also be expressed as the characteristic-zero even projector
on the two direct orientations.  It is legitimate in the coefficient/root
representation.  It is not a map from the central reset source row to the
four physical cap-corner rows.

The local terminal is

\[
 \Psi_{\rm loc}={1\over12}
    \sum_{c,m}\delta_c(B_{c,m}-Eq_{c,m}),             \tag{9}
\]

where there are three `C4` matchings.  Repeating `Eq=-delta` on all three
matchings gives

\[
 {1\over12}\,3\,\delta\cdot(0-(-\delta))=1.          \tag{10}
\]

For comparison,

```text
B=0,      Eq=-delta     Psi=+1,
B=-delta, Eq=0          Psi=-1,
B=-delta, Eq=-delta     Psi= 0.
```

Thus operation decoration really can break the operation-blind diagonal
darkness at coefficient level.  The negative result below is a typing and
totalization result, not a symmetry assertion that (3) vanishes.

The same profile propagates to the formal proper-face shadow.  In direction
order

```text
dD, dq01, dp0, ds1, dp1, ds0,
```

the `dT` packet is

\[
                    (-2,-2,1,1,1,1),                 \tag{11}
\]

the negative of the primitive local direction profile.  An Eq-only placement
of (11) has normalized terminal value `2`; the two comes from the two
direction slots in each chart.  The corresponding Eq-only tail packet also
has value `2`, from its two tail deletions.  Tying either packet in private
and Eq makes its value zero.

## 2. The full Leibniz boundary

Put

\[
 K=W-1,
 \qquad dH_W=K,
 \qquad d(T H_W)=(dT)H_W+TK.                          \tag{12}
\]

Treat `N_v` and `T H_W` as odd.  Then (5) follows from the graded product
rule.  Its second boundary splits as

\[
\begin{array}{c|l}
\text{first face}&\text{second boundary}\\ \hline
(dN_v)T H_W&(dN_v)(dT)H_W+(dN_v)TK,\\
-N_v(dT)H_W&-(dN_v)(dT)H_W-N_v(dT)K,\\
-N_vTK&-(dN_v)TK+N_v(dT)K.
\end{array}                                           \tag{13}
\]

All three pairs cancel, so `d^2=0`.  Keeping only the tempting first row of
(13) leaves both

```text
(dN_v)(dT)H_W  and  (dN_v)T(W-1)
```

uncancelled.  Therefore the bright reset shadow cannot be extracted from the
product while discarding its `dT` and root/W faces.

The switch audit gives exactly eighteen tail and eighteen direction faces in
`dT`.  Across five reset carriers this is

```text
90 tail carrier families + 90 direction carrier families = 180.
```

Each `h_v` contains three distinct matching monomials, and all fifteen
monomials across the five faces are distinct.  At fully decorated occurrence
level the same count is

```text
270 tail + 270 direction = 540.
```

There are additionally five `N_v T(W-1)` root/W families.  These are not
optional augmentation decorations; they are the terms which make (13)
cancel.

## 3. Why the literal corner projection is zero

The input and desired output tags are different:

| datum | reset factor | switch--Weyl factor | required cap output |
|---|---|---|---|
| word | `01211222` | response/fan Weyl orbit | response-to-`01211222` arrow |
| repeated/fine | squarefree `2K2` | response `C2+/C4/P2` | `t*q_(v,N)`, repeated `P3+K2` |
| operation | central Hasse/Koszul | chart `DQ/PS` plus root colour | one corner and `AB/AC` root |
| row | central `e_Eq` | Cartan/Weyl homotopy | private `B_c` or reduced `Eq_c` |

Multiplication concatenates these source labels.  It does not silently apply
a comparison functor which replaces their tensor product by the last column.
In particular:

- `(dN_v)T H_W` contains the central Eq or derived `Yw` reset face tensored
  with the switch/Weyl homotopy;
- `N_v(dT)H_W` contains the reset carrier tensored with 90 tail and 90
  direction response faces;
- `N_vT(W-1)` lies in the root/`W` row, not the private cap row.

The signed Weyl action changes colour words but preserves the underlying
matching, repeated-edge label, and `Hasse[2]` direction-pair tag.  A rational
root projector can implement (2) on coefficients, but it has the same scope.
Neither operation creates the absent source-labelled tensor-to-cap chain map.

Thus, in the currently defined direct-sum projection,

\[
                 \Pi_{B/Eq}^{\rm literal}(d(N_vX))=0. \tag{14}
\]

Equation (14) says off-grade, not algebraically dark.  Forgetting the tags
first gives the nonzero shadow (4).

## 4. Why the cap value is still not forced after a grant

Suppose one grants the missing tensor-to-corner square and normalizes its
source boundary.  The exact projected mapping-cylinder calculation permits
an arbitrary cap augmentation

\[
 \Pi_{B/Eq}(\kappa)\equiv\lambda(\delta,0)
       \pmod{\text{old cap rows}},
 \qquad \chi=4\lambda.                                \tag{15}
\]

A dark filler and a bright filler have the same source square boundary and
both satisfy `d^2=0`.  The formal operation profile (3) suggests the Eq-only
choice, but the source differential does not assert that the root/W face is
private `B`, that the central factor is reduced `Eq`, or that their relative
coefficient is untied.  Those are precisely the missing cap/descent readout
laws.

Consequently the mandatory cross terms do not prove that the product is
tied.  They prove that the coefficient shadow is not a closed physical cell,
while (15) proves that closure alone would still not select its augmentation.

## 5. The remaining `h_v` coefficient

If a future physical comparison chooses the Eq-only convention in (4), its
value on the `v`-th product is exactly `h_v`, not one.  The five denominator
hafnians form a height-five complete intersection.  Their first syzygies are

\[
                         h_i e_j-h_j e_i,             \tag{16}
\]

so denominator-only combinations do not produce a primitive unit aggregate.
The q-zero contraction of `h_v` or localization at one `h_v` remains a
separate physical descent/localization theorem; it cannot be inferred from
the product shadow.

## Shortest positive datum

The mixed-product route would become real after one multiplicative,
source-labelled chain comparison

\[
 \mu:\langle N_v\rangle\otimes\langle T,H_W,W-1\rangle
       \longrightarrow C_{\rm cap}^{B/Eq}             \tag{17}
\]

which:

1. sends the central-Eq/switch shadow to the corner profile `Eq=-delta`;
2. routes all 90 tail and 90 direction carrier faces and the five root/W
   faces in (5), retaining word, fine, repeated, operation and root labels;
3. specifies an untied nonzero class in (15), rather than merely a tied
   physical response; and
4. supplies a source-valid primitive normalization of the remaining `h_v`
   coefficient.

This is not another scalar identity.  It is the missing cross-grade
restriction/insertion and cap-augmentation theorem in multiplicative form.

## Verification

Run

```text
python3 computations/verify_h3_hv_switch_weyl_mixed_product_beq_leibniz_gate.py
python3 -O computations/verify_h3_hv_switch_weyl_mixed_product_beq_leibniz_gate.py
python3 -I -S computations/verify_h3_hv_switch_weyl_mixed_product_beq_leibniz_gate.py
```

Frozen ledger digest:

```text
cf424a6adbccfc4bf0fffd969c0402a16020d4924e78f9df110029e7f508e472
```
