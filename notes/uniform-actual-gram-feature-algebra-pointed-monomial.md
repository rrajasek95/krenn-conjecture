# The nonlinear Gram-feature algebra has a monic pointed selector

## Result

The actual insertion Gram matrix cannot linearly isolate an occurrence, but
its coefficient feature algebra can.  Let

\[
 f=(p,s,F)
\]

be a marked occurrence at order (h+1).  Write (Q_{p,s}) for the
ordered-endpoint fibre indicator and (X_e) for the residual-edge incidence
function.  For any marked edge (e_0\in F),

\[
 \boxed{
 Q_{p,s}\prod_{e\in F\setminus\{e_0\}}X_e=e_f.
 }
\]

Indeed, after the (h-1) displayed edges are fixed, only two residual
vertices remain unmatched, so the final edge is forced.  The selector has
feature degree (h): one endpoint factor and (h-1) edge factors.

At (h=3), this is the particularly small cubic

\[
                       Q_{p,s}X_{e_1}X_{e_2}=e_f.
\]

Checker:
[`verify_uniform_actual_gram_feature_algebra_pointed_monomial.py`](../computations/verify_uniform_actual_gram_feature_algebra_pointed_monomial.py).

## Exact completion counts

Within a fixed endpoint fibre, choosing (d) disjoint edges of the marked
matching leaves (2(h-d)) residual vertices.  The number of matching
completions is

\[
                         (2(h-d)-1)!!.
\]

Thus the monic selector counts at (h=2,3,4) descend as

```text
h=2: 3, 1
h=3: 15, 3, 1
h=4: 105, 15, 3, 1.
```

The checker enumerates every literal occurrence in these three orders and
verifies the unique final support.  The uniform argument is the two-vertex
completion observation above.

## Relation to the linear no-go

The linear Gram theorem identifies

\[
 \operatorname{im}K=\langle Q_{p,s},X_e\rangle
\]

and gives an eight-matching covector which kills that span.  There is no
contradiction: the displayed pointed class is a product in the feature
algebra, not a linear combination of features.  The eight-matching
covector detects precisely this first nonlinear escape.

This sharpens the remaining proof obligation.  At (h=3), no higher
coefficient ansatz is needed: one endpoint selector and two edge
restriction projectors already give the marked delta exactly.  What is
missing is a source-valid lift of their cubic product through the
principal-parts/Hasse complex.

Such a lift must retain:

* the endpoint and matching labels;
* all product-rule faces of the two edge restrictions;
* word, fine, and repeated-site grades;
* target, ordinary residue, physical (q), anchor, (W), ridge, and
  eta/sigma readouts.

These are exactly the faces isolated by the current Gate-II and cubic
totalization audits.  The coefficient selector is now explicit; the open
statement is its augmented multiplicative realization.

## Scope

This is an identity in the pointwise algebra of occurrence features.  It
does not assert that pointwise multiplication of Gram-image vectors is an
allowed fixed-source operation.  Macaulay multiplication changes the
physical polynomial grade, and restriction/reinsertion creates the proper
PP/Hasse faces.  Identifying the cubic feature product with a physical
same-grade response-to-cap comparison would assume the missing theorem.
