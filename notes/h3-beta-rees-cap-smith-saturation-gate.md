# The first beta-torsion class is the selected cap direction

## Result

There is a clean conditional theorem which would merge the `beta=0` corner
into generic Interface III:

> If the cokernel of the complete augmented physical Rees map is
> beta-torsion-free, then a physical generic order-(h) comparison
> specializes to the protected `D0` cell at `beta=0`.

Equivalently, the physical image must be beta-saturated.  This condition is
not implied by multiaffinity, and it is not implied by flatness of the image
module itself.  Over the beta-local DVR, every submodule of a free module is
free; the load-bearing condition is flatness/torsion-freeness of the
**cokernel**, or purity of the image inclusion.

The existing literal cap packet already exhibits the first exact torsion
carrier.  In the selected/complementary root basis `(rho0,rho2)`, its two
physical jets are

\[
 Z_1=\beta\rho_0+\rho_2,
 \qquad
 Z_2=-\beta\rho_0+(h-1)\rho_2.                         \tag{1}
\]

They generate exactly

\[
                 R\rho_2\oplus\beta R\rho_0,           \tag{2}
\]

so the Smith form is `diag(1,beta)` and `[rho0]` is killed by beta.  At the
collision, `rho0` is precisely the selected `D0` shadow after quotienting
the known complementary `D2` line.

The formal order-(h) unary cell does not remove this torsion: it carries
`rho0` together with the pinned nonzero source-descent/connecting defect.
Including that primitive defect row changes the Smith form to
`diag(1,1,beta)`.  A physical column carrying the same defect and zero root
output would remove the torsion immediately; subtracting it from the unary
cell gives a protected `rho0`, and the resulting matrix has a unit minor.

This freezes the positive theorem at its smallest exact form.  It does not
prove that the exhaustive physical cokernel has torsion: another complete
source column may supply exactly the missing defect correction.  It proves
that no argument from multiaffinity, generic normalization, or the two cap
jets alone can establish saturation.

The torsion also has an exact Bockstein interpretation.  The cap source
combination whose boundary is `beta*rho0` becomes a cycle at beta zero, and
its beta-Bockstein is `[rho0]`.  The full rho-even product-rule orbit of
`a872264` has the only current **coarse** proper-face candidate for the
required correction, but not yet its physical type: the formal face retains
the endpoint ridge and wrong word, and the pinned data do not identify its
primitive descent coordinate with the beta-zero unary defect.  Nor does it
come from an integral `k[beta]`-linear source cell.  This identifies a
stronger single theorem which would close generic and collision strata
together.

## 1. The complete physical Rees module

Work at the trace collision over

\[
                   R=k[\beta]_{(\beta)},                       \tag{3}
\]

with the nonzero selected scalar `alpha` and the characteristic-zero integer
`h` inverted.  Retain the normal/Rees coordinate through order (h):

\[
                   R_h=R[\ell]/(\ell^{h+1}).                  \tag{4}
\]

Fix one physical word, fine grade, repeated label, and endpoint orientation.
Let `C_R^(h)` be the free `R_h`-module on every source-valid physical chain
in this packet, and let

\[
 J_R=(P_R,\theta_R):C_R^{(h)}\longrightarrow
 Y_R=R_{\rm prot}\oplus R_h[D_0]                              \tag{5}
\]

be the complete augmented readout.  The protected summand retains literal
lower, source descent, endpoint ridge, wrong word, reduced Eq, labelled
ordinary residue, anchor incidence, `Yw`, and `W`; the last row is mandatory
by the augmented inactive-cap theorem.  Set

\[
                 I=\operatorname {im}J_R,qquad
                 b=\ell^h[D_0].                               \tag{6}
\]

Once the generic root-even orbit has been constructed physically in this
same module, clearing its beta denominator gives

\[
                         \beta^m b\in I                        \tag{7}
\]

for some (m\geq1).  If `coker(J_R)=Y_R/I` has no beta-primary torsion,
then (7) forces `[b]=0`, so `b in I`.  Reducing the resulting equality at
`beta=0` gives

