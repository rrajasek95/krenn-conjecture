# Exact-fibre conormal and asymptotic-gap framework

Status date: 2026-08-21.  This is a proof-design note, not a certificate.

## Scope correction: the full exact fibre is the right domain

For the exact `N=8,D=3` fibre, minimizing norm on the full fibre is not only
valid but strictly stronger than minimizing on a chosen incidence chart.
The fibre is a closed algebraic subset of the finite-dimensional realification
of the 252 complex source coordinates.  If it is nonempty, the coercive
Euclidean norm therefore attains a global minimum.

Moreover **no point of the exact fibre can have an active clean cap**.  The
audited clean-pair theorem would turn such a cap into an exact ternary
six-site source, contradicting the certified unrestricted `(6,3)` theorem.
This is the literal quantifier statement already isolated in
`notes/clean-bridge-at-eight-is-the-open-case.md`.  Consequently, under the
counterexample hypothesis, every full-fibre minimizer is automatically
no-cap.  The approximate active-cap families used as optimization controls
have nonzero mixed output and do not contradict this statement.

At the attained full-fibre minimum, the correct Fritz--John equation is

```text
alpha*A = J_A^*lambda,
```

with `(alpha,lambda)` nonzero and the singular branch `alpha=0` retained.
The proof target is inconsistency of the GHZ plus Fritz--John system after
adding the 728 no-cap consequences and the regularity-free blockwise minimum
conditions below, or a second-order violation on its tangent space.

The invisible-cell deletion rule below is unconditional for this full-fibre
minimum; no incidence-preservation qualification is needed.

## Exact first bounded milestone

The blockwise and first conormal controls now have an exact literal checker.
For an edge `e=pq`, fixing the other 27 blocks gives

```text
F(A)=T_e(A_e)+b_e.
```

The column labelled `(e;i,j)` is supported precisely on words with
`w_p=i,w_q=j`; on such a word its coefficient is the residual six-site
Hafnian.  Hence the nine columns have disjoint word supports.  At a global
fibre norm minimum, every `u in ker(T_e)` is an exact affine fibre direction,
so

```text
A_e perpendicular ker(T_e),  equivalently A_e in im(T_e^*).
```

In particular, if all residual Hafnians for one endpoint-labelled cell
vanish, that cell vanishes at the minimum.  This statement is regularity-free.

The exact `n=4` GHZ witness has squared norm six, and Cauchy proves this is
the global fibre minimum: each unit pure coefficient costs at least two in
squared diagonal-cell norm.  Literal Jacobian replay gives

```text
rank J = rank([J;A*]) = 51,   dim ker J = 3.
```

The three kernel directions are the opposite-edge rescalings.  With the
pure-word multiplier `lambda=(1,1,1)`, the bordered/constrained Hessian on
this kernel basis is exactly `4 I_3`.  Each direction integrates as
`(exp(t),exp(-t))`; in `A+t v+t^2 w` notation it satisfies
`Jw+(1/2)D^2F(v,v)=0` literally.

For the frozen `K8` colour-zero matching plus chord `02^(0,0)`, every residual
six-site Hafnian in the chord column vanishes.  Thus `T_02=0`.  The full
Jacobian has rank 37, adjoining the source norm row raises it to 38, and the
chord-coordinate kernel vector pairs with the source by one.  The chorded
source is rejected at first order, while deleting it preserves the output.

The realified regular KKT and second-order equations, using objective
`(1/2)||A||^2`, are

```text
A_e = T_e^* lambda,
J_A v = 0,
J_A w + (1/2) D^2F_A(v,v) = 0,
||v||^2 - Re<lambda,D^2F_A(v,v)> >= 0.
```

For a tangent supported on two distinct edges `e,f`, the mixed second
derivative vanishes if the edges meet.  If they are disjoint, its literal
coefficient is the residual four-site Hafnian times the two endpoint-labelled
variation cells.  This is the source-labelled two-edge patch in which the
carrier response occurs after the complementary matching split.

The order guard is decisive: `T_e` is first derivative, whereas

```text
rho_ab^(alpha,beta)(K)
 = sum_ij K_ij (
     A_pa^(i,alpha) A_qb^(j,beta)
   + A_pb^(i,beta) A_qa^(j,alpha))
```

is the corresponding degree-two response, with the frozen direct rank-one
term separated in the complementary-split identity.  No row of `L_C` is
silently inserted into `T_e` or `J`.

