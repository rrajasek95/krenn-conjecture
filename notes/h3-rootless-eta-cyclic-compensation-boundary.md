# The stabilizer obstruction has a unique cyclic compensation, but it is the missing comparison map

## Exact compensation

Work on the marked clean-C5 open and write

\[
             t=q_{pq}^{00},\qquad u_v=q_{xv}^{00}.
\]

For Godel's five physical target-stabilizer tangents,

\[
 \eta_z(t)=1,qquad
 \eta_z(u_v)=-\delta_{zv}\frac{u_z}{t}.                \tag{1}
\]

The uncorrected aggregate terminal readout therefore has

\[
                         \Lambda(\eta_z)=-5-\frac{u_z}{t}. \tag{2}
\]

There is an exact cyclic correction.  Facewise, put

\[
                         c_v=t-u_v.                    \tag{3}
\]

Then

\[
 \eta_z(c_v)=1+\delta_{zv}\frac{u_z}{t},\qquad
 \eta_z\!\left(\sum_vc_v\right)=5+\frac{u_z}{t}.      \tag{4}
\]

Thus (4) cancels (2) for every (z), simultaneously and without imposing
(u_z=-5t).  Equivalently, the corrected face expression is

\[
 \boxed{\Omega_v+c_v=q_{pq}^{22}-q_{xv}^{0m_v},}       \tag{5}
\]

which is manifestly fixed by every (eta_z): the stabilizer weights are
supported only at ((p,0)) and ((z,0)).

The correction is minimal and unique.  A cyclic face-local linear ansatz
(c_v=A t+B u_v) has aggregate derivative

\[
                         5A-B\frac{u_z}{t}.
\]

Matching (4) forces (A=1,B=-1).  Without face locality, the aggregate is
still uniquely

\[
                         5t-\sum_vu_v                 \tag{6}
\]

modulo functions killed by all five stabilizer tangents; only its
distribution among the five faces can change.

## Correct augmented typing

The compensation must enter the rootless coordinate with

\[
          d r_v(\eta_z)=1+\delta_{zv}\frac{u_z}{t}.    \tag{7}
\]

Since (d\Omega_v(\eta_z)) is the negative of (7), the corrected physical
kernel column is a linear combination of

\[
                            \Omega_v-r_v.              \tag{8}
\]

The formal comparison relations (8) have

\[
             (W,\operatorname{tgt},\operatorname{ores},
                       \operatorname{ainc})=(0,0,0,0).
\]

Hence (7), if supplied by a physical comparison, preserves every required
augmented readout and cyclic symmetry.  This is stronger than canceling the
single aggregate numerically: it kills the stabilizer obstruction face by
face.

## Why the current (q)-inventory does not supply it

Every selected (q_{v,N}) companion uses only the nonzero colours
(m_i\in\{1,2\}).  Therefore

\[
                         \eta_z(q_{v,N})=0             \tag{9}
\]

for every (z,v,N).  Constant combinations of the known (q)-companions
cannot change (2).  Moreover an individual source-valid (q) route carries
its private ordinary-residue companion.  Zero ordinary residue kills that
single-face coefficient; only adjacent differences survive, and those give
the already known rank-four C5 edge module rather than a vertex value.

After homogeneous transport, the candidate source-labelled value can be
written

\[
                         (t-u_v)Q_v,                   \tag{10}
\]

where (Q_v) is the selected repeated matching tail.  The clean
normalization has (Q_v=1), and every (eta_z) fixes (Q_v), so (10)
reduces exactly to (3).  But (10) is presently only a value to be carried by
a comparison, not a constructed source chain.

Indeed, the endpoint-to-collision audit proves that the first literal
source object is an adjacent comparison square, not a single vertex
(Omega_v-r_v).  Constructing (10) with zero (W), target, ordinary
residue, and anchor incidence is precisely the missing common-companion
(Omega\)-to-(r) comparison.  The formula (3) identifies its value; it
does not manufacture the map.

## Outcome and scope

The new stabilizer columns do not force the five scalar equations
(u_z=-5t).  They sharpen the physical comparison gate:

* the unique cyclic compensation is (r_v^{\rm comp}=t-u_v);
* it has the correct zero-readout typing and cancels all five tangents;
* no existing (q)-only correction supplies it; and
* the sole remaining construction is the already isolated source-labelled
  rootless vertex/common-companion comparison.

This is exact on the marked (t\ne0), (R_v=0) clean-C5 slice.  It is not
a construction of the comparison and does not exclude an enlarged relative
source resolution.

Run:

```text
python3 computations/verify_h3_rootless_eta_cyclic_compensation_boundary.py
python3 -O computations/verify_h3_rootless_eta_cyclic_compensation_boundary.py
python3 -I -S computations/verify_h3_rootless_eta_cyclic_compensation_boundary.py
```

The checker pins the physical stabilizer obstruction, the exact endpoint
and first-collision modules, and the target-preserving C5 normalization.  It
solves the cyclic compensation system, verifies all five facewise
comparison decompositions and augmented readouts, and replays the (q)-only
ordinary-residue no-go.

Frozen ledger SHA-256:

```text
4e13ecf57d3c4ed8b7f09af5139ab623262e621ea09804bb9f74b6f66107ae46
```
