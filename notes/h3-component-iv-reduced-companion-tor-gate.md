# The reduced companion augmentation is exactly a five-class Tor transgression

Research boundary only.  This does not construct the missing relative cells,
prove the Component-IV comparison, or prove Krenn's conjecture.

## Outcome

The natural next source-resolution inventory does **not** supply the five
reduced augmentations requested after the endpoint-word-change audit.  The
fifteen physical endpoint routes have boundaries

\[
                    (-\Omega_v,q_{v,N}),
 \qquad v=1,\ldots,5,\quad N\in\operatorname{PM}(F_v).
\]

All literal matching incidence, first/second Euler, matching-Bianchi, and
two-chart rows package the three matching labels on each face into

\[
 h_v=\sum_Nq_{v,N},
\]

but leave a primitive cokernel \(\mathbb Z^5\), one class for every deleted
site.  The first derived layer is real: on the five-cycle torus the five
cubic denominator/principal-parts S-pairs cancel adjacent companions.  Their
boundary matrix is the oriented incidence matrix of \(C_5\), hence has rank
four.  The unique degree-five Tate cell is the relation among those five
columns; it adds no boundary image.  The primitive aggregate

\[
                         \lambda_1+\cdots+\lambda_5
\]

therefore survives.  This is an exact no-go for the complete matching/Euler,
cubic PP/first-Tor, and degree-five compatibility inventory—not a no-go for
an arbitrary larger source resolution.

## Exact missing source operation

There is a source-coordinate formulation with no invented cap map.  Let

\[
 b:R^{15}\longrightarrow R^{243},\qquad
 d_{v,a}\longmapsto e_a^{(v)}q^{[2]},
\]

and split its columns into the five selected generators
\(d_{v,m_v}\), for \(m=12112\), and the other ten generators.  Universally,
\(b\) has rank 15 and the unselected block has rank 10.  Thus there is no
universal kernel to rename as a relative face.

In the intended active full-source ring

\[
 S=(\mathscr R/J_{\mathrm{full\ nine}})[\kappa^{-1}],
\]

a source-provenant augmentation on face \(v\) exists precisely when there is
a kernel vector

\[
 k_v=d_{v,m_v}+\sum_{(u,c)\ne(u,m_u)}z_{u,c}d_{u,c},
 \qquad b(k_v)=0.                                      \tag{1}
\]

Equivalently,

\[
 b(d_{v,m_v})\in\operatorname{im}(b_{\rm oth})
                 \pmod {J_{\mathrm{full\ nine}}}.     \tag{2}
\]

All five augmentations exist exactly when the transgression

\[
 \tau:\operatorname{Tor}_1(\operatorname{coker}b,S)
       =\ker(b\otimes S)\longrightarrow S^5
\]

is onto.  Equations (1)--(2) are the first genuinely new attaching datum:
they cancel the face companions while carrying zero ridge, target, cap
boundary, and ordinary residue.  The two frozen rational packets have
transgression ranks four and three, respectively, but neither is a full
source point; they are counterguards, not nonexistence proofs over \(S\).

## Why the old candidates do not qualify

The complete old ordinary EqSystem row-plus-cap module is already excluded
by the all-word homogenizer extraction: arbitrary polynomial multipliers of
all 6,561 rows do not construct the completed \(n_c\).  The cubic
\(P_3\sqcup K_2\) cells only give face differences, and their degree-five
compatibility has zero primitive aggregate.  Common-\(q\) Euler identities
leave the same five primitive classes.

The chart-25 relative trace is also not a replacement for (1).  Its 4D
projection discards at least 818 off-fibre rows, retains four target labels,
and has product-anchor endpoint grade rather than the selected repeated
response grade.  It is a mapping-cylinder projection in an incompatible
graded quotient.

Consequently the exact next proof obligation is finite in statement but not
yet proved: establish the five memberships (2), or produce a full-source
covector showing that at least one remains outside the unselected image.
Another Euler identity, Bianchi shuffle, formal C5 syzygy, or chart-25
projection does not address this obligation.

## Verification

Run

```text
.venv/bin/python computations/verify_h3_component_iv_reduced_companion_tor_gate.py
.venv/bin/python -O computations/verify_h3_component_iv_reduced_companion_tor_gate.py
```

The checker reconstructs the fifteen endpoint companions, the doubled
rank-105-in-110 matching/Euler module with primitive cokernel \(\mathbb Z^5\),
the full \(5@2,5@3,1@5\) cycle resolution, its physical denominator-PP
realization, the chart-25 grade guard, the universal denominator ranks, and
the exact Tor transgression criterion.  No non-source calibration or
declared relative cell is used.
