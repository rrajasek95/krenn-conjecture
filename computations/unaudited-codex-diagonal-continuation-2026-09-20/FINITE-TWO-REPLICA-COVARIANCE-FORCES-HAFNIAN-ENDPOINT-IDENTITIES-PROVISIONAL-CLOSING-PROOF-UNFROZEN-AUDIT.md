# Independent complete audit of the finite-replica endpoint proof and its full closing chain

**Analytic review: PASS, with no remaining mathematical correction identified.**
Reviewer: `/root/audit_det_bridge`, 2026-09-26. This audit independently
reconstructs the saved endpoint argument and every section of the complete
proof. Prior audit labels, numerical evidence, and the anticipated conclusion
were not used as premises. The conclusion is a written mathematical proof;
this is neither a Lean certificate nor external peer review. Root review and
publication status are separate from this independent audit.

## Exact reviewed texts

| Text | Lines | Bytes | SHA256 |
| --- | ---: | ---: | --- |
| [Complete proof](../../proofs/krenn-gu-all-orders-two-replica-proof.md) | 336 | 15658 | `fb0fa1e9447d8044981692d6e9bbbeff8e6a2cfc90119b6a296cbf506b9a3c9d` |
| [Endpoint source](FINITE-TWO-REPLICA-COVARIANCE-FORCES-HAFNIAN-ENDPOINT-IDENTITIES-PROVISIONAL-CLOSING-PROOF.md) | 243 | 10550 | `e5e9e1ba7a396e307ce176bfdd75c1c905e1fd33e5f6b75acd5bac18a542a230` |

The full proof was read at its earlier 335-line bytes and the one-line
precision amendment was then inspected. The final text explicitly
differentiates `K(E(P_1 x+Qc_1 y),Z)` before restricting `Qc_1=0`.
The mathematical calculation below already uses that full expression.
The subsequent rendering and grammar amendments were also inspected:
braces replace parentheses after `[k^S]`, and `an assumed` replaces
`a assumed`. They do not change either mathematical argument.

The load-bearing foundations were also read completely. Paths in this table
are in `../unaudited-codex-higher-common-power-bridge-2026-09-05/`.

| Text | SHA256 |
| --- | --- |
| `UNIFORM-ALL-ODD-DIAGONAL-RESPONSE-FACTORS-AND-NULL-PAIR-TRANSFER.md` | `3f75dcf21adffb42369985efe37ef947152b4db8f2ad8192bff36031fa3f612c` |
| `UNIFORM-ALL-ODD-TWO-COLOR-MIXED-VANISHING-AND-KERNEL-PENCIL.md` | `03edf88285ca2a0d1dda8354d266b5d3e329be05149129e8843b2bb2dd9a12e1` |
| `UNIFORM-THREE-ACTIVE-COLOR-HIGHER-PURE-RESPONSE-VANISHING.md` | `14811c0332c217e1a5520bd619482f641573b9456783404f48a93dbc3542b190` |
| `UNIFORM-ALL-EVEN-OMISSION-PURE-RESPONSE-VANISHING.md` | `450f75c2c6280c601e2d012c1ae892d1f18f14f62aae8ec5dd448c3a157b7688` |
| `UNIFORM-GLOBAL-EDGE-MONOCHROMATICITY-AND-COFACTOR-INVERSE.md` | `4e140eb5cd74a4e0d9869f76e975ce2f7d46c8d7d1ba9be332a8128424082e89` |

The complete source [notes/termwise-rank3-cubic-uniqueness.md](../../notes/termwise-rank3-cubic-uniqueness.md),
SHA256 `d4b6ccb09a184bb28fc9854f798b368c4e714ac66d3b020114f0fede418642c3`,
was checked specifically for its Section 3 analytic graph argument. None of
its finite graph enumerations is required or was replayed for this audit.

## 1. Algebraic model and arbitrary weighted source scope

The physical-site-square-zero algebra counts exactly ordinary perfect
matchings: expanding a divided quadratic power counts each collection of
disjoint unordered edges once. Arbitrary endpoint-color cells are legitimate
coefficients of that quadratic. Parallel cells with the same endpoint colors
aggregate by addition, including cancellation to zero. Zero aggregate cells
can be removed. Symmetry here exchanges physical endpoints and their local
coordinates; no Hermitian or positivity assumption is imposed.

Projection of a larger target palette onto any three active coordinates
preserves the three target coefficients and all coefficients in their
receiving palette. Thus the claimed even-order obstruction applies to every
target dimension at least three. The proof concerns finite complex edge
weights, and does not rule out a singular coefficient-image limit by the same
argument. Such limits do not satisfy the finite-source hypotheses used below.

## 2. Independent reconstruction of reflection and the whole odd tower

Use ordinary labeled Wick variables with the actual quadratic covariance,
zero covariance within a physical site, and a hollow auxiliary with row
covariance `L`. With `p` auxiliary occurrences, their `p!` assignments to
distinct physical variables exactly give the raw row power `L^p`; the
remaining matching factor is the divided power of the actual core.

