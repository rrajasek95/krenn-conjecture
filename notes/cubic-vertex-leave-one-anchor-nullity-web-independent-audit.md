# Independent audit: cubic leave-one-anchor nullity web

## 1. Verdict and exact scope

The conditional theorem in
[cubic-vertex-leave-one-anchor-nullity-web.md](cubic-vertex-leave-one-anchor-nullity-web.md)
is sound.  If an exact ternary source \(H_B(A)=\Delta_{B,3}\) has an
**aggregate support** vertex \(p\) with exactly three nonzero neighbours,
then for each of the \(N-4\) zero-block neighbours \(q\), all three
leave-one-anchor maps are singular and at least two have nullity at least
two.  The minimum possible sorted nullity profile is therefore
\((1,2,2)\).

This is not a proof that a cubic vertex exists.  The target-flattening
route licenses that hypothesis when an endpoint has exactly three
essential neighbour supports, the equality case of its dimension-three
essential-subspace bound.  Having at most two essential neighbours does
not license it.  The nullity theorem also gives no clean cap, separator,
support reduction, or all-even descent; its conclusion is precisely the
determinantal rank ledger stated in the primary note.

## 2. Reconstruction of equation (9)

Write \(N=2m\).  Cubic rigidity supplies distinct neighbours
\(a_0,a_1,a_2\) and nonzero scalars \(\lambda_c\) with

\[
 A_{pa_c}=\lambda_c e_c^{(p)}\otimes e_c^{(a_c)},
 \qquad
 H_{B\setminus\{p,a_c\}}(A)
   =\lambda_c^{-1}e_c^{\otimes(B\setminus\{p,a_c\})}. \tag{A1}
\]

Fix a nonneighbour \(q\), so \(A_{pq}=0\), and put
\(W=B\setminus\{p,q\}\) and \(K_c=W\setminus\{a_c\}\).  Partition the
perfect matchings of \(B\setminus\{p,a_c\}\) by the unique site
\(v\in K_c\) paired to \(q\).  With every tensor slot restored to its
physical position this gives

\[
 H_{B\setminus\{p,a_c\}}(A)
 =\sum_{v\in K_c} A_{q\mid v}\otimes
       H_{K_c\setminus\{v\}}(x),                       \tag{A2}
\]

where \(A_{q\mid v}\in V_q\otimes V_v\) is oriented with its \(q\)-slot
first and \(x\) contains exactly the blocks internal to \(W\).  Contracting
the \(q\)-slot by \(e_d^*\), and writing
\(s_{d,v}=(e_d^*\otimes\mathrm{id})A_{q\mid v}\), yields

\[
 \sum_{v\in K_c}s_{d,v}^{(v)}\otimes
       H_{K_c\setminus\{v\}}(x)
 =\delta_{cd}\lambda_c^{-1}e_c^{\otimes K_c}.          \tag{A3}
\]

The left side is exactly
\(\Phi_{q,c}(\pi_cs_d)\), proving equation (9).  No individual matching
summand has been inferred from a cancelling coefficient: (A2) is a
partition of the complete matching expansion, followed by a linear
contraction.

The divided-power normalization is also exact.  Since
\(\lvert K_c\rvert=2m-3\), a full-support term in

\[
       \left(\sum_{v\in K_c}z_v\right)
                       \frac{x^{m-2}}{(m-2)!}           \tag{A4}
\]

chooses one centre \(v\) and an unordered matching of the other
\(2m-4\) sites.  Ordinary multiplication orders its \(m-2\) internal
edges in \((m-2)!\) ways, so division leaves every matching once.  The
endpoint-ordered cell on \(qv\) supplies \(z_v\); the remaining cells give
the cofactor in (A3).  Thus (A4) and the column definition of
\(\Phi_{q,c}\) agree coefficient by coefficient, including asymmetric
endpoint cells.

## 3. Lemma 3.1, including both degeneracies

For distinct anchors define the complete shared cofactor

