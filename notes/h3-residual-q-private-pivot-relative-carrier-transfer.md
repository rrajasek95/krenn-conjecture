# The residual-q private pivots transfer exactly to the AugP2 carrier

## Result

The literal obstruction to the normalized residual-(q) cap factorization
is not an additional algebraic generator once the relative occurrence
carrier is retained. It transfers exactly to that carrier.

In the four tail corners

```text
P+q00, P-q00, P+q11, P-q11
```

the desired endpoint-odd correction uses coefficients



\[
                  \alpha=(-1,1,1,-1).                 \tag{1}
\]

The quotient identity

\[
             K=-r_0+T+\rho-C                         \tag{2}
\]

has a literal private pivot on (r_0). Consequently the four complete-row
copies of (2) yield the desired residue-only KS signature plus the private
debt

\[
                     p=-\alpha=(1,-1,-1,1).           \tag{3}
\]

Crucially, (sum p_i=0).

The universal relative occurrence graph has (C=12I-J) and

\[
                       d\Gamma_i=t_i-c_i.             \tag{4}
\]

After embedding the four labelled private pivots as four (c_i) coordinates,
take the (p)-combination:

\[
                       d\Gamma_p=t_p-p.               \tag{5}
\]

Adding (5) to the complete cap combination cancels every displayed private
pivot and leaves

\[
         \boxed{\text{desired KS residue correction}+t_p}.          \tag{6}
\]

Thus one physical boundary with principal part (-t_p) completes the
literal correction.

Verified by
[`verify_h3_residual_q_private_pivot_relative_carrier_transfer.py`](../computations/verify_h3_residual_q_private_pivot_relative_carrier_transfer.py).

## Why this is the same carrier

On the centered subspace, (C) acts by 12. Hence (3) has raw occurrence
preimage (p/12), and (C(p/12)=p). No localization or division by a source
variable is involved—only the characteristic-zero scalar (1/12).

The relative graph is presentation-safe because (t_p) remains. Equation
(5) does not assert (p=0); it identifies the private debt with a retained
degree-zero carrier. Erasing (t_p) would change the physical fibre, exactly
as in the general relative-graph theorem.

This is the useful convergence:

- the residual-(q) KS quotient needs the private pivots canceled;
- the AugP2/P2 construction needs the centered occurrence carrier landed;
- after the labelled embedding, these are the same physical landing problem.

So a successful complete AugP2 carrier landing also removes the separate
private-pivot obstruction in the residual-(q) construction. Conditional on
the remaining residue/eta faces, the already pinned KS theorem then closes
the E14 endpoint self-loop and the unequal-tail five-lock holonomy.

## What remains open

Two physical statements are deliberately not hidden in (5).

First, the complete full-nine rows have many private monomials. One must
construct the source-labelled occurrence embedding functorially for every
one needed by the four-corner packet; the four-coordinate calculation only
proves the universal formula after that typing.

Second, the landing of (t_p) must carry all its forced faces:

1. the E14 unary target-normal face;
2. scalar cap residue and reduced Eq;
3. the pointed anchor conormal;
4. physical (q);
5. the shifted Kähler ridge, (W), and eta/sigma readouts.

These are precisely the mixed AugP2/E14 cell isolated by the current
frontier. The coefficient transfer neither constructs it nor promotes a
failure covector to a physical terminal.

## Scope

This is an exact theorem for the four-corner linear cap block and the
universal relative graph. It reduces the number of independent interfaces;
it is not yet the source-labelled embedding, the absolute carrier landing,
or a proof of the conjecture.
