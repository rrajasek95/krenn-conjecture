# N=8 P5 degree-eight mixed tails and component lifts

## Result

The 39 normal-eliminated mixed equations have been streamed through original
degree eight on the full 45-parameter P5 branch.  The next strict
compatibility calculation then gives:

- the component $z_{16}=0$ lifts symbolically through strict order six, with
  the entire incoming residual already zero;
- the component $z_{41}=0$ lifts symbolically through strict order six: its
  248-term incoming residual is removed by eight pivot corrections, leaving
  no compatibility equation;
- one exact rational point on the generic open part of $L=0$ lifts through
  strict order six after two free bends transverse to $L$.

Here

$$
L=z_9z_{25}-z_{11}z_{46},\qquad b=z_{44}+z_{45}\ne0.
$$

The full generic $L$ component has not yet been reduced symbolically at this
order.  The rational point proves that the next compatibility does not kill
the entire $L$ component, but it is not an all-point component identity.

The exact checkers are:

- `computations/verify_n8_p5_streamed_degree8_mixed_tails.py`;
- `computations/verify_n8_p5_degree8_component_compatibility.py`.

## Second normal graph

Let $d_p$ be the dual ambient directions to the 196 echelon Jacobian forms,
and let $E_p^{(k)}$ be their homogeneous pieces.  The first normal coefficient
is

$$
W=\sum_p E_p^{(2)}d_p,
$$

with sign $-W$ in the normal graph.  The second coefficient used by the new
checker is

$$
N_2=-\sum_p\left(E_p^{(3)}-W(E_p^{(2)})\right)d_p.
$$

The checker verifies all 196 graph equations exactly at orders two and three.
The second direction has 104 active pivots, 104 ambient coordinates, and 242
terms.

For a factorized residual with old homogeneous pieces $F_d$, its degree-eight
normal-graph restriction is assembled as

$$
T_8=F_8-W(F_7)+N_2(F_6)+[W^2F_6]_{\mathrm{divided}},
$$

where the last term is the coefficient of the square of the first normal
direction, not the undivided second derivative.  Before accepting $T_8$, the
implementation reconstructs all 39 committed degree-seven tails exactly.

The 39 degree-eight tails have 42,200 terms in total, at most 4,881 in one
equation, and are all nonzero.  Their polynomial SHA-256 is
`bc9606f71e37b99007626e90583b204cc0d2b388a92854ffbf2b5145d2c3d1d9`.
The full tail ledger has SHA-256
`13ca39b753cae39c5d36bdee7fd8ce0d5bc8822a4b7a45f1fcaad847de9e5dc3`.

## Bigraded strict jets

The component checker retains two filtrations simultaneously: ambient normal
order through two and strict P5 arc order through two.  Its order-five output
is regressed for all 39 equations against the previously committed
$Q^{(6)}(n_1)+Q^{(7)}$ contribution.  Only then does it assemble strict order
six from

$$
T_6[n_1,n_2]_{(2)}+T_7[n_1]_{(1)}+T_8|_{P5}.
$$

On $z_{16}=0$, the fifth correction and the entire strict-order-six residual
are zero.  On $z_{41}=0$, the fifth correction has eight nonzero entries and
31 terms.  The order-six residual has 248 terms, at most 22 per equation, and
its projection to all compatibility directions is zero.

## Exact point on the L component

The deterministic point uses $z_i=i+2$ on the free P5 coordinates, the P5
normal coordinates zero, $z_{15}=z_{16}=18$, and

$$
z_{46}=\frac{z_9z_{25}}{z_{11}}=\frac{297}{13}.
$$

It lies on $L=0$ with $b,z_{11},z_{16},z_{41}$ and
$u=z_{26}+z_{45}$ all nonzero.  The first free bend is

$$
z_{46}^{(1)}=\frac{2430}{13}.
$$

Before the second free bend, the only order-six compatibilities are

$$
h_{30}=-165689793000,
\qquad
h_{33}=39765550320.
$$

Their ratio is exactly

$$
h_{30}:h_{33}=u:v=-25:6,
\qquad v=z_{26}-z_{44},
$$

so the pair satisfies the same single-bend consistency relation.  Taking

$$
z_{46}^{(2)}=\frac{317140}{13}
$$

and recomputing every subsequent transverse correction kills both values and
leaves no order-six compatibility.  The component ledger has SHA-256
`7a460d5d9223327e40a657d9236592dd7f2df0c13fd08009627ff9d9bc36c7b7`.

## Pure frontier

The corrected prior result still stands: H1 at degree seven is zero and H0 at
degree eight vanishes on all three degree-six components.  This calculation
does not produce the following H0/H1 coefficients.  Continuing them requires
the next tangent standard-basis layer: after the degree-six H1 corrections,
the existing quadratic-obstruction reducer no longer closes the full
degree-seven tangent residual.  Thus the next pure calculation must either
extend that tangent basis or perform a component-local reduction directly.

No exact pure survivor is presently certified on P5, but the mixed recursion
has advanced another order on both symbolic coordinate components and at one
generic rational point of the third component.
