# The missing pure coefficients have cubic contact

## Exact outcome

Let (p) be the rational (a=b=c=d=e=1) specialization of the
five-parameter mixed-ideal torus from `aa4a731`.  Thus

\[
  (H_0(p),H_1(p),H_2(p))=(0,0,1).
\]

The first-jet audit showed that (dH_0) and (dH_1) belong to the mixed
conormal at (p).  The exact second-jet calculation strengthens this to

\[
  \boxed{H_0(x(t)),H_1(x(t))\in t^3\mathbf Q[[t]]}
\]

for every formal arc (x(t)) in the full 252-variable mixed fibre with
(x(0)=p).  A branch on which all three pure coefficients are nonzero can
therefore meet this one-pure stratum only with at least cubic contact.

## Certificate

The full mixed Jacobian has rank (196), and an exact sparse elimination
constructs a {\(\pm1\)}-valued basis (v_1,\ldots,v_{56}) of its kernel.
The largest basis support has size ten.  Every one of the 1,312 nonzero
mixed Jacobian rows is replayed against all 56 vectors.

At (p) there are exact first-differential identities

\[
  dH_0=dH_{00000010},\qquad
  dH_1=dH_{11000111}.
\]

For a coefficient (H_w), write (q_w(v)) for the coefficient of (t^2)
in (H_w(p+tv)).  Direct expansion of the 105 perfect-matching terms gives
two nonzero ambient quadratic differences

\[
  q_0-q_{00000010},\qquad q_1-q_{11000111},
\]

with respectively 24 and 96 signed coordinate-pair terms.  They are not
ambient polynomial identities.  Nevertheless their restrictions to the
entire mixed tangent space vanish exactly.  The checker verifies all 56
diagonal evaluations and all

\[
  \binom{56}{2}=1540
\]

polar evaluations for each quadratic difference.

Now let

\[
  x(t)=p+tv+t^2w+O(t^3)
\]

be a mixed-fibre arc.  Its linear equations give (v\in\ker J_{\rm mix}).
The selected mixed equation at second order gives

\[
  dH_{w_i}(w)+q_{w_i}(v)=0.
\]

Because (dH_i=dH_{w_i}) and
((q_i-q_{w_i})|_{\ker J_{\rm mix}}=0), the coefficient of (t^2) in
(H_i(x(t))) is zero, for (i=0,1).  Constants and linear coefficients
already vanish, proving the displayed cubic-contact assertion.

The five-parameter Laurent family is a port-torus orbit.  Diagonal torus
transport therefore carries this second-order osculation statement to
every generic point of that family (with the corresponding nonzero scalar
factors in the two selected mixed equations).

## Structural meaning

This explains why natural local attacks have looked unexpectedly weak.
The pure map is not merely critical along the exceptional torus: its two
missing coordinates have zero second fundamental form on the mixed tangent
space.  Linear transversality, a generic tangent search, and even a
quadratic deformation search cannot see an all-pure branch there.

The promising proof route is consequently an osculation/valuation lemma,
not another sparse-zero search.  One should try to show that the Hasse
jets of a missing pure coefficient are successively controlled by selected
mixed coefficients, ideally by a port-graded identity that persists to all
orders.  A third-jet identity would be the next decisive test: persistence
would point toward formal local membership; failure would identify the
first genuinely new deformation that any global proof must control.

## Reproduction

```sh
python3 computations/verify_n8_counterexample_pure_second_jet.py
python3 -O computations/verify_n8_counterexample_pure_second_jet.py
python3 -I computations/verify_n8_counterexample_pure_second_jet.py
python3 -S computations/verify_n8_counterexample_pure_second_jet.py
```

The frozen ledger records the Jacobian rank and tangent dimension, exact
kernel shape, ambient quadratic supports, all restricted-form checks, and
the formal-arc conclusion.
