# The silent Hasse mate has no new full-source completion branch

## Result

The rowwise divided-Hasse guard has

```text
marked pair H2(q01,q23) = +1,
silent mate H2(q02,q13) = -1,
base occupied q support = {q45[22]}.
```

All four varied cells are zero at the base.  This explains why the rowwise
guard does not itself give minimum-support deletion or a nonzero
offdiagonal active cell.

After adjoining the three normalized pure targets and all complete
five-tensor response rows, however, the full extension is exhaustive:

```text
axis-pure completion -> impossible;
off-axis completion  -> source-provenant private-site active fan.
```

Checker:
[`verify_h3_silent_hasse_pair_full_source_extension_classification.py`](../computations/verify_h3_silent_hasse_pair_full_source_extension_classification.py).

## Why the axis-pure extension is empty

Suppose every additional physical `q`, `p`, and `s` cell is axis-purified:
each `q` edge has equal endpoint colours and each endpoint row occupies its
own output colour.  Then the completed base point lies in the canonical
`h=3` axis-pure five-tensor locus

\[
 q^{[3]}=X_0,
 \qquad
 p_i s_j q^{[2]}=\delta_{ij}X_i,quad i,j\in\{1,2\}.
\]

The unrestricted global minimum-support census has only six supports, all
of size `27`, and the pinned coefficient certificate excludes all six.
After blocking them the support formula is UNSAT.  Consequently the entire
axis-pure exact-source locus is empty, not merely the smallest continuation
of the silent mate.

The direct response shadow in the guard is harmless.  It is `D*q^[3]`, hence
is `X0`-valued.  On the selected mixed word it is `D*H_001122` and vanishes
with the target row; on the complete response system it disappears after
quotienting the output by `<X0>`.  It therefore cannot evade the `q,p,s`
five-tensor equations used by the axis-pure census.

The augmented companion rows—unary Hasse, anchor, physical `q`, ridge,
ordinary residue, `eta/sigma`, `W`, and terminal readouts—are additional
equations.  They can only cut the already empty axis-pure primary locus;
they cannot create an extension.

## Classification of every surviving extension

Every full exact extension must therefore contain a nonzero off-axis
physical cell.  The target-augmented private-site identity is a literal
polynomial combination of the pure and mixed source rows, so such a cell
produces a nonzero determinant/cofactor product and hence an active fan.

The evaluated `h=3` fan theorem gives exactly two outcomes:

1. **four-good:** the existing transverse landing applies;
2. **literal pure-colour coloop:** finite Hall saturation reduces to the
   normalized Gate-II packet.

The second arm has one—and only one—unproved statement:

> Construct the fan-grade source-valid protected odd comparison `Phi`, with
> `J0 Phi = A J` and the literal physical rows `q=M-a` on both packets.

After `Phi`, packet disagreement, the anchor bright/dark alternative,
minimum target circuit, and termination are already exhaustive.  Thus the
surviving extension is not a new Hasse-pair terminal; it is exactly the
pre-existing trapped-coloop comparison frontier.

## Corrected branch map

```text
silent Hasse-pair row guard
  -> add 3 pure targets + complete five-tensor rows
       +-- all support axis-pure -> impossible
       `-- a nonzero off-axis cell -> active fan
              +-- four-good -> landed
              `-- literal coloop -> trapped Hall shore
                     `-- OPEN fan-grade Phi/q=M-a comparison.
```

This is exact at canonical `h=3` in characteristic zero for a
maximum-anchor/minimum-support source.  It does not construct `Phi` and does
not assert an all-order axis-pure theorem.

Pinned ledger:

```text
ebde5ecfe1070f41ff406ccf8fbf21c7149223fddf46aa871c6c18c7e24e45f5
```