In two independent identical replicas, the displayed rational orthogonal
reflection preserves every covariance, fixes `s g_1+t g_2`, and negates
each local determinant. At odd physical order its total determinant sign is
minus one. Coefficient extraction in `s,t` therefore gives the complete
antisymmetric identity, with a harmless nonzero binomial factor. Equality on
the generic parameter locus extends polynomially to isotropic parameters.

Constant local color pairs give `f_b t_a=f_a t_b`. Independent linear
functions `f_a,f_b` are coprime in the coordinate ring of the actual row
space, so the pure responses have one common polynomial factor. A mixed
receiving word avoiding an active third color has exactly one possible
constant complementary word. Its coefficient multiplied by that third
target function is zero, so polynomial cancellation kills that whole binary
mixed coefficient, including where the function's point value vanishes.

The shifted odd Wick tensor is the finite sum of raw odd responses divided
by their row factorials. In a binary palette it is exactly the common even
polynomial `g(L)` times the original two-target response. Replica rotations
preserve its alternating contraction. The nonzero target determinant can be
cancelled in the integral domain before setting the second mean to zero.
The 45-degree rotation then gives `g(L/sqrt(2))^2=g(L)`. Finiteness and
`g(0)=1` force `g=1`; homogeneous degree separation and polarization give
the whole higher binary tower, including its terminal odd degree.

At every original root of a full ternary source the three root rows have
three independent pure responses. These are exactly the rows to which this
argument is applied. No higher response of a repaired or unrelated core is
being assumed, and an all-three-color higher tensor is never discarded.

## 3. Independent reconstruction of even omission and diagonalization

After omitting a second physical site, the coefficient of its color `h` in
the shifted odd tensor is literally `d_h E(U)+E_(V_h)(U)`: that site is
occupied by a mean or by its actual star edge. The even finite mean has zero
first derivative at zero. Two-replica rotation gives both identities (4) of
the complete proof, the second by differentiating means `U,U+tV` at zero.
Substituting the original omitted-site boundary at `L` and at `sqrt(2)L`
cancels the direct term `d_h`; this yields
`f_h(L)[k^S](E(U)-E(0))=0`. The cancellation is in a polynomial ring on
the original row space. Homogeneous separation and polarization give the
degree-two even omission identity also at the `m=1` endpoint.

The diagonal entry of `B_ih C_h` is the original one-defect coefficient.
For its off-diagonal entry `p,q`, expanding each literal deletion hafnian at
the retained vertex `p` gives the ordered two-row sum in (6). The ordered
sum agrees with the raw row product, including the two orders when the rows
coincide. Hence no factor of one half is missing. The even omission identity
kills that sum, while the diagonal entries are `delta_(i,h) tau_h`.

Since `tau_h` is nonzero, `M_h C_h=tau_h I` makes the actual scalar cofactor
matrix invertible. Thus `B_ih C_h=0` for `i!=h` kills every original
off-color cell. This is ordinary scalar matrix inversion; neither a retained
zero-top inverse nor scalar closure under cofactor iteration is invoked.

## 4. The new endpoint argument, checked independently

Fix a physical supported B edge `pq`, so `d=B_pq!=0`, and any other active
color H, so `eta!=0`. No condition on `e=H_pq`, `alpha`, `gamma`, or physical
endpoint-row independence is needed. The endpoint source even permits
`beta=0`; only its matching corollary needs `beta!=0`.

The four endpoint boundary equations follow by expanding the original odd
mean at the other root. Its degree-one term is the full binary top, and every
higher binary coefficient is zero by the original tower. The terminal
`N+1` coefficient is included; it is not lost because the retained even
mean itself has maximum degree `N`. Differentiating these mean parameters
with the retained quadratic fixed is legitimate polynomial differentiation.
It gives `E_v(sx)=E_u(ay)=0`, `E_yu(sx)=-ds E_u(sx)`, and
`E_uv(0)+eF=eta h^U` with the displayed factorials.

The complementary tensor pairing is symmetric at even retained order.
Its two-replica finite Wick kernel is O(2)-invariant: rotations preserve each
local determinant, and a reflection contributes `(-1)^N=1`. Consequently
the matrix of one u derivative and one v derivative transforms covariantly.
Its off-diagonal entries vanish on the separate coordinate axes and are
literally divisible by `P_1 Q_2` and `P_2 Q_1`.

On a dense locus rotate P or Q onto an axis. This proves `MP` parallel to
P and `M^T Q` parallel to Q. The two eigenvalues agree where `P dot Q!=0`.
In dimension two their residual rank-one matrix is a multiple of
`(P dot Q)I-P Q^T`. The literal off-diagonal quotient is polynomial, so
there is no residual division by a Gram determinant or by physical row
entries: `M=a_0 I+b P Q^T` holds everywhere polynomially. Uniqueness on
the generic locus makes both coefficients invariant; adding `e f I` preserves
that conclusion.

