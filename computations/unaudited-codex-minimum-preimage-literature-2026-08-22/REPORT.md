# Minimum-preimage theorem survey for the matching map

Status: **three primary-theorem candidates audited; no off-the-shelf closure
theorem found, but the ED/conormal equations are the only source-faithful
survivor.**

Write the literal matching map as

\[
 \Phi_n(A)_{i_1\ldots i_n}
 =\sum_{M\in\operatorname{PM}(n)}\prod_{uv\in M}A_{uv}[i_u,i_v].
\]

For `n=8`, its source is the 252-dimensional space
`direct_sum_{uv in K8} C^3 tensor C^3`; `Phi_8` is homogeneous of degree four
and equivariant for the local `product_v GL(3)` action.

## 1. Tensor scaling / capacity / Kempf--Ness

Bürgisser--Franks--Garg--Oliveira--Walter--Wigderson give algorithms and
certificates for scaling a tensor to prescribed one-body marginals and for
membership in the associated moment polytope.  Applied to the matching source
representation, the literal conclusion is exactly the already-frozen orbit
minimum condition

```text
R_v = c I_3  for every site v.
```

It does not use the fixed nonlinear equation `Phi_8(A)=GHZ`: the full local
group moves both source and output, whereas a fixed fibre is preserved only by
the target stabilizer.  Both exact controls pass (`R_v=I_3` for the `n=4` GHZ
minimum and `R_v=7I_3` for the phased `n=6` non-GHZ smooth minimum).  Therefore
this candidate reduces to moment balance and is rejected.

Primary source: P. Bürgisser et al., [Efficient algorithms for tensor scaling,
quantum marginals and moment
polytopes](https://arxiv.org/abs/1804.04739).

## 2. Geometric Brascamp--Lieb / operator scaling equality

The natural source-labelled attempt takes the incident edge matrices as maps
in a BL datum.  Full isotropy supplies only the summed normalization
`sum_u A_vu A_vu^*=cI`.  A geometric BL datum also needs fixed codomains and
individual coisometry/surjectivity after normalization.  The exact `n=4` GHZ
minimum has all six live `3 by 3` edge maps of rank one, so the naive uniform
datum fails this hypothesis immediately.  Replacing each codomain by its
point-dependent image can repair coisometry, but then the datum varies with
the source and the BL equality statement contains no matching polynomial
`Phi_n`; its remaining normalization is again just isotropy.  This candidate
is rejected before any inequality search.

Primary source: A. Garg et al., [Algorithmic and optimization aspects of
Brascamp--Lieb inequalities, via Operator
Scaling](https://arxiv.org/abs/1607.06711).

## 3. Euclidean-distance / conormal correspondence

Let `X_y=Phi_n^{-1}(y)`.  At every smooth minimum of `||A||^2` on `X_y`, the
ED/conormal criticality equation is

\[
 A=D\Phi_A^*\lambda.
\]

This one is literal and source-faithful.  Edgewise,

\[
 D_e\Phi_A(X_e)=X_e\mathbin{\lrcorner}H_{V\setminus e}(A),
 \qquad
 A_e=(D_e\Phi_A)^*\lambda,
\]

so every equation retains the exact six-site residual-Hafnian columns.  It is
the global form of block normality, not an invariant trace relaxation.  The
exact audit verifies row-space membership for the global `n=4` norm minimum.
The phased `n=6` model has derivative rank `130/135`; its kernel is exactly the
five scalar vertex gauges, and full isotropy makes the source orthogonal to
that kernel, so it also satisfies the conormal equation while having a
non-GHZ output and injective star/triangle blocks.  Thus ED supplies useful
equations but no theorem forcing a cap; the missing step must exploit the
specific GHZ mixed-output equations inside this conormal system.

Primary source: J. Draisma et al., [The Euclidean distance degree of an
algebraic variety](https://arxiv.org/abs/1309.0049).

Singular-vector tuple theorems are the Segre/best-rank-one specialization of
ED criticality.  They concern approximation of a fixed tensor by decomposable
tensors, not minimum preimages under this 105-term quartic map, and are
therefore rejected as output-only.  See S. Friedland and G. Ottaviani, [The
number of singular vector tuples and uniqueness of best rank one approximation
of tensors](https://arxiv.org/abs/1210.8316).

## Exact must-pass audit

`audit_minimum_preimage_candidates.py` verifies, without floating point:

* the `n=4` source is exact ternary GHZ, has norm squared six, all live edge
  ranks one, `R_v=I_3`, eight injective star/triangle blocks, and
  `A in row(D Phi_A)`;
* the phased `n=6` source has pure amplitudes one, a literal mixed amplitude
  `1+omega`, `R_v=7I_3`, star ranks 45, triangle ranks 27, and derivative rank
  130 modulo seven;
* a hostile mutation changing the required `n=4` live-edge rank is killed.

The only theorem worth carrying into the proof spine is therefore the exact
conormal system.  Tensor capacity and BL equality add no information beyond
the already-used moment equations.