Finally, one blocker membership plus stationarity does not force a tangent.
The canonical second diagonal `P=2` source is an exact hostile guard:
`rank J=rank([J;A*])=226`, while carrier `(01,star 2)` has response rank one
and blocker mask `[0,0,1,0]`.  It is not a GHZ-fibre point (it has two mixed
outputs).  Thus `A perpendicular ker J` and one literal blocker membership
coexist and, tautologically, cannot yield a first-order `v` with
`<A,v>!=0`.  The GHZ equations plus a genuine map from local `K` to an
integrable pair `(v,w)` are load-bearing; blocker membership alone supplies
neither.  At singular points the `alpha=0` Fritz--John branch remains
separate and cannot be discarded.

Exact checker logical digest:
`801ee4fc86a3d9013c462e100d27da987adbc495638b7c74bc650eaf69875518`.

## Exact 13-block cap-pair environment

Fix the 15 residual--residual blocks at a pair `pq` and vary `A_pq`, the six
`p`-stars, and the six `q`-stars.  This is a 13-block/117-cell environment.
For an endpoint word `(i,j)`, literal matching partition gives

```text
F_ij = A_pq[i,j] H6
     + sum_(a<b,alpha,beta) H4_(R\{a,b})
         rho_ab^(alpha,beta)(E_ij).
```

There are 15 direct matchings and 90 cross matchings.  A dense signed rational
source replay verifies the identity on all 6,561 words.  The map is linear in
the direct block and bilinear in the two star families; this is the genuine
location of `rho`.

For a bare full-fibre regular minimum, the direct normal equation is

```text
A_pq[i,j] = sum_u conjugate(H6[u]) lambda[i,j,u],
```

and each `p`-star equation contracts `lambda` against the opposite `q`-star
and `H4`; the `q` equation is endpoint-swapped.  On a fixed no-cap incidence
chart, the additional `Dg^*mu` term from the scope correction must be included.

The canonical second diagonal `P=2` source is an exact hostile guard for the
bare implication.  At pair `01`, the local Jacobian has rank 106 and kernel
dimension 11, and the pure-word multiplier satisfies all 117 normal equations.
Nevertheless both of the following branches are blocked:

```text
star centre 2:       response rank 1, mask [0,0,1,0]
triangle (2,3,5):    response rank 2, mask [0,0,1,0].
```

Every local fibre tangent has zero norm pairing.  Hence one blocker membership
plus the local normal equations cannot manufacture the desired tangent.  This
guard is not a GHZ point—it has two mixed outputs—so it proves that the full
GHZ mixed rows and the incidence-chart equations are load-bearing.  The next
valid computation is a bounded KKT consistency test on one genuine no-cap
rank chart, not a 728-carrier tangent search.

13-block checker logical digest:
`8790177d50f6ba324baa4fe4471842f00460dc656113e2bcd81a7f79dfcaa900`.

## Common-matching pair-product control (nonexact)

Put `I_3` on `01,23,45,67` and zero on all other blocks.  The source realizes
three pure coefficients equal to one, but it does **not** realize GHZ: its
tensor product has 78 additional mixed outputs.  Its full carrier census has
104 active carriers—24 stars and 80 triangles—and every active carrier lies
over one of the four matching edges.  The residual-six response matrix is
zero on each of them.  Everything in this section is therefore a response
control, not an exact-fibre boundary computation.

The mixed Jacobian has rank 33.  All 216 off-matching source cells have zero
first derivative, leaving a 219-dimensional mixed tangent space.  More
importantly, for a matched cap pair both incident residual star families vanish
at the source, so

```text
L_C(A0)=0,       dL_C|A0(Y)=0
```

on all 104 active carriers.  The first response term is quadratic:

```text
B2_ab^(alpha,beta)(Y)_(i,j)
 = Y_pa^(i,alpha)Y_qb^(j,beta)
 + Y_pb^(i,beta)Y_qa^(j,alpha).
```

Thus ordinary linearized membership is vacuous.  The correct leading
incidence condition is rank-stratified.  For a chosen blocker
`b in {E00,E11,E22,I}`, on a rank-`r` chart require a live `r`-minor of `B2`
and vanishing of all augmented `(r+1)`-minors of `[B2;b]`.  This does not
falsely declare blocker membership closed at the rank-zero limit.

