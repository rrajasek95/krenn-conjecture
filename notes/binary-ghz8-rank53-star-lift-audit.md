# Independent rank-53 audit and the star-lift branch

This note independently audits the exact rational binary GHZ8 source from
`binary-ghz8-exact-rank53-source.md` and explains why its collapsed mixed
endpoint packet does not permit rank above 53.  The result below is a branch
theorem, not a universal resolution of the binary GHZ8 problem.

## Independent exact audit

The checker
[`audit_binary_ghz8_rank53_star_lift.py`](../computations/audit_binary_ghz8_rank53_star_lift.py)
imports no project module.  It reconstructs the 45 source cells from the 26
displayed rational parameters and the 19 triangular formulas.  A separately
implemented sparse Laurent ring and a separately enumerated perfect-matching
sum verify all 256 eight-site identities identically in the parameters.  At
the default rational specialization it independently rebuilds the
deletion-`(3,4)` differential and obtains

\[
 \operatorname{rank}D=53,
 \qquad
 \operatorname{rank}D^{\rm mixed}=51
\]

by exact Gaussian elimination over \(\mathbb Q\).

## The collapsed packet and its replacement

Let \(R=(0,1,2,5,6,7)\), and write \(U^a_r\) and \(V^b_r\) for the two
endpoint-vector families at deleted vertices 3 and 4.  The edge between the
deleted vertices is zero, so the adjusted mixed packets are simply

\[
 P=N_{01},\qquad Q=N_{10}.
\]

At this exact source, \(U^0\) is supported only at \(z=7\), with
\(U^0_7=(7/5)e_0\).  The supports of \(U^1\) and \(V^0\) meet only at the
same residual vertex 0, which cannot form a residual edge.  Therefore

\[
 P=\frac75 S(e_0),\qquad Q=0,
 \qquad S(\ell)_{r7}=V^1_r\ell^{\mathsf T}.
\]

Thus the two named packets are not independent modulo gauge.  Exact
calculation instead gives

\[
 D S(e_0)=D S(e_1)=0.
\]

The five standard gauges have rank 5, and successively adjoining
\(S(e_0)\) and \(S(e_1)\) raises the rank to 6 and 7.  Since \(D\) has
nullity 7,

\[
 \ker D=\mathcal G\oplus
 \operatorname{span}\{S(e_0),S(e_1)\}.
\]

So the transverse star column is exactly the missing quotient-kernel class.

## General star-lift lemma

Let \(M\) be any six-site binary residual source and \(D=d\Psi_M\).  Fix a
centre \(z\).  Suppose a tangent is supported on the \(z\)-star and factors
as

\[
 K_{rz}=h_r u^{\mathsf T}\qquad(r\ne z),
\]

with \(u\ne0\).  For a residual word \(x\), let \(C_{rz}(x)\) be the
four-site matching cofactor obtained after removing \(r,z\).  Directly from
the differential,

\[
 D(K)(x)
 =u[x_z]F_h(x_{R\setminus\{z\}}),
 \qquad
 F_h=\sum_{r\ne z}h_r[x_r]C_{rz}(x).
\]

The factor \(F_h\) does not depend on \(x_z\).  Choose a colour \(c\) with
\(u[c]\ne0\).  If \(D(K)=0\), evaluating at \(x_z=c\) forces \(F_h=0\) for
every word on the other five sites.  Consequently

\[
 D\bigl(S(\ell)\bigr)=0,
 \qquad S(\ell)_{rz}=h_r\ell^{\mathsf T},
 \qquad \ell\in\mathbb C^2.
\]

One nonzero rank-one star kernel tangent therefore lifts to the full
two-dimensional column family.

## Excluding absorption by gauge

A gauge tangent has

\[
 G(\lambda)_{rs}=(\lambda_r+\lambda_s)M_{rs},
 \qquad \sum_{r\in R}\lambda_r=0.
\]

If it is supported on the \(z\)-star, then
\(\lambda_r+\lambda_s=0\) on every live edge of the graph induced on
\(R\setminus\{z\}\).  When that live graph is connected and nonbipartite,
alternating the signs along paths and around an odd cycle forces every
off-centre \(\lambda_r\) to vanish; the zero-sum equation then gives
\(\lambda_z=0\).  Hence no nonzero gauge is star-supported.

If also \(h\ne0\), the map \(\ell\mapsto S(\ell)\) is injective.  The two
binary star columns are consequently independent modulo the five gauges,
so

\[
 \dim\ker D\ge 5+2=7,
 \qquad \operatorname{rank}D\le60-7=53.
\]

This is the promised branch theorem: a nonzero rank-one star kernel tangent,
together with a connected nonbipartite off-star live graph, rules out residual
rank 54 or 55.  For the exact source above the off-star graph is connected
and contains the live triangle \(0-1-2-0\), so the theorem applies sharply.
