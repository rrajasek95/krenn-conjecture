# Gate II has a relative three-cap totalization, not an absolute Tate filler

## Result

The formal source-labelled three-cap can be totalized without changing the
old occurrence algebra, but only after retaining two new carrier rows.  Put

\[
 A=Dq_{01},\qquad B=p_0s_1,\qquad C=p_1s_0,
 \qquad H=q_{23}q_{45}+q_{24}q_{35}+q_{25}q_{34},
\]

and

\[
 R_{01}=(A+B+C)H,\qquad L_{01}=(2A-B-C)H.
\]

The presentation-safe graph attachment is

\[
 d\Gamma_R=t_R-R_{01},\qquad d\Gamma_L=t_L-L_{01}.       \tag{1}
\]

Both equations are monic in a new carrier coordinate, so eliminating
`t_R,t_L` recovers the old response algebra.  In contrast, declaring
`dGamma_R=-R01` or `dGamma_L=-L01` quotients that algebra by a new equation.
Modulo the complete `105`-occurrence response row, `R01` and `L01` are two
independent classes: the conormal rank rises from three to four and then
five when `t_R=0` and `t_L=0` are imposed.  Thus the hoped-for absolute Tate
cell is not a resolution attachment.

Exact checker:
[`verify_h3_gate_ii_three_cap_relative_tate_carrier_obstruction.py`](../computations/verify_h3_gate_ii_three_cap_relative_tate_carrier_obstruction.py).

## The Gate-II dual does extend—onto the carrier

Use the corrected occurrence covector from `4aa11b9`, normalized by

\[
 \psi(L_{01})=1.
\]

It has

\[
 \psi(R)=\psi(AH)=0,\qquad \psi(R_{01})=-1.          \tag{2}
\]

An extension over both columns in (1) is therefore forced to have

\[
                  \widetilde\psi(t_R,t_L)=(-1,1).    \tag{3}
\]

Equation (3) is decisive.  The local dual is not killed by the relative
totalization, but neither does it become a terminal on the old physical
rows: it becomes a nonzero covector on the new carrier.  Zero extension is
impossible.

The known augmented cap--Cartan values remain exactly

```text
B       = ( 1, 1,-1,-1)
target  = (-1,-1, 1, 1)
W       = (-1,-1, 1, 1)
ores    = ( 1, 1,-1,-1)
q       = 0
ridge   = 0.
```

They annihilate the old `r0/T/rho/K` packet.  Values (3) are additional;
they are not hidden combinations of target, `W`, ordinary residue, `q`, or
ridge.

## First PP and the endpoint-even face

Differentiating (1) gives

\[
 d(t_R)-dR_{01},\qquad d(t_L)-dL_{01}.               \tag{4}
\]

The normalized covector again has values `(-1,1)` on the two differentiated
carriers.  Its values on the literal first-principal-parts packet are

```text
dR = 0,  d(AH) = 0,  dR01 = -1,  dL01 = 1.
```

The `36` terms of `dL01` split into `18` residual-tail terms and `18`
endpoint/direction terms.  The covector reads zero on the tail half and one
on the endpoint/direction half.  Consequently the latter is exactly the
first physical face of `d(t_L)`; it cannot be discarded as a boundary of an
absolute top cell.

## The downstream `0102` carrier

The finite labelled two-root square is already constructed in the relative
P2 graph.  With twelve occurrence coordinates, let

\[
                         C=12I-J,
\]

so its universal relative generators satisfy

\[
                    d\Gamma_i=t_i-(Cu)_i.             \tag{5}
\]

For the private word-`0102` detector

\[
                  d=e_0^*+e_3^*-e_1^*-e_6^*,
\]

annihilating every column in (5) forces the carrier covector

\[
                         d_t=Cd=12d.                  \tag{6}
\]

It is nonzero.  On the exact second `B-4` preimage,

\[
                         d(z_{\rm private})=35/72.    \tag{7}
\]

The `q23` product rule carries the same class into the independent `dq23`
block.  Even under the strongest formal occurrence-by-occurrence use of the
primitive `p` cap, its `Q` component cancels this `dq23` class only at the
cost of an occurrence-labelled ordinary-residue packet with detector

\[
                              -35/72.                 \tag{8}
\]

Its scalar ordinary residue is zero.  Hence the committed scalar `ores` row
cannot absorb (8) by itself; one needs an occurrence-labelled `Q/ores`
landing.

There is no additional residue generator after that landing.  The exact
two-cut calculation shows that a complete-response gauge moves every one of
the eight labelled residues onto the `d_even` line.  Conditional on the
physical occurrence-to-`Q/ores` map, mixed-target square, complete gauge,
pure `d_even` section, and aggregate scalar correction, all labelled
residues cancel.  Those hypotheses remain unconstructed here.

## Consequence

The exact ladder is now

```text
(t_R-R01, t_L-L01)
        -> d(t_L)-dL01
        -> 18 endpoint/direction terms
        -> relative P2 carrier t_zprivate
        -> dq23 / occurrence-labelled Q-ores.
```

This obstructs the literal absolute-Tate shortcut.  It also explains why
the existing `psi_delta` is not yet an accepted physical terminal: its
extension is forced to be nonzero on the relative carrier orbit.

The sharp remaining theorem is to land that orbit source-validly in the
same word/fine/repeated augmented complex, retaining mixed target, physical
`q/dq`, occurrence-labelled `Q/ores`, the `d_even` face, `W`, and ridge.
Alternatively one
must extend the forced carrier covector across exactly that exhaustive
landing.  There is no further unlabelled recursive Hasse problem.

## Scope and verification

The calculation is exact for the canonical `K8` occurrence and first-PP
modules and for the literal lower P2 graph/reinsertion packet.  The
response-row countermodel shows that `L01` is not a consequence of the
single complete response equation; it is not asserted to be a complete GHZ
source point.  No physical carrier landing or final terminal is claimed.

Run normally, optimized, and isolated/no-site.  Frozen ledger SHA-256:

```text
7350f787825d596465b98e018a883446f8557cf738a17d729d217c588ae06511
```
