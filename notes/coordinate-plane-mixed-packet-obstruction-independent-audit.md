# Independent audit: coordinate-plane mixed-packet obstruction

## 1. Verdict and frozen scope

**Verdict: sound.**  I found no algebraic, cancellation, rank, endpoint-order,
or graph-coverage gap in
[`coordinate-plane-mixed-packet-obstruction.md`](coordinate-plane-mixed-packet-obstruction.md).
The theorem really proves that a plane-valued quadratic

\[
 q=\sum_{u<v}q_{uv},\qquad q_{uv}\in W_u\otimes W_v,
\]

cannot satisfy all nine equations

\[
 p_i s_j q^{[2]}=\delta_{ij}X_i
\]

for the three coordinate-plane omission pairs.  The argument uses no
coefficient of \(q^{[3]}\).

This audit was made against these SHA-256 identities:

~~~text
a9dee27e756b9241ddeffc1d4f0b73215d39cdf24116aaa5e8101e047f97d138  notes/coordinate-plane-mixed-packet-obstruction.md
a84e600cb8d9eed4371653e52401c37946163a9c4c9879f178b34e3c4c99e660  computations/verify_coordinate_plane_mixed_packet_obstruction.py
a8b9f434ef41fa33b5f64e53c78951d0918ce6084f99b58cbc1914f88b8ce639  notes/common-annihilator-plane-obstruction.md
d5d3971fa18ed1a1cace4f93af1fff4c4eee048028cfee03c3d24d6de87a9653  computations/verify_common_annihilator_planes.py
~~~

The independent checker
[`audit_coordinate_plane_mixed_packet_obstruction_independent.py`](../computations/audit_coordinate_plane_mixed_packet_obstruction_independent.py)
imports none of those checkers.  It reconstructs the symbolic and finite
certificates directly over \(\mathbb Q\).

## 2. The double quotient is exact

The preliminary projection \(V_u\to T_u\) is legitimate: it fixes every
\(W_u\), hence fixes \(q\), \(q^{[2]}\), and the targets, while sending any
putative multi-site response rows to another putative solution.  No assertion
about the discarded row components is needed.

Write \(F_P\) for the degree-four component occupying \(U\setminus P\).
When quotient functionals are applied at a pair \(P=\{u,v\}\), a slice
\(F_Q\) survives only if both quotient sites are absent from its support.
Thus \(P\subseteq Q\), and the equal cardinalities force \(P=Q\).  The
response factor is exactly

\[
 N_P=a_u b_v^{\mathsf T}+a_v b_u^{\mathsf T};
\]

the two endpoint orders are retained, and this matrix is not assumed
symmetric.  For \(P=B_i\), only \(X_i\) survives.  For a cross-class pair,
no \(X_i\) survives.  Therefore

\[
 N_{B_i}\otimes F_{B_i}=E_{ii}\otimes E_i(B_i),\qquad
 N_P\otimes F_P=0\quad(P\text{ cross-class}).
\]

Uniqueness of factors in the first nonzero simple-tensor equality gives
\(N_{B_i}=\theta_iE_{ii}\) and makes the **entire** slice \(F_{B_i}\)
pure.  The second equality gives \(F_P\ne0\Rightarrow N_P=0\).  This step
does not isolate a term inside a sum, so arbitrary complex cancellation is
fully retained.  The clean-room checker verifies all \(15^2=225\)
missing-pair/quotient incidences.

## 3. The four-site lemmas have the required hypotheses

On the complement of \(B_i\), each \(W_u\) is two-dimensional and contains
the target line \(\mathbb C e_i^{(u)}\).  The restricted edge blocks are
arbitrary elements of \(W_u\otimes W_v\).  Consequently the pure-\(K_4\)
lemma from `common-annihilator-plane-obstruction.md` applies verbatim; it
does not require symmetric, invertible, rank-one, or scalar blocks.

For an independent check, normalize the nonzero components of a linear
annihilator \(\ell\) to \(e_0\) and solve \(q\ell=0\) on four two-spaces.
For support sizes \(1,2,3,4\), the exact kernel dimensions are

\[
                         12,\ 8,\ 5,\ 2.
\]

The matching tensor is zero in support strata \(1,3\).  In support two,
its two supported factors are \(e_0\), its residual \(2\times2\) tensor
has determinant zero, the complementary edge vanishes, and every edge
across support and complement has rank at most one.  In support four, the
matching tensor lies only on \(e_0^{\otimes4}\).

Differentiating a nonzero pure matching tensor transversely at each site
produces such an annihilator.  If there were no target apex, all four
annihilators would have support two.  Their unique nonsupport-neighbor map
must be reciprocal, and the checker finds exactly the three perfect
matchings.  Every nonmissing edge is then transverse at both endpoints,
so its matrix has rank two; the support-two normal form simultaneously
makes that edge rank at most one.  This is the needed contradiction.

