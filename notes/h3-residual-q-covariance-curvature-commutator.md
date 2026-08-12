# The residual-(q) cell is one covariance--curvature commutator

The missing mapping-cone direction is not an arbitrary four-corner class.
Its principal symbol is the commutator of two mechanisms already visible in
the source:

1. the endpoint-odd curvature (E_- - E_+), and
2. the two-site colour covariance changing the pure tail
   (T_0=24{:}11mid35{:}11) to the mixed tail
   (T_1=24{:}21mid35{:}12).

This gives a considerably narrower construction problem, but it does not
yet construct the physical relative cell.

## Literal source transport

Use endpoint orientations

\[
 E_+=P0{:}11\mid S1{:}11,
 \qquad
 E_-=P1{:}11\mid S0{:}11.
\]

The two relevant complete source words are

```text
pure:   11111111,
mixed:  11211211.
```

Applying the sitewise covariance derivations

\[
 \delta_2(1\to2)\,\delta_5(1\to2)
\]

to the complete direct-free pure row gives the complete mixed row term by
term.  Both rows have 90 terms.  The derivation also preserves separately
the (E_+) and (E_-) endpoint-hole sectors, each of which has three
residual matchings.  Thus the tail transport is genuinely source-labelled;
it is not a decorated-edge relabelling.

## The signed fourth symbol

Order the four decorated matching corners as

```text
E+T0, E-T0, E+T1, E-T1
```

and put

\[
                  \alpha=(-1,1,1,-1).                 \tag{1}
\]

The fourth derivative of a complete matching row by one corner is one
exactly when that decorated perfect matching occurs in the row.  Across all
(3^8) source words, only the two displayed words are active:

\[
 (1,1,0,0)\quad\hbox{and}\quad(0,0,1,1).
\]

Their pairings with (1) vanish separately.  Hence the signed fourth symbol
has no unit obstruction on any complete source row.

More is true.  Its codimension-one Hasse shadow also cancels literally.  The
first surviving shadow occurs in codimension two and factors as

\[
 \boxed{
   -E_+T_0+E_-T_0+E_+T_1-E_-T_1
   =(E_--E_+)(T_0-T_1).}                              \tag{2}
\]

There are sixteen decorated endpoint--tail products in (2), all with
coefficient (pm1).  In the established corner order its coarse
coefficient vector is precisely

\[
                         -\delta=(-1,1,1,-1).          \tag{3}
\]

Thus the residual isolated by the mixed-curvature/rootless-bar audit is the
first curvature face of one signed covariance square.  The fourth-Hasse
unit and its first face are not the obstruction.

## What remains

Covariance supplies horizontal equality, not a nullhomotopy.  Replaying the
complete standard bar/first-PP/Hasse/matching transport gives the exact law

\[
                              R=D.
\]

The desired face (3) has (D=0) and (R\ne0), and remains outside that
span.  Therefore (2) does not by itself give the literal cell (M_v) from
the private-boundary audit.

The positive theorem needed next can now be stated more economically:

> Construct one relative Spencer homotopy for the endpoint-curvature / tail-
> covariance commutator (2), in the labelled repeated
> (P_3\sqcup K_2) grade.  Its full image must be the pinned
> (sum_j\alpha_jB_j) plus Eq-corner packet, and the same cell must carry
> the eta and sigma terminal values.

If this homotopy exists, `2593831` consumes the unequal-tail five-lock and
E14 endpoint holonomy.  If it does not, nonmembership becomes a useful dual
only after the complete physical relative source map is known.  The present
calculation constructs the principal source symbol, not that exhaustive map
or the physical filler.

Verification:

```text
python3 computations/verify_h3_residual_q_covariance_curvature_commutator.py
python3 -O computations/verify_h3_residual_q_covariance_curvature_commutator.py
python3 -I -S computations/verify_h3_residual_q_covariance_curvature_commutator.py
```

Frozen ledger SHA-256:

```text
2ff6aa922fd927096e33cef78bdfb684f26d6372a511eee5d7e1b20c04b14c1e
```
