# Proper carrier-incidence compactification

Status: **exact structural PASS; negative complexity verdict at the current
tail interface**.

For a source space `X`, fixed carrier response `L(A):K^9->K^m`, and generic
rank `r`, let `S` be the universal rank-r subbundle on `Gr(r,9)`.  The
incidence

```text
I_r = {(A,W): rows(L(A)) subset W} subset X x Gr(r,9)
```

is closed: it is the zero locus of `rows(L):O^m -> O^9 -> O^9/S`.  Adding a
chosen blocker gives the closed incidence

```text
I_(r,beta) = I_r intersect {ell_beta(A) in W}.
```

The Grassmannian is projective, so projection to `X` is proper.  The smaller
space relevant to the original branch is

```text
Gamma_(r,beta) = closure{(A,rowspan L(A)):
                          rank L(A)=r, ell_beta in rowspan L(A)}.
```

It is closed and proper over its image, with
`Gamma_(r,beta) subset I_(r,beta)`, generally strictly.  Its image is the
closure of the fixed-r affine blocker branch—not the original unstratified
membership set.

The site-colour torus action lifts by

```text
(A,W) -> (lambda.A, W D_kappa),
```

because `L(lambda.A)=D_rho L(A)D_kappa`.  Diagonal blocker lines are fixed
projectively, and the direct blocker is equivariant.  Both incidences and the
graph closure are torus invariant.

## Explicit ghost plane

The pure-normalized rank-drop curve from the torus audit is itself a
pure-preserving one-parameter degeneration.  Take colour-0 site weights

```text
(0,0,1,-1,0,0,0,0)
```

and zero weights in colours 1 and 2.  Every pure character has weight zero.
On the curve, all nonzero coordinates have weight zero except
`A_27[0,0]`, which has weight one.  For the star `(67, centre 0)`,

```text
L(t) = t E_(row 12:00, column K00),
rank L(t)=1,                 t != 0,
W(t)=<K00>.
```

At `t=0`, `L(0)=0`, but the Grassmann limit is still
`W_0=<K00>`.  This is the ghost one-plane retaining the K00 blocker.  It
records the normalized leading row `t^-1 L(t)` that disappears from the
affine special fiber.

## Boundary fibers and finite signatures

Let `U=rowspan L(A_0)` have dimension `s<r`, and let the chosen blocker
`ell` be nonzero.  The full incidence fiber is:

```text
ell in U:      Gr(r-s,   9-s), dimension (r-s)(9-r),
ell notin U:   Gr(r-s-1, 8-s), dimension (r-s-1)(9-r).
```

Only the planes arising as leading rowspaces of rank-r arcs lie in the graph
closure.  For fixed `r`, the smallest nonzero-blocker rank/Schubert ledger has
`2r-1` signatures.  Summing `r=1,...,9` gives 81 per blocker type.  Modulo
colour symmetry there are two blocker types (diagonal/direct), and there are
two carrier types (star/triangle), for 324 boundary signatures before any
matroid refinement.  The direct-zero divisor `A_pq=0` is separate: its
blocker is zero and imposes no Schubert condition.

For Hilbert--Mumford limits, these signatures must be refined by the
Pluecker support/realizable column matroid, one-parameter weights, the leading
row module, and the leading direct-blocker line when it vanishes.  Matroid
types are finite on nine columns but can still carry coefficient moduli.

## Tail-response interaction

Naively pulling `I_(r,beta)` back to the X5/tail source locus does not shrink
its Grassmann fibers: tail equations contain no `W` variables.  They can
eliminate a ghost plane from the smaller graph closure only by forbidding
every rank-r X5 arc with that leading rowspace.  This is a tangent-cone/Rees
algebra condition on the carrier minor ideal.

The frozen 380-by-12 tail-response rank theorem supplies no such arc or
initial-module relation, and no frozen source identity maps its Fitting
module to the carrier complete-collineation data.  Consequently the naive
proper compactification enlarges the current state space.  A useful reduction
requires a new X5-compatible leading-row theorem; none is presently frozen.

## Diagram

```text
Z^o_(r,beta)={(A,rowspan L):rank L=r, ell_beta in rowspan L}
        | open graph
        v
Gamma_(r,beta)  ----->  I_(r,beta) subset X x Gr(r,9)
        | proper                 | proper
        v                        v
closure_X(pi Z^o)       larger closed rank-drop locus

base change to X5 preserves properness, but not Gamma=I.
```

## Replay

```sh
python3 computations/unaudited-codex-carrier-incidence-compactification-2026-08-21/audit_carrier_incidence_compactification.py --write-results
python3 -O computations/unaudited-codex-carrier-incidence-compactification-2026-08-21/audit_carrier_incidence_compactification.py --write-results
python3 -I -S computations/unaudited-codex-carrier-incidence-compactification-2026-08-21/audit_carrier_incidence_compactification.py --write-results
```

