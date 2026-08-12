# The standard residual-q transport is graph-locked

## Exact correction problem

The mixed-curvature/rootless-bar near-hit has reduced the shared attachment
to the common seven-site word

```text
1211222
```

and the first common labelled repeated `P3+K2` grade.  In the ordered
ordinary-residue basis

\[
 (P_+q_{00},P_-q_{00},P_+q_{11},P_-q_{11}),
\]

where

\[
 q_{00}=a_{24}^{11}a_{35}^{11},\qquad
 q_{11}=a_{24}^{21}a_{35}^{12},
\]

the existing near-hit leaves

\[
 \delta=(1,-1,-1,1)=(P_+-P_-)(q_{00}-q_{11}).       \tag{1}
\]

Thus a Kodaira--Spencer correction must have residue

\[
 -\delta=(-1,1,1,-1),                               \tag{2}
\]

zero main endpoint boundary, and `W=target=ainc=0`.  The sign in (2) is
forced: it is the negative of the pinned curvature-minus-bar residue.

## The complete standard two-site square

Project to the endpoint-odd line `P+ - P-`.  The two residual colour changes
have exactly four corners:

\[
\begin{array}{c|c}
q_{00}&a_{24}^{11}a_{35}^{11}\\
q_{10}&a_{24}^{21}a_{35}^{11}\\
q_{01}&a_{24}^{11}a_{35}^{12}\\
q_{11}&a_{24}^{21}a_{35}^{12}.
\end{array}
\]

Let `D_w` denote the endpoint-odd main-boundary coefficient at a corner and
`R_w` its resolved ordinary-residue coefficient.  The pinned mixed
bar-curvature identity has equal normalized `q` augmentation and ordinary
residue at every endpoint.  Therefore each corner column has the form

\[
                         g_w=(D_w,R_w)=(e_w,e_w).     \tag{3}
\]

The standard normalized local bar has `dE=L-D`.  Hence every one-site
transport edge is

\[
                         g_v-g_w.                    \tag{4}
\]

The four edges have rank three.  Their sole square relation is

\[
 (q_{00}\to q_{10})+(q_{10}\to q_{11})
 =
 (q_{00}\to q_{01})+(q_{01}\to q_{11}),             \tag{5}
\]

which is exactly the first Hasse/Bianchi compatibility.  It adds no new
column.  Even after adjoining all four corner columns, the span has rank
four in the eight rows `(D_q00,...,D_q11,R_q00,...,R_q11)` and obeys the
coefficientwise graph law

\[
                              R_w=D_w.                \tag{6}
\]

This calculation deliberately enlarges the literal source image by allowing
every graph corner.  A failure in this enlarged span is therefore also a
failure for the actual standard source submodule.

## Primitive obstruction

After endpoint-odd projection the required correction (2) is

\[
 z=(D=0,\ R=-e_{00}+e_{11}).                         \tag{7}
\]

The primitive coefficient covectors

\[
 \Phi_{11}=R_{11}-D_{11},\qquad
 \Phi_{00}=R_{00}-D_{00}                             \tag{8}
\]

kill every corner (3), every edge (4), and the square relation (5), while

\[
                    \Phi_{11}(z)=1,\qquad
                    \Phi_{00}(z)=-1.                 \tag{9}
\]

So the desired residue-only correction is not in the standard transport
span.  Equivalently, any combination of standard columns with zero main
boundary automatically has zero resolved residue.  This is the first
primitive readout; no larger rank calculation is needed.

## Why the other pinned rows do not change the result

The checker replays the complete bounded inventories used by the shared
four-term audit.

* All `3^6=729` response words have only the signless endpoint pair `(1,1)`
  at the correct tail.  They vanish in the endpoint-odd projection.
* The reciprocal quadratic `K` channel is symmetric, so its proposed
  antisymmetrization is literally zero.
* First PP comparison cells project to the adjacent differences (4); the
  formal single-vertex difference is not a source-valid column.
* The fourth-Hasse candidate is formal rather than source-valid, while its
  literal square is already (5).
* Matching switches either change the selected-matching fine grade or,
  after alignment back to the selected tail, contribute the same incidence
  projection.  The committed matching/Tate audit contains no ordinary cell
  supplying (7).

Thus no source-valid cell in the **pinned standard response/bar/first-PP/
Hasse/matching inventory** breaks (6).

## Exact frontier shift

The fastest standard construction is eliminated.  The first possible new
object is a genuinely relative/Spencer residual-q comparison generator with

```text
endpoint-odd main boundary:  0
ordinary residue:             -q00 + q11
W, target, ainc:               0, 0, 0
```

It must break the graph law `R=D`; renaming a bar, Hasse, or matching edge
cannot do that.  Physical promotion imposes one further independent law
already isolated by the rootless duality audit:

\[
 d r_v(\eta_z)=-d\Omega_v(\eta_z)
 =1+\delta_{vz}u_z/t,                                \tag{10}
\]

with aggregate compensating readout `5+u_z/t`.

The graph obstruction and the eta law are two independent **conditions on
one possible cell**, not evidence for two missing generators.  A single
relative/Spencer comparison can in principle carry both the residue-only
boundary (7) and the physical eta response (10).  The present ranks force at
least one graph-breaking generator but do not force a second one.

This is a complete no-go only for the pinned standard first repeated
inventory.  It is not yet an exhaustive physical source-resolution no-go:
a new relative collision/mapping-cone/Spencer cell could have (7) and (10).
The proof frontier is therefore one graph-breaking physical comparison
cell, or an exhaustive census proving that no such cell exists.

Verification:

```text
python3 computations/verify_h3_residual_q_ks_standard_transport_graph_lock.py
python3 -O computations/verify_h3_residual_q_ks_standard_transport_graph_lock.py
python3 -I -S computations/verify_h3_residual_q_ks_standard_transport_graph_lock.py
```

Frozen ledger SHA-256:

```text
1ca1b295c8a9f8ce59696a37dea124a71cea06c084d827ddb92bf2f6e53c989a
```
