# The actual Gram projector composite is nonzero for every order

## Result

Let the marked occurrence at order (h+1) be

\[
f=(p_f,s_f,F),
\]

where (F) is the marked perfect matching on the (2h) residual sites.
For another literal occurrence (g=(p,s,R)), the all-role insertion Gram
row has the uniform formula

\[
k_f(g)=|F\cap R|+C_{p,s},
\]

with

\[
C_{p,s}=\begin{cases}
4h^2+4h,&(p,s)=(p_f,s_f),\\
2h-1,&p=p_f\text{ or }s=s_f\text{, but not the marked pair},\\
0,&\text{otherwise}.
\end{cases}
\]

This is the literal Gram row, including the multiplicity (2h) of the
chart in which both new sites become endpoints.

Let (A_h) be the residual two-switch adjacency and put

\[
\lambda_h=h^2-3h+1.
\]

The matching numerator acts fibrewise by

\[
(A_h-\lambda_h I)k_f
=q_{p,s}+(2h-1)C_{p,s},
\]

where (q_{p,s}) counts marked residual edges avoiding both endpoints.  The
right side is independent of (R).  Applying the endpoint cubic

\[
P_h(B_h)=(B_h+2I)(B_h-(2h-2)I)(B_h-2hI)
\]

then gives the closed formula

\[
\boxed{
P_h(B_h)(A_h-\lambda_h I)k_f
=56h^3(2h-1)\,\mathbf 1.
}
\]

In particular the actual composite is nonzero for every (h\ge2).  It
recovers the formerly bounded values

```text
h=3:  7560
h=4: 25088.
```

Checker:
[`verify_uniform_actual_gram_projector_composite_formula.py`](../computations/verify_uniform_actual_gram_projector_composite_formula.py).

## Chart count

The Gram formula follows by classifying the insertion charts which contain
the marked occurrence.

1. A residual-edge chart contributes one precisely when its marked edge is
   also an edge of (R).  Summing gives (|F\cap R|).
2. If the new (p)-endpoint remains (p_f), there are (2h) bridge choices
   at (s=s_f), and (2h-1) otherwise.  The new (s)-endpoint charts are
   symmetric.
3. If both marked endpoints are new, the unique oriented chart has fibre
   multiplicity (2h) on both sides of the Gram product and contributes
   (4h^2).

At the marked ordered pair these endpoint contributions total

\[
2h+2h+4h^2=4h^2+4h.
\]

If only the marked (p)- or marked (s)-endpoint remains, the total is
(2h-1).  No other insertion chart contributes.

## Matching numerator

For each available marked edge (e), its incidence function on residual
matchings obeys

\[
A_h\phi_e=1+\lambda_h\phi_e.
\]

There are (q_{p,s}) available marked edges.  Constants have switch degree
(h(h-1)), and

\[
h(h-1)-\lambda_h=2h-1.
\]

These identities give the displayed matching-flat row without any bounded
enumeration.

## Endpoint average

There are (n=2h+2) sites and (n(n-1)) ordered endpoint pairs.  Double
counting marked residual edges gives

\[
\sum_{p\ne s}q_{p,s}=h(n-2)(n-3)=2h^2(2h-1).
\]

The endpoint constants satisfy

\[
\sum_{p\ne s}C_{p,s}
=(4h^2+4h)+4h(2h-1)=12h^2.
\]

Therefore the matching-flat row has sum (14h^2(2h-1)).  Its mean is

\[
\frac{7h^2(2h-1)}{(h+1)(2h+1)}.
\]

The endpoint cubic kills every nonconstant ordered-pair sector, while on
the constant sector it acts by

\[
P_h(4h)=8h(h+1)(2h+1).
\]

Multiplying this eigenvalue by the mean proves the boxed formula.

## Scope

This closes the all-order coefficient and evidence gap for the actual Gram
row.  It does not build the physical lift of (A_h) and (B_h).  The
remaining uniform theorem is still the augmented Cartan/Hasse totalization
of the two-switch, one-endpoint, mixed, quadratic, and cubic product-rule
faces with word, fine/repeated grade, target, residue, physical (q),
anchor, (W), ridge, eta/sigma, and terminal data retained.
