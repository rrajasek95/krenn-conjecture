# Fibre-preserving torus gauges cannot isolate the endpoint-even chart packet

## Exact answer

No diagonal physical source gauge, including an endpoint-site scaling with
arbitrary compensating `q` scalings, produces the chart-complete
endpoint-even Spencer family.

Let the complete response be the hafnian on an even complete graph and give
each edge an additive torus weight `w_ij`. Homogeneity of the response says
that every perfect matching has the same weight. Perfect-matching exchanges
on every four-set then force

\[
 w_{ij}+w_{k\ell}=w_{ik}+w_{j\ell}=w_{i\ell}+w_{jk}.
                                                               \tag{1}
\]

Equivalently, over characteristic zero,

\[
                         w_{ij}=a_i+a_j.                       \tag{2}
\]

The checker guards this proof by exact ranks for `K6,K8,K10`. For `K8`, the
`104` matching-difference equations have rank `20` in the `28` edge
characters. Their common-weight kernel has dimension `8`, exactly the rank
of the eight vertex gauges. If the response coefficient is normalized to
`1`, its common character must also vanish, leaving the seven-dimensional
product-one vertex torus. For a homogeneous zero response row the common
character need not vanish, but it still cannot split occurrences.

Checker:
[`verify_uniform_chart_complete_torus_reynolds_gate.py`](../computations/verify_uniform_chart_complete_torus_reynolds_gate.py).

## Endpoint and `q` compensation is already the vertex gauge

Use augmented vertices `P,S,0,...,5`, so

```text
D = PS,       p_i = Pi,       s_i = Si,       q_ij = ij.
```

Every fibre-preserving diagonal compensation has the form

\[
\begin{aligned}
 \operatorname{wt}(D)&=a_P+a_S,&
 \operatorname{wt}(p_i)&=a_P+a_i,\\
 \operatorname{wt}(s_i)&=a_S+a_i,&
 \operatorname{wt}(q_{ij})&=a_i+a_j.
\end{aligned}                                                   \tag{3}
\]

Therefore the three local direction pairings have identical character:

\[
\begin{aligned}
 \operatorname{wt}(Dq_{01})
 &=\operatorname{wt}(p_0s_1)
  =\operatorname{wt}(p_1s_0)\\
 &=a_P+a_S+a_0+a_1.                              \tag{4}
\end{aligned}

Compensating the residual `q` variables cannot change (4); the four-cycle
relations (1) are exactly the consistency equations for those
compensations.

Tensoring with a tail adds the common sum of the remaining vertex weights.
Passing to principal parts also does not help: `dx_ij` has the same
character as `x_ij`. Thus each of

```text
dD*q01, D*dq01, dp0*s1, p0*ds1, dp1*s0, p1*ds0
```

has the full perfect-matching character. The entire

\[
       (2,2,-1,-1,-1,-1)\otimes H_Y                         \tag{5}
\]

packet lies in one weight space.

## Reynolds projection cannot make `R01` or `L01`

For a homogeneous zero response equation, a character projector applied to
the complete response returns either the whole response character or zero.
For an affine normalized response equation, every occurrence is invariant,
so Reynolds averaging is the identity on all of them. In neither case is
the nine-occurrence block `R01` a weight subspace. Consequently no such
projector produces

\[
 L_{01}=(2Dq_{01}-p_0s_1-p_1s_0)H_{2345}                  \tag{6}
\]

or its first-PP packet (5) from the complete response row.

This is stronger than testing one proposed endpoint torus. Every diagonal
torus preserving the response presentation is already covered by (2). It
is also compatible with the older exact rank obstruction `3c60c7e`: the
larger span of all 28 coordinate Euler rows still misses `L01`, as detected
by its twelve-occurrence dual.

## The first failure is the known pointed chart face

To distinguish the `A=Dq01` cap from `B=p0s1` and `C=p1s0`, a proposed
weight must make one of

\[
 \operatorname{wt}(A)-\operatorname{wt}(B),\qquad
 \operatorname{wt}(A)-\operatorname{wt}(C)                 \tag{7}
\]

nonzero. These are precisely the two four-cycle homogeneity equations on
the selected `K4`. Endpoint/root symmetry identifies their even
combination, whose normal component is the pointed scalar `L01`.

Thus the torus route has a sharp dichotomy:

```text
four-cycle defect zero     -> action is scalar on A,B,C and cannot isolate;
four-cycle defect nonzero  -> action is not tangent to the response fibre
                              and leaves the pointed L01 chart face.
```

The second branch is not a new construction. The pointed chart theorem
`d1b8ec4` shows that the presentation-safe graph cone retains `L01`, and its
first principal-parts face is exactly the packet we are trying to fill.

## Remaining positive theorem

The diagonal gauge/Reynolds lane is exhausted before physical `q`, anchor,
`W`, ridge, or `eta/sigma` enter. The shortest remaining positive statement
is genuinely non-diagonal:

> Construct a source-labelled Spencer/cobar comparison whose first face is
> (5) and whose complete second face includes all cross-chart
> `C2+`, `C4`, and `P2` companions classified in `c82bc96`.

The exact conditional `C+` coefficient from `7b67277` remains the correct
local shadow, but a fibre-preserving weight projector cannot promote it to
the physical source cell.

The checker runs normally, optimized, and isolated/no-site. Its frozen
ledger digest is recorded in the checker.
