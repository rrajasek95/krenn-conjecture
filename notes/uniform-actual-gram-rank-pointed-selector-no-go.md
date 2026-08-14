# The actual insertion Gram correspondence cannot isolate an occurrence

## Result

Let (n=2h+2).  A literal order-((h+1)) occurrence is an ordered
endpoint pair ((p,s)), together with a perfect matching (F) of the
remaining (2h) sites.  The actual insertion Gram entry is

\[
 K((p,s,F),(p',s',R))=|F\cap R|+C((p,s),(p',s')),
\]

where the endpoint term is the one computed in the uniform projector
theorem:

\[
 C=\begin{cases}
 4h^2+4h,&(p,s)=(p',s'),\\
 2h-1,&\text{exactly one ordered endpoint agrees},\\
 0,&\text{otherwise}.
 \end{cases}
\]

The Gram matrix has the exact uniform rank

\[
 \boxed{\operatorname{rank}K=\frac{n(3n-5)}2.}
\]

At (h=3), this is only (76) inside the (840)-dimensional literal
occurrence space.  More strongly, for every (h\ge3) an explicit
eight-matching covector in one fixed endpoint fibre annihilates the entire
Gram image and reads (-1) on a marked occurrence.  Therefore the nonzero
uniform projector composite does not construct the pointed occurrence
selector (P_f).

Checker:
[`verify_uniform_actual_gram_rank_pointed_selector_no_go.py`](../computations/verify_uniform_actual_gram_rank_pointed_selector_no_go.py).

## Factorization and rank

Let (Q) be the occurrence-by-ordered-endpoint incidence matrix and let
(X) be the occurrence-by-physical-edge incidence matrix,

\[
 Q_{(p,s,F),(a,b)}=[(p,s)=(a,b)],\qquad
 X_{(p,s,F),e}=[e\in F].
\]

Then

\[
 K=Q C_E Q^t+XX^t.
\]

Writing (b=2h-1) and (c=4h^2+2), the endpoint matrix is

\[
 C_E=cI+b(P+S),
\]

where (P) and (S) are the positive-semidefinite block all-ones
matrices for a fixed first or second endpoint.  Since (c>0), (C_E) is
positive definite.  Hence over the characteristic-zero theorem field,

\[
 \operatorname{im}K=\operatorname{col}(Q)+\operatorname{col}(X).
\]

The edge columns of (X) are independent.  Indeed, if edge weights
(w_{ij}) sum to zero on every residual perfect matching, four-vertex
matching exchanges give

\[
 w_{ab}+w_{cd}=w_{ac}+w_{bd},
\]

so (w_{ij}=a_i+a_j).  The vanishing matching sums then say
(sum_i a_i-a_p-a_s=0) for every (p\ne s), forcing every (a_i=0).

The intersection of the endpoint and edge column spaces consists exactly
of these additive vertex weights:

\[
 \sum_{ij\in F}(a_i+a_j)=\sum_i a_i-a_p-a_s.
\]

It has dimension (n).  Thus

\[
 \dim(\operatorname{col}Q+\operatorname{col}X)
 =n(n-1)+\binom n2-n
 =\frac{n(3n-5)}2.
\]

The checker independently obtains the ranks (39,76,125) for
(h=2,3,4) by exact finite-field elimination; the displayed argument
proves the formula over (mathbb Q) for every (h\ge2).

## Explicit pointed cokernel

On six residual sites use the integral matching relation

```text
- 01|23|45   + 01|25|34
+ 02|14|35   - 02|15|34
+ 03|12|45   - 03|14|25
- 04|12|35   + 04|15|23.
```

Its coefficient sum is zero and the marginal at every edge is zero.  It
therefore kills both endpoint-fibre indicators and all physical-edge
incidence columns.  It reads (-1) on the marked matching
(01|23|45).

For (h>3), tensor every displayed matching with one fixed perfect
matching of the additional (2h-6) residual sites.  The fixed-edge
marginals also vanish because the coefficient sum is zero.  This embeds
the same pointed cokernel at every order.

Thus even a source-valid lift of the complete actual Gram correspondence
would provide only endpoint aggregates and edge-additive matching
functions.  It cannot by itself supply the occurrence-asymmetric row
needed by Gate II.  A further selected response/Spencer comparison remains
load-bearing.

## Scope

This is an exact theorem about the actual all-role insertion Gram matrix,
not a denial of the already proved nonzero projector formula.  The two
results are compatible: the projector composite lands in the constant
aggregate sector, which lies in the rank-(n(3n-5)/2) Gram image.  The
present theorem proves that this aggregate success cannot be upgraded to a
pointed occurrence by linear combinations of Gram rows alone.

It does not exclude a nonlinear occurrence selector, a new
restriction/reinsertion comparison, or the missing response-to-cap
operation arrow.
