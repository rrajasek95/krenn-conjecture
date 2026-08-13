# The generic lower Cartan remainder is one universal trace jet

Research reduction and typing guard.  The generic target construction of
`c6e08c6` is strengthened to a full cap-matrix identity.  The resulting
lower remainder is parameter-free.  Its literal truncated-Rees value is not
yet defined because the required shifted map into the diagonal Rees module
has not been constructed.

Checker:
[`verify_h3_trace_cartan_lower_rees_typing_gate.py`](../computations/verify_h3_trace_cartan_lower_rees_typing_gate.py).

## Full trace reduction

For general `h`, write

\[
 K_1=(\alpha+\beta)K_0-\alpha I,
 \qquad
 J_2=((h-1)\alpha-\beta)K_0-(h-1)\alpha I.
\]

Then the generic combination is an identity of full cap matrices:

\[
\begin{aligned}
J_*&=(\beta-(h-1)\alpha)J_1+(\beta+\alpha)J_2\\
   &=-h\alpha\beta I.                                  \tag{1}
\end{aligned}
\]

Since the cap polynomial `P(L)` is linear in `L`, the normalized even
Cartan remainder from `c6e08c6` becomes

\[
 \boxed{R_+=-{1\over h}(1+\rho)H_wd(P(I)).}             \tag{2}
\]

At `h=3`, its coefficient is exactly `-1/3`.  All `alpha` and `beta`
dependence cancels.  Thus the generic inactive lower-face problem is not a
family of unequal `J1/J2` calculations.  It is one universal identity-cap
trace jet.

## Why its truncated-Rees value cannot yet be computed

The two objects needed to form the class currently live in different
committed modules:

```text
R+       complete trace principal-parts Cartan source orbit,
N_lit    diagonal 15-label collision/Rees source module.
```

Commit `981f1b0` proves what happens **after** a source-labelled
Hasse/Rees-linear comparison is given: the three seed coherences propagate
at every jet order.  It does not construct the comparison from the trace
Cartan orbit to the physical fifteen-label quotient.

This is a real logical gap, not missing arithmetic.  In the smallest Rees
model let

\[
 M=\langle b,z,r\rangle,\qquad N_{\rm lit}=\langle b\rangle,
 \qquad \epsilon(b)=\epsilon(z)=0,\quad\epsilon(r)=1.
\]

Two Hasse/Rees-linear maps with identical evaluated target and fixed
order-zero data may send the trace remainder respectively to `b` or `z`.
The first gives zero obstruction and the second gives the nonzero class
`[z]`.  Tensoring with `Q[ell]/ell^r` repeats, rather than removes, this
choice.  Therefore the expression

\[
 \left[-{1\over3}\tau_+((1+\rho)H_wd(P(I)))-L_{\rm adj}ight]
 \in(\ker\epsilon/N_{\rm lit})\otimes\mathbb Q[\ell]/(\ell^r) \tag{3}
\]

is the exact truncated-Rees class only **after** the shifted physical label
map `tau_plus` is supplied.  Without `tau_plus`, assigning a numerical value
to (3) would silently choose the missing comparison.  This is the even
analogue of the Gate-I `K d(u)` typing guard.

## Existing fillers do not decide the choice

The fourth-Hasse adjacent cone has formal projected boundary

\[
              ((H_0-u)e_{\rm Eq},Yw)
\]

instead of `(0,Yw)`.  The covector `(Y,-(H0-u))` kills the projected vector
and detects the desired one by `-(H0-u)Y`.  Root decoration simply tensors
this nonzero conormal with `(w-1)Delta`; it does not make it vanish.  Hence
the known reduced-Eq/fourth-Hasse family cannot define the good choice of
`tau_plus`.

The now constructed literal `M_v` family does not help either.  Its Cartan
and collision source type is `rho`-odd, while (2) is `rho`-even.  Over
characteristic zero the two parity summands meet trivially, at every Rees
order.

The smallest remaining datum is therefore

> a source-provenant shifted map `tau_plus` from the complete trace-Cartan
> principal-parts orbit to the diagonal fifteen-label Rees module.  If (3)
> vanishes, it constructs the generic adjacent target cone.  If it does not,
> its first nonzero coefficient is the literal Rees/typed-exit class.  The
> old fourth-Hasse repair of that coefficient still needs the independent
> zero-target, zero-residue reduced-Eq relative cell.

## The `beta=0` branch is genuinely separate

At `beta=0`,

\[
                 J_2=(h-1)J_1,qquad J_*=0.             \tag{4}
\]

For the selected colour `0` and the physical local `0 <-> 2` roots, the
collapsed row sees only the pure-`2` root defect `D2`.  The desired
two-sided Weyl defect is `D0+D2`.  Thus the missing coordinate is exactly
the `D0` branch.  It is the selected-colour order-`h` unary target jet
already isolated by the collision calculation (or, equivalently, a proof
that a complementary label survives).

The abstract identity-cap Cartan cell `-(1/h)(1+rho)H_w(P(I))` remains
defined at `beta=0`, but it no longer identifies the collapsed selected
diagonal jet with that cell.  Hence it does not remove the unary/complement
obligation.

## Verification

Run:

```text
python3 computations/verify_h3_trace_cartan_lower_rees_typing_gate.py
python3 -O computations/verify_h3_trace_cartan_lower_rees_typing_gate.py
python3 -I -S computations/verify_h3_trace_cartan_lower_rees_typing_gate.py
```

Frozen ledger SHA-256:

```text
3b6a9b46c2511b69c06be5810e603cdc42856290b233d86dca7d5f8a57d50da2
```
