# The full native linear Spencer orbit still misses `L01`

## Exact non-diagonal calculation

Let `R` be the complete `K8` hafnian response in its 28 independent edge
coefficients. The entire degree-preserving filtered differential-operator
space below order two is spanned by

```text
R,  and  x_y partial_(x_e) R   for all 28 x 28 ordered pairs (y,e).
```

This includes arbitrary non-diagonal linear coefficient changes, not merely
the physical vertex torus, raw chart permutations, or vertex shears tested
previously.

Extend the primitive twelve-occurrence covector `psi01` by zero to every
degree-four monomial which is not a perfect matching, including every
collision monomial. Exact enumeration gives

\[
                 \psi_{01}(x_y\partial_{x_e}R)=0
                 \quad\hbox{for all }784\hbox{ pairs}.       \tag{1}
\]

Checker:
[`verify_h3_l01_full_linear_spencer_dual_gate.py`](../computations/verify_h3_l01_full_linear_spencer_dual_gate.py).

The reason is structural. For `y=e`, the output stays in the matching block
and is an ordinary edge-Euler row, which `psi01` kills. For `y!=e`, replacing
one matching edge by another either creates a collision or no longer covers
all eight vertices once. The zero extension kills that output. The checker
nevertheless expands all 784 operators literally rather than relying only
on this argument.

## The desired second-order symbol has unavoidable curvature

The chart-complete principal symbol is

\[
 \mathcal D=
 2Dq_{01}\partial_D\partial_{q_{01}}
 -p_0s_1\partial_{p_0}\partial_{s_1}
 -p_1s_0\partial_{p_1}\partial_{s_0}.                \tag{2}
\]

Direct application to `R` gives

\[
                         \mathcal D(R)=L_{01}.         \tag{3}
\]

The output has the expected nine perfect-matching occurrences, and

\[
                         \psi_{01}(L_{01})=1.          \tag{4}
\]

In the filtered Weyl/Spencer algebra, two order-two operators with the same
principal symbol differ by an operator of order below two. Every degree-
preserving such correction is in the space tested in (1), together with the
scalar response row. The dual kills that entire space. Therefore no native
lower-order, including non-diagonal, Spencer correction makes (2) tangent to
the response fibre while retaining its prescribed `Hasse[2](DQ,PS,PS)`
symbol.

This is the precise meaning of the `L01` curvature. The order-two operator
does produce the desired coefficient, but only as its failure to preserve
the source equation. Calling that output a boundary would assume the new
cell being sought.

## What a positive construction must add

The obstruction does not rule out a larger Koszul--Tate source resolution.
It says that such a resolution needs a new generator whose boundary is the
curvature (3), together with the collision and product-rule faces required
by the physical presentation. In the current notation this is exactly one
of the equivalent objects

```text
a source-labelled L01 Tate generator;
a covariant three-cap / endpoint-even C+ totalization;
a physical pointed chart cylinder retaining all proper faces.
```

The complete response, all linear non-diagonal coefficient motions, and the
lower protected `U_C4` signature do not supply that generator.

## Does the dual become an accepted terminal?

Not yet. Equation (1) proves that `psi01` is a full cokernel dual for the
native degree-preserving coefficient Spencer map through filtration one.
That map is not the exhaustive physical same-grade source map:

- arbitrary coefficient `GL28` motions have no automatic physical
  word/fine/repeated or target/`q`/anchor/ridge lift;
- a source-labelled Tate/collision column, if it exists, can pair nontrivially
  with `psi01`; and
- the downstream word-`0102` placement is outside this native coefficient
  block.

There are two exact completions compatible with all presently tested native
columns. Keeping only those columns leaves `psi01` as a nonfill dual. Adding
one source-labelled column with boundary `L01` fills it. Hence the native
calculation cannot decide accepted physical terminality.

After literal same-grade placement, the committed augmented extension is
already exhaustive. If `mu_j` are the induced four cap-corner values, use

```text
q=ainc=Eq=0,
target_j=W_j=-mu_j,
ores_j=mu_j,
ridge=-sum_j alpha_j mu_j.
```

Exact duality then gives either a protected-zero filler or a full augmented
terminal, with no third branch. The remaining issue is solely construction
or exhaustive nonexistence of the source-labelled Tate/three-cap cell; it is
not another lower-order Spencer correction.

Run normally, optimized, and isolated/no-site. The checker pins all inputs
and records a frozen ledger digest.
