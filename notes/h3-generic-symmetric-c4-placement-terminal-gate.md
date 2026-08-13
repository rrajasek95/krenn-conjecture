# The generic symmetric C4 leaves exactly one same-grade source column

## Verdict

The sole generic symmetric four-site residual isolated by `f382251` is not
an already committed punctured-C4, Kodaira–Spencer, or Cartan cell after
physical word/grade transport.

On residual sites `2,3,4,5`, write

\[
 s=q_{23}q_{45}+q_{24}q_{35}+q_{25}q_{34}.
\]

The three matching occurrences form the permutation module
`Q^3 = Q*s + ker(epsilon)`.  The generic equal-value face is the invariant
line.  Centered occurrence/KS directions, collision differences, and the
endpoint-odd Cartan shadow lie in the augmentation-zero plane.  The
primitive covector

\[
                    \epsilon={1\over3}(1,1,1)
\]

kills that entire plane and has `epsilon(s)=1`.

Checker:
[`verify_h3_generic_symmetric_c4_placement_terminal_gate.py`](../computations/verify_h3_generic_symmetric_c4_placement_terminal_gate.py).

## Why the three tempting identifications fail

The punctured-C4 theorem is an integral complete-row certificate in the
normalized target-coloop chart.  It uses selected endpoints and a common
tail, then reselects an alternate pure target.  It is a route theorem, not a
relative-C4 source column for an arbitrary flat four-site face.

The universal response KS generator has centered boundary `c_f`, hence
occurrence augmentation zero.  The endpoint-odd Cartan prism has corner
signature `(-1,1,1,-1)`, also augmentation zero, and requires a root-oriented
seed.  Neither operation creates the invariant augmentation-one C4 line.

Finally, the committed collision C4 censuses only identify possible matching
replacements.  Their repeated-edge packets include `02` and `01/04/12/24`,
but no theorem makes those occurrence pairs protected relative boundaries in
the original second-Hasse direction-pair object.  For the two literal
representatives that object is

```text
Hasse[2](D,Q01), residual sites 2345,
Hasse[2](P0,S1), residual sites 2345.
```

Site and colour relabelling preserve the Hasse order and the `D/P/S/Q`
operation profile.  Equality of a bare edge label therefore does not supply
the missing word/fine/direction-pair comparison.

## One explicit missing column

It is enough to construct one covariant representative:

```text
U_C4[D,Q01;2345]

domain       relative restriction/insertion generator in the literal
             Hasse[2](D,Q01) response word/fine/direction-pair grade
local face   q23*q45 + q24*q35 + q25*q34, with occurrence tags retained
tail         one literal augmentation-one b_i in the six-column C4 tail,
             selected by the physical C4 replacement
augmentation 1
zero rows    q, ainc, Eq, target, W, ordinary residue, shifted ridge
```

The site/colour and `DQ/PS` source transports must carry this column to the
other representatives without forgetting the second-Hasse tag.  What is
missing is the column's physical source provenance and same-grade protected
landing, not a choice in the six-dimensional target module.

## Exact terminal promotion

After this placement, let `mu_j` be the primitive local dual's values on the
four literal cap corners `B_j^cap`.  The cap/Cartan extension theorem
`4373ae6` gives the explicit augmented extension

```text
target_j = -mu_j,   W_j = -mu_j,   ores_j = mu_j,
ridge = -sum_j alpha_j*mu_j,       q = ainc = Eq = 0,
alpha = (-1,1,1,-1).
```

For example, `mu=(1,0,0,0)` gives `target0=W0=-1`, `ores0=1`,
and `ridge=1`.  This is only a sign check on the cap packet: the four
`B_j^cap` corners here are distinct from the six pure tails `b_i` in the C4
replacement census.

It annihilates every committed `r0`, `T`, `rho`, and physical Cartan `K`
column.  Hence, in the exhaustive physical map in this same grade, there are
exactly two branches:

1. the symmetric C4 class lies in the image, giving the protected-zero
   relative filler/generator; or
2. it lies outside, and the displayed extension is an augmented terminal.

There is no third branch.  The scope guard is important: `4373ae6` promotes
the dual only after the source-labelled grade placement.  It does not itself
construct `U_C4`, and the coefficient covector is not a physical terminal
before that comparison exists.

## Frontier change

The generic C4 branch is therefore reduced to one named column, not a new
four-site theory and not three matching-occurrence cells.  Constructing
`U_C4[D,Q01;2345]` retires it; proving its absence from the exhaustive
placed map immediately produces the terminal by the formula above.

Run normally, optimized, and isolated/no-site.  The checker records the
frozen ledger digest:

```text
63a39bb1c510e86b67e8fbf5867a4abc691aaf5d7545781e7ee11ae8e64ae49d
```
