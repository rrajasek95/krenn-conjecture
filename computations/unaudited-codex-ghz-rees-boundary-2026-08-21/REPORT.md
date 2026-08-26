# GHZ graph/Rees boundary at `N=8`

Status: **exact leading-arc audit**.  The whole exceptional fiber is not
classified.

Let `I=(F_w)` be the 6,561-coordinate quartic base ideal of the rational map
`P^251 --> P^6560`.  Its graph closure is `Proj Rees(I)` and its exceptional
divisor is `Proj gr_I`.  The first expansion of the known Laurent prism
family has twelve finite source coordinates with raw valuations
`(-1,0^10,1)`.  Multiplying the source by `t` gives a projective arc

```text
B(t)=B0+t B1+t^2 B2,
B0 support = A_01[00],  |B1 support|=10,  B2 support=A_25[00].
```

The one-cell point `[B0]` lies in the base locus.  Direct matching
enumeration gives

```text
F(B(t)) = t^4 Delta_8,3
        + t^5 (e_12012000 + e_21000012).
```

Thus the pulled-back base ideal is `(t^4)`.  The unique lift of this DVR arc
to the blow-up has reduced special fiber `P^0` and exceptional point
`([A_01[00]],[Delta_8,3])`.

Literal GHZ-reaching valuations do not form finitely many `B4 x S3` orbits.
For every `N>=2`, add `+N` to `nu(A_24[11])` and `-N` to
`nu(A_57[11])`.  The two cells occur together only in the pure colour-one
matching and in neither mixed matching, so the output remains exactly the
same.  After projective normalization the vector is primitive and its finite
valuation range is `2N`, an invariant under coordinate permutations.  Hence
these are infinitely many distinct orbits.

This rules out a finite literal valuation census.  A finite replacement
would have to quotient the output-invisible valuation torus and classify
Gröbner cones.  The next local computation is the Rees initial ideal/normal
cone at the one-cell base orbit, to determine the entire exceptional-fiber
intersection over GHZ rather than the single point selected here.

Standard, optimized, and isolated/no-site modes agree at logical SHA
`14c9e1df0cab33d75041d5d13ff4acc3544ab873b52c898164f22928aa2e936e`.
