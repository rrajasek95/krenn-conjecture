# The twelve one-bad successor targets form a terminating class DAG

## Result

The twelve one-class successor identities from the orbit-1 one-bad packet
have sixteen singleton contaminating classes in total.  Retain only exact
source provenance: the selected target word, the new matching's Laurent
class, and the first translated target class in the resulting source packet.
The complete map has the sharp split

```text
16 singleton provenance edges
  = 14 translated one-class targets
  +  2 parallel-character holonomy units.
```

Every one of the sixteen new matchings occurs only in the selected target
source row.  In the fourteen migration cases, the translated target word is
strictly later in lexicographic order.  None is a source vertex having a
singleton outgoing edge in this exact map.  Consequently every chain in the
complete successor singleton-provenance graph has length at most one.  There
is no coefficient-feasible closed target-migration cycle in this graph.

This conclusion is about Laurent classes and source labels, not support size.
No new repair layer is enumerated.

## The algebraic migration lemma

After quotienting the original plus-binomial rows, a two-class source row is
an equation

\[
                         \chi(d_i)=r_i\in\mathbb C^* .
\]

For an integer dependency \(\sum n_i d_i=0\), consistency requires

\[
                         \prod_i r_i^{n_i}=1.          \tag{1}
\]

Conversely, consistency of every such dependency defines a character on the
generated subgroup, which extends to the ambient free Laurent lattice over
\(\mathbb C^*\).  Thus (1) is the exact closed-cycle test, including
nonprimitive displacement lattices.

The two non-migrating endpoints each contain two source rows with the same
displacement but opposite required character values:

```text
top 000101: chi(d) = -1
top 220101: chi(d) =  1.
```

Their dependency is `-d+d=0`, while its character product is `-1`.  This is
an ordinary parallel-character unit, reconstructed from the original source
rows; it is not a native-solver verdict.  The two occurrences arise from

```text
successor x34_10, contaminant x34_22
successor x25_01, contaminant x25_22.
```

The remaining fourteen endpoints are source-faithful one-class Laurent
units.  Their seven translated target words and multiplicities are

| translated target | multiplicity |
|---|---:|
| `000222` | 2 |
| `000201` | 1 |
| `002101` | 1 |
| `002122` | 2 |
| `010122` | 4 |
| `010201` | 2 |
| `012101` | 2 |

## Precise scope

This proves termination for the **complete singleton-contaminant map already
frozen by the twelve-successor repair theorem**.  It does not claim that an
arbitrary later term belongs to this map.  In particular, the 173 double-cell
tails and any later Laurent classes remain outside the theorem.  Extending
the global one-bad proof now has a precise algebraic obligation: either map
those classes into a finite ordered target system of the same kind, or exhibit
a closed cycle satisfying (1).  A merely local repair count would not do so.

## Verification

Run

```bash
uv run python computations/verify_n8_one_bad_target_migration_dag.py
uv run python -O computations/verify_n8_one_bad_target_migration_dag.py
```

The checker pins the predecessor by SHA-256, reconstructs all sixteen
contaminating matching classes and their source records, rebuilds every
rank-24 plus-binomial quotient, checks all translated target units, and
reconstructs the two rank-two character systems and their opposite-character
dependencies.  The frozen ledger digest is

```text
daf29ded884f44c61a6e83e30f5000514699937ac03a8c20c88d7657be9b7fae
```
