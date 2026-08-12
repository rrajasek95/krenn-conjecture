# Flat transport on every alternating even cycle is vertex gauge

## Theorem

Let an alternating cycle `C_(2r)` have its two perfect matchings `M` and
`N`.  Put an endpoint-ordered edge table `X_e` on every cycle edge.  If

\[
 \prod_{e\in M}X_e(x_e)
   =\lambda\prod_{e\in N}X_e(x_e)\ne0                 \tag{1}
\]

coefficientwise for every colour word, then there are nonzero one-site
functions `u_v` and edge scalars `alpha_e` such that

\[
                  X_{uv}(a,b)=\alpha_{uv}u_u(a)u_v(b), \tag{2}
\]

with

\[
             \prod_{e\in M}\alpha_e
                =\lambda\prod_{e\in N}\alpha_e.      \tag{3}
\]

Coordinates of the `u_v` may vanish.  Thus a chordless `C6` or `C8` has no
flat coefficient geometry beyond the same vertex gauge already found on
`C4`.

There is an analogous support theorem.  If the two nonempty
matching-product supports agree, then for nonempty colour subsets `S_v`,

\[
                    \operatorname{supp}X_{uv}=S_u\times S_v              \tag{4}
\]

on every cycle edge.  The common word support is the single Cartesian
product `prod_v S_v`, hence is Hamming-connected.

Checker:
`computations/verify_even_cycle_flat_transport_vertex_gauge.py`.

## Proof

Choose a word `p` where the common tensor in (1) is nonzero.  Every edge
entry used at `p` is nonzero.  Fix an edge `uv` of `M` and freeze all other
coordinates at `p`.  On the `N` side, the variable at `u` appears only in
the `N` edge preceding `u`, while the variable at `v` appears only in the
`N` edge following `v`.  All other factors are constants.  Therefore

\[
              X_{uv}(a,b)=c\,f_u(a)f_v(b),
\]

so `X_uv` has rank one.  The same argument applies to every edge of `M` and
`N`.  Comparing the two pure-tensor decompositions, or normalizing each
one-site factor by the pivot word, identifies a common line `u_v` at every
vertex and gives (2)--(3).

For supports, use the same pivot slice.  Membership of `(a,b)` in the
support of `X_uv` is equivalent to membership of the word obtained from
`p` by changing only `u,v` in the common matching-product support.  On the
opposite matching this condition separates into one condition on `a` and
one on `b`.  Hence the edge support is a rectangle.  Adjacent pivot slices
identify the same vertex subset at their common endpoint, proving (4).

The proof works for every finite palette and does not use a coefficient
torus.  An invertible vertex gauge on the entire palette still requires the
entrywise-nonzero torus; with zeros, (2) is geometric factorization on the
vertex supports.

## Shift in the proof frontier

This removes a misleading distinction in Theorem A.  Once a genuine
two-base coefficientwise equality has been isolated, `C4`, chordless `C6`,
and chordless `C8` all have the same flat conclusion: vertex gauge.  A
distance-three chord is needed only on the nonflat/extra-term side to
shorten a cycle and expose a literal carrier.

The remaining hard step is consequently **source isolation**, not cycle
geometry.  The complete unary and response rows contain additional
matching bases.  They must prove one of:

1. an additional term gives the first support mismatch or curvature and
   routes to an active carrier;
2. the selected two-base equality propagates through the connected
   matching-base graph; or
3. the residual incidence becomes a source-labelled Hall/lock family.

Only after that propagation may the vertex gauge be promoted to a complete
one-star response-column dependence and the proved finite `nu`-safe
deletion.  The theorem does not perform that source-saturation step.

## Verification

Run

```text
python3 computations/verify_even_cycle_flat_transport_vertex_gauge.py
python3 -O computations/verify_even_cycle_flat_transport_vertex_gauge.py
python3 -I -S computations/verify_even_cycle_flat_transport_vertex_gauge.py
```

The checker audits `C4`, `C6`, and `C8` over three colours, including zero
vertex coordinates, exact pivot reconstruction, edge rank-one minors, and
the rectangular-support pivot slices.

Frozen ledger SHA-256:

```text
9bee2de423db959391b81eb2e7adaf1ee9ca7a7e3107828ab1fd6c3d2bbc859f
```