There are three carrier shapes per matched pair: six stars, twelve triangles
containing one full residual matching pair, and eight transversal triangles.
Transport across the four matching pairs gives all 104 leading incidence
packets.

The projected homogeneous second-variation equation used in this control is

```text
J_A0 Z + (1/2)D^2F_A0(Y,Y)=0.
```

Exact matching enumeration produces 8,748 quadratic cell terms.  Eliminating
the 33-dimensional direct-correction image gives 912 deduplicated quadratic
cokernel equations in the 216 off-matching `Y` variables, with full constraint
digest
`93e08edd4ecd484e4fa9bc6a7391275ca5339e47ce267dcb67a9cdc0f3ef43f6`.

The dense control `Y_uv=I_3` on every off-matching edge blocks each of the
three canonical leading carrier shapes, but violates 109 of the quadratic X5
controls.  Hence leading incidence alone is feasible in this nonexact model.

No exact-fibre, emptiness, or Puiseux-arc claim follows from this system.

Leading-boundary logical digest:
`9a09799eb2bdba7c9f13181fdf972a2b6549d7927323fe31c4a1de37e03490dc`.

## Historical conormal diagnostic

The previous carrier/Hessian attempt lacked a global conormal: a blocker
`K` is a covector on one nine-dimensional cap slice, but need not lie in
`ker(J_A^T)`.  Trying to glue the 728 local blockers inside the degree-at-most
two word grade was exactly injective on the sharp controls, so that route
could not manufacture a conormal.

The unconstrained exact fibre

```text
Z = { A in C^252 : F(A)=GHZ }
```

