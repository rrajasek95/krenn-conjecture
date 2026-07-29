# Odd-characteristic six-boundary barrier

This note isolates what an odd-prime reduction would actually have to add.
For a retained six-set, the pair-cap obstruction has an integral form that
survives characteristic three.  An exact binary eight-site source has a
tensor-active pair for which **every** nondegenerate covector has a nonzero
six-boundary defect over every odd-characteristic extension.  For primes at
least five, all bounded-degree cap, adjugate, and polarization assertions
transfer unchanged to characteristic zero.

This does not rule out a global, specifically ternary selection theorem.  It
rules out obtaining one merely by passing to an odd-characteristic extension
or by treating the characteristic-three factorial collapse as cleanliness.

## 1. Denominator-free six-site pair-cap equation

Delete a pair `p,q` and retain six vertices `U`.  Cap the deleted slots by
an arbitrary covector `K`.  In the square-free vertex algebra, let `x` be
the old internal quadratic, let `r=r_K` be the first-jet quadratic, and put

\[
 s=\langle K,X_{pq}\rangle .
\]

Write `H_(3,0)(x,r)=H_U(x)`, let `H_(2,1)(x,r)` be the sum over perfect
matchings with two `x`-edges and one `r`-edge, let `H_(1,2)(x,r)` be the
sum with one `x`-edge and two `r`-edges, and put
`H_(0,3)(x,r)=H_U(r)`.  Directly sorting matchings by the number of
first-jet edges gives

\[
 K\mathbin{\lrcorner}H_{U\cup\{p,q\}}(X)
   =sH_{(3,0)}+H_{(2,1)},                                \tag{1}
\]

whereas, for `s!=0`,

\[
 sH_U(x+r/s)
  =sH_{(3,0)}+H_{(2,1)}
    +s^{-1}H_{(1,2)}+s^{-2}H_{(0,3)}.                    \tag{2}
\]

Consequently the canonical first-jet absorption is clean exactly when

\[
 \boxed{\quad H_U(r)+sH_{(1,2)}(x,r)=0.\quad}             \tag{3}
\]

Equation (3) is integral and valid in every characteristic.  If `2` and
`3` are invertible, it is equivalent to the logarithmic condition

\[
 r^3+3sr^2x=0,                                           \tag{4}
\]

after dividing the support-six component by `6`.  In characteristic three,
(4) is identically zero and therefore carries no information: the actual
condition remains (3).  In particular, the vanishing of `3!` in a
square-free power must not be mistaken for the vanishing of the hafnian,
which is defined as the unordered matching sum.

For a rank-one cap, the balanced-signature identity gives
`H_U(r)=6D_(U,3)=0` in characteristic three.  Even then (3) reduces only to

\[
                         sH_{(1,2)}(x,r)=0,               \tag{5}
\]

and the two-first-jet sector is not forced to vanish.

## 2. An all-covector obstruction that survives every odd prime

Take the rational binary six-site source from `notes/induction-route.md`
and subdivide its old edge `56` by the path `5-7-8-6`, exactly as in
`notes/uniform-six-vertex-reduction.md`.  Its nonzero cells are

\[
\begin{array}{c|c}
12&(e_0+e_1)e_0\\
34,24&e_0e_0\\
13&-e_1e_0\\
16,23&e_1e_1\\
45&\frac34e_1e_1\\
15,46&\frac12e_1e_1\\
57,68&e_0e_0\\
78&e_1e_1.
\end{array}                                               \tag{6}
\]

Perfect-matching enumeration over `Z[1/2]` gives exactly

\[
                         H_8(X)=e_0^{\otimes8}+e_1^{\otimes8}. \tag{7}
\]

The edge `13` is tensor-active.  Cap it by the completely general covector

\[
 K=\sum_{a,b=0}^1k_{ab}e_a^*\otimes e_b^*.
\]

On `U=(2,4,5,6,7,8)`,

\[
 s=-k_{10},\qquad \kappa_0=k_{00},\qquad\kappa_1=k_{11}. \tag{8}
\]

Let `R_K` be the exact first-jet edge family and clear the denominator by
putting `Z=sX|_U+R_K`.  Since a six-site hafnian is cubic, cleanliness is
equivalent to

\[
 H_U(Z)=s^2\{k_{00}e_0^{\otimes6}+k_{11}e_1^{\otimes6}\}. \tag{9}
\]

All coefficients in the difference in (9) vanish except one:

\[
 \boxed{
 [e_1^{(2)}e_0^{(4)}e_1^{(5)}e_1^{(6)}e_1^{(7)}e_1^{(8)}]
 \left(H_U(Z)-s^2K\mathbin{\lrcorner}\Delta_{8,2}\right)
      =-k_{10}^2k_{11}=-s^2\kappa_1.}                    \tag{10}
\]

Thus `s*kappa_0*kappa_1!=0` forces a nonzero higher-boundary defect for
every covector.  The coefficient in (10) is `-1`, so the conclusion remains
valid over every field of odd characteristic and every extension of such a
field.  Characteristic three does not clean this pair.

This is a six-boundary version of the four-boundary example in
`notes/pair-covector-selection-obstruction.md`.  It refutes any local rule
claiming that activity, a coordinate rank-one direct edge, arbitrary choice
of covector, and passage to an odd-characteristic extension suffice.  The
source has other clean pairs, so it does not refute a genuinely global pair
selection theorem.

## 3. Why infinitely many large odd primes give no bounded-degree shortcut

Fix `n`.  Any proposed reduction using finitely many cap parameters,
hafnian adjugates, bounded polarization variables, polynomial equations,
and polynomial nonvanishing conditions can be written as a first-order
sentence in the language of rings with integer coefficients.  An inequality
`f!=0` is encoded by adjoining `t` and the equation `tf-1=0`.  Allowing an
arbitrary algebraic field extension adds nothing once the base field is
already algebraically closed.

By the Lefschetz principle for algebraically closed fields, every fixed such
sentence has the same truth value over characteristic zero and over
`overline(F_p)` for all sufficiently large primes `p`.  One elementary
proof uses compactness: either the sentence or its negation belongs to the
complete theory `ACF_0`; a finite subset of the characteristic-zero axioms
already implies it, and that finite subset excludes only finitely many
positive characteristics.

Therefore:

**Large-prime transfer proposition.**  For fixed `n`, a single
bounded-degree algebraic cap/adjugate/polarization selection assertion holds
over `overline(F_p)` for infinitely many primes if and only if it holds over
`C` (equivalently, it then holds for every sufficiently large prime).

This does not make an odd-prime theorem useless: combined with the known
six-site obstruction, it would prove the characteristic-zero conjecture at
that fixed order.  It shows that primes `p>=5` do not supply an easier
factorial or extension-field mechanism.  A genuinely characteristic-
dependent route must use operations whose degree grows with `p`.  The
inverse-hafnian reciprocity in
`notes/odd-prime-inverse-hafnian-tautology.md` is of that type, but its full
transversal expansion is exactly a scalar multiple of the original GHZ
identity and yields no new constraint.

## 4. Exact audit

Run

```text
uv run python computations/verify_odd_characteristic_paircap_barrier.py
```

The checker independently enumerates all `105` matchings of the eight-site
source, verifies (7), derives the full symbolic first-jet family for a
general four-parameter covector, verifies activity of `13`, and proves the
complete coefficient identity (10).
