# Exact target standardness through homogeneous degree eight

The `y10*t^2` target has 143 homogeneous d8 divisors: 23 y8, 48 y7*t,
and 72 y6*t^2.  Literal source incidence gives 205 genuinely new t-free
y4 multiplier columns, split into 61 feeding y7*t and 144 feeding y6*t^2;
there is no direct y8 target incidence.

Exact inverse incidence partitions these seeds into 117 y8 components with
70,578 columns and 3,650,920 rows.  A deterministic private-row peel removes
all 70,578 columns, leaving no residual core.  The largest component has
8,243 columns and 414,321 rows.  Thus the new y8 head is injective.  Every
remaining degree-eight column lies in `t*M7`, so the frozen degree-seven
standardness theorem excludes all shorter target pivots.

Therefore the transferred row is standard through total degree eight in the
frozen chart26 t-last order.  This is target-specific; no degree-nine claim
is included.

Deterministic terminal artifact:

- `results_y10_d8_terminal.json`, logical
  `5573ea640136fc17748aa131ec2bb6d5ad1c793834ce62ad9f7cbd689c31ad18`,
  file SHA-256
  `5bfd5a482d0a53f933c7456d5847b952e58574356c55ae96a9e50d6c941af4f0`.
