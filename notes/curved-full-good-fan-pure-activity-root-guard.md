# A curved full good fan still permits only inactive clean roots

## 1. Outcome

The common-root branch in
[the good-clique alternative](good-clique-curvature-or-zero-shore.md)
cannot be closed from good-star injectivity and the exact four-site/Bianchi
identities alone. There is a literal rational aggregate family on eight
sites with all of the following properties.

1. One centre \(p\) has a full seven-neighbour fan, and both aggregate star
   maps have rank three at every pair in that fan.
2. In the selected \(pq\)-chart the internal Hessian is gauge-rigid. Its
   rank-three block graph is empty, so this is the maximally defective E2
   graph rather than a hidden E1 chart.
3. A canonical physical transition has scalar curvature \(-3\). The full
   four-site connection identity and its three-pair Bianchi identity hold
   literally in the same source variables.
4. The exact target-compatible cap locus at \(pq\) contains the projective
   plane

   \[
      \mathcal L=\operatorname{span}\{I,E_{12},E_{21}\}.
   \]

   In fact this is the complete kernel of the cap residual. If

   \[
      K=\lambda I+uE_{12}+vE_{21},
   \]

   then

   \[
   K\mathbin{\lrcorner}H_8(A)
      =K\mathbin{\lrcorner}\Delta_{8,3}
      =\lambda\Delta_{6,3},\qquad
   s(K)\kappa_0(K)\kappa_1(K)\kappa_2(K)=3\lambda^4,              \tag{1}
   \]

   while its clean error is

   \[
      \mathcal E_{p,q}(K)=\lambda^3R,\qquad
      R=9\bigl(e_{100100}+6e_{201102}\bigr)\ne0.                  \tag{2}
   \]

   Thus every clean point of this plane is inactive.
5. On the curvature-derived candidate line

   \[
      K(z)=E_{00}+zI,
   \]

   the source-side clean polynomial is exactly

   \[
      \mathcal E_{p,q}(K(z))=(1+z)^3R.                            \tag{3}
   \]

   Its sole root \(z=-1\) kills both \(s\) and \(\kappa_0\). This is
   precisely the pure-activity-power exception left open by the
   [augmented-gauge gcd criterion](augmented-e2-gauge-clean-cap-polynomial.md).

The family is deliberately not an exact ternary GHZ source: its full
transverse pair rows fail. It is therefore not a counterexample to the
conjecture or to a common-root theorem that uses the complete target
system. It is a sharp source-variable guard: physical curvature, a full
good fan, gauge rigidity, four-site compatibility, and Bianchi do not
prevent the saturated gcd from being constant or a pure power of the
activity form. A positive theorem must additionally couple curvature to
the full transverse target rows or to genuinely nonzero spanning E2
primitives.

## 2. Construction

Use the six-site quadratic \(q\) and boundary forms \(P,Q\) from
[the dirty-cap model](n8-rank-one-clean-cap-local-torus-obstruction.md),
Sections 2–3. Thus

\[
   (q+3PQ)q^{[2]}=\Delta_{6,3},                                  \tag{4}
\]

and \(P_0=0,\ Q_0=e_{0,1}\). Keep all internal blocks of \(q\). For
\(u\ne0\), keep

\[
   A_{pu}=3e_{p,0}P_u,\qquad A_{qu}=e_{q,0}Q_u.                   \tag{5}
\]

Replace the direct block and the two blocks at site \(0\) by

\[
\begin{aligned}
 A_{pq}&=3e_{p,0}e_{q,0}+e_{p,1}e_{q,1}-e_{p,2}e_{q,2},\\
 A_{p0}&=e_{p,1}e_{0,0}+e_{p,2}e_{0,2},\\
 A_{q0}&=e_{q,0}e_{0,1}+e_{q,1}e_{0,0}+e_{q,2}e_{0,2}.           \tag{6}
\end{aligned}
\]

All products between the new \(p\)- and \(q\)-rows in colours \(1,2\)
collide at site \(0\). Consequently their square-free products vanish:

\[
   p_1q_1=p_2q_2=p_1q_2=p_2q_1=0.                               \tag{7}
\]

The traceless direct padding in (6) also cancels under \(I\). Hence the
cap data of \(I\) and \(E_{00}\) are identical:

\[
   (s_I,r_I)=(s_{00},r_{00})=(3,3PQ),                            \tag{8}
\]

while \(E_{12}\) and \(E_{21}\) have zero cap data. Equation (4) proves
the compatibility assertion in (1) without selecting a matching term.

## 3. The entire centre fan is aggregate-injective

At the pair \(pq\), the \(p\)-star has a nonzero \(3\times3\) minor on
the output coordinates

\[
   (0,0),(0,2),(1,0)
\]

with determinant \(3\). The \(q\)-star has one on
\((0,0),(0,1),(0,2)\) with determinant \(-1\).

For a boundary neighbour \(r\in\{0,\ldots,5\}\), the \(p\)-star after
deleting \(p,r\) retains the invertible direct block \(A_{pq}\). The
opposite \(r\)-star has the following explicit minors; an entry \((v,c)\)
means the colour-\(c\) output coordinate at site \(v\).