The isolated-vertex proof also matches the hypotheses exactly.  If \(y\)
is isolated and \(x\) is its class mate, the four zero cofactors obtained
by deleting \(y\) and one vertex of the pure four-site core are precisely
the four multidegrees of \(q_{\rm core}L_x=0\).  Applying the extension
lemma row by row is therefore valid even when \(L_x\) has several site
components or a block has rank zero.  It aligns every core endpoint of the
\(x\)-star with one fixed target line.  Quotienting each of the other two
pure four-site equations by that line kills both cross matchings and makes
the internal \(B_0\) block nonzero on two distinct pure lines, an
impossibility.  The checker replays all 72 matching incidences and all 36
quotient incidences in this argument.

## 4. Every disconnected graph is covered

After isolated vertices are excluded, a disconnected graph on six vertices
has component sizes

\[
                         2+4,\qquad3+3,\qquad2+2+2.
\]

For the last two patterns I rebuilt the target-apex propagation from the
single tensor-product rule

\[
 \text{two incident blocks factor through }L
 \quad\Longrightarrow\quad
 \text{third incident block factors through }L
 \ \text{or the opposite block is zero}.
\]

This follows by quotienting a zero four-site matching tensor at the common
endpoint.  It is valid over any field and does not distinguish individual
summands of a cancelling coefficient.

Rather than relying on the representatives in the primary checker, the
clean-room search enumerates every vertex partition directly:

* all 10 unordered \(3+3\) partitions: four have six mandatory zero
  cofactors and six have eight;
* all 8 admissible \(2+2+2\) partitions: each has nine mandatory zero
  cofactors;
* all \(4^3=64\) choices of a target apex for every partition.

Every branch ends with all three matching terms of some required nonzero
pure coefficient killed.  Thus both \(3+3\) orbits and the entire
\(2+2+2\) case are excluded for arbitrary complex plane-valued blocks.

An independent enumeration of all \(2^{12}\) cross-class graphs gives
exactly 246 disconnected graphs without isolated vertices:

\[
 168\text{ of type }2+4,\qquad70\text{ of type }3+3,
 \qquad8\text{ of type }2+2+2.
\]

For a \(2+4\) split, the two-component is necessarily a mixed pair and the
connected four-component contains both sites of exactly one class \(c\).
The equations \(N_{uv}=0\) propagate a zero \(a\)-vector (or \(b\)-vector)
through that component; this would make \(N_{B_c}=0\), so all those vectors
are nonzero.  Equality of nonzero rank-one summands propagates their lines,
and \(N_{B_c}=\theta_cE_{cc}\) identifies both common lines with
\(\mathbb C f_c\).  A split class \(d\ne c\) then has

\[
 N_{B_d}=f_cx^{\mathsf T}+yf_c^{\mathsf T},
\]

whose \((d,d)\) entry is zero, contrary to
\(N_{B_d}=\theta_dE_{dd}\).  Hence the \(2+4\) pattern is also impossible.

## 5. Connectivity and final contradiction

The preceding steps force the nonzero-cofactor graph to be connected.  A
site cannot have both \(a_u=b_u=0\), because its same-class response matrix
is nonzero.  If one \(a_u\) vanishes, the edge equation

\[
 a_ub_v^{\mathsf T}+a_vb_u^{\mathsf T}=0
\]

propagates that vanishing along every graph edge; connectivity would make
all three same-class response matrices zero.  Thus every \(a_u\) is
nonzero, and the same argument applies to every \(b_u\).

On each edge, equality of the two nonzero rank-one summands identifies the
two \(a\)-lines and the two \(b\)-lines.  Connectivity therefore puts all
six \(a_u\)'s on one line and all six \(b_u\)'s on another.  The three
nonzero matrices \(N_{B_i}\) are then proportional to one fixed rank-one
matrix, contradicting their proportionality to the three pairwise
nonproportional units \(E_{00},E_{11},E_{22}\).

The two-triangle example was also reconstructed coefficient by coefficient.
It has the three required pure hole slices, a connected six-cycle of
nonzero mixed cofactors, and \(q^{[3]}=0\).  It fails only when the response
matrices are imposed.  This confirms both that the response step is
essential and that \(q^{[3]}=0\) is not hidden in the obstruction proof.

Run the independent audit with

~~~sh
uv run python computations/audit_coordinate_plane_mixed_packet_obstruction_independent.py
~~~

The expected first line is

~~~text
independent coordinate-plane mixed-packet audit: PASS
~~~
