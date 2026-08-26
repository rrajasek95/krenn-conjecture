# Fourier-Z3 virtual-symmetry audit for the fixed one-hot PEPS

Status: **terminal negative PASS**.  Fourier transformation exposes an exact
local Z3 covariance, but arbitrary Krenn bonds do not support the corresponding
edgewise pull-through.  More decisively, no proper K4 or K8 blocked region is
normal/injective or Z3-injective.

## 1. Fourier target and exact local action

Use the unnormalised Fourier matrix `F_(s,a)=omega^(sa)` and let
`Z=diag(1,omega,omega^2)`.  Then

```text
(F^tensor n) sum_a |a>^tensor n
 = 3 sum_(sum_i s_i=0 mod 3) |s_1,...,s_n>.
```

The checker evaluates every word for `n=4` and `n=8`: respectively 27 and
2187 of the 81 and 6561 coefficients are nonzero, with the asserted residue
rule.

Let `X|a>=|a+1 mod 3>` on the nonvacuum colour space and
`G=diag(1,X)` on `E=C|vac>+V`.  Since the fixed site projector `P_d` accepts
exactly one excitation,

```text
P_d G^tensor d = X P_d,
Z (F P_d) = (F P_d) G^tensor d.                 (1)
```

This is checked over `Q(omega)` on all 64 inputs for degree 3 and all 16384
inputs for degree 7.

Equation (1) is only a local covariance.  To cancel the induced virtual action
on an unoriented edge one additionally needs

```text
X A_uv X^T = A_uv.                              (2)
```

With opposite virtual orientations the corresponding condition is
`X A_uv (X^-1)^T=A_uv`.  Neither condition follows from pure normalization
and the full X5 equations.  The exact K4 GHZ witness assigns a rank-one colour
block to each edge; all six blocks fail (2), although the contracted output has
the global Z3 symmetry.  Thus target symmetry does not imply a bondwise
pull-through.

## 2. Exact blocked-map ranks

For a proper `r`-site region in Kn, the number of boundary half-edges is

```text
b = r(n-r),
M_R : E^tensor b -> V^tensor r.
```

The map always has exact rank `3^r`, independently of the internal bond
coefficients.  For the lower bound, choose one boundary half-edge at every
site, excite exactly those chosen legs, and leave every other boundary leg in
vacuum.  The resulting `V^tensor r -> V^tensor r` submatrix is the identity.
The physical codomain supplies the matching upper bound.

The K4 standard GHZ witness was also built explicitly and row-reduced over Q:

| r | b | domain `4^b` | exact rank `3^r` |
|---|---:|-------------:|-----------------:|
| 1 | 3 | 64  | 3  |
| 2 | 4 | 256 | 9  |
| 3 | 3 | 64  | 27 |

The complete K8 table is:

| r | b | domain `4^b` | exact rank `3^r` |
|---|---:|-------------:|-----------------:|
| 1 | 7  | 16,384        | 3     |
| 2 | 12 | 16,777,216    | 9     |
| 3 | 15 | 1,073,741,824 | 27    |
| 4 | 16 | 4,294,967,296 | 81    |
| 5 | 15 | 1,073,741,824 | 243   |
| 6 | 12 | 16,777,216    | 729   |
| 7 | 7  | 16,384        | 2,187 |

Therefore every proper block has a nonzero kernel.  Blocking the entire closed
graph leaves no virtual boundary and is only the tautological scalar-to-output
map; it cannot establish normality on extendible local regions.

This directly violates the load-bearing hypothesis of the normal-PEPS
fundamental theorem: normality means that a sufficiently large local blocked
tensor is injective.  The fixed edge-dependent complete graph also lies
outside the translational/uniform geometry hypotheses used in standard normal
PEPS gauge theorems.

## 3. Stronger G-injective obstruction

For either choice of boundary orientation, the Z3 representation on
`E=C+V` has character traces `4,1,1`.  Hence its invariant boundary subspace
has exact dimension

```text
dim (E^tensor b)^Z3 = (4^b+2)/3.
```

Dimension already rules out Z3-injectivity on every K8 proper block and on
the one- and two-site K4 blocks.  The remaining three-site K4 case is killed
by a coefficient-independent parity obstruction, which in fact handles every
proper region:

- paired internal bonds imply that a surviving boundary input has excitation
  count congruent to `r mod 2`;
- if `r` is odd, the all-vacuum boundary vector is invariant and is killed;
- if `r` is even, put the charge-zero excitation
  `|0>+|1>+|2>` on one boundary leg and vacuum elsewhere.  It is fixed by both
  `X` and `X^-1` and is killed.

Thus `M_R` has a nonzero kernel even after restriction to the invariant
boundary space.  It cannot have the invariant-subspace left inverse required
by G-injectivity.  This conclusion is independent of all 252 source
coefficients and therefore cannot distinguish a no-cap locus from a clean-cap
locus.

## 4. Why noninjectivity ends this route

The previously frozen invisible-chord pair changes an internal bond from
vacuum Schmidt rank 1 to rank 2 without changing a single top coefficient.
It consequently changes the local pull-through defect while preserving the
entire output tensor and every global symmetry.  This is exactly the
fixed-projector noninjectivity that normal/G-injective reconstruction theorems
exclude by hypothesis.

The relevant primary theorem scopes are therefore not met:

- the normal-PEPS fundamental theorem assumes injectivity after finite
  blocking before deriving virtual gauge equivalence;
- G-injective PEPS assumes virtual group invariance and a left inverse on the
  invariant virtual subspace.

Here the first fails by the rank table, while the second fails both at the
edge pull-through condition and at the explicit invariant parity kernel.
Failure is universal and supplies no clean-cap alternative.  The Fourier-Z3
route therefore adds no source constraint beyond the already known target
symmetry and one-hot selection rule.

Primary theorem references used for hypothesis scope:

- Molnar et al., *Normal projected entangled pair states generating the same
  state*, arXiv:1804.04964.
- Schuch, Cirac, and Perez-Garcia, *PEPS as ground states: degeneracy and
  topology*, arXiv:1001.3807.
- Acuaviva et al., *The minimal canonical form of a tensor network*,
  arXiv:2209.14358 (the broader all-contraction-graphs/orbit-closure theorem
  already audited in the pinned PEPS report).

## Replay

```sh
python3 computations/unaudited-codex-fourier-z3-peps-2026-08-21/audit_fourier_z3_peps.py --write-results
python3 -O computations/unaudited-codex-fourier-z3-peps-2026-08-21/audit_fourier_z3_peps.py
python3 -I -S computations/unaudited-codex-fourier-z3-peps-2026-08-21/audit_fourier_z3_peps.py
```

Frozen logical digest:
`4e58445b01356631bdf82309204df8713c9623ea4f0989ceef7d5cd4481468fd`.
