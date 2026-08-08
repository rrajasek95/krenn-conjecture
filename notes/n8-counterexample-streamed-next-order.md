# Streamed next orders at the exceptional eight-site mixed torus

## Exact outcome

Let (p) be the rational point on the five-parameter mixed torus and let
(I_{\rm mix}) be the ideal of the 6,558 mixed hafnian coefficients in the
translated 252-variable ring.  The previous automatic calculation proved

\[
 H_0\in I_{\rm mix}+\mathfrak m_p^7,
 \qquad H_1\in I_{\rm mix}+\mathfrak m_p^6.
\]

The memory-bounded next-order reducer now proves

\[
 \boxed{H_1\in I_{\rm mix}+\mathfrak m_p^7.}
\tag{1}
\]

For (H_0), translated degree seven does not close through the known
48-element tangent standard basis.  Its exact standard-monomial remainder is

\[
\boxed{
 z_{0411}^{,2}z_{3511}(z_{3710}+z_{3711})
 (z_{6711}-z_{6701})
 (z_{0301}z_{1301}-z_{0321}z_{3712}).
}
\tag{2}
\]

Expansion of (2) has eight unit-coefficient terms.  It is already reduced by
the 39 quadratic leading forms and none of the nine additional cubic leading
monomials divides a term.

This is progress in both directions.  Equation (1) removes the former
degree-six memory boundary for (H_1).  Equation (2) is the first explicit
higher pure class not absorbed by the current lifted initial ideal, so it
replaces an unspecified all-orders obstruction with one small polynomial.

## Why the computation is memory bounded

The old reducer first formed the full ambient residual and then divided by the
196 independent linear conormals.  The unfinished (H_1) degree-six run
passed 1.32 GiB before returning a result.

Let (\rho) be restriction to the 56-dimensional mixed tangent space.  The
echelon construction makes (\rho) the normal-form map modulo those 196
linear forms.  Since it is a ring homomorphism,

\[
             \rho(mG)=\rho(m)\rho(G).                       \tag{3}
\]

The new reducer applies (3) separately to every stored multiplier and literal
mixed-equation combination.  It never forms their ambient product.  For
(H_1) at degree six, 643 corrections project to a 573-term tangent
polynomial; exact division by the 39 quadratic obstruction rows takes 426
steps and has zero remainder.  The largest individual projected product has
2,048 terms.  Because every linear conormal and every quadratic obstruction
has a literal mixed-equation lift, zero tangent remainder proves (1), not only
formal-arc vanishing.

For (H_0) at degree seven, 474 corrections project to 134 tangent terms.
After 105 quadratic reductions, the eight terms in (2) remain.

As a regression against an implementation shortcut, the checker compares the
streamed projection with the old materialize-then-divide normal form at every
previously feasible degree: one through six for (H_0) and one through five
for (H_1).  All eleven polynomial identities agree exactly over
(\mathbb Q), including the former 291,123- and 380,392-term ambient inputs.

## Ferrers branch localization

Restrict (2) to the five linear minimal primes (P_1,\ldots,P_5) of the
second-lift Ferrers radical.  Direct polynomial substitution gives remainder
term counts

\[
                         (0,0,0,0,8).                       \tag{4}
\]

Thus the new class vanishes on (P_1,P_2,P_3,P_4) and survives unchanged on
(P_5).  In the tangent-index notation of the branch audit, its factor
(z_{3710}+z_{3711}) is the Ferrers variable (b), which kills the first four
branches; (P_5) does not contain it or another factor of (2).

The next counterexample-lane target is therefore sharply localized: compute
the strict-transform recursion on (P_5) through the order at which (2)
appears.  A new mixed initial equation may still cut (2), while survival on a
genuine lifted (P_5) component would identify the first direction on which
the missing pure coefficient can turn on.  Nothing here proves that (P_5)
lifts, that (H_0\notin\sqrt{I_{\rm mix}}), or that an all-pure point exists.

## Reproduction

```sh
.venv/bin/python computations/verify_n8_counterexample_streamed_next_order.py
```

The checker uses exact rational arithmetic, retains the earlier literal
mixed-equation provenance, freezes the streamed/full regression ledger, the
two next-order reductions, factorization (2), cubic-lead test, and all five
branch restrictions by SHA-256.
