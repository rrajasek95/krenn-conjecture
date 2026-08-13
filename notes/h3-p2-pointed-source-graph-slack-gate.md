# The pointed graph exists relatively; its absolute face is a new basepoint

## Verdict

The marked occurrence admits an explicit presentation-safe graph/Koszul
resolution, but the graph and full response alone do **not** construct the
absolute pointed conormal

\[
                         P_f=d(u_f-u).
\]

The graph transfers `P_f` to one private slack coordinate:

\[
                    [d(u_f-u)]=-[dz_f]=-[dG],          \tag{1}
\]

where `G` is the other-occurrence aggregate in the complete response.
An old-source construction exists exactly if `dG` belongs to the conormal
span of the remaining complete physical source equations.  No such
membership is supplied by the graph/full-response calculation.  If one
instead kills the slack directly, the required new basepoint relation is
`z_f=0`, equivalently `G=0` or `f=u`; it changes the classical physical
fibre.  The exact first nonfill detector lives on the private graph
coordinate and is not yet a physical terminal.

Checker:
[`verify_h3_p2_pointed_source_graph_slack_gate.py`](../computations/verify_h3_p2_pointed_source_graph_slack_gate.py).

## 1. Presentation-safe relative construction

Write the target-normalized complete response equation as

\[
                         R=f+G-u.                     \tag{2}
\]

Equivalently, this is the pair `H0=f+G`, `H0=u` used in the existing
occurrence-to-target gate.  The convention `R=f+G=0` used in the mixed-row
chart absorbs the target term `-u` into its symbol `G`; here `G` denotes
only the other-occurrence polynomial, so the target is displayed.

Adjoin degree-zero variables `u_f,z_f` and degree-one Koszul generators
`theta,pi` with

\[
 d\theta=u_f-f,
 \qquad
 d\pi=z_f-G.                                          \tag{3}
\]

The Jacobian of (3) with respect to `(u_f,z_f)` is

\[
\begin{pmatrix}1&0\\0&1\end{pmatrix},
 \qquad \det=1.                                       \tag{4}
\]

Thus (3) is a triangular monic graph extension: eliminating the new
variables gives back the original source algebra, with

\[
                  u_f=f,
 \qquad           z_f=G=u-f.                         \tag{5}
\]

It is therefore a genuine relative cotangent/Koszul construction inside a
resolution of the original source.  It is not an imposed diagonal.

## 2. What the graph does to the pointed class

Adding the three conormal relations gives

\[
             dR+d\theta+d\pi=d(u_f-u)+dz_f.
\]

Hence (1) holds in the conormal quotient.  Incorporating (2) gives the
stronger literal identification

\[
                      [d(u_f-u)]=-[dG].               \tag{6}
\]

So the full response equation does help: it identifies the exact first
obstruction as the mate aggregate.  It does not make that aggregate zero.
The relative graph is best viewed as a transfer of the pointed class from
the marked/global diagonal to `z_f`.

In cotangent coordinates

```text
(f,G,u,u_f,z_f)
```

the tangent

\[
                         \xi=(1,1,2,1,1)               \tag{7}
\]

kills `dR,dF0,dtheta,dpi`, while

\[
 d(u_f-u)(\xi)=-1,
 \qquad dz_f(\xi)=1,
 \qquad dG(\xi)=1.                                   \tag{8}
\]

This proves that neither `P_f` nor the slack is a boundary in the
presentation-safe response graph.  With every other physical source row
restored, the exact criterion is

\[
 [P_f]=0
 \quad\Longleftrightarrow\quad
 [dG]=0
 \quad\Longleftrightarrow\quad
 dG\in dI_{\rm remaining}.                            \tag{9}
\]

Thus another already-physical equation could close face 1 only by proving
this one membership; the graph construction itself does not.

## 3. The smallest absolute attachment changes the fibre

Adding one more Koszul generator

\[
                          d\kappa=z_f                 \tag{10}
\]

does kill (1).  But its classical truncation is

\[
                A/(z_f)=A/(G)=A/(f-u).               \tag{11}
\]

For example,

```text
(f,G,u,u_f,z_f)=(1,1,2,1,1)
```

satisfies every equation in (2)--(3) and is deleted by (9).  Thus (9) is a
new marked basepoint condition, not a contractible presentation pair.

This sharply distinguishes the two constructions:

```text
K(u_f-f, z_f-G)         presentation-safe; P_f becomes -dz_f;
add K(z_f)               fills P_f; changes the source to G=0.
```

## 4. Nonfill versus a physical terminal

The tangent (7) is an exact nonfill certificate.  It is not yet an accepted
conjecture-level terminal: `z_f` and `G` select private occurrences inside a
complete source polynomial and carry no canonical physical `q`, anchor,
word/fine/repeated, ridge, eta/sigma, or `W` readout.

There are therefore two honest positive routes.

1. Land `z_f` in the complete augmented `P2` comparison.  Then the existing
   kernel-versus-Fredholm alternative either kills the slack or promotes its
   detector to a physical terminal.
2. Use the weaker all-occurrence centered law.  Its formal identity gives
   `90[du_f]=[du]`, which is sufficient for anchor visibility in
   characteristic zero.  Its centered occurrence class still requires the
   same physical landing/terminal typing.

The exact unscaled `P_f` cannot be declared constructed in the original
source without proving the membership (9).  If that membership fails, the
smallest literal boundary-arm extension is one marked basepoint cell (10);
the shortest fibre-preserving strategy is the relative slack construction
plus augmented physical landing.

## Scope

This result uses the literal complete response decomposition (2), constructs
the monic graph resolution, proves the cotangent identities (1) and (6), and
exhibits both a tangent nonfill certificate and a deleted classical point.
It does not land the private slack in the physical augmented complex or
promote its detector to a terminal.

Run:

```text
python3 computations/verify_h3_p2_pointed_source_graph_slack_gate.py
python3 -O computations/verify_h3_p2_pointed_source_graph_slack_gate.py
python3 -I -S computations/verify_h3_p2_pointed_source_graph_slack_gate.py
```

Frozen ledger SHA-256:

```text
244a2305e08462e3a6e15888a6c539fcc57fc6073a045718d39110e6f0716f8f
```
