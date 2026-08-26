# Segre master-syzygy pullback audit

## Outcome

The literature-inspired pullback is not a new open route at its first two
layers.  The repository had already computed both layers, under different
names, and their exact combination reaches a **sharp non-forcing boundary**.

The first linear syzygy among the (2\times2) minors of the endpoint-star
Segre matrix pulls back to the literal Pluecker/star-minor transport
identity.  Its first chart-26 Buchberger cell is nontrivial—180 terms and
two new squarefree leading monomials—but the same-star critical pairs reduce
by the ordinary Eagon--Northcott/Pluecker relations.  Thus this layer
organizes the source equations without supplying a new common-power class.

On the (h=3) clean cap line, the induced presentation is exactly

\[
u^3,quad u^2v,quad uv^2,quad v^3
\]

with the three adjacent linear Hilbert--Burch syzygies.  Their total column
degree is (3), while a common-factor/Fitting contradiction requires at
most (2).  The clean Macaulay map has full rank (6), so the simultaneous
Bezout kernel is zero.  Uniformly, ordinary response Pluecker reaches total
degree (h), exactly one above the forcing threshold (h-1).

The next, differentiated layer is also already audited.  Differential
Pluecker identities genuinely strengthen transition flatness on
gauge-rigid charts and exclude the separated defect-three packet.  They do
not lower the Hilbert--Burch degree.  Adding a diagonal second polar does
not repair this: the contracted full-nine row has response grades (0,1),
while the clean tail has grades (2,\ldots,h); its second polar sees only
grade (2).

## Consequence

The phrase “use Segre master syzygies” is therefore too coarse.  Ordinary
Segre syzygies, their first Buchberger transports, and their first
differential polarization have already been tried exactly.  The genuinely
untested theorem must be a **labelled higher response--Fitting identity**:
one operation must combine at least one individually labelled diagonal
anchor with all response grades (2,\ldots,h), retaining the common
matching word and endpoint labels, and lower the presentation degree by
one.

This substantially narrows the literature-derived idea.  A useful next
construction is not another Pluecker relation; it is a source-provenant
Hasse/Spencer totalization or moment tower whose terminal is the missing
degree-((h-1)) Hilbert--Burch column.

## Reproduction

Run:

```text
python3 computations/unaudited-codex-segre-master-syzygy-pullback-2026-08-22/audit_segre_master_pullback.py
python3 -O computations/unaudited-codex-segre-master-syzygy-pullback-2026-08-22/audit_segre_master_pullback.py
python3 -I -S computations/unaudited-codex-segre-master-syzygy-pullback-2026-08-22/audit_segre_master_pullback.py
```

The checker verifies a representative first Segre master syzygy and its
rank-one endpoint-star pullback, reconstructs the (h=3) Hilbert--Burch
maximal minors, proves full clean Macaulay rank, and pins ten existing exact
source-labelled artifacts covering the Buchberger, response-Pluecker,
differential-Pluecker, and diagonal-polar layers.
