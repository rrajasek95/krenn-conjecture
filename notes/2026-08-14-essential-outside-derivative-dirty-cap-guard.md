# Complete outside derivatives do not determine a typed active clean cap

## Result

The independent outside branch of `32d205e` has a sharp restricted positive
theorem and a sharp general obstruction.

* In the actual seven-cell `C6` packet, every one of the twelve minimal
  escapes is a literal rank-one pure derivative with one source-labelled
  cofactor occurrence and no mixed derivative coordinate.  It is not yet an
  active clean cap: it has only the colour-one target channel, so
  `kappa_0 kappa_2=0` before cleanliness is tested.
* If either missing pure colour is supplied support-minimally, the theorem of
  `3d78125` gives a literal mixed singleton in all 192 first completions.
* Without support-minimal completion, even the complete `3^N` derivative
  tensors and the full linear GHZ cap identity do not force a unit or an
  active clean cap.  A three-parameter, order-eight abstract boundary
  signature has three independent pure outside columns summing to the full
  ternary target, no mixed coordinates, and no active clean covector.

The missing hypothesis is therefore higher-response **common-edge
integrability**.  Matching-covered or terminal-ear support structure helps
only when its flips preserve the actual shared-star cofactor products.

The exact checker is
[`verify_uniform_essential_outside_derivative_dirty_cap_guard.py`](../computations/verify_uniform_essential_outside_derivative_dirty_cap_guard.py).

## 1. The actual `C6` first jet

For the tight shore `{3}`, `32d205e` computes the complete physical
derivative matrix on all 729 six-site output words.  For each cap-avoiding
fine matching there are four live cut cells:

```text
34;00, 34;11, 34;22,
the unique colour-one escape edge incident with site 3.
```

Modulo the forced residual equation `H=0`, the three cap derivatives vanish.
The outside derivative has

```text
pure projection       (0,+/-1,0),
mixed support         empty across all 726 mixed words,
literal cofactor      exactly the selected escape matching,
rank change           0 -> 1.
```

After multiplying by the actual escape-cell coefficient, its `111111`
coordinate is one.  Thus it is a genuine typed outside cut state, not a free
occurrence shadow.

This still falls short of a typed active clean cap.  For a pair cap covector
`K`, activity requires

\[
                    s(K)\kappa_0(K)\kappa_1(K)\kappa_2(K)\ne0.          \tag{1}
\]

The single-colour escape supplies only `kappa_1`.  It has no mixed singleton
and cannot itself prove (1).  The first failure is activity, not the
homogeneous clean error.

There is a complete restricted continuation.  Starting from any of the eight
support-minimum first colour-one escapes, `3d78125` enumerates the twelve
minimum escapes for each missing colour.  All

\[
                            8\cdot12\cdot2=192                         \tag{2}
\]

first completions have a literal mixed singleton.  Thus

```text
minimum completion -> source unit
```

is proved.  A nonminimum completion may adjoin cancellation mates at the same
time and is not covered by that census.

## 2. Why complete derivatives are only first-jet data

At an eight-to-six cap, put `U={0,...,5}` and let `x` be the internal
quadratic edge family.  The full contracted GHZ identity can be written

\[
 C_6+C_4x+\frac12C_2x^2+\frac16sx^3
       =\sum_{i=0}^2\kappa_iX_i.                                  \tag{3}
\]

The denominator-cleared clean error is

\[
 D=6s^2\sum_i\kappa_iX_i-(sx+C_2)^3.                              \tag{4}
\]

The complete outside derivative tensors determine the right side of (3).
They do not determine `C_2`, the crossed two-port response built from
products of endpoint stars.  Equation (4), and hence cleanliness, depends
cubically on that missing higher response.

This distinction survives after keeping every pure and mixed coordinate of
the first derivative.  It is not caused by projecting to the pure rows.

## 3. Smallest three-channel full-GHZ-compatible guard

Work on six residual sites and choose the literal internal quadratic

```text
x = 01;01 + 23;20 + 45;12.                                      (5)
```

Its three edges are disjoint, so in the site-square-zero algebra

\[
                              x^3=6e_{012012}.                     \tag{6}
\]

Use the diagonal cap-parameter space

\[
 K=\operatorname{diag}(k_0,k_1,k_2),\qquad
 \kappa_i(K)=k_i,qquad s(K)=k_0+k_1+k_2.                         \tag{7}
\]

This embeds in the physical nine-dimensional cap space.  The scalar (7) is
the pairing with direct block `I_3`; off-diagonal cap directions may be added
as inactive dummies.

Define the boundary signature

\[
 \begin{aligned}
 C_0&=s,\\
 C_2&=-sx,\\
 C_4&=0,\\
 C_6&=\sum_i k_iX_i+\frac13sx^3.                                  \tag{8}
 \end{aligned}
\]