The invariant ring calculation is correct over C. In torus coordinates its
generators are `sigma,tau,z,w` with `zw=sigma tau`; reflection swaps z,w.
Averaging a representative and using symmetric polynomials gives precisely
`C[sigma,tau,c]`, `z+w=2c`. The axis substitution has dense image because
every `tau!=0` and arbitrary `sigma,c` can be realized with complex square
roots. Thus it is an injective substitution of polynomial rings.

On `Q_1=0`, the original equation `E_yu(sx)=-ds E_u(sx)` gives
`partial_(Q_1) M_12=-d P_1 M_12`. In invariant coordinates this is
`P_1^2 Q_2(b_c+d b)=0`. Cancel only auxiliary polynomial monomials and
use the injective axis substitution. Since d is a fixed nonzero complex
number, a finite polynomial satisfying `b_c+d b=0` must be zero by its
highest power of c. There is no formal-series or localization inference.

Now the full expression for the second diagonal entry is
`T_22=K(E(P_1 x+Q_1 y), E_uv(P_2 x+Q_2 y)+e E(P_2 x+Q_2 y))`.
Differentiate it before taking `Q_1=0`. The original y boundary gives
`partial_(Q_1)T_22=P_1 beta eta-d P_1 T_22`: the second factor's pure-H
coefficient is exactly eta, since every positive B mean insertion forbids
an all-H word. With `b=0`, invariant-coordinate differentiation and the
same injective substitution give `a_c+d a=beta eta`. Finiteness forces
`a=beta eta/d`. At the parameter origin the same entry is
`K(F,E_uv(0)+eF)=eta alpha`. Thus `beta=d alpha` follows with no missing
sign or scalar factor.

## 5. Matching conclusion and complete terminal graph argument

Expand the ordinary B hafnian at any vertex. Every supported summand now
equals beta, so `deg_B(p) beta=beta`. For nonzero beta and characteristic
zero, every vertex has exactly one B neighbor. Repeat for all three colors.
Two resulting colored matchings cannot share a physical edge: that edge
in one color and the retained other-color matching produce a mixed word
with a unique nonzero weight product when n>=4. Thus the union is simple
cubic and properly colored. A receiving word determines at most one
colored perfect matching because each vertex has exactly one available
edge of the requested color. Weighted cancellations have therefore been
eliminated by the endpoint argument, not assumed away earlier.

The complete proof's minimal-arc graph argument independently reconstructs.
If a union of two colors has several alternating cycles, switching only one
cycle gives a mixed matching. Otherwise it is Hamiltonian and the third
matching consists of chords. An opposite-parity chord leaves cycle paths
with even vertex counts and gives a mixed matching. Hence every chord joins
equal parities. Interlacing even-even and odd-odd chords give another mixed
matching for n>4, because two chords then form a proper subset of the third
matching. So no opposite-parity chord pair interlaces. A chord side with
minimum interior size contains opposite-parity vertices; their partners
must stay inside, yielding a strictly smaller interior chord side. This is
the required contradiction. Disconnected unions were already covered by
the alternating-cycle switch.

The checked primary statements agree with exactly this final scope:
Bogdanov's bound in [Chandran--Gajjala, Theorem 1](https://arxiv.org/html/2202.05562v2)
applies to simple finite loopless graphs. The multigraph version is also
stated as Theorem 7 in the HTML of [Chandran--Gajjala--Illickan](https://arxiv.org/html/2407.00303v1).
Neither paper's separate weighted sparse-class theorem is imported.
The elementary argument above is sufficient on its own after the proved
matching reduction.

## 6. Four-site and other scope boundaries

All algebraic steps remain valid at n=4: the odd root core has three sites,
the retained mean is `Q+L^2/2`, empty hafnians equal one, and the degree-three
terminal odd response is part of the original tower. The graph step then
allows K4. Its three edge-disjoint matchings, with nonzero weights, give the
permitted ternary source. The interlacing two-chord construction at n=4 is
the complete third matching and therefore supplies no mixed-word contradiction.

At n=2 neither the odd-core lemma nor the even omission theorem is claimed,
and the edge-disjointness argument lacks a retained mixed word. Arbitrary
two-site target dimension is consequently not excluded. Odd order has no
perfect matchings in this ordinary quadratic model. The argument excludes
every full ternary source of even order greater than four, with arbitrary
finite complex weights and arbitrary density, and its palette projection
gives the stated higher target-dimension scope.

No new computation, family classification, support minimum, matching-safe
selection, source descent, derivative-ideal stability, or cofactor dual
scalar theorem is required for this conclusion. This audit creates only
this fresh review file; it does not edit the reviewed proof, endpoint
source, any prior receipt-bound file, or the external README.
