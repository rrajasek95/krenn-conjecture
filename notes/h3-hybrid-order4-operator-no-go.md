# Hybrid homogenizer directions do not rescue the order-four Spencer operator

This is an exact bounded no-go, not a proof of Krenn's conjecture.

## Outcome

In the direct-free (h=3) model put

\[
 I=(A,B),\qquad A=H_m,\qquad B=H_0-u,
\]

where (A) is a squarefree quartic in 27 mixed edge variables and the
homogenizer (u) has weight four.  Write an arbitrary polynomial
differential operator in left-normal Weyl form

\[
                         D=\sum_T c_T\partial_T .
\]

There is no such operator of total order at most four satisfying

\[
                         D(I^2)\subseteq I,
             \qquad       D(A)=1.                         \tag{1}
\]

This closes the hybrid-(\partial_u) gap left in
[`h3-apolarity-operator-split-verdict.md`](h3-apolarity-operator-split-verdict.md)
at the only order where the formal fourth-Hasse unit first appears.

## Proof

Decompose (D) by the weight shift which contributes the constant in
(D(A)).  Since both generators of (I) have weight four, only shift
(-4) can contribute that unit.  For a derivative multiset using only
edge variables and having total order at most four, its coefficient in
that shift has weight

\[
                         |T|-4.
\]

It is therefore zero for (|T|<4) and constant for (|T|=4).  A
four-edge derivative sends (A) to a nonzero constant precisely for one
of the 90 matching monomials of (A).  The cited exact ideal-level
calculation proves that the (A^2) part of (1) has rational rank 90 on
these 90 coefficients and forces all of them to zero.  Hence the
edge-only part has zero unit trace.

Now allow (u).  Since (A) and (A^2) are independent of (u), every
normal-form term whose derivative multiset contains (\partial_u)
annihilates both.  It can change the (AB) and (B^2) conditions, but it
cannot change either the (A^2) forcing system or (D(A)).  The same is
true of derivatives in the 27 pure edge variables absent from (A).
Thus no hybrid term repairs the already full-rank obstruction, proving
(1).

The argument uses normal form only: coefficients are placed to the left
of derivatives, as every polynomial Weyl operator can be uniquely
written.  It does not assume constant coefficients for hybrid terms.

## Scope and next boundary

The result is deliberately order-bounded.  An edge derivative of order
five through eight annihilates the quartic (A) but can act nontrivially
on (A^2), so it could in principle repair the order-four forcing system
without changing (D(A)=1).  This note does not exclude that possibility.
It also does not decide the weaker generator-level (R)-linear Hasse
totalization or construct a physical source chain.

Reproduce with

```text
python3 computations/verify_h3_hybrid_order4_operator_no_go.py
python3 -O computations/verify_h3_hybrid_order4_operator_no_go.py
```

The checker reruns the pinned exact apolarity calculation, verifies the
55-variable support split, recomputes the 90 unit derivatives, directly
checks that (\partial_u) and every edge outside (\operatorname{supp}A)
annihilate both (A) and (A^2), and freezes the resulting ledger.
