# N=8 P5 streamed degree-seven mixed tails

## Result

The 39 normal-eliminated mixed equations have now been continued on the full
45-parameter P5 branch through original degree seven.  The exact checker is
`computations/verify_n8_p5_streamed_degree7_mixed_tails.py`.

This is the continuation artifact needed after the degree-six compatibility
relations kill the eight-term H0 class.  It does not yet compute the next
pure H0 or H1 normal form.

## Quotients without the degree-six ambient expansion

At degree six, a direct ambient residual/quotient expansion crossed the local
memory budget.  The checker instead uses the following exact identity.

Let $L_p$ be the 196 echelon linear normal forms and let $d_p$ be their dual
ambient directions, so $L_q(d_p)=\delta_{pq}$.  If

$$
R^{(6)}=\sum_p L_p Q_p+R_T
$$

is the degree-six normal division, then the restriction of $Q_p$ to the
tangent is the first normal derivative

$$
Q_p|_T=(d_pR^{(6)})|_T.
$$

The degree-seven correction needs only the contraction of these quotients
with the quadratic part $E_p^{(2)}$ of the corresponding mixed equation.
Rather than compute every $Q_p$, the checker forms the single
polynomial-valued ambient direction

$$
D=\sum_p E_p^{(2)}|_{P5}\,d_p
$$

and applies $D$ to each factorized degree-six residual.  Product rules are
applied before P5 restriction, so neither the degree-six ambient residual nor
its quotient polynomials are materialized.

The 196 dual directions have only 283 nonzero ambient entries in total and at
most 9 in one direction.  Only 95 pivots have a nonzero quadratic restriction
on P5; the contracted direction uses 95 ambient coordinates and 192 terms.

## Exact regression

The quotient-as-normal-derivative construction is checked one order earlier,
where the old materialized answer is available.  For all 39 equations, it
reconstructs exactly the 1,910 terms in the degree-five P5 restrictions.
This validates both the dual directions and the sign/product-rule convention
before they are used at the memory frontier.

## Frozen degree-seven ledger

Across the 39 equations:

- the degree-six P5 residuals have 6,090 terms;
- the old degree-seven factorized restrictions have 83,943 terms;
- the contracted degree-six quotient correction has 85,619 terms;
- cancellation leaves 16,507 degree-seven terms;
- all 39 degree-seven equations are nonzero, with at most 1,658 terms in one
  equation.

The exact 39-polynomial output has SHA-256
`fe215181e1e2d16bfe7bd47eb9e8934a44c4c1f8b96b4116f8b6b15417da4660`.
The full checker ledger has SHA-256
`e995dfca1bfab971279dc88bfad82ef1c9bb53f6522b832371ce24e5e71e717c`.

## Scope and next calculation

This checker certifies the ambient-normal-eliminated mixed tails only.  The
next formal-local step is to combine them with the degree-six P5
compatibility generators, solve the strict-order-five P5 pivots on each
compatible component, and then reduce:

- the next H1 coefficient at original degree seven; and
- the next H0 coefficient at original degree eight, including the lifted
  tail of the relation that killed its degree-seven class.

Until those reductions are frozen, this result neither exhibits a later pure
standard-monomial survivor nor advances formal-local pure membership by
another order.
