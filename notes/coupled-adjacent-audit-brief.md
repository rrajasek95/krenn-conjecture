# Clean-room audit brief: coupled adjacent directions E10, E20

This brief specifies, from first principles, everything an independent
auditor needs to reconstruct and check the two new local theorems

- `notes/three-cut-internal-23-arbitrary-block-adjacent-25-10-fourth-cut-obstruction.md`
- `notes/three-cut-internal-23-arbitrary-block-adjacent-25-20-fourth-cut-obstruction.md`

with primary verifiers

- `computations/verify_three_cut_internal_23_arbitrary_block_adjacent_25_10_fourth_cut_obstruction.py`
- `computations/verify_three_cut_internal_23_arbitrary_block_adjacent_25_20_fourth_cut_obstruction.py`

The audit scripts must import **no project module** and reuse **no
matrix, normal, killed set, program text, or hash** from the primary
implementation.  Reading the primary sources to learn the *case list and
configuration* (which colour pair, whether lock rows are used) is
allowed; everything mathematical must be rebuilt from the definitions
below with different algorithmic choices (different matching recursion,
reversed variable and generator orders, `std` instead of `slimgb`).

## 1. Objects

Sites are `0..7`; internal sites `0..5`, boundary sites `6,7`.  Colours
are `{0,1,2}`.  A *block* on an edge `(u,v)` with `u<v` is a map from
ordered colour cells `(a,b)` (colour `a` at `u`, colour `b` at `v`) to
rational/complex weights.  The fixed six-site interior is

    (0,1):E00  (4,5):E00  (0,2):E11  (1,4):E11
    (0,4):E22  (1,3):E22  (3,5):E10

where `Ecd` means the single cell `(c,d)` with weight 1 (endpoint order:
first colour at the smaller site).  The two variable internal blocks are

    (2,3): X, an arbitrary 3x3 complex block, and
    (2,5): E00 + t*Ecd, with (c,d)=(1,0) for direction E10
                         and (c,d)=(2,0) for direction E20.

Boundary blocks: `(i,6)` carries entries `p[a,i,c]` (colour `c` at `i`,
colour `a` at `6`), `(i,7)` carries `q[b,i,c]`, and `(6,7)` carries
`r[a,b]`; all arbitrary complex.

For a vertex set `V` with even size and blocks on its edges, the
*matching tensor* is the sum over perfect matchings of `V` of the tensor
product of the chosen cells' weights, recorded as a map from colour
words on `V` to weights.  `H_S(X,t)` is the matching tensor of `0..5`
with the internal blocks above.

For a cut site `z` in `0..5`, the *cylinder* `C_z(X,t)` is the span of
the 45 insertion columns: for each colour `cz` at `z`, each hole site
`h != z`, each colour `ch` at `h`, the column is the matching tensor of
the remaining four sites extended by `ch` at `h` and `cz` at `z`.

The *fibre* of the boundary stars is, for ordered boundary colours
`(a,b)`,

    beta_ab(word) = sum over unordered internal pairs {i,j}, over the
      matching-tensor cofactor of the other four sites, of
      cof(rest_word) * ( p[a,i,ci]*q[b,j,cj] + p[a,j,cj]*q[b,i,ci] )

collected on the six-site word assembled from `rest_word`, `ci` at `i`,
`cj` at `j`.  **Literal identity to verify numerically with random
rationals:** the full eight-site matching tensor's `(a,b)` boundary
fibre equals `r[a,b]*H_S + beta_ab`.

*Fourth-cut necessary condition.*  The three cuts `2,3,4` are active on
this interior.  If a fourth complete cut existed at `z in {0,1,5}`, then
for every ordered pair `(a,b)` the vector
`beta_ab - delta_ab * e_a^{x6}` (Kronecker delta; `e_a^{x6}` the
all-`a` word) would lie in `C_2 ∩ C_3 ∩ C_4 ∩ C_z` at the given
`(X,t)`.  The audit checks that this is impossible for every complex
`X`, `t`, stars, and `r`, by the quotient method below.  (The framing —
that this membership is the correct necessary condition — is exactly the
one used by the five previously audited adjacent-direction theorems and
by the base arbitrary-A23 theorem; the audit re-derives everything
downstream of it.)

## 2. Quotient method to reconstruct

1. *Output blocks.*  For each of the nine cells of `X`, its output
   block is the set of six-site words whose `H`/cofactor coefficients
   can involve that cell: concretely, the set of words reachable by
   varying that cell alone (35 words each; pairwise disjoint).  The
   moving `t`-cell has its own 35-word block; for E10 it meets the
   `x10,x11,x12` blocks in `9,9,12` words and the fixed-interior tensor
   support in 2 words; for E20 it meets `x20,x21,x22` in `9,9,12` and
   the fixed support in 0.  Edges `(2,3)` and `(2,5)` share site 2, so
   no matching uses an `X` cell and the `t` cell simultaneously; all
   tensors and columns are jointly affine in `(X,t)` with no cross
   terms.  Verify this affineness exactly at probe points.
2. *Coupled character.*  Compute the rank-10 stabilizer torus of the
   eight fixed cells (weight vectors in `Z^{18}`, one coordinate per
   (site, colour) of sites `0..5`); check the effective X-character rank
   is 5 and that the `t`-character equals `wt(x_cd) - wt(x00)` in the
   effective quotient, so adding `t` does not raise the rank.  This is
   why `t` must stay a polynomial ring variable everywhere.
