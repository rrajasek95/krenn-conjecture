# Only one extra singular type can rescue the shared zero

## 1. Outcome

Retain the cyclic three-zero branch and the notation of
[live-three-zero-extra-singular-axis-capacity.md](live-three-zero-extra-singular-axis-capacity.md).
Let \(a,b\) be the two forced type-\(22\) centres, let \(z_0\) be the
zero site shared by their two different coordinate ports, and let
\({\cal D}_0(x,z)=0\) be the complete residual response forced by the
cyclic port calculation.

For an additional nonzero singular site \(e\), put

\[
 C_e=\{c:e_c\in\operatorname {im}P_e\},\qquad
 M_e=\{0,1,2\}\setminus C_e .
\]

**Theorem 1.1 (shared-star rank reduction).**  If
\(M_e\cap\{0,1\}\ne\varnothing\), then

\[
                         \operatorname {rank}q_{e z_0}<3.          \tag{1}
\]

Consequently an extra singular site can be a rank-three neighbour of
\(z_0\) only if

\[
             M_e=\{2\},\qquad
             \operatorname {im}P_e=\langle e_0,e_1\rangle .       \tag{2}
\]

The capacity theorem makes the missed-axis sets of distinct extra sites
disjoint, so there is at most one site of type (2).  Thus the entire
additional-singular escape at the shared zero has been reduced to one
rank-two plane site.  Its kernel is not asserted to be coordinate; that
remaining freedom is genuine and is not suppressed in the argument.
For the smallest parity-compatible residual with two exceptional live
sites, all three kernel charts are excluded by the triangular response in
[live-three-zero-minimal-extra-plane-all-exceptional.md](live-three-zero-minimal-extra-plane-all-exceptional.md).
The same residual is excluded when exactly one of the two live sites is
exceptional by
[live-three-zero-minimal-extra-plane-one-exceptional.md](live-three-zero-minimal-extra-plane-one-exceptional.md).
Finally,
[live-three-zero-minimal-extra-plane-common.md](live-three-zero-minimal-extra-plane-common.md)
excludes the case in which both live sites have the common beta value.
Thus every beta stratum at the smallest residual order is closed.
Moreover,
[live-three-zero-extra-plane-common-beta-all-orders.md](live-three-zero-extra-plane-common-beta-all-orders.md)
excludes the common-beta stratum for every parity-compatible live-shore
size when this is the sole extra singular site.
[live-three-zero-extra-plane-minority-exceptional.md](live-three-zero-extra-plane-minority-exceptional.md)
extends this uniformly to \(t\le r-2\) exceptional beta values on a
\(2r\)-site live shore.

## 2. Contracting the vanishing residual response

All additional singular sites have beta value \(\mu\).  Fix

\[
                  0\ne\eta\in
                  L_e:=\operatorname {Ann}(\operatorname {im}P_e).
\]

For every other nonzero site \(k\), beta parity gives
\(\beta_e+\beta_k\ne0\), and hence

\[
 \eta^{\mathsf T}P_e=0,\qquad
 \eta^{\mathsf T}q_{ek}
 ={1\over\beta_e+\beta_k}
       \eta^{\mathsf T}P_eHP_k^{\mathsf T}=0.                     \tag{3}
\]

Contract \({\cal D}_0(x,z)\) at \(e\) by \(\eta\).  A marked factor at
\(e\) is killed by (3), as is every internal edge from \(e\) to the
nonzero shore.  The only possible surviving edge pairs \(e\) with
\(z_0\).  The complete direct-plus-marked common power therefore factors
exactly:

\[
  \eta\!\mathbin{\lrcorner}{\cal D}_0(x,z)
   =q_{e z_0}^{\mathsf T}\eta
        \otimes{\cal C}_{N\setminus\{a,b,e\}}(x,z)=0.              \tag{4}
\]

Here \({\cal C}\) is the residual expression from the
zero-shore Hall--Schmidt factorization.  Formula (4) retains the direct
term: removing the edge \(e z_0\) lowers the power of \(q\) by one in
both its marked and direct summands, giving exactly the two powers in
\({\cal C}\).

## 3. The cofactor is a nonzero pure cap

Suppose first that \(e\) misses \(c\in\{0,1\}\).  Both type-\(22\)
centres have image \(\mathbb C e_2\), so the three-centre set

\[
                              T=\{a,b,e\}
\]

misses the target axis \(c\).  The capacity lemma prohibits \(e\) from
missing both \(0\) and \(1\).  Hence \(T\) covers exactly two target
axes: \(e_2\) and the other binary axis.

Apply the equality case of the Hall--Schmidt factorization to \(T\).
Since there are exactly three zero sites, its residual factor is the same
one appearing in (4), and the pure-cap conclusion gives

\[
 {\cal C}_{N\setminus\{a,b,e\}}(x,z)
   =\rho\,{x_cz_c\over d_c}X_{c,N\setminus\{a,b,e\}},
 \qquad \rho\ne0.                                                  \tag{5}
\]

The second tensor factor in (4) is therefore nonzero.  It follows for
every \(\eta\in L_e\) that

\[
                         q_{e z_0}^{\mathsf T}\eta=0.              \tag{6}
\]

Equivalently,

\[
       \operatorname {im}q_{e z_0}
          \subseteq L_e^\perp=\operatorname {im}P_e,
\]

which proves (1) because \(P_e\) is singular.

The allowed nonempty missed sets are

\[
       \{0\},\ \{1\},\ \{2\},\ \{0,2\},\ \{1,2\}.
\]

All but \(\{2\}\) meet \(\{0,1\}\) and hence satisfy (1).  If
\(M_e=\{2\}\), then \(P_e\) is singular while its image contains the two
independent vectors \(e_0,e_1\), proving (2).  Pairwise disjointness of
the missed sets permits at most one such site.

## 4. Exact audit

[verify_live_three_zero_extra_singular_shared_star.py](../computations/verify_live_three_zero_extra_singular_shared_star.py)
enumerates all admissible extra missed-axis families, verifies that every
family has at most one unresolved \(\{2\}\) member, and checks that every
other member makes \(\{a,b,e\}\) an exact two-axis cover.  The tensor
factorization (4) and nonvanishing (5) are the proof; the finite program
only audits the incidence boundary.
