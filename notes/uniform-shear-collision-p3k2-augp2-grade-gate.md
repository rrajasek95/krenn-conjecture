# The shear collision meets `P3+K2` only on a first cofactor face

## Exact classification

The augmented-vertex shear collision is not already the repeated-site
`P3+K2` cell.  At `h=3`, every monomial of `C_(a,b)` has four edges and
graph type

```text
P3 + 2 K2
```

with `a` missing, `b` doubled, and every other augmented vertex used once.
For one ordered shear there are 45 such monomials, all with coefficient
two.

Its labelled first principal-parts boundary has 180 edge-removal flags and
splits exactly as

```text
remove an edge through doubled b:   90 faces of type 3 K2,
remove a disjoint tail edge:        90 faces of type P3 + K2.
```

Thus there is a real associated-graded connection to the existing
repeated-site packet, but it occurs one PP level below `C_(a,b)`.

Checker:
[`verify_uniform_shear_collision_p3k2_augp2_grade_gate.py`](../computations/verify_uniform_shear_collision_p3k2_augp2_grade_gate.py).

## The selected `P<-0` block

The selected collision block is

\[
                   2s_0q_{01}H_{2345}.
\]

Deleting one of the two tail edges gives the six literal `P3+K2` cubics

\[
\begin{gathered}
s_0q_{01}q_{45},\quad s_0q_{01}q_{23},\\
s_0q_{01}q_{35},\quad s_0q_{01}q_{24},\\
s_0q_{01}q_{34},\quad s_0q_{01}q_{25}.
\end{gathered}
\]

These are `SQQ` terms with the physical site `0` repeated.  They are
therefore exactly the combinatorial `P2` species expected after residual
reinsertion.  Deleting `s0` or `q01` instead gives six `3K2` proper faces.
The collision top must carry both sets; keeping only the six attractive
`P3+K2` cofactors would violate its full Hasse boundary.

Globally the 90 `P3+K2` cofactors and 90 `3K2` cofactors are all distinct as
labelled cubics.  This is not a multiplicity or cancellation artifact.

## Why this is not yet `AugP2`

The exact homogeneous grades are:

| object | source block / word | operation and repeated type | level |
|---|---|---|---|
| shear collision top | selected response chart, `11:110000` | `SQQQ`, `P3+2K2` | response collision top |
| tail cofactor | same response word | `SQQ` with a labelled removed-tail differential, `P3+K2` | first PP face |
| canonical cap | `01211222` | `t*q_(v,N)`, `P3+K2` | primitive `p=(-Q,-ores)` face |
| shifted ridge | `01211222` | `gamma_v=-dOmega_v`, shifted `P3+K2` | relative Kähler face |

The tail cofactor and canonical cap agree only after forgetting the response
word, fine operation label, and homological face.  Those are genuine direct
sum gradings in the pinned physical interfaces.  The primitive response,
cap-word, and shifted-Kähler projections have rank three, so a common site
degree cannot identify them.

This also explains why the shifted ridge is not hidden in the shear.  The
augmented-vertex operation-role shear already fails to preserve the
response equation.  It therefore has no defined pullback on `Omega`,
physical `q`, anchor, ridge, or eta/sigma.  The ridge remains the independent
face `-dOmega_v` of an enriched relative principal-parts/Kähler comparison.

## Even the physical repeated-site edge is conditional

Suppose a source-labelled map did transport the six tail cofactors to the
canonical repeated grade.  The pinned literal `P3+K2` edge still has the
reduced-Eq defect

\[
             \delta_v(H_0-u)e_{\rm Eq}.
\]

In rows `(pure Eq, ainc, W, target, ores)`, the covector

\[
                    \text{pure Eq}+\operatorname{ainc}
\]

kills the admitted `r0,T,rho` corrections and reads nonzero on the desired
reduced face.  Exact rank rises from three to four.  Therefore “same
`P3+K2` graph” does not mean “existing physical filler”: the source map must
also carry the committed reduced pure-Eq descent correction.

## Shortest positive theorem

The collision calculation does sharpen the construction target.  It is
enough to construct one source-labelled Hasse/Spencer collision top whose
full boundary contains:

1. the six selected `SQQ/P3+K2` tail cofactors;
2. the six `3K2` path cofactors; and
3. their complete labelled analogues over all 45 collision monomials.

Then an augmented cross-word `P2` comparison must send the first family to
the canonical `01211222 / t*q_(v,N)` packet, carry the reduced-Eq correction,
and include the independent shifted ridge.  This is a concrete bridge to
`AugP2`; it is not supplied by the shear or by topology alone.

The checker is exact for the complete canonical `h=3` collision packet and
its first labelled PP boundary.  It does not construct the cross-word map
or prove an all-resolution no-go.

Run normally, optimized, and isolated/no-site.  Frozen ledger SHA-256:

```text
d09ff0f804f569295e4f70d2f1000a4ea8ea9e681ae4e4bff143a0f272df2315
```