3. *Case partition of the 512 supports of X.*  Old five-cell locus:
   supports inside `{x00,x01,x02,x11,x21}` (32 masks), classed by
   membership of `x00,x11,x21` into five classes with retained cells:
   `no_x00 -> {}`, `x00_no_x11_no_x21 -> {x00}`,
   `x00_no_x11_with_x21 -> {x00,x21}`  (maximal adds x01,x02),
   `x00_x11_no_x21 -> {x00,x11}`, `x00_x11_with_x21 -> {x00,x11,x21}`;
   the killed word set of a class is the union of the output blocks of
   the cells in `maximal - retained`, plus the fixed-support words not
   in the retained union (retained union = t-block plus retained cells'
   blocks).  Outside locus: 480 masks partitioned by first nonzero cell
   in the order `x10,x12,x20,x22`; retained tuples are
   `x10 -> (x10,x11,x21,x22)`, `x12 -> (x11,x12,x21,x22)`,
   `x20 -> (x10*,x11,x20,x21,x22)` and `x22 -> (x10*,x11,x12*,x20*,x21,x22)`
   as in the base theorem (`*` = forced-zero cells are killed as well:
   the killed set is the fixed-support words outside the retained union
   plus all non-retained cells' blocks); representatives set the
   present retained cells to 1, cases enumerated by presence of
   `x11` (`d&2`), `x22` (`d&4`), and `x21` (`b`).  The sole circuit is
   `x12+x21 = x11+x22`: the case `x12` family, `d=6`, `b=1` instead
   retains `x12=x11=x22=1, x21=lam` with `lam` a second polynomial
   variable.  Verify the exact partition census `512 = 32 + 480` and
   the per-case torus normalizability (character ranks).
4. *Killed-cell arbitrariness.*  For every case and every cell not in
   the retained tuple, adding that cell with value 1 must change
   neither the projected word terms (`beta` coefficients restricted to
   non-killed words) nor the span of any of the six projected cylinder
   column families, at every parameter specialization used.  For old
   classes, check instead that every class member mask reproduces the
   representative's projected data (both at `t in {0,1}`).
5. *Expanded overspace.*  For final cut `z`, with specialization
   points `theta` in `{0, e_1, ..., e_k}` (unit points of the 1- or
   2-dimensional parameter space `(t)` or `(t,lam)`), the space

       N+_z = intersection over w in {2,3,4,z} of
              span( projected columns of C_w at all points )

   contains the projected `C_2∩C_3∩C_4∩C_z` at every parameter value
   (affine columns).  Verify the projected `H_S` at every
   specialization lies in `N+_z`, and that the two selected diagonal
   targets are neither killed nor inside `N+_z`'s span.  Expected
   dimensions per case are listed in the configuration tables.
6. *Lock functionals* (only the `x12` circuit case needs them).  For
   each cut `w in {2,3,4,z}`, compute the space of functionals
   `phi(theta) = phi_0 + t*phi_1 + lam*phi_2` supported on the retained
   coordinates with `phi(theta) . column(theta) = 0` for every one of
   the 45 projected columns and every `theta` (vanishing constant,
   linear, and quadratic coefficients).  Verify them at three probe
   points.  Each lock gives an extra generator per fibre.
7. *Systems.*  For the configured colour pair `(A,B)` of a case and
   final cut `z`: for the four ordered fibres `(a,b)` with
   `a,b in {A,B}`, impose membership of
   `beta_ab - delta_ab e_a^{x6}` (projected) in `N+_z` — via exact
   rational row reduction of the `N+_z` basis (annihilator rows), with
   the `beta` coefficients affine polynomials in `(t[,lam])` — plus
   the lock generators where configured.  Collect the ideal over
   `Q[t[,lam], star variables]` and require reduced Groebner basis
   `[1]` (use `std`, not `slimgb`; use a *reversed* variable order and
   a *reversed* generator order relative to naive construction).  A
   unit ideal excludes the fourth cut on the whole case for every
   complex parameter value, including `t=0` and `lam=0`.

## 3. Configuration to audit

Per-case expected overspace dimensions (cuts 0,1,5), colour pair, and
lock usage are recorded in the primary verifiers' `FROZEN` tables; the
generator counts there are for the primary's own ordering and need not
be reproduced.  The audit passes when all `2 x 99` systems are unit,
every geometric/partition/arbitrariness check above passes, and the
literal eight-site fibre identity holds on random rationals.

## 4. Deliverables

- `computations/verify_three_cut_internal_23_arbitrary_block_adjacent_25_10_fourth_cut_obstruction_independent_audit.py`
- `computations/verify_three_cut_internal_23_arbitrary_block_adjacent_25_20_fourth_cut_obstruction_independent_audit.py`
- `notes/three-cut-internal-23-arbitrary-block-adjacent-25-10-fourth-cut-obstruction-independent-audit.md`
- `notes/three-cut-internal-23-arbitrary-block-adjacent-25-20-fourth-cut-obstruction-independent-audit.md`

Each script must be runnable as
`uv run python computations/<name>.py` from the repository root and end
with an unambiguous PASS ledger.  Any discrepancy must be reported, not
patched over.
