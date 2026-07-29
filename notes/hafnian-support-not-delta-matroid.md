# Nonzero principal hafnians do not form a delta-matroid

A tempting uniform interpretation of the Boolean recurrence shadow is as
an even delta-matroid.  Complex cancellation makes this false, already on
six vertices.

Split

\[
                   V=\{0,1,2\}\mathbin\dot\cup\{3,4,5\}.
\]

Give every edge within a shore weight `1` and every cross edge the same
weight `z`, where

\[
                              z^2=-\frac12.                 \tag{1}
\]

For an even set `S`, let `h(S)` be its principal hafnian and put
`F={S:h(S)!=0}`.  The full hafnian is `6z`, so it is nonzero.  Now take

\[
                    X=\{0,1,2,3\},\qquad Y=\{3,4\}.         \tag{2}
\]

One has `h(X)=3z` and `h(Y)=1`, so `X,Y in F`.  Their symmetric difference
is `{0,1,2,4}`.  Choose `u=4`.  For each
`v in {0,1,2}`, the set `X triangle {u,v}` has two vertices on each shore,
and hence

\[
             h(X\mathbin\triangle\{u,v\})=1+2z^2=0.        \tag{3}
\]

The symmetric-exchange axiom for an even delta-matroid would require some
such `v` to make the toggled set feasible.  Equation (3) excludes every
choice.  Thus `F` is not an even delta-matroid.

This example still satisfies the exact per-pivot hafnian recurrence used in
`proofs/diagonal-hafnian-recurrence-obstruction.md`.  Consequently a
uniform proof has to use that weaker recurrence structure directly; it
cannot import delta-matroid exchange or a representable-Pfaffian partition
theorem.

The exact quadratic-field audit is
[`computations/verify_hafnian_support_not_delta_matroid.py`](../computations/verify_hafnian_support_not_delta_matroid.py).