\[
                 1\in\theta_0(\ker P_0).                      \tag{8}
\]

Thus beta-saturation is exactly strong enough to specialize the generic
comparison.  It is conditional on the generic orbit being physical and
fully augmented; an occurrence-level orbit is not an element of (5).

## 2. Flatness and the unit-minor criterion

The following conditions are equivalent for the finite free map (5) over
the beta-local DVR:

1. `coker(J_R)` has no beta-primary torsion;
2. `I` is beta-saturated in `Y_R`;
3. the rank of `J_R` at `beta=0` equals its generic rank;
4. if the generic rank is `r`, some `r x r` minor is a beta-adic unit.

This is the Smith normal form criterion.  In particular, a generic-rank unit
minor would prove the desired saturation without enumerating coefficient
supports.

Two weaker properties do not suffice.

* `I` being flat is automatic here and says nothing about its embedding.
  The inclusion `beta R -> R` has a free rank-one source and the torsion
  cokernel `R/(beta)`.
* Multiaffinity only bounds the beta degree of matrix entries.  The matrix
  `[beta]` is multiaffine and has the same torsion cokernel.

The actual cap matrix below is a physical two-dimensional version of both
guards.

## 3. Smith form of the two cap jets

Using `(rho0,rho2)` as row basis and `(Z1,Z2)` as columns, (1) is

\[
 B_h(\beta)=
 \begin{pmatrix}
   \beta&-\beta\\
   1&h-1
 \end{pmatrix}.                                             \tag{9}
\]

Its determinant is `h beta`, while the lower-left entry is the unit one.
Hence its Smith form is `diag(1,beta)` up to units.  More explicitly,

\[
 {Z_1+Z_2\over h}=\rho_2,
 \qquad
 {(h-1)Z_1-Z_2\over h}=\beta\rho_0.                         \tag{10}
\]

At beta zero the two columns span only `rho2`, so `rho0` is not in the
image.  Equations (10) prove that its nonzero cokernel class is killed by
beta.  This is the exact algebra behind the collision identities
`J2=(h-1)J1` and `J*=0`.

Every entry of (9) has beta degree at most one.  Therefore the literal
physical cap packet itself is already a sharp counterexample to the claim
that multiaffinity forces saturation.

## 4. Adding the unary top retains the torsion

The order-(h) unary/third-cofactor construction has a unit selected-root
coefficient, but its primitive connecting/source-descent functional is
nonzero.  Normalize that functional to one and use row order

```text
(descent defect, rho0, rho2).
```

The smallest augmented packet is

\[
 \widetilde B_h(\beta)=
 \begin{pmatrix}
  1&0&0\\
  1&\beta&-\beta\\
  0&1&h-1
 \end{pmatrix},                                           \tag{11}
\]

with columns `(U,Z1,Z2)`.  Again

\[
                         \det\widetilde B_h=h\beta.          \tag{12}
\]

There is a unit two-by-two minor, so the Smith form is
`diag(1,1,beta)`.  The class of the protected vector `(0,rho0,0)` is
nonzero at beta zero: the descent coordinate forces the coefficient of `U`
to vanish, after which the cap columns see only `rho2`.  It is nevertheless
killed by beta through (10).

This identifies exactly why the formal order-(h) Hasse coefficient is not
the desired special-fibre cell.  It supplies the selected root and the
primitive defect together; saturation asks whether that defect can be
removed physically.

## 5. The smallest positive unit minor

Suppose a source-valid column

\[
                         V=(1,0,0)                       \tag{13}
\]

exists in the same fixed grade: it has the unary cell's primitive protected
defect but zero selected/complementary root output.  Then

\[
                         U-V=(0,1,0)=\rho_0,             \tag{14}
\]

and the columns `(U,V,Z1)` have determinant `-1`.  This unit minor proves
beta-saturation and (8) at once.

Equation (13) is a normal form for a complete correction packet, not a
claim that a bare descent symbol is a source column.  Physically `V` must
also match every other protected row of `U`: endpoint ridge, word, Eq,
ordinary residue, anchor correction, and `Yw/W`.  The pinned third-cofactor
audit shows that the current formal proper-face tail does not do so—it
retains the descent unit, rank-five `Omega` ridge, and wrong midpoint word.