\[
\begin{array}{c|c|c}
r&\text{three output coordinates}&\det\\ \hline
0&(1,0),(3,0),(5,2)&1\\
1&(0,1),(2,2),(5,1)&1/3\\
2&(1,0),(1,2),(5,0)&-1/6\\
3&(0,0),(0,1),(4,2)&1/3\\
4&(0,1),(1,2),(3,2)&1/3\\
5&(0,2),(1,1),(2,0)&-1/18
\end{array}                                                     \tag{9}
\]

Thus every one of the seven centre pairs has aggregate ranks \(3,3\).
For the selected internal \(q\), exact row reduction gives Hessian rank
\(130\) on its \(135\)-dimensional quadratic space. The five independent
vectors

\[
   \Gamma_q(\epsilon_i-\epsilon_5),\qquad 0\le i<5,              \tag{10}
\]

are in its kernel, so they are the complete kernel. Every block of this
\(q\) has rank at most two. Hence the chart is gauge-rigid and its
rank-three graph has six isolated vertices.

## 4. Curvature and Bianchi survive the padding

Choose exposed sites and colours

\[
   (p,q,r,s;a,b,c,d)=(p,q,0,1;0,0,1,0).
\]

In the notation of the
[connection note](overlapping-pair-cap-bianchi-connection.md), the six
direct entries are

\[
   (A,B,C,E,F,U)=(3,0,1,3,1,-1).                                \tag{11}
\]

Therefore

\[
   AU-BF=-3,\qquad AU-EC=-6,\qquad BF-EC=-3,                     \tag{12}
\]

and

\[
   (AU-BF)-(AU-EC)+(BF-EC)=0.                                   \tag{13}
\]

The checker also expands every quadratic coefficient on the four-site
common complement and verifies the stronger connection equation

\[
 UP_{pq}+tL_{pq;s}-FP_{pr}-yL_{pr;s}
       =(At-By)v+(AU-BF)z.                                      \tag{14}
\]

Thus the nonzero transition and Bianchi data are not formal assignments;
they come from the same endpoint-ordered aggregate blocks as the cap
plane.

## 5. Exact cap plane and the inactive-root mechanism

Let

\[
 \mathcal C_A(K)=K\mathbin{\lrcorner}H_8(A),\qquad
 \mathcal T(K)=\sum_cK_{cc}X_c.
\]

Exact enumeration of the \(729\times9\) residual matrix
\(\mathcal C_A-\mathcal T\) gives rank six and

\[
 \ker(\mathcal C_A-\mathcal T)
      =\operatorname{span}\{I,E_{12},E_{21}\}.                   \tag{15}
\]

Equations (7)–(8) then give, for
\(K=\lambda I+uE_{12}+vE_{21}\),

\[
 s=3\lambda,\qquad r=3\lambda PQ,\qquad
 (\kappa_0,\kappa_1,\kappa_2)=(\lambda,\lambda,\lambda).         \tag{16}
\]

The clean error is cubic at the \(8\to6\) boundary. Homogeneity and the
already audited value at \(I\) prove (2). Its only zero locus is the
inactive line \(\lambda=0\).

For the physical curvature line \(E_{00}+zI\), equation (8) instead gives

\[
 s=3(1+z),\qquad r=3(1+z)PQ,                                    \tag{17}
\]

which proves (3). Its activity polynomial is

\[
 s\kappa_0\kappa_1\kappa_2=3(1+z)^2z^2.                         \tag{18}
\]

The clean polynomial therefore has no active root. On the affine
target-compatible lines \(I+zE_{12}\) and \(I+zE_{21}\), the error is the
nonzero constant \(R\). Projectively, (2) is the corresponding pure
power of the activity coordinate. These are exactly the two exceptional
gcd shapes identified in the augmented-gauge note.

## 6. What the guard does and does not exclude

The family fails the complete target equation. For example, its
\(E_{11}\) cap row is not \(X_1\). More intrinsically, the fixed-\(q\)
functional from
[the full pair-suspension audit](../computations/verify_n8_full_pair_suspension_subcharts.py)
annihilates the entire image of the pair Hessian but has values

\[
   1,-\tfrac12,-\tfrac12
\]

on \(X_0,X_1,X_2\). It vanishes on their sum, which is why the compatible
plane (15) survives, but it forbids the three separate diagonal target
rows. Thus the guard cannot be completed to an exact source while this
internal \(q\) is fixed.

This pinpoints the remaining positive route. The high-order curved branch
must use information absent here, such as:

1. the two transverse diagonal target rows and their physical product-star
   provenance;
2. nonzero off-diagonal E2 primitives spanning a defect space, rather than
   cap-data-kernel directions like \(E_{12},E_{21}\); or
3. a coupling theorem forcing a common divisor away from the activity
   locus between the curvature-selected direct line and an augmented E2
   defect line.

Another four-site or Bianchi identity alone cannot supply that coupling.

The lightweight exact
[checker](../computations/verify_curved_good_pair_dirty_cap_line_guard.py)
reconstructs the rational blocks, checks all seven pairs' two star ranks,
the gauge-only Hessian kernel, the curvature and full connection identity,
the exact cap-residual kernel, and both coefficients of \(R\). It uses no
search or numerical root finding.
