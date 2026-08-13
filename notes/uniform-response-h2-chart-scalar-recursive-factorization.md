# The response-chart scalar is recursively a lower hafnian

## Uniform factorization

At response order `h`, use the complete hafnian on the `2h+2` sites

```text
0, 1, the other 2h-2 residual sites, P, S.
```

For the selected four-set `X={0,1,P,S}`, its three internal matchings are

\[
 A=01\,PS,\qquad B=0P\,1S,\qquad C=0S\,1P.
\]

Let `Y` be the complement and let `H_Y` be its hafnian.  Every response
matching with no edge across `X|Y` splits uniquely into one of `A,B,C` and
a perfect matching of `Y`.  Therefore its fixed-chart block is

\[
                   R_X=(A+B+C)H_Y.                   \tag{1}
\]

The endpoint-chart tag is `(2,-1,-1)`, so its pointed scalar proper face is

\[
 \boxed{L_h=(2A-B-C)H_Y=3AH_Y-R_X.}                  \tag{2}
\]

Here `H_Y` has response order `h-1`.  Thus the chart obstruction is
recursive: it is always one four-site direction factor multiplied by the
lower-order hafnian.  No new coefficient species appears with `h`.

Checker:
[`verify_uniform_response_h2_chart_scalar_recursive_factorization.py`](../computations/verify_uniform_response_h2_chart_scalar_recursive_factorization.py).

The checker exhausts the literal matching sectors through `h=6`.  If
`m=(2h-3)!!`, the scalar has `3m` occurrences, coefficient profile
`m x 2` and `2m x (-1)`, augmentation zero, and squared norm `6m`.
For `h=3`, the complete response splits by the number of `X|Y` crossings as

```text
0 crossings    9
2 crossings   72
4 crossings   24,
```

recovering exactly the nine-term `L01` and 96-term complement in
`abcce03`.

## The scalar is still a genuine proper face

For every `h`, retain one matching of `Y`, set `A=1`, `B=-1`, and set all
other displayed variables to zero.  Then the complete response value is
zero while `L_h=3`.  Hence neither the response row nor its homogeneity
kills (2).  The recursive factorization identifies the face; it does not
make it a fixed-source boundary.

## Physical implication and remaining theorem

The full-site coefficient theorem contracts every second-Hasse direction
tag, while the fixed-chart audit shows that its honest source realization
needs a pointed chart cylinder.  Formula (2) now identifies the uniform
shape of that cylinder.

A physical induction must be monoidal for disjoint-union hafnian
multiplication.  Capping a lower comparison by `A`, `B`, or `C` produces
Leibniz faces; folding the three caps into one fixed response chart produces
the selected-block face `R_X`.  Those faces carry word, fine, repeated,
anchor/`q`, `W`, and shifted-ridge data.  Bare spectator multiplication is
therefore insufficient, exactly as earlier product-rule guards showed.

The shortest positive theorem is:

> Construct the endpoint-chart PP cylinder compatibly with the product
> decomposition (1).  Use the order-`h-1` comparison on `H_Y`, and land all
> cap/product-rule faces in the already classified `C2+`, `C4`, and `P2`
> lower packets with the complete augmented readouts.

Once this is done, the full-site action removes every direction tag and the
existing filler-or-terminal theorem handles a failed physical filling.  The
present result proves the uniform recursive coefficient identity, not that
monoidal physical comparison.

The checker runs normally, optimized, and isolated/no-site.  Its frozen
ledger digest is
`6c3531c058c8c28e30f063d65905aa5b42c78212d18a89508cf50c5e2e066791`.