Consequently the beta-saturation attack and the earlier `theta` membership
are the same construction in two languages:

```text
generic orbit + beta-saturation
        = protected correction V
        = U-V with unit D0 readout
        = 1 in theta_0(ker P_0).
```

The first explicit torsion carrier is `[rho0]`; the first missing positive
object is the fully typed defect correction `V`.  No stronger conclusion is
available from the current packet.

## 6. The beta-Bockstein of the cap packet

Let `e1,e2` be source generators mapping to `Z1,Z2`.  Formula (10) is the
chain equality

\[
 J_R\!\left({(h-1)e_1-e_2\over h}\right)=\beta\rho_0. \tag{15}
\]

Therefore

\[
 s_0={ (h-1)e_1-e_2\over h}\bmod\beta
        \in\ker J_0.                                      \tag{16}
\]

For the two-term complex `C_R -> Y_R`, the beta-Bockstein of a special
cycle represented by `s` with `J_R(s)=beta*y` is the cokernel class of
`y mod beta`.  Equations (15)--(16) give exactly

\[
                         \delta_\beta([s_0])=[\rho_0].       \tag{17}
\]

Thus the previously abstract normal-cone obstruction is literally the
Bockstein of the generic cap comparison.  This statement is integral and
uniform in `h`; the checker verifies it through `h=12`, while (15) proves it
for all characteristic-zero `h`.

## 7. Comparison with the full rho-even orbit

The single generic orbit isolated in `a872264` has occurrence landing

\[
                          v={B_1+B_4\over2}                   \tag{18}
\]

and its formal proper-face tail has coarse signature

```text
(ainc,W,target,ores)=(-1,0,0,0).
```

This has exactly the required zero target/residue/`W` shadow and the useful
anchor incidence.  Hence the Bockstein picture is not a new unrelated
construction: the product-rule proper face is the canonical candidate for
`V`.  But the recorded signature does **not** prove that its primitive
source-descent coordinate is the same as the beta-zero unary defect.

It is not yet an equality in the physical source complex.  The frozen full
orbit audit also records

```text
source-valid                         false
endpoint-ridge space rank            6
primitive Omega rank                 5
selected midpoint source-word hits   0.
```

Moreover, the generic orbit in `a872264` is a fixed occurrence/full-output
prescription after normalization; it is not an integral `k[beta]`-linear
source cell.  Without such an integral cell there is no full physical
Bockstein to compare with (17).  Calling the formal proper face `V` would
discard exactly the ridge/word/descent typing which made the beta-zero
membership nontrivial.

The strongest uniform Interface-III theorem is therefore:

> Construct one integral `k[beta]`-linear rho-even
> product-rule/Bianchi cell `X(beta)` in the actual omitted-`25` repeated
> grade.  On `beta != 0`, its normalized face must be (18), carrying the
> complete `delta+`, mixed target, reduced-Eq, labelled-residue, and `W=0`
> packet.  At `beta=0`, its proper-face beta-Bockstein must be the complete
> physical correction `V`, including every ridge, word, Eq, residue, anchor,
> and `Yw/W` coordinate.

If this theorem holds, (14) gives the protected `D0` unit and the same unit
minor proves beta-saturation.  The generic Interface-III orbit and the
beta-zero `theta` membership then close simultaneously.  Conversely, any
failure is measured first by the already explicit Bockstein `[rho0]` and
then by the single terminal-extension equation of `d2085ca`.

## Verification

Run:

```text
python3 computations/verify_h3_beta_rees_cap_smith_saturation_gate.py
python3 -O computations/verify_h3_beta_rees_cap_smith_saturation_gate.py
python3 -I computations/verify_h3_beta_rees_cap_smith_saturation_gate.py
python3 -S computations/verify_h3_beta_rees_cap_smith_saturation_gate.py
```

All modes print ledger digest
`d57abe489ef3daa029362cee5748937b5b211c5a4d08bdeecfb39c929e87cada`.
