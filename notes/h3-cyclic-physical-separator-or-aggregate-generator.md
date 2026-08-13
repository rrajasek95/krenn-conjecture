# The five physical face separators assemble over the C5 edge lattice

Each repeated face grade has a primitive six-term covector.  In the
canonical face its pure marker has been identified with minus physical
anchor incidence, giving

\[
 \Lambda_v=\sum_{i=1}^{6}m_{v,i}-\operatorname{ainc}_v. \tag{1}
\]

Normalize each facewise covector to read one on its desired boundary-zero
anchor.  The five covariance--Spencer comparison edges have the oriented
incidence columns

\[
 e_3-e_1,\ e_5-e_3,\ e_2-e_5,\ e_4-e_2,\ e_1-e_4.  \tag{2}
\]

Therefore

\[
                      \Lambda=\sum_v\Lambda_v         \tag{3}
\]

kills every column in (2).  These columns span the saturated rank-four
sum-zero lattice.  The only cyclic direction outside their span is the
primitive aggregate

\[
                         (1,1,1,1,1),                 \tag{4}
\]

and (3) reads `5` on (4).

This gives an exact cyclic alternative.  If a physical relative aggregate
cell exists, its nonzero value normalizes by `1/5` in characteristic zero
and supplies the relative-generator branch.  If no admitted relative cell
has nonzero value, (3) descends across the complete cyclic edge comparison
as the physical separator.

The absolute source part is already exhausted independently in every face
grade.  Hence the only remaining local comparison audit is the genuinely
relative aggregate family—not five independent face constructions and not
another higher source census.

## Scope

This is the exact incidence assembly of the five componentwise physical
covectors.  It does not itself realize the symbolic edge comparisons as
physical augmented chains, audit every future relative terminal correction,
identify the summed covector with the final pentagon terminal, or establish
transverse rank landing.

Verification:

```text
python3 computations/verify_h3_cyclic_physical_separator_or_aggregate_generator.py
python3 -O computations/verify_h3_cyclic_physical_separator_or_aggregate_generator.py
python3 -I -S computations/verify_h3_cyclic_physical_separator_or_aggregate_generator.py
```

Frozen ledger SHA-256:

```text
3175a867a20de2a9cdf7ba2214f42b7b19709d831bc2f506310204fd3b28af51
```
