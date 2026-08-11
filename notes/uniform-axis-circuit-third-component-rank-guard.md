# A third minimum axis component need not complete the active port ranks

## Result

The proposed rank implication is false at the stated structural level.
A nonzero determinant/cofactor product plus a third occupied component of a
minimum axis circuit does not force a distinct-head active
rank-`(3,3,3,3)` pair.  The port maps can remain exactly
rank-`(2,2,3,3)`.

The smallest counterguard is linear algebra at `k=3`.  It extends verbatim
to every `k>=3`; no physical support census is involved.

The exact checker is
`computations/verify_uniform_axis_circuit_third_component_rank_guard.py`.

## Independent response tails versus local port rank

Let `a` be one fixed nonzero local axis and let `w_0,w_1,w_2` be independent
cofactor-tail vectors.  Put

\[
                       C_i=a\otimes w_i,
 \qquad T=C_0+C_1+C_2.                                  \tag{1}
\]

The complete response columns `C_i` are independent, so `(1)` is a genuine
minimum-support axis circuit with unique full-support quotient relation.
Their independence lives entirely in the tails `w_i`; their local axis span
has dimension one.

This distinction is load-bearing.  Minimum support controls the complete
response tensors, not the rank of their local physical port factors.

## Exact active rank guard

Take two active rank-one arms with independent centre heads `h_0,h_1` and
one common outer head `ell_0`.  Give each a nonzero cofactor.  Then

\[
             \det(h_0,h_1)=1,
 \qquad      \det(\ell_0,\ell_0)=0.                    \tag{2}
\]

Let the third occupied axis component repeat the local arm
`h_1 tensor ell_0`, while its independent tail is `w_2`.  Thus it is a new
minimum response column but neither a new centre direction on the deficient
deletion nor a new outer-head direction.

One common star presentation makes the rank boundary literal.  At the
shared centre use columns

```text
arm u = h0,  arm v = h1,  third axis = h1,  background = h2.
```

Deleting `u` leaves `span(h1,h2)`, of rank two.  Deleting `v` leaves
`span(h0,h1,h2)`, of rank three.  Choose the corresponding outer deleted
stars with ranks two and three.  The four ranks are therefore

```text
(centre|u, u|centre, centre|v, v|centre) = (2,2,3,3).
```

All three active arms still have outer-head span one, so no pair has the
distinct heads required by the curved OO theorem.

Adding further independent tails `w_i` gives arbitrary `k>3` without
changing any local rank or head datum.  The checker audits this extension
through `k=10`; the displayed tensor-factor construction is uniform.

## Sharp missing input

The unary private-site identity supplies the nonzero active
`Delta*K` product.  The unique quotient circuit supplies independence of the
complete `C_i`.  Neither statement couples tail independence to local port
geometry.

A positive theorem therefore needs a genuinely new source-labelled
incidence statement:

> some occupied response tail must be carried by a local outer head
> transverse to the active common head, with nonzero cofactor and with the
> missing rank-three minors at both deficient deleted stars.

Without that incidence, the third column can remain tail-independent but
locally parallel exactly as above.  This guard is not a physical source and
does not refute an implication using additional full one-bad rows; it proves
that active-minor data plus minimum-circuit linear algebra alone are
insufficient.

## Verification

Run

```text
python3 computations/verify_uniform_axis_circuit_third_component_rank_guard.py
python3 -O computations/verify_uniform_axis_circuit_third_component_rank_guard.py
python3 -I -S computations/verify_uniform_axis_circuit_third_component_rank_guard.py
```

The frozen ledger digest is

```text
9e75521a53ad851d714d25b1dac54e32ba2129ec0a5288fa1a8c90922ef6a742
```
