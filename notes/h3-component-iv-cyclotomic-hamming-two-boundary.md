# The cyclotomic face-zero slice survives the first literal Hamming-two row

Research boundary only.  This is the first source-grade calculation after
the square-zero classification in `1932822`.  It does not construct a full
physical source.

## The first coefficient is a genuine coupling

Let (D=\{1,\ldots,5\}), (m=12112), and normalize the dense component of
(q_m^{[2]}=0) by putting the five cycle edges equal to one and the five
chords equal to

\[
             \zeta,\qquad \zeta^2+\zeta+1=0.             \tag{1}
\]

This works over the quadratic algebra in (1), so both conjugate cyclotomic
orbits are treated simultaneously.

Adjoin the exposed site (x).  The first complete word visible from the
pure-1 anchor is

\[
                         1m=112112,                       \tag{2}
\]

which has Hamming distance two from (111111).  The only new internal
cells in this word are

\[
               r_v=q_{xv}^{,1,m_v}\qquad(v\in D).       \tag{3}
\]

For every one of the nine full-row labels, the direct coefficient at (2)
is

\[
                     d_{ij}\sum_v r_vh_v=0.              \tag{4}
\]

The terms in which one endpoint star occupies (x) also have a factor
(h_v) and vanish.  The remaining response coefficient is the literal
matrix

\[
                         P_m^TK_\zeta(r)S_m,              \tag{5}
\]

where (P_m,S_m) are the sitewise endpoint-star entries in the colours
prescribed by (m), and for distinct (u,v\in D)

\[
 (K_\zeta(r))_{uv}
   =\sum_{k\in D\setminus\{u,v\}}
       r_k q_{ab},
 \qquad \{a,b\}=D\setminus\{u,v,k\}.                    \tag{6}
\]

Thus Hamming two is not identically blind.  For the localized carrier
(r_1=1), the entry (K_{23}=q_{45}=1).

## Exact surviving kernel

On the same carrier chart, exact elimination in
(\mathbb Q[\zeta]/(\zeta^2+\zeta+1)) gives

\[
             \operatorname {rank}K_\zeta(r_1)=3          \tag{7}
\]

with kernel basis

\[
 e_1=(1,0,0,0,0),\qquad
 k=(0,1,\zeta,\zeta,1).                                  \tag{8}
\]

Put the two retained endpoint-label columns of each star in the plane
(\langle e_1,k\rangle).  Both selected-word star restrictions still have
rank two, but every entry of (5) is zero.  The third global star direction
may live in another colour/word grade and does not change this coefficient.

The completed two-anchor/direct/crossed static block still has determinant
(-3).  Its columns occupy the already certified static grades; they do not
remove the kernel (8) in the distinct complete-word grade (2).  Hence the
bounded symbolic module has

\[
 \kappa\ne0,\quad r_1\ne0,\quad
 q_m^{[2]}=0,\quad P_m^TK_\zeta(r_1)S_m=0               \tag{9}
\]

without a scalar unit or endpoint-word change.  This is a source-grade
counterguard, not a simultaneous solution of all higher full-word rows.

## The first missing row is now literal

The physical endpoint recolouring needed by the Component-IV landing changes
the exposed colour from 1 to 0.  Its complete residual word is

\[
                         0m=012112,                      \tag{10}
\]

at Hamming distance three from the pure-1 anchor.  The corresponding source
cells

\[
                  \rho_v=q_{xv}^{,0,m_v}                \tag{11}
\]

are disjoint variables from the Hamming-two carriers (3).  No coefficient at
the fixed word (2) can constrain (11).  Before deleting the two chart
endpoints, (10) is exactly the selected full-nine word `01211200` whose bare
two-chart Schur polar has the already certified nonzero connecting class.

Therefore the first Hamming-two row supplies a nonzero coupling, but not the
needed provenance.  The exact next datum is a source relation coupling the
kernel plane (8) at `112112` to the endpoint-changed full-nine word
`012112`/`01211200`.  More constant static transport cannot do this, and the
calculation gives no reason to enumerate higher support packets before that
specific relation is constructed.

## Verification

Run

```text
.venv/bin/python computations/verify_h3_component_iv_cyclotomic_hamming_two_boundary.py
.venv/bin/python -O computations/verify_h3_component_iv_cyclotomic_hamming_two_boundary.py
```

The checker uses exact arithmetic in the quadratic algebra (1), reconstructs
all five face hafnians, derives (4)--(6) by literal matching complements,
verifies the rank and kernel (7)--(8), tests a nonzero coupling and the
rank-two vanishing guard, and pins the square-zero, through-Hamming-two,
two-chart Schur, and complete typed-inventory boundaries.
