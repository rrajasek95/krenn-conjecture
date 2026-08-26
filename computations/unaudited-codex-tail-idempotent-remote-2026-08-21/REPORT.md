# Tail idempotent split and remote carrier target

Status: **UNAUDITED exact structural PASS**.  The idempotent split is
constructive once a full-tail relation `J=J^2` is proved.  It does not by
itself force a clean-cap blocker to clear.

## Constructive split

Let `A=R/I` and let the tail ideal `J=(T_1,...,T_n)` be finitely generated.
Assume `J=J^2`.  Choose a matrix `B` with entries in `J` such that

```text
T = B T.
```

Set

```text
d=det(I-B),  e=1-d.
```

Adjugate multiplication shows `dJ=0`; since `d=1 mod J`, one has `e in J`,
`ex=x` for every `x in J`, and therefore `e^2=e` and `J=eA`.  The Chinese
remainder split is

```text
A = A/(e) x A/(1-e).
```

On `A/(e)`, `J=0`: this is the zero-tail factor.  On `A/(1-e)`, `e=1` and
`J=A`: this is the remote factor.  This construction is conditional on a
relation for the full 168-generator tail ideal.  The current 380-by-12
theorem does not provide that relation by itself.

For the exact cyclic obstruction

```text
A=Q[x,y,z]/(x-yz,y-xz,z-xy),
```

take

```text
B = [[0,z,0],[z,0,0],[y,0,0]],  e=z^2=1-det(I-B).
```

Then `e=0` is the origin and `e=1` contains the four nonzero sign points.
The checker replays explicit ideal identities for idempotence and for
`(1-e)x=(1-e)y=(1-e)z=0`.

## Carrier blockers do not follow from the split

Modulo the remote equation `1-e=0`, each carrier still has its independent
cap-response matrix

```text
L_C : K^9 -> response cells outside C
```

and activity forms `K00,K11,K22,<K,A_pq>`.  Activity requires all four
forms to be outside `rowspan(L_C)`.  The equation `e=1` says only that the
tail cells generate the unit ideal; it supplies no augmented cap minor.  In
the cyclic toy one may adjoin `L=I_9`, after which all four blockers lie in
the row space on the remote factor.  This is an exact logical countermodel
to an idempotent-only cap implication, not a source-faithful X5 point.

The determinant systems are distinct.  Tail rescue determinants are Fitting
minors of a 380-by-12 source-coefficient module.  Carrier certificates are
augmented minors of 90-by-9 or 108-by-9 cap-response matrices.  No frozen
source identity maps one Fitting ideal to the other.

Two source-coordinate controls make this independence concrete.

- W40 has an active star cap at `(67,5)` with carrier rank one and explicit
  augmented 2-by-2 determinants `1,1,-1,1`.  Yet ten of its twelve fixed-tail
  `D611` cofactors vanish.  It also has
  `F_20002111=-1`, so it is X4 but not X5 and is only a cap positive control.
- For lexicographic edge index `k`, set
  `A_edge[i,j]=1+((k+i+2j+ij) mod 13)`.  All twelve `D611` cofactors are
  nonzero, but all 168 star and 560 triangle matrices have rank nine.  Thus
  every activity form is blocked.  This dense positive source fails every
  mixed X5 target, so it proves precisely that the tail determinant alone
  cannot imply a cap; the X5 equations must do the work.

## Exact remote ideal target

After constructing and clearing denominators of `e`, the remote no-cap
obligation is finite.  For every rank-stratified blocker branch `beta`, prove

```text
1 in ( I_X5 + I_rank(beta) + I_membership(beta) + <1-e> )
```

after localizing at the declared tail rescue factors and one chosen nonzero
rank minor for every carrier.  For a carrier of rank `r`, `I_rank` contains
all `(r+1)` minors of `L_C`; after choosing blocker `i_C`, `I_membership`
contains all `(r+1)` minors of `[L_C;ell_i_C]`.

An idempotent-free pointwise form introduces 168 variables `lambda_j` and
adds

```text
1-sum_j lambda_j T_j=0.
```

Over a field this is equivalent to `T!=0`.  It is the smallest direct
Rabinowitsch target for the remote locus, still coupled to the finite no-cap
branches.  No unit certificate for this target is presently frozen.

## The 1,638 zero-tail rows and existing closures

The terminal diagonal packet splits exactly as follows.

| profile | count | literal row | existing interface | coverage |
|---|---:|---|---|---|
| `6+2+0` | 168 | `Haf(G_c[V\{a,b}]) g^d_ab` | directional entry/cofactor | proper chart/mate closures |
| `4+4+0` | 210 | `Haf(G_c[S]) Haf(G_d[S^c])` | complementary Q/Q mate rows | twisted-44 and other proper charts |
| `4+2+2` | 1260 | `Haf(G_c[S]) g^d_ab g^e_cd` | trichromatic Q/edge/edge rows | no global three-colour closure |

Thus every type is recognizable in the existing diagonal/mate library, but
the library is not an exhaustive cover of their common normalized scheme.
The missing terminal theorem remains containment in the 728-carrier activity
open, or emptiness of the diagonal scheme.

## Replay

```sh
python3 computations/unaudited-codex-tail-idempotent-remote-2026-08-21/audit_tail_idempotent_remote.py --write-results
python3 -O computations/unaudited-codex-tail-idempotent-remote-2026-08-21/audit_tail_idempotent_remote.py
python3 -I -S computations/unaudited-codex-tail-idempotent-remote-2026-08-21/audit_tail_idempotent_remote.py
```

All modes have byte-identical stdout/result SHA-256
`b92370d3de3265d9e8840b69fef5871e5114f647bf25427569a77e0b42ff2866`;
the logical digest is
`131952ef3a7dc4762cb5ebf105ed9bcc9dd0fc5971088a48ef9ab7a84c64fff2`.
