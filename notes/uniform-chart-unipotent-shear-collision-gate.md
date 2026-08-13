# Augmented-vertex unipotent shears leave a collision face before the chart packet

## Verdict

Elementary unipotent transformations mixing the augmented matching vertices
do not construct the endpoint-even Spencer family. Their first derivative
already leaves the complete hafnian response fibre, in a multigrading
disjoint from the desired squarefree packet.

Checker:
[`verify_uniform_chart_unipotent_shear_collision_gate.py`](../computations/verify_uniform_chart_unipotent_shear_collision_gate.py).

## Exact infinitesimal action

Regard the response variables as off-diagonal entries `x_ij` of a symmetric
matrix on the augmented vertices

```text
P, S, 0, 1, 2, 3, 4, 5.
```

An actual congruence shear does not preserve the zero-diagonal symmetric
matrix slice: it creates diagonal entries. Give the route its strongest
possible interpretation by projecting back to the off-diagonal physical
coordinates. This projected elementary shear `E_(a<-b)` acts by

\[
 X x_{aj}=x_{bj}\quad(j\ne a,b),\qquad X x_{ab}=0.       \tag{1}
\]

The last equality records that the physical matching source has no loop
`x_bb`. Applying (1) to the complete hafnian `R` gives

\[
                         X(R)=C_{a,b}.                  \tag{2}
\]

Every monomial in `C_(a,b)` has vertex degree

```text
degree(a)=0, degree(b)=2, every other degree=1.
```

It arises twice, according to which of the two edges incident to the doubled
vertex came from the original `a` edge. Therefore at order `n`

\[
 |\operatorname{supp} C_{a,b}|
   ={n-2\choose2}(n-5)!!,\qquad\text{every coefficient}=2.       \tag{3}
\]

For `n=8`, this is `45` monomials.

The ordered pair `(a,b)` is recovered from the vertex degree: it is the
missing and doubled vertex. Hence all `n(n-1)` off-diagonal shear faces lie
in disjoint multidegree sectors. It follows immediately that

\[
        \sum_{a\ne b}c_{ab}C_{a,b}=0
        \quad\Longrightarrow\quad c_{ab}=0\text{ for all }a,b.  \tag{4}
\]

Thus the off-diagonal tangent stabilizer of the complete response is zero.
The diagonal semistabilizer is exactly the vertex-gauge torus already
exhausted in `48515d5`; on the normalized affine fibre its trace must be
zero.

## The representative `P<-0` face

Under `P<-0`,

```text
D=PS   -> s0=0S,
p0=P0  -> loop 00, absent,
p1=P1  -> q01=01,
pj=Pj  -> q0j.
```

For the selected three pairings

\[
 A=Dq_{01},\qquad B=p_0s_1,\qquad C=p_1s_0,
\]

this gives

\[
 X(A)=s_0q_{01},\qquad X(B)=0,\qquad X(C)=s_0q_{01}.  \tag{5}
\]

Consequently

\[
 X(R)\supset2s_0q_{01}H_{2345},
 \qquad
 X(L_{01})=s_0q_{01}H_{2345}.                         \tag{6}

The first expression is the selected part of the 45-term collision packet.
The second is not the desired

\[
       (2,2,-1,-1,-1,-1)\otimes H_{2345}.             \tag{7}
\]

Packet (7) marks one edge differential but retains vertex degree one at all
eight augmented vertices. Packet (6) is missing `P` and doubled at `0`.
They are separated by the literal fine/multigrading, before any protected
readout is considered.

## Why the known chart graph does not absorb it

The pointed chart graph from `d1b8ec4` retains the squarefree scalar `L01`.
It does not contain a coordinate in the missing-`P`/doubled-`0` collision
sector. The primitive multigrading projection onto that sector detects
`C_(P,0)` and kills:

```text
the complete response R,
the squarefree L01 and Kahler dL01 packets,
every C_(a,b) with (a,b)!=(P,0).
```

One can formally adjoin a graph/Tate coordinate with boundary `C_(P,0)`.
But that is a new source-labelled collision generator. It is precisely the
first face a non-diagonal Spencer comparison must construct; it does not
come for free from the unipotent action.

Opposite shears do not evade this. A two-step commutator can return to a
squarefree diagonal action only through a two-cell whose first boundary
contains both disjoint collision sectors. Signs cannot cancel them at the
first stage.

## Source and target scope

This augmented-vertex `GL` must not be confused with the committed physical
Cartan action. Sitewise local-colour `GL3` acts by related vector fields on
the decorated source and output tensor. By contrast, `P` and `S` are
operation/direction roles, not physical GHZ tensor sites. Mixing `P` with
`0` changes `D/P/Q` operation types and has no induced GHZ target action.

Accordingly the construction fails already at the source response equation.
Physical target, `q`, anchor, `W`, ridge, and `eta/sigma` never become
well-defined pullbacks for this shear.

## Remaining positive theorem

The shortest surviving route is still a genuinely non-diagonal,
source-labelled Spencer/cobar totalization. It must include the collision
faces (2), complete their squarefree second faces by the `C2+`, `C4`, and
`P2` companions classified in `c82bc96`, and only then transport the
augmented readouts. An elementary unipotent action alone supplies none of
those collision fillers.

The checker runs normally, optimized, and isolated/no-site. Its frozen
ledger digest is recorded in the checker.
