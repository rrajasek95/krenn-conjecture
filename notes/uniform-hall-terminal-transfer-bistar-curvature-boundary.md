# The strict terminal Hall bistar chart is empty

**Promotion.**  The weighted-SCC shortcut below is still not source-valid,
but the complete strict response packet closes before any nonlinear transfer
is needed.  The colour-one companion rows cancel the two colour-two alternate
aggregates and leave localized monomials.  Thus the endpoint-support-complete
strict `K2,2` chart has no source point.

## Exact source row

The strict unequal-tail theorem `f2c02cf` correctly removes the odd-path
parity issue: complete exchange at either endpoint crossing cell gives a
pure-anchor reselection, an off-anchor term, a unit, or a non-pure cell on
the original two-shared pivot.  The last alternative invokes the finite
label migration `07a1f02`.

That invocation is a routing statement, not yet a termination statement.
Label migration may return to the same terminal direct cell `q_e^(m,m)`
whose missing cofactor activity produced the two-block row.  The tempting
weighted-SCC proof must therefore be source-typed across the two endpoint
stars.

On the canonical strict chart, take

```text
Q0 = 01 | 24 | 35,
Q1 = 01 | 23 | 45,
Q2 = 02 | 13 | 45.
```

The pivot `e=01` is shared by `Q0,Q1`; the third anchor avoids it through
`g=02,h=13`.  For the genuine mixed word `220000`, every
anchor-contained matching term is displayed by

\[
  q_{01}^{22}
    (q_{24}^{00}q_{35}^{00}+q_{23}^{00}q_{45}^{00})
  +q_{02}^{20}q_{13}^{20}q_{45}^{00}=0.              \tag{1}
\]

The checker is
[`verify_uniform_hall_terminal_transfer_bistar_curvature_boundary.py`](../computations/verify_uniform_hall_terminal_transfer_bistar_curvature_boundary.py).

## Why one weighted same-star SCC is not yet available

At site `0`, equation (1) is affine-linear in the two star cells

```text
q01_22, q02_20,
```

with `q13_20*q45_00` frozen in the tail.  At site `1`, it is likewise
affine-linear in

```text
q01_22, q13_20,
```

with `q02_20*q45_00` frozen.  These are exactly the valid one-endpoint
complete exchanges used by `f2c02cf`.

They are not one simultaneous switch space.  The two crossing arms `02`
and `13` are disjoint, and together with `45` form a physical perfect
matching.  If their variations are `d_g,d_h`, the mixed finite difference
of (1) is

\[
                         d_gd_hq_{45}^{00}.           \tag{2}
\]

It is a genuine source monomial, not a formal grade.  Thus a kernel obtained
by propagating ratios across both endpoint stars is only a tangent kernel
unless (2) is cancelled.

There is an exact correction for the unary row alone.  Put
`C=A+B=-ghT/e`.  After finite changes `d_g,d_h`, set

\[
 d_e=-T(gd_h+hd_g+d_gd_h)/C.                          \tag{3}
\]

Then `(e+d_e)C+(g+d_g)(h+d_h)T=0` identically.  The obstruction is therefore
not formal implicit solvability of the one unary coefficient; it is its
compatibility with the response rows.

The smallest tangent guard is already visible in `F=e+gh`.  At
`(e,g,h)=(-1,1,1)`, the direction `(0,1,-1)` kills the first variation, but

\[
                  F(-1,1+s,1-s)=-s^2.                \tag{4}

So the usual same-star argument—linear kernel plus divided square zero—does
not extend across this return.  This does not challenge the signless or
five-lock theorems: their hypotheses require all directions to lie in one
physical same-star square-zero space.

## The missing companion rows close the chart

The strict colour-two endpoint support gives two more exact rows.  With
`p2` supported at sites `1,2` and `s2` at `0,3`, the words `222000` and
`220200` contain respectively

```text
p2_2*s2_0*q13_20*q45_00
  + p2_1*s2_0*(q23_20*q45_00 + q24_20*q35_00) = 0,

p2_1*s2_3*q02_20*q45_00
  + p2_1*s2_0*(q23_02*q45_00 + q24_00*q35_20) = 0.
```

The exact colour-one companion rows for words `112000` and `110200` are

```text
G112000 = p1_0*s1_1
  *(q23_20*q45_00 + q24_20*q35_00),

G110200 = p1_0*s1_1
  *(q23_02*q45_00 + q24_00*q35_20).
```

The checker enumerates every literal anchor-contained term in all four
rows.  There are no suppressed terms in this strict endpoint envelope.
Consequently the following are ordinary source-row identities, not quotient
or tangent calculations:

\[
\begin{aligned}
 &(p1_0s1_1)G_{222000}-(p2_1s2_0)G_{112000}\\
 &\qquad=p1_0s1_1p2_2s2_0q13_{20}q45_{00},\\[2mm]
 &(p1_0s1_1)G_{220200}-(p2_1s2_0)G_{110200}\\
 &\qquad=p1_0s1_1p2_1s2_3q02_{20}q45_{00}.
\end{aligned}                                                     \tag{5}
\]

Every factor on the right of each identity is localized in the strict
effective chart.  Either equality in (5) is therefore a scalar unit.  In
particular, all four formerly exposed decorated-anchor choices `A/B` and
`C/D` are closed simultaneously; no exchange recursion remains.

Formula (3) does not help the two colour-two rows by itself: `q01_22` is absent from both
coefficients.  With all selected factors normalized, their first defects
after changing `h` and `g` are exactly `d_h` and `d_g`.  One can absorb them
formally by reciprocal rescaling of `p2_2` and `s2_3`, but that changes the
two selected diagonal target contributions.  Making that rescaling
source-valid would require further work if the companion rows were omitted.
Equation (5) shows why that omission is artificial in the full strict
packet.

This promotion is scoped to the endpoint-support-complete strict chart.
If an extra endpoint component exists outside this envelope, the pinned
theorem `7114577` routes it to an active distinct-head wedge; such a port is
therefore a landing, not a strict-chart survivor.  The earlier curvature
calculation remains useful only as a method guard: weighted holonomy by
itself does not prove the unit, while the genuine cross-colour source rows
do.

## Verification

Run

```text
python3 computations/verify_uniform_hall_terminal_transfer_bistar_curvature_boundary.py
python3 -O computations/verify_uniform_hall_terminal_transfer_bistar_curvature_boundary.py
python3 -I -S computations/verify_uniform_hall_terminal_transfer_bistar_curvature_boundary.py
```

Frozen ledger SHA-256:

```text
9e2ecc8cd8554340ab94fa77539f51b1cb8e881b4062283d5e000a282e23a792
```