is nonempty on the standard active-cap charts, and it has a point of minimum
Euclidean norm because `Z` is closed and the norm is proper.  Nearest-point
criticality is the standard conormal construction underlying Euclidean
distance degree; see Draisma--Horobet--Ottaviani--Sturmfels--Thomas,
[The Euclidean distance degree of an algebraic
variety](https://arxiv.org/abs/1309.0049).

Minimizing on all of `Z` does **not** retain a hypothetical no-cap
counterexample: the minimizer may simply lie on a known active-cap chart.
The sound use is a dichotomy on a fixed locally closed no-cap rank/incidence
stratum `S` containing the proposed counterexample.  Either the norm infimum
is attained in the interior of `S`, where the conormal equations below apply
to stratum-preserving tangents, or it exits through a finite rank-drop/cap
boundary or through infinity.  The latter cases belong to the separate
incidence/tangency analysis.

At a regular real point, the KKT equation is

```text
A = J_A^* lambda,
```

after absorbing the harmless factor two.  At a singular point one keeps the
Fritz--John homogenization

```text
alpha*A = J_A^* lambda,       (alpha,lambda) != 0,
```

rather than silently assuming a constraint qualification.  Thus an attained
interior no-cap minimizer supplies the global conormal that the local carrier
data did not.  It is not legitimate to assign this conormal to an arbitrary
no-cap source or to the unconstrained active-cap minimum.

Equivalently, after realifying the complex source and Jacobian, the regular
first-order test contains no output multiplier variables:

```text
A perpendicular to ker(J_A)
    iff rank([J_A ; A*]) = rank(J_A).
```

Thus it is enough to produce one true fibre tangent `v` with
`Re <A,v> != 0`.  This is potentially much cheaper than the retired target of
forcing an additional independent Jacobian row.  Conjugation/realification
is load-bearing here; the Hermitian norm condition must not be replaced by a
bilinear complex transpose in a general exact source.

For the unconstrained full-fibre minimum this choice removes the known
invisible-chord obstruction: any source coordinate that can be varied to zero
while leaving `F(A)` fixed must vanish.  On a no-cap stratum the deletion is
valid only if it preserves the chosen rank/incidence conditions; an output-
invisible chord may still be load-bearing for blocker membership.

There is also a regularity-free blockwise consequence.  Hold the other 27
edge blocks fixed.  Multi-affinity writes

```text
F(A) = T_pq(A_pq) + b_pq
```

for a literal `6561 x 9` linear map `T_pq`.  Every `u in ker T_pq` is an
exact full-fibre direction, not merely an infinitesimal one.  Hence an
unconstrained global minimum-norm source satisfies

```text
A_pq perpendicular to ker T_pq,
equivalently A_pq in im(T_pq^*),
```

for every pair `pq`, with no smoothness assumption.  The star/triangle
response matrices are **not** row submatrices of `T_pq`: the frozen
Jacobian audit shows that a first-derivative row is `H6*I9`, whereas a
carrier row `rho` has degree two and enters only after the complementary
matching split.  In fact the nine columns of `T_pq` have disjoint output-word
supports.  Thus the immediate consequence is the exact support rule

```text
if every residual six-site Hafnian for cell (pq;ij) vanishes,
then A_pq[ij]=0 at a minimum-norm source.
```

This removes invisible cells in the unconstrained control but does not itself
prove a cap.  At an attained no-cap-stratum minimum it applies only to kernel
directions preserving the stratum.  The real bridge remains second order:
combine its global conormal with the audited
`rho = D^2F - direct` identity.  Any argument treating `L_C` as a first-
Jacobian block repeats the already-falsified carrier/Jacobian identification.

## Second-order must-pass equation

For a regular minimum and a real tangent `v in ker J_A`, constrained
second-order optimality gives

```text
||v||^2 - Re <lambda, D^2 F_A(v,v)> >= 0
```

with the normalization determined by the KKT convention.  More generally,
for an actual second-order fibre arc `A+t v+t^2 w+...`, use

```text
J_A v = 0,
J_A w + (1/2) D^2 F_A(v,v) = 0,
```

and differentiate the norm directly.  This avoids treating every vector in
`ker J_A` as second-order integrable at a singular point.

The already-audited carrier identity is exactly of the required derivative
order:

```text
rho = (a source-labelled D^2 F slice) - (direct rank-one term).
```

The concrete theorem target is therefore:

> At an attained interior minimum on an exact no-cap incidence stratum, the
> Fritz--John conormal and the four-way no-cap membership at all 728 carriers
> produce either an active clean cap,
> a nonzero first-order tangent lowering the norm, or a second-order
> integrable tangent violating the constrained-Hessian inequality.

This statement is strictly weaker than gluing every blocker into a conormal.
Only one negative tangent is needed.

## Smallest exact screens

1. Replay the construction on the exact `n=4` GHZ fibre and check that a
   support-minimal/minimum-norm representative satisfies the KKT and bordered
   Hessian equations.
2. On every frozen finite exact chart component, add the norm-stationarity
   rows after eliminating the output multiplier to `im J_A`; test whether
   the component becomes a known cap chart or a unit ideal.
3. At the sharp W40/W25 controls, which are not full exact-fibre points, use
   only hostile guards: the proposed implication must *not* fire merely from
   carrier membership.
4. Keep the singular alternative `alpha=0` as a separate conormal branch.
   Dropping it would make the proof conditional on an unproved smoothness
   assertion.

## Quantitative gap at infinity: separate, secondary lane

The balanced no-cap inequality `P_mixed >= 2` is false.  The exact six-cell
family has `P<2`, remains no-carrier, and has a certified unique positive
minimum in `[1.99490005061,1.99490202117]`; it grows like
`(1894177/2000000)*s^8` at infinity.
A smallest exact two-cell enlargement decreases this value, but its infimum
occurs at a finite support boundary: the six original leakage cells vanish,
active clean caps reappear, and the value becomes the previously certified
active-cap minimum `1.7980700759...`.  The no-cap open stays strictly above
that boundary for every positive enlargement parameter.  This is a concrete
instance of the attained-interior versus finite-cap-boundary dichotomy, not
evidence for an interior zero.
A weaker uniform positive gap would still prove nonexistence, but it is a
stronger statement than the conjecture and no-cap incidence is not closed at
rank drop.  A finite active-cap limit can therefore create `P -> 0` without
creating an exact no-cap point.

The first full normal-cone guard is now negative.  At the active-cap minimum
of the two-cell family, every inclusion-minimal two- or three-ray support
that removes all arbitrary-`K` carriers has positive outward coefficient
(minimum `0.4289925585...`).  This does **not** imply positivity on the whole
carrier-killing cone.  Combining a descending ray with a small full hitter
gives the exact port-Gram-orthogonal direction

```text
-(02;2,0) + (57;0,2) - (1/10)(26;1,0) - (1/10)(47;1,0),
```

which has no active carrier among all 168 stars and 560 triangles and has
outward coefficient in
`[-1.1673273435176432,-1.1673273435175493]`.  Thus the finite-boundary arm of
the dichotomy needs either an iteration of exact boundary descent or a
different well-founded quantity; inclusion-minimal support positivity is not
a valid normal-cone certificate.

The correct established framework for testing a gap on an unbounded
semialgebraic stratum is the tangency variety/asymptotic critical-value
construction.  Pham proves that boundedness, attainment, compact sublevels,
and coercivity are characterized by the tangency variety in
[Tangencies and Polynomial Optimization](https://arxiv.org/abs/1902.06041).
Jelonek's nonproperness set records precisely the target values approached by
unbounded source sequences; see [The set of points at which a polynomial map
is not proper](https://doi.org/10.4064/ap-58-3-259-266).

For each fixed algebraic no-cap incidence chart, an asymptotic minimizer must
lie in the radial Fritz--John system

```text
grad P = sum_i lambda_i grad g_i + nu*A,
g_i(A)=0,
||A|| -> infinity,
```

with active inequalities and singular multiplier branches retained.  Curve
selection at infinity then produces a Puiseux arc.  The existing phase-base
jet computations are hand-resolved pieces of precisely this tangency-at-
infinity system: orders four through six are closed and order seven has eight
primitive packets.

The useful dichotomy for the auxiliary mixed-output energy is not simply
`P >= epsilon`:

```text
P -> 0 along a balanced no-cap sequence
    => finite limit on an active-cap boundary
       OR an asymptotic critical Puiseux arc at infinity.
```

These branches concern approximate pure-normalized sources, not the exact
fibre.  They are hostile controls for proposed inequalities.  The exact-fibre
minimum-norm proof has neither branch: closedness plus coercivity gives an
attained minimum directly.
The current order-seven finite antichain attacks one canonical balanced
base-locus type; a global theorem still needs a finite reduction of all
possible moment-zero base types or a source-faithful argument that selects
that type.

## Decision rule

Use the conormal lane on the global minimum of the **full exact fibre**.  It
exists under the counterexample hypothesis and is automatically no-cap by
exact descent plus the six-site theorem.  Add every blockwise
`A_e perpendicular ker(T_e)` condition before attempting a global
elimination.  Keep the singular Fritz--John branch `alpha=0`.  Tangency at
infinity and finite active-cap normal cones remain useful only for auxiliary
mixed-energy experiments; they are not logical branches of the exact-fibre
minimum-norm proof.

## Nonexact common-matching response control

At the common-matching pair-product source

```text
A_01=A_23=A_45=A_67=I_3,       all other blocks zero,
```

the output is **not** `Delta_8`: it has 81 nonzero words, namely three pure
and 78 mixed words, all with coefficient one.  For example `00000011` has
coefficient one.  This must therefore be read only as a pure-normalized
response control, never as an exact-fibre boundary.  Its 216 off-matching
first-order cells have zero mixed Jacobian columns; the exported 912
quadratics and 104 order-two carrier responses are homogeneous diagnostics
around this nonexact base.

The full stabilizer-invariant ansatz assigns the same oriented matrix `M` to
all 24 off-matching blocks, with `M^t` under reversed edge access.  Exact
restriction compresses the 912 equations to 114 nonzero quadrics in the nine
entries of `M`.  Their reduced characteristic-zero Groebner basis has size 42,
dimension zero, and quotient length 28.  The diagonal entries are nilpotent of
exponent two and the off-diagonal entries of exponent three.  Since the ideal
is homogeneous, its algebraic-closure zero set is exactly `M=0`.  At zero all
three canonical order-two carrier matrices vanish, so no nonzero activity
functional can lie in their row spaces.  Therefore there is no
stabilizer-invariant solution of this response control.  This is not a
tangent-cone theorem for the exact fibre.

The structural compression is literal.  For each two anchor pairs
`A={a,a'}`, `B={b,b'}`, the order-two tensor is

```text
R_AB(i,i';j,j') =
    Y_ab(i,j) Y_a'b'(i',j') + Y_ab'(i,j') Y_a'b(i',j).
```

Summing these six four-cycle reconnection tensors reproduces all 8,748 source
matching terms and, after quotienting by the 33 direct-correction directions,
exactly the same 912-row space.  Changing the crossed `+` to `-` changes 2,673
literal output rows and the quotient constraint family, providing a hostile
sign guard.

The invariant failure is not an emptiness result.  An exact Boolean
singleton/cancellation census proves that fewer than ten live off-matching
cells cannot both avoid a singleton in the 912 quadrics and give every active
carrier a diagonal response column.  A ten-cell support exists:

```text
(04;2,1) (05;1,0) (06;2,0) (13;2,0) (16;1,0)
(24;2,1) (26;0,1) (27;1,0) (34;1,0) (57;1,0).
```

With all ten coefficients equal to one, every raw order-two mixed amplitude is
zero, so all 912 quadrics vanish without a direct correction.  Exact rational
row reduction of every order-two carrier matrix shows actual activity-blocker
membership for all 104 formerly active carriers, not just nonzero response or
column coverage.  The support has trivial stabilizer and orbit size 2,304
under `(S_2 wr S_4) x S_3`.

Thus a literal non-invariant ten-cell quadratic response pattern survives,
but it is not a no-cap jet of an exact source.  The order-zero mixed residual
already prevents any formal or Puiseux exact-fibre arc based here.

### Higher-order hostile diagnostic

For `A(t)=A0+tY`, order zero already has the 78 mixed failures above.  If
that failure is deliberately ignored, the higher homogeneous coefficients are

```text
[t^2]F = 0,
[t^3]F: 12 nonzero words from 12 source terms,
[t^4]F: 3 nonzero words from 3 source terms.
```

Reduction of the order-three vector against the exact 33-dimensional mixed
image of the base Jacobian leaves 12 nonzero cokernel rows.  Six are stronger
literal certificates: their base-Jacobian row is identically zero.  The
lexicographically first is

```text
word       00010110
matching   01 | 26 | 34 | 57
cells      (01;0,0) (26;0,1) (34;1,0) (57;1,0)
coefficient 1.
```

No order-three source correction can affect that output word.  The raw
order-four vector also has a nonzero cokernel projection (three residual
rows).  Both facts are diagnostics only: there was never an exact-fibre
formal branch because order zero already fails.

The complete leading carrier replay is nevertheless internally consistent.
The 624 carriers blocked at the base have blocker membership at response order
zero; all 104 formerly active carriers acquire exact blocker membership in the
order-two response.  Thus the leading census is `728/728` blocked.  This does
not promote the order-zero memberships to full `Q((t))` incidences, and no such
promotion is relevant to the exact-fibre proof; the base is nonexact.

## Supersession: the full exact fibre is automatically no-cap

The earlier attained-interior/finite-cap-boundary/infinity trichotomy applies
to relaxed `X_k` and separately imposed no-cap incidence strata.  It is not
the right framework on the full exact `N=8,D=3` fibre.

Indeed, suppose `F_8(A)=Delta_8` and `(p,q,K)` is any active clean cap in
the exact sense of the descent theorem:

```text
s*kappa_0*kappa_1*kappa_2 != 0,       E_pq(K)=0.
```

Exact clean-pair descent then constructs arbitrary complex endpoint-ordered
aggregate blocks on the remaining six sites with matching tensor
`Delta_6`.  This is exactly the scope excluded by the certified arbitrary-
complex six-site theorem.  Therefore every hypothetical point of the exact
eight-site fibre has no active clean cap.

There is no interface gap with the 728 response carriers.  A passing star or
triangle row-space test is equivalent to an active `K` whose response is
supported in that carrier; pairwise-intersecting support makes the canonical
eight-site cap error vanish.  Thus a passing carrier is an active clean cap
and is impossible on the exact fibre.  The converse is not claimed: failure
of all 728 carriers is only a finite sufficient-support residual, while a
wider response can be clean by cancellation.

Consequently minimizing norm over the whole exact fibre is safe.  In fact the
conclusion is stronger than “attained minimum versus infinity”: the fibre is
closed in `R^504` and the squared Hermitian norm is coercive, so any nonempty
fibre has an attained global minimum.  There is neither a finite active-cap
boundary nor an infinity branch for this particular minimization.

### Smallest safe ED interface

More strongly than the single-edge statement, every pairwise-intersecting
edge family is an exact affine block.  The maximal such families are the eight
full seven-edge stars and the 56 site triangles.  At a full-fibre norm minimum,

```text
A_E orthogonal to ker L_E
```

for all of them: 63 scalar columns per star and 27 per triangle.  These are
genuine affine fibre lines and require no regularity assumption.  The
single-edge corollary fixes the other 27 blocks and writes

```text
F(A)=T_e A_e+b_e.
```

Every `h in ker T_e` gives a genuine affine line in the full fibre, not just
a Zariski tangent.  Hence a global norm minimum satisfies

```text
A_e orthogonal to ker T_e                      (all 28 edges).
```

The nine columns of `T_e` occupy disjoint endpoint-word supports and carry
the same six-site residual tensor.  Therefore `rank T_e` is zero or nine,
and the blockwise condition becomes the exact implication

```text
H_6(A restricted to B minus endpoints(e))=0  =>  A_e=0.
```

On the regular Euclidean-distance branch, the full normal equation

```text
F(A)=Delta,                    A=J_A^* lambda
```

can be compressed from 6,561 output multipliers to 252 source-sized
multipliers:

```text
F(A)=Delta,                    A=J_A^* J_A eta,
```

because `im(J_A^*)=im(J_A^*J_A)` in the Hermitian realification.  Euler's
identity `J_A A=4Delta` is an exact guard.

At an exact GHZ point literal full column rank is impossible: the target torus
orbit tangent has dimension `21-s` inside `ker J_A`, so
`rank(J_A)<=231+s`.  If the induced map on `E/im(T0.A)` has full column rank,
then `ker J_A=T0.A`.  Balance at the global minimum makes `A` orthogonal to
this kernel, so the regular ED equation is automatic on this quotient-rigid
branch.  Its leverage requires an extra quotient-kernel direction plus
second-order information, or one of the exact star/triangle block conditions.

The naive singular Fritz--John branch must **not** be used.  In the redundant
6,561-coordinate output presentation,

```text
alpha=0,        J_A^* lambda=0,        lambda!=0
```

holds at every source for dimensional reasons:
`dim_C ker(J_A^*) >= 6561-252 = 6309`.  A discriminating singular branch
requires a pointwise independent local generating set for the fibre ideal,
or the actual real normal cone/tangent cone after quotienting these universal
output-cokernel directions.  The current smallest exact system is therefore
the full fibre plus all star/triangle least-norm block equations and the
source-sized regular Gram equation after quotienting `T0`, with the singular
locus kept as a separate local-ideal problem.

## T0-quotient rigidity and terminal rank-direction audit

At an exact `N=8,D=3` GHZ point put `s=dim ker G_A`.  The exact complex

```text
Lie(T0) --G_A--> E^252 --J_A--> W^6561
```

has `rank G_A=21-s` and `J_A G_A=0`.  Thus the quotient source has dimension
`231+s`.  There are exactly two first-order branches:

```text
rank(J_A)-s = 231   <=>   ker J_A=im G_A   (quotient rigid),
rank(J_A)-s <=230   <=>   ker J_A/im G_A !=0.
```

In the rigid branch the fibre germ is regular of dimension `21-s` and equals
the local `T0` orbit germ.  In the second branch an extra Zariski tangent
exists, but its integrability and the sign of the constrained Hessian remain
separate.  This must not be confused with the older direct contradiction:

```text
X5 + 728 blocked => rank(J_A)-s >=232,
```

which would contradict equivariance immediately.  Neither direction is
currently proved.

Literal exact controls confirm sharpness.  The exact `n=4` GHZ source has
`s=6`, orbit tangent dimension three, `rank J=51`, and no quotient kernel;
the exact `n=2` control is likewise quotient rigid.  `W40` is quotient rigid
only at the `X4` rung (`rank-s=231`) and has an active carrier.  `W25` is all
blocked only at `X3`, where `rank-s=209`, and violates higher output rows.
Thus exact GHZ, the full `X5` equations, and all-carrier incidence are all
load-bearing in any rank implication.

The 1,638 zero-tail rows support neither inequality: they are mixed-amplitude
values after restriction to the diagonal `e=t=0` chart, so their factorization
only sees the pulled-back Jacobian and loses normal derivatives.  The 13-block
identity also supports neither inequality: its carrier `rho` rows are
degree-two Hessian responses, not cubic first-Jacobian rows, and the frozen
non-GHZ blocker/stationarity guard rules out a local blocker-to-rank shortcut.

The smallest source-faithful nonlinear substitute is branchwise Fitting data.
On one exact `X5+blocked` pivot chart with fixed `s`, choose an explicit
complement to `im G_A` and reduce the maximal quotient-Jacobian minors modulo
the full chart ideal.  Universal vanishing would establish `rank-s<=230`;
a live maximal minor only reaches quotient rigidity and would still need one
additional independent row for the direct `>=232` contradiction.

Quotient-rigidity checker logical digest:
`dc558db51593560af0d98f00dd1d4a8e8a42974c7fd2626d751bee7e5103b411`.
