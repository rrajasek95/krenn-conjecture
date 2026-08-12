# Coefficientwise flat C4 transport is vertex gauge

## Theorem

Let four nonzero edge tables satisfy, for every colour word
`(a,b,c,d)`,

\[
 X_{01}(a,b)X_{45}(c,d)
   =\lambda X_{05}(a,d)X_{14}(b,c),\qquad \lambda\ne0. \tag{1}
\]

Then there are nonzero one-site functions `u0,u1,u4,u5` (individual
coordinates may vanish) and edge scalars such that

\[
\begin{aligned}
X_{01}&=\alpha_{01}u_0\otimes u_1,&
X_{45}&=\alpha_{45}u_4\otimes u_5,\\
X_{05}&=\alpha_{05}u_0\otimes u_5,&
X_{14}&=\alpha_{14}u_1\otimes u_4,
\end{aligned}                                             \tag{2}
\]

with the scalar products related by (1). Thus the common matching tensor is

\[
             T=u_0\otimes u_1\otimes u_4\otimes u_5.     \tag{3}
\]

## Proof

Choose a word `(a0,b0,c0,d0)` where the common tensor is nonzero. All four
edge entries at that word are nonzero. Fixing `(c0,d0)` in (1) writes
`X01(a,b)` as a function of `a` times a function of `b`; hence `X01` has
rank one. Fixing `(a0,b0)`, `(b0,c0)`, and `(a0,d0)` gives rank one for the
other three tables. Comparing factors recovers the common vertex lines. In
tensor language, the left side is simple across `01|45`, the right side is
simple across `05|14`, and the intersection of these two Segre subspaces is
the fully decomposable four-site Segre variety.

No all-entry torus assumption is required. The checker includes a
coefficientwise equality whose vertex factors contain zeros.

When the vertex factors contain zeros, (2) is a geometric vertex
factorization, not an invertible gauge on the whole palette. An actual
invertible diagonal gauge exists on the entrywise-nonzero torus, or after
restricting to a nonzero rectangular support component.

Checker:
`computations/verify_c4_torus_flat_transport_vertex_gauge.py`.

## Relevance to the proof

This proves a stronger flat half of the proposed structure:

```text
complete coefficientwise flat C4 transport => vertex gauge.
```

On the special one-bad chart, such vertex gauge is exactly the form from
which a coherent finite matching switch should be built. It does not by
itself prove a complete response-column deletion: other matching bases in
the same endpoint column must also participate in the gauge. That is the
base-exhaustivity/source-saturation obligation.

## Why support-only equality is insufficient

Take all four edge tables to be the `3 x 3` identity matrix. The two matching
products are simultaneously nonzero on the three all-equal words and agree
there, but every edge table has rank three. They do **not** agree on every
coefficient. Thus equality merely on common nonzero support does not yield
vertex gauge.

The actual source difficulty is therefore not zeros by themselves. It is
the presence of additional matching-base terms, which can prevent the
source rows from giving the two-base coefficientwise equality (1). Their
support incidence must be handled by base-exchange/Hall routing or removed
by source saturation.

## Scope

This is an elementary tensor-intersection theorem, not the full
gauge-curvature-Hall theorem. The next steps are:

1. extend vertex gauge across the entire matching-base exchange graph;
2. classify separators created by additional matching terms as routed or
   Hall incidence; and
3. prove primitive source saturation so the gauge becomes a physical
   joint-kernel deletion.

Frozen ledger SHA-256:

```text
eb4ac8232e20c7de4fe991382f7be83f16b503fe212032941f1486753d33c12c
```
