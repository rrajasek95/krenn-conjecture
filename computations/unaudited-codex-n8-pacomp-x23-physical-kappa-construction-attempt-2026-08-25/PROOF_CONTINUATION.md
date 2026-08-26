# Attempted physical construction of the root-natural mixed cell

Status: **NO CONSTRUCTION FROM THE PINNED ORIGINAL MATCHING DATA; FIRST OBSTRUCTION IS THE TWO-DIMENSIONAL AB/AC RESPONSE-TO-CAP HOM QUOTIENT**.

Parent manifest: `45fd37cab35450b6e53918ff77c2d7b2c4dd8cee83bb202dadbf94e29f17535b`.
The previous audit proved the mixed-square formula and its signs.  This note
asks the strictly stronger question whether the original source-labelled
matching complex contains the required physical cell.

## Required domain and codomain

For each root label `rho in {AB,AC}`, the response complex is

\[
R_1^\rho=\langle\epsilon_s^\rho\rangle
 \xrightarrow{d}R_0^\rho=\langle c_f^\rho\rangle,
\qquad d\epsilon_s^\rho=-c_f^\rho.                 \tag{1}
\]

Its literal grade is response word `11110000=11:110000`, ordered response
head `01/10`, the selected `db01` fine packet with its six `P4+K2` tails,
and the relative response-occurrence repeated grade.

The cap complex is

\[
C_1^\rho=\langle r_0^\rho\rangle
 \xrightarrow{d}C_0^\rho=\langle E^\rho\rangle,
\qquad dr_0^\rho=E^\rho=(H_0-u)e_{Eq}.             \tag{2}
\]

Its literal grade is cap word `01211222`, the AB or AC root-labelled cap
repair, the six `t*q_(v,N)` fine degrees, repeated grade `P3+K2`, and the
`AugP2/K_Eq` cap operation.

The only normalized ungraded chain-map shape is

\[
\Phi_1(\epsilon_s^\rho)=r_0^\rho,
\qquad \Phi_0(c_f^\rho)=-E^\rho.                   \tag{3}
\]

Indeed, `d Phi_1(epsilon)=E=Phi_0(-c_f)`.  Thus there is no coefficient or
sign obstruction in (3).  A physical `kappa_c^rho` would be the oriented
naturality cell of (3) across the `P_f/D4` square and would satisfy the
already proved formula

\[
d\kappa_c^\rho=P_{f,c}^\rho-K_{Eq,L,c}^\rho
 +K_{Eq,R,c}^\rho-D_{4,c}^\rho.                    \tag{4}
\]

## Tests of the literal candidates

Three natural constructions fail for different, exact reasons.

1. **Koszul product.**  Formally one wants `epsilon_s wedge theta`, where
   `theta` is the cap Eq/Koszul cell.  But the two factors lie in orthogonal
   response and cap operation idempotents.  The pinned physical algebra has
   no matrix unit `e_C A e_R`; the product is undefined in the typed grammar
   (or zero in the diagonal direct-sum model).
2. **Difference of the two marked matching routes.**  On the canonical q23
   carrier, the deletion/reinsertion route and the delete-first response
   route have coefficient `+1` on the same literal cap monomial.  This is
   checked on all 90 marked descendants.  Their difference is zero.  It
   proves the edge square commutes but does not manufacture a homotopy
   generator filling it.
3. **Root/Weyl transport times r0.**  Root/Weyl stays in the response
   diagonal corner and `r0` stays in the cap diagonal corner.  Products of
   the available operations still have zero `e_C A e_R` coordinate.

Thus the obvious generator formulas reproduce the correct coefficient
shadow but fail physical typing before `d kappa` can even be tested.

## Smallest rank obstruction

Grant every diagonal word, head, fine, repeated, and operation repair
independently, withholding only `Hom(response,cap)`.  Across AB and AC this
strong base has rank 24.  The exact rank ladder is

```text
base, +AB, +AC, +(AB+AC), +(AB and AC)
 24,   25,  25,      25,             26.
```

The two primitive duals are `omega_AB^Hom` and `omega_AC^Hom`.  Therefore
the first missing physical object is not yet the mixed two-cell: it is the
two-dimensional family of degree-zero response-to-cap matrix units needed
to type (3).  One root-forgetting aggregate raises rank by only one and
leaves `(omega_AB^Hom-omega_AC^Hom)/2` nonzero.

Conditional on adjoining both root-labelled `Phi` sections, (4) is the next
obstruction: there is one primitive mixed-square `H1` for AB and one for AC.
Their direct sum has rank two; the unlabelled aggregate again has rank one.
Cut covariance then forces `sigma(kappa_23^rho)=-kappa_45^rho`.  After those
mixed cells, the shifted ridge is still an independent proper face.  This
recovers the pinned smallest positive object: one root-natural paired
collision mapping bicomplex, not a bare isolated `kappa`.

## Relation to Conjecture 6.2

The balanced chart character is

\[
z_{chart}=(1,1,-1,-1)
\]

in order `(A_[a|b],A_[b|a],B,C)`.  The mixed-square edge cycle is

\[
z_{edge}=(1,-1,1,-1)
\]

in order `(P_f,K_L,K_R,D4)`.  There is a unique evident coefficient
placement

```text
A_[a|b] -> P_f,
B         -> K_Eq,L,
A_[b|a] -> K_Eq,R,
C         -> D4,
```

which sends `z_chart` to `z_edge`.  This is an exact character-level map.
It is not currently a source-labelled physical map: the two sides have
different word/fine/repeated/operation idempotents, precisely the missing
cross-grade interface detected above.

Consequently bare equality of the balanced characters, or even an abstract
filler `d Lambda=z_chart`, does not construct `kappa`.  A sufficient extra
hypothesis is the following strengthened filler-branch instance of
Conjecture 6.2:

> For every `c in {23,45}` and `rho in {AB,AC}`, the Conjecture 6.2 filler
> `Lambda_c^rho` exists in the identical response/cap word, fine, repeated,
> common-tail, and operation grade, and there is a source-labelled placement
> `J_c^rho` realizing the four assignments above.  `J` commutes with `d`,
> restriction, reinsertion, every protected readout, AB/AC transport, and
> sigma.

Under this exact hypothesis one may define

\[
\boxed{\kappa_c^\rho=J_c^\rho(\Lambda_c^\rho)},     \tag{5}
\]

and then (4), AB/AC naturality, sigma covariance, and root-forgetting follow
formally.  Conjecture 6.2 as a character-level filler alternative does not
by itself provide `J`; adding this placement is the load-bearing physical
content.  Equivalently, the needed hypothesis is the physical
`Phi_KS,r0`/paired-collision mapping-bicomplex clause, specialized to the
canonical h=3 q23/q45 packet.

## Conclusion and scope

No explicit physical `kappa` is constructed from the pinned original
matching/source data.  The smallest exact obstruction is the missing
two-dimensional AB/AC `Hom^0(response,cap)` quotient, with the primitive
mixed-square rank-two obstruction only after that quotient is filled.
The strengthened Conjecture 6.2 placement above is sufficient and isolates
the exact additional hypothesis.

This is h=3 only.  It does not prove the strengthened filler hypothesis,
construct the shifted ridge packet, prove Q23, PAComp(3), uniform PAComp(h),
or promote a terminal/conjecture result.