Every entry depends linearly on `K`.  Substitution into (3) gives

\[
 \left(\frac13-\frac12+\frac16\right)sx^3=0,                       \tag{9}
\]

so (3) holds on all 729 coordinates for every `K`.

Let `eta_i` be the `i`th diagonal basis direction.  Its complete contracted
tensor is

\[
                              T(\eta_i)=X_i.                         \tag{10}
\]

The three columns in (10) are independent, have no mixed coordinate, and
sum to

\[
                    X_0+X_1+X_2=\Delta_{6,3}.                       \tag{11}
\]

Thus the guard retains the whole linear GHZ contraction identity and exactly
the three essential single-colour outside states needed by the ternary
target.  There is no mixed row from which to extract a unit.

This is minimal in the tested category: three independent single-colour
columns are needed to span the three independent target tensors, and order
eight is the first live inductive clean-cap boundary over the proved six-site
base obstruction.

## 4. Every clean covector in the guard is inactive

For (8), `sx+C_2=0`, so (4) reduces to

\[
                  D_i(K)=6s(K)^2k_iX_i\qquad(i=0,1,2).              \tag{12}
\]

If `D(K)=0` and `s(K) != 0`, then (12) forces all `k_i=0`, contradicting
`s=k_0+k_1+k_2`.  Hence

\[
                              V(D)=V(s).                             \tag{13}
\]

Every clean covector is inactive.  Conversely the active direction
`K=diag(1,1,1)` has

```text
s=3, kappa=(1,1,1), contracted top=Delta_(6,3),
D=54 Delta_(6,3).
```

It is maximally target-active and explicitly unclean.

The obstruction has a one-line localization certificate.  With

\[
 I_D=(6s^2k_0,6s^2k_1,6s^2k_2),\qquad
 h=sk_0k_1k_2,                                                     \tag{14}
\]

one has

\[
 1=(1-th)(1+th)
   +t^2\frac{k_0k_1^2k_2^2}{6}(6s^2k_0).                           \tag{15}
\]

Therefore

\[
                         I_D:h^\infty=(1).                          \tag{16}
\]

The checker verifies (5)--(16) over the rationals, including all 729 top
coordinates and the exact polynomial identity (15).

## 5. Scope: a counterguard, not a Krenn source

The signature is **abstract full-GHZ-compatible**, in the precise sense that
it satisfies the contraction of the full GHZ tensor for every cap covector.
It is not claimed to come from one physical common-edge aggregate source.
The omitted condition is that `C_2,C_4,C_6` must all be matching cofactors of
the same endpoint-ordered edge blocks.  In particular, (8)'s assignment
`C_2=-sx` is not supplied with a shared-star factorization.

This is exactly the scope allowed by the requested terminal alternative: it
is a counterguard to the inference from complete derivative tensors plus
full-GHZ compatibility, not a counterexample to Krenn's conjecture.

The guard also explains why a matching-covered core or ear decomposition is
not enough by itself.  Those theorems constrain occurrence support, crossing
parity, and alternating flips.  They do not determine the coefficient-level
map `K -> C_2(K)` in (4).  An ear argument becomes relevant only after proving
that its contraction/flip preserves the common endpoint stars and therefore
the actual `C_2` products.

## 6. Exact remaining source theorem

Let `u_out` be the nonzero pure coordinate of an essential outside derivative
and let `I_clean` be the coordinate ideal of the physical homogeneous cap
error.  The needed source theorem is

> For a boundary signature arising from one common aggregate edge family,
> either a source-labelled mixed singleton/private cap occurs, or
>
> \[
> I_{clean}:
> (u_{out}s\kappa_0\kappa_1\kappa_2)^\infty\ne(1).                  \tag{17}
> \]

The nonunit saturation in (17) gives a typed active clean cap retaining the
outside channel.  The guard has unit saturation, so any proof of (17) must
use common-edge/shared-star identities absent from first derivatives and the
linear GHZ equation.

This is the shortest remaining attack on the outside branch.  A useful ear
lemma would prove (17) by lowering boundary-transfer rank or by producing a
private mixed face whenever the shared-star factorization fails.

## Verification

```text
python3 computations/verify_uniform_essential_outside_derivative_dirty_cap_guard.py --mode structural
python3 -O computations/verify_uniform_essential_outside_derivative_dirty_cap_guard.py --mode full
python3 -I -S computations/verify_uniform_essential_outside_derivative_dirty_cap_guard.py --mode exhaustive
```

All modes have frozen ledger SHA-256
`40c3f63190b420840f8fbc1c27f49f83b2afecc7e32078c6f8594f522abd1b12`.