\[
       T_{cb}=H_{W\setminus\{a_c,a_b\}}(x).             \tag{A5}
\]

If a vector is supported only at \(a_b\), its image under
\(\Phi_{q,c}\) is its local \(a_b\)-factor tensored with (A5).  This is the
whole cofactor, not one selected matching.  The same \(T_{cb}=T_{bc}\)
appears when the two anchors are reversed; only the restored position of
the singled-out local factor changes.

Fix \(c\), and call the other colours \(d,e\).  If both wrong restrictions
\(\pi_cs_d\) and \(\pi_cs_e\) vanish, both global rows are supported only
at \(a_c\).  The diagonal \(d\)-equation is

\[
 s_{d,a_c}^{(a_c)}\otimes T_{dc}
       =\lambda_d^{-1}e_d^{\otimes K_d}\ne0.            \tag{A6}
\]

Hence both factors on the left are nonzero.  The off-diagonal \(e\)-row
in the same map gives
\(s_{e,a_c}^{(a_c)}\otimes T_{dc}=0\), so the local vector, and therefore
the entire row \(s_e\), is zero.  Its own nonzero diagonal equation is then
impossible.  This covers the case in which either prospective local row
is zero; no division by a row coordinate is used.

If instead the two nonzero restrictions are proportional,
\(\pi_cs_e=t\pi_cs_d\) with \(t\ne0\), then
\(v=s_e-ts_d\) is supported only at \(a_c\).  The \(d\)- and \(e\)-maps
give

\[
 \Phi_{q,d}(\pi_dv)=-t\lambda_d^{-1}e_d^{\otimes K_d},
 \qquad
 \Phi_{q,e}(\pi_ev)= \lambda_e^{-1}e_e^{\otimes K_e}. \tag{A7}
\]

Both right sides are nonzero.  In the first factorization the \(a_c\)
factor is \(v_{a_c}\), so equality with a pure rank-one tensor forces
\(v_{a_c}\in\mathbb C^*e_d\); the second forces
\(v_{a_c}\in\mathbb C^*e_e\).  These axes are disjoint for \(d\ne e\).
The argument uses only the elementary fact that a nonzero decomposable
tensor has unique one-dimensional factor spaces.

Thus the two wrong restrictions are either independent or exactly one is
zero and the other nonzero.  In either case \(\Phi_{q,c}\) has a nonzero
kernel vector.  If its nullity is one, independence is impossible, so
there is a unique wrong colour \(\rho(c)\) whose whole row is supported at
\(a_c\).

## 4. Lemma 4.1 and shared-cofactor purity

Suppose two maps, indexed by \(c\ne b\), both have nullity one.  Their
exceptional rows \(s_{\rho(c)}\) and \(s_{\rho(b)}\) are nonzero because
each has a nonzero diagonal equation.  The colours \(\rho(c)\) and
\(\rho(b)\) are distinct: if equal, the same nonzero global row would be
supported in the two disjoint summands \(V_{a_c}\) and \(V_{a_b}\).

Now inspect \(T_{cb}\).  The row supported at \(a_b\), viewed in the
\(c\)-map, gives exactly one of two conclusions:

* if \(\rho(b)=c\), its response is the nonzero pure \(c\)-tensor.  Unique
  rank-one factors force both its local vector and \(T_{cb}\) to be
  nonzero and pure of colour \(c\);
* if \(\rho(b)\ne c\), its response is zero.  The local vector is nonzero,
  so the tensor-product zero law forces \(T_{cb}=0\).

Reversing \(b,c\) gives the same alternatives with colour \(b\).  The
complete case table is

| \(\rho(b)=c\) | \(\rho(c)=b\) | forced states of \(T_{cb}\) |
|---|---|---|
| yes | yes | nonzero pure \(c\), and nonzero pure \(b\) |
| yes | no | nonzero, and zero |
| no | yes | zero, and nonzero |
| no | no | \(\rho(b)=\rho(c)\), already excluded |

