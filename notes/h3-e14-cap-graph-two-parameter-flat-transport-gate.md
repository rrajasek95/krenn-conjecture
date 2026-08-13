# The cap graph is formally flat over occurrence centering and the D4 orbit

## Result

At normalized cap parameter `Y=1`, the old cap complex is

```text
dT=-w,     d(rho)=w,     Gcap=T+rho,     dGcap=0.
```

Tensor this complex with the ninety occurrence tags and the sixteen vertices
of the four-root moving-target cube.  Occurrence centering

\[
                         C=90I-J
\]

acts only on tags; the four site roots act only on colour labels; and the cap
differential acts only on the cap factor.  Consequently

\[
 [C,D_i]=0,
 \qquad [D_i,D_j]=0,
 \qquad [D_i,d_{cap}]=0.                              \tag{1}
\]

All 32 oriented Boolean edges and all 24 embedded squares have identity cap
transport.  Thus `Gcap` has a canonical flat extension over the *formal
tensor/enriched* two-parameter presentation, with zero curvature and trivial
holonomy.

Checker:
[`verify_h3_e14_cap_graph_two_parameter_flat_transport_gate.py`](../computations/verify_h3_e14_cap_graph_two_parameter_flat_transport_gate.py).

## This removes a separate formal cap-holonomy theorem

Given one pointed physical bottom occurrence/AugP2 section that already
carries the cap graph, the occurrence direction and all fourteen proper D4
faces transport it compatibly.  No new curvature correction is needed.  In
that enriched presentation the bottom centered face and the moving-target
four-root cone are one bicomplex rather than two unrelated comparisons.

The cap graph itself is terminal-dark.  Its boundary, `W`, `Eq`, lower,
anchor, eta, and sigma rows are zero.  It repairs the target/scalar-residue
normalization, while physical `q` is still governed only after a fully typed
comparison exists.

## Literal physical descent is not automatic

The formal extension is not yet a source-labelled E14 cell.  The old cap
generator has physical type

```text
word 01211222 / fine degree t*q_(v,N) / repeated grade P3+K2.
```

At the four D4 root sites `2,3,4,5`, its letters are

```text
2,1,1,2.
```

The E14 response cube starts at six-site word `110000`, whose four root-site
letters are `0,0,0,0`, and applies `0 -> 1` at each site to reach `111111`.
Therefore literal source-root covariance cannot transport the old cap word
along this cube: the required input colours are absent, and the cap object is
in a distinct eight-site word/fine grade.  Declaring a spectator cap copy at
every vertex constructs the enriched tensor model, not its comparison with
the physical correction complex.

The obstruction is consequently a degree-zero word/fine/repeated-grade
section, not a curvature or holonomy class.

## The central Eq incidence completes the coefficient-level square

Retain the two necessary quotient coordinates

```text
(private return R_E14, central source incidence E=(H0-u)e_Eq).
```

The moving-target D4 top and the clean Koszul `K_Eq` normal cell have
columns

```text
orbit D4 top     = (1,0),
clean K_Eq       = (0,1),
required Phi_orb = (1,1).
```

Therefore their sum is exactly the required coefficient-level comparison.
The cap graph is `(0,0)` in this quotient: it performs target/residue
normalization but does not supply the Eq incidence.

This also removes `T12` as an independent construction.  The complete old
unary row satisfies

\[
 T_{12}=v_{24}^{11}U_{000101}+R_{E14}.                \tag{2}
\]

Once `Phi_orb` places the source-labelled `R_E14`, the old `U` column
supplies all twelve tails.  The earlier `D1`--`D3` dual correctly detected
the absent `R` placement; it does not survive after this column is added.

The positive statement is conditional at the physical level.  The clean
cell is canonical in the unaugmented derived intersection:

\[
 dC_K=-(H_0-u)e_{\rm Eq}.
\]

Its nearest old physical lift has, however,

```text
Eq                  +E
lower/private       +E
word-labelled ores  -E
anchor incidence     0.
```

Thus adding `(1,0)+(0,1)` is a sound construction in the enriched
PP/Koszul totalization, but it is not yet the literal physical comparison.
One must cancel the private and labelled-residue faces in the same
`P_f`/D4 totalization.  The pointed conormal `P_f` and the higher `K_Eq`
normal cell are distinct homogeneous faces; their direct sum cannot be
replaced by the nonpointed raw substitution `H0-u -> 1-v04`.

## Shifted Kähler transport

For one ridge face write

\[
 a=q_{pq}^{22},\quad t=q_{pq}^{00},\quad
 b=q_{xv}^{0m_v},\quad u=q_{xv}^{00},\qquad
 \gamma_v=-d\Omega_v=-d((a-t)-(b-u)).                 \tag{3}
\]

Let `X_i` be the `0 -> 1` root at site `i`.  The only nonconstant case is
`i=v`:

\[
 X_vu=q_{xv}^{01}=:c_v,
 \qquad X_vb=0,
\qquad L_{X_v}\gamma_v=-dc_v.                       \tag{4}
\]

For `i != v`, the connection face is zero.  A second application kills
`c_v`, and roots at distinct sites commute, so the Kähler connection also has
zero mixed curvature and trivial Boolean holonomy.

The new one-face is terminal-dark in the fixed terminal frame.  The field
`eta_z` has weights `+1` on
`p:0` and `-1` on `z:0`; `c_v` has endpoints `x:0,v:1`.  The field `sigma`
has weights `+1` on `p:2` and `-1` on `x:2`.  Hence both kill `c_v`; the
connection one-face itself adds no eta/sigma coefficient.  In the
equivariantly transported terminal frame, contraction naturality gives

\[
 \iota_{g_*\eta_z}(g^*\gamma_v)
   =g^*(\iota_{\eta_z}\gamma_v),
\]                                                        

so the exact laws become

\[
 \iota_{\eta_z(s)}\gamma_v(s)=1+\delta_{vz}u_z(s)/t,
 \qquad
 \iota_\sigma\gamma_v=-q_{pq}^{22}.                  \tag{5}
\]

So there is no terminal curvature.  However, `gamma_v` is not
coefficientwise constant: a physical lift must place both its shifted
`pq/xv` halves and the connection face `-d(q_xv^01)` in the labelled
`P3+K2` source module.  That comparison remains open.

## Updated shortest frontier

The formal two-parameter construction reduces the physical work to:

1. construct one augmented pointed `P_f`/D4/clean-`K_Eq` comparison in the
   actual cap grade, cancelling the physical lower/private and labelled
   residue debts;
2. include its flat cap graph and shifted Kähler connection, with physical
   `q` handled by the existing transport/generator alternative.

There is no third independent `T12` theorem after the first item: equation
(2) closes it with the old unary row.

This is exact for canonical `h=3`, normalized `Y=1`, the ninety occurrence
tags, and the four E14 root sites.  It proves formal flatness and terminal
preservation, not physical word/grade descent.

Run normally, optimized, and isolated/no-site.  Frozen ledger SHA-256:

```text
3a3e59186dd613fbb7975ff626e0b52ca49a2bd154ab3778fdee84c3655e9762
```
