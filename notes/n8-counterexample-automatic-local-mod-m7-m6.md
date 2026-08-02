# Automatic local reduction reaches \(\mathfrak m^7\) and \(\mathfrak m^6\)

## Exact bounded result

At the rational point (p) on the exceptional (n=8) mixed torus, the
automatic translated-ring reducer proves

\[
 \boxed{H_0\in I_{\rm mix}+\mathfrak m_p^7,
 \qquad H_1\in I_{\rm mix}+\mathfrak m_p^6.}
\tag{1}
\]

All arithmetic is exact over ℚ.  Every correction has literal provenance:
it is a polynomial multiplier times a rational combination of full mixed
hafnian equations.  Thus (1) is an ideal-theoretic statement, not merely
vanishing on arcs or on the reduced tangent cone.

## Automatic reducer

The reducer begins with only three pieces of data:

1. the selected mixed coefficient having the same first conormal as the
   relevant pure coefficient;
2. the 196 exact Jacobian pivots, each expressed by literal mixed equations;
3. the 39 quadratic second-lift obstruction pivots, each lifted by cokernel
   back substitution to a literal mixed-equation combination with zero
   gradient.

At translated degree (d), it performs:

1. exact triangular division by the 196 linear conormals;
2. exact reduction of the free tangent remainder by the 39 quadratic
   obstruction forms;
3. lifting of those quadratic reductions to full mixed equations; and
4. a second conormal division clearing the ambient normal-coordinate tail.

Every division is replayed term by term.  The literal quadratic lifts are
checked to have zero gradient and exactly the requested tangent quadratic.
Corrections found at degree (d) are retained, so their higher Hasse tails
are automatically included at every later degree.

## Completed degrees

For colour zero, every translated degree from one through six closes with
zero tangent-obstruction and final-normal remainders.  The degree-six input
has 291,123 terms and its tangent normal form has only 32 terms; all 32
reduce through the quadratic obstruction basis.  This gives the
(I_{\rm mix}+\mathfrak m_p^7) statement.

For colour one, every degree from one through five closes.  The degree-five
input has 380,392 terms and its tangent normal form has 126 terms, again
with zero quadratic-obstruction remainder.  This gives the
(I_{\rm mix}+\mathfrak m_p^6) statement.

## Bounded scope

An exploratory colour-one degree-six run was stopped at approximately
1.32GB resident memory before producing a result, respecting a 1.5GB cap.
The frozen checker intentionally stops at degree five for colour one and
does not reproduce that unfinished run.  Therefore no claim about
(H_1\in I_{\rm mix}+\mathfrak m_p^7), and no all-orders membership claim,
is made here.

The five-linear-branch decomposition of the reduced quadratic tangent cone
and the 48-element Gröbner basis of its nonreduced ideal suggest the next
implementation improvement: reduce and checkpoint branchwise, or stream
normal-coordinate contributions directly into the tangent normal form,
rather than materializing the full colour-one degree-six ambient residual.

## Reproduction

```sh
python3 computations/verify_n8_counterexample_local_automatic_mod_m7_m6.py
```

The checker freezes all per-degree term counts, correction counts, zero
remainders, exact ranks, literal functional supports, and the bounded-scope
guard.
