# N=8 P5 degree-six compatibility kills the H0 escape

## Verdict

The eight-term degree-seven H0 class does not survive on a compatible P5
strict-transform component.  The full symbolic degree-six calculation leaves
two mixed compatibility equations, and H0 is an explicit linear combination
of them on the only chart where H0 can be nonzero.  On the complementary
boundary H0 vanishes directly.

The exact checker is
`computations/verify_n8_p5_degree6_compatibility_kills_h0.py`.

This closes the specific P5 escape found in
`notes/n8-counterexample-streamed-next-order.md`.  It is not an all-orders
standard-basis computation and does not by itself prove the global
conjecture.

## Symbolic P5 recursion

P5 is the 45-parameter linear branch

$$
z_{12}=z_{13}=z_{14}=z_{17}=\cdots=z_{23}=0,
\qquad z_{15}=z_{16}.
$$

All 45 remaining coordinates are retained as polynomial variables.  For the
39 normal-eliminated mixed equations, write

$$
Q_i=Q_i^{(2)}+Q_i^{(3)}+Q_i^{(4)}+\cdots
$$

and expand the strict transform with eleven transverse corrections.  The
checker verifies exact polynomial corrections at strict orders one, two, and
three.  They have respectively 6, 8, and 8 nonzero transverse entries.  The
incoming residual vectors have 48, 88, and 128 terms and cancel identically,
not merely at a sampled point.  Thus the mixed equations close through
original degree five over the entire 45-parameter P5 coordinate ring.

This also explains why allowing the free P5 coordinates themselves to bend
with the radial parameter cannot change the first degree-six compatibility.
The three earlier coefficients vanish as identities in those free variables;
substituting a moving free point into them still gives zero.  The first
nonzero coefficient is therefore evaluated at the limiting free point.

## Memory-bounded degree six

The direct all-equation degree-six expansion previously crossed roughly
3.7 GB.  The new checker restricts each correction multiplier and each mixed
equation factor to P5 separately, multiplies only after that restriction, and
then accumulates the result.  Its frozen ledger is:

- 12,022 candidate correction factors;
- 8,102 factors killed by the P5 multiplier restriction;
- 1,602 killed by the equation-factor restriction;
- 2,318 nonzero products, comprising 84,814 product terms before
  cancellation;
- 6,090 terms across the final 39 degree-six pieces, with at most 499 terms
  in one equation;
- 176 terms in the final strict-order-four residual.

This is the same exact normal remainder: eliminated linear normal forms
vanish after tangent restriction, so restricting the factorized residual is
equivalent to restricting its normal form.

## The compatibility ideal

Put

$$
b=z_{44}+z_{45},
\qquad
A=z_{16}^2z_{41}(z_9z_{25}-z_{11}z_{46}).
$$

There is an especially simple rank-11 chart.  In equations

$$
2,5,8,17,20,29,32,35,12,23,39,
$$

the transverse Jacobian is exactly $bI_{11}$, so its determinant is
$b^{11}$.  Since H0 itself contains $b$, every point where H0 is nonzero lies
on this chart.

After solving these eleven pivot equations, 26 of the 28 remaining
compatibilities vanish.  The two nonzero normalized equations are

$$
g_{30}=-\frac12 A(z_{26}+z_{45}),
\qquad
g_{33}=-\frac12 A(z_{26}-z_{44}).
$$

The earlier deterministic point check is recovered exactly:
$g_{30}=170841150$ and $g_{33}=-41001876$.

Let $u=z_{26}+z_{45}$ and $v=z_{26}-z_{44}$.  Since

$$
u-v=z_{44}+z_{45}=b,
$$

the chart ideal is $A\langle u,v\rangle$ and

$$
\langle g_{30},g_{33}\rangle:b^\infty=\langle A\rangle.
$$

Its reduced chart components are therefore

$$
z_{16}=0,
\qquad z_{41}=0,
\qquad z_9z_{25}-z_{11}z_{46}=0.
$$

Every one of them kills H0.  The omitted boundary component $b=0$ also kills
H0 directly.

## Exact H0 reduction

The degree-seven eight-term class was

$$
H0=A\,b\,(z_{53}-z_{51}).
$$

The compatibility factors give the stronger exact identity

$$
H0=-2(z_{53}-z_{51})(g_{30}-g_{33}).
$$

Thus H0 is already in the localized degree-six compatibility ideal on
$b\ne0$, not only in its radical.  Together with the direct $b=0$ vanishing,
every compatible P5 component forces H0 to vanish.

The frozen checker ledger has SHA-256
`0029166951a75000c77856a54d0606c940d78af19c9f1466fbc40e9550aca1f0`.

## Consequence for the search

The apparent eight-term H0 near miss is not evidence for an N=8
counterexample once the next mixed initial equations are included.  Further
P5 lifting is unnecessary for this class.  The local counterexample lane must
now find a different surviving pure standard-monomial class or push the
mixed standard-basis closure to the next filtered order; the present result
does not certify that no later class can appear.
