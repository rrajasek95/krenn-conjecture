# Framed-quiver audit for the eight-site GHZ equation

Status: **the quiver reformulation is exact only as a graph-tensor/involutive
quiver, and it supplies no larger stability mechanism**.

## 1. Source-faithful tensor representation

Let `V_i=C^3` at the eight sites and

```text
E = direct_sum_(i<j) V_i tensor V_j.
```

The 3-by-3 edge block `A_ij` is a tensor, not an ordinary arrow.  The full
site base-change group `G=product_i GL(V_i)` acts by

```text
A_ij -> (g_i tensor g_j) A_ij.
```

The matching/Hafnian map

```text
H:E -> tensor_i V_i
```

is degree four and `G`-equivariant.  This is literal: each of the 105
perfect-matching summands contains every site representation exactly once.
The target equation is

```text
H(A)=Phi,       Phi=sum_(c=0)^2 e_(0,c) tensor ... tensor e_(7,c).
```

Consequently a base change preserves the framed equation exactly when it
stabilizes `Phi`.

## 2. Largest actual base-change group

For sites `i,j`, contract `Phi` at the other six sites.  The resulting
intrinsic subspace is

```text
D_ij=span(e_(i,c) tensor e_(j,c): c=0,1,2).
```

A point `diag(a0,a1,a2)` of this plane has tensor rank one precisely when

```text
a0*a1=a0*a2=a1*a2=0.
```

Thus its projective rank-one locus is exactly the three coordinate lines.
Every stabilizer must permute those lines; consistency for all site pairs
forces the same permutation at all eight sites.  Therefore

```text
g_i e_(i,c)=d_(i,c)e_(i,sigma(c)),
product_i d_(i,c)=1,
G_Phi = T0 semidirect S3.
```

The exact infinitesimal replay gives 48 off-diagonal equations and three
independent diagonal-sum equations inside `gl(3)^8`: orbit rank 51 and
stabilizer dimension `72-51=21`.  The six common permutations give the six
components.  Ordering the three global GHZ summands removes `S3`; fixing the
three local frame vectors removes the torus as well.  No framing convention
enlarges the continuous group beyond the already-audited 21-torus.

## 3. Why this is not an ordinary King quiver

An ordinary arrow `i->j` transforms as `g_j A g_i^-1`.  The edge tensor can
instead be viewed as

```text
V_i tensor V_j = Hom(V_i^*,V_j),
```

which transforms as `g_j A g_i^T`.  Hence every physical edge would have to
join a dual site vertex to a primal site vertex.  A single-space-per-site
ordinary quiver model exists only if the physical graph is bipartite.  The
checker exhausts all 256 two-colourings of `K8`; none works, already because
of triangle `01,12,02`.

One can double each site into primal and dual vertices, but source
faithfulness then imposes

```text
g_(i,-)=g_(i,+)^(-T).
```

This is an involutive graph-tensor representation, not the independent
vertex base-change action used by ordinary King stability.  Forgetting the
constraint creates artificial one-parameter subgroups that do not act on
the source equation.

## 4. King stability and HN filtrations

For an ordinary quiver, a character `theta` with `theta.d=0` gives the usual
sign test on `theta(dim W)` for every subrepresentation `W`, and the
Harder--Narasimhan filtration is formed from the associated slopes.  Two
obstructions prevent using that criterion here:

1. the ordinary quiver action is not source-faithful; and
2. the fixed GHZ equation provides no distinguished nonzero King character.

On the actual stabilizer, the natural character is zero, which yields no
destabilizing filtration.  If the three local GHZ vectors are used as
generating framings, they already span every `V_i`; any subrepresentation
containing the framing is the whole representation, independent of the 28
edge blocks.  Standard cyclic framed stability is therefore vacuous.

This also misses the geometry of a clean cap.  A cap is a matrix `K` in the
kernel of a 90-by-9 or 108-by-9 response matrix, with four activity forms
nonzero.  It is not a collection of site subspaces preserved by the 28 edge
maps.  No source-faithful King/HN subrepresentation canonically produces
such a `K` or a strict `N8->N6` support descent.

As an exact control, W25-F8 is cyclically stable under the full local GHZ
framing for the trivial spanning reason, yet passes none of the 168 star or
560 triangle carrier tests.  It is outside `X4` by 78 rows, so this is not a
counterexample to the conjecture; it shows that framed cyclic stability has
no formal implication to the 728-carrier cap criterion.

## 5. Terminal verdict

The framed-quiver idea introduces no new continuous symmetry: after the
target framing is respected, it is precisely the torus theory already
terminalized.  That audit found the no-cap locus nonclosed; fixed-rank repair
has zero generic degeneration cone and only support-fixing stabilizers on
the frozen 310 records.  Quiver HN therefore cannot supply the missing
promotion or descent lemma.

The cheapest viable theory target remains a non-toric initial-ideal/support
descent compatible with all 728 carrier rank strata, or direct
response-kernel/tail algebra on larger supports.

## Replay

```sh
python3 computations/unaudited-codex-x5-framed-quiver-audit-2026-08-21/audit_x5_framed_quiver.py --write-results
python3 -O computations/unaudited-codex-x5-framed-quiver-audit-2026-08-21/audit_x5_framed_quiver.py
python3 -I -S computations/unaudited-codex-x5-framed-quiver-audit-2026-08-21/audit_x5_framed_quiver.py
```

All modes return logical SHA-256
`3931cb2dec7eecfebac1106e8068a5bd065ebad4ad18b7161afe5f33b2d8237b`.