The first row is impossible because the remaining tensor has
\(N-4\ge4\) sites and the constant \(c\)- and \(b\)-tensors are not
proportional.  The middle rows are zero/nonzero contradictions.  Hence at
most one map has nullity one.  Together with Lemma 3.1, the minimum profile
is \((1,2,2)\), with total nullity at least five.

## 5. The \(N=8\) boundary and cubic scope

At \(N=8\), a cubic \(p\) has exactly four nonneighbours \(q\).  For each
one, \(W\) has six sites, \(K_c\) has five, and \(T_{cb}\) has four.  Thus
each map has \(3\lvert K_c\rvert=15\) columns and codomain dimension
\(3^5=243\).  There are \(3\cdot4=12\) singular maps and at least
\(2\cdot4=8\) maps of rank at most \(13\).  No empty tensor, negative
divided power, or low-order coincidence occurs at the boundary.

The route from essential stars to this theorem has one precise trigger.
For the mode-\(p\) support spaces of incident aggregate blocks, equality
with three essential indices makes those three supports independent lines
and every other support zero.  Zero mode support means a zero aggregate
block; a nonzero one-dimensional support means rank one.  Hence \(p\) has
aggregate support degree exactly three.  Cubic rigidity, which also uses
the full target equation, then upgrades those blocks to the same-colour
coordinate cells in (A1).  Parallel decorated sources remain combined
inside each aggregate block.

Nothing analogous follows merely from the universal statement “at most
three neighbours are essential.”  In particular, the cases of zero, one,
or two essential neighbours do not make \(p\) cubic.  Conversely, the
nullity-web proof may be applied to a cubic vertex obtained by some other
valid argument; it does not itself depend on essential-star terminology.

## 6. Independent exact checker

Frozen audited artifacts:

```text
f37e4ae6f46d31bc5b8784450c37d850fd6388726a93308c97b1318e71577740  notes/cubic-vertex-leave-one-anchor-nullity-web.md
4b2c1d51c4060a1dba57fa1a1a4a0438d2e3c88b3d351c9e9996c09259009c03  computations/verify_cubic_vertex_leave_one_anchor_nullity_web.py
74bcdc5f5ef893dad3855ea2b877980e402c4ea13edc87b8e502d3d66f86496d  computations/audit_cubic_vertex_leave_one_anchor_nullity_web_independent.py
```

The clean-room checker
[audit_cubic_vertex_leave_one_anchor_nullity_web_independent.py](../computations/audit_cubic_vertex_leave_one_anchor_nullity_web_independent.py)
does not import the primary checker.  It

* compares 32,805 tagged endpoint-ordered terms from direct matching,
  cofactor-column, and divided-square constructions of (A3) at \(N=8\);
* verifies the factorial normalization independently at degrees two and
  three and checks all 18 orientations of the shared-cofactor
  factorization;
* solves the pure rank-one factor and zero tensor-product equations exactly
  over \(\mathbb F_5\), covering all both-zero and proportional cases of
  Lemma 3.1 and all zero/pure and distinct-pure cases of Lemma 4.1;
* enumerates 168,338 spanning seven-neighbour multisets of subspaces of
  \(\mathbb F_2^3\), finding 28 three-essential equality multisets and
  checking that each consists of three independent lines plus zeros; and
* audits the minimum profile \((1,2,2)\) and the exact \(N=8\) dimensions
  and counts.

The finite-field computations certify the displayed combinatorial and
factor equations; the characteristic-zero theorem follows from the
field-independent tensor arguments above.

## 7. What is not proved

Singular cofactor maps can occur in active cancellation sources.  A kernel
vector of \(\Phi_{q,c}\) has not been shown to lift to a support-reducing
deformation, and compatible kernels for different \(q\)'s have not been
shown to produce a cap or separator.  Accordingly the primary note's two
continuation targets are accurately labelled as targets, not consequences.
The audit therefore passes the stated nullity web and rejects any stronger
claim of descent from this artifact alone.
