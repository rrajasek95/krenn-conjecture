# R2 singular-star budget and closure of the four-invertible stratum

Research evidence only. Krenn's conjecture remains open,
**SP-CLEAN-BRIDGE** is untouched, and no certified dependency changes.

## 1. Outcome

For a selected level-two block, write

\[
 P_r=(A_{pr}[c,a],A_{pr}[c,b]),\qquad
 Q_r=(A_{qr}[c,a],A_{qr}[c,b]),\qquad
 X_r=[P_r\ Q_r],
\]

and let \(M\) be the binary residual packet on the six vertices \(R\).
Two classification-free consequences now hold.

> **R2 singular-star budget.** Let \(S\) be the graph of singular internal
> blocks \(M_{rx}\), and put
> \[
>              s_r=\mathbf 1_{P_r\ne0}+\mathbf 1_{Q_r\ne0}.
> \]
> In every full solution,
> \[
>                    \deg_S(r)\ge s_r,\qquad
>                    \sum_r s_r\le2|S|.               \tag{1}
> \]

> **Four-invertible closure.** On the generic-kernel branch
> \[
> X_rJX_x^{\mathsf T}=(\nu_r+\nu_x)M_{rx},            \tag{2}
> \]
> if four of the six \(X_r\) are invertible, then
> \[
>                         \operatorname{rank}d\Psi_M\le54.           \tag{3}
> \]
> Hence a rank-\(55\) block satisfying (2) has at most three invertible
> endpoint matrices.

The earlier pair-pencil theorem proved (3) when the two exceptional \(X\)'s
were zero. The result here allows them to be arbitrary singular \(2\times2\)
matrices. Its new ingredient is a sharp constant-spoke theorem:

\[
                         \operatorname{rank}d\Psi_M\le50.            \tag{4}
\]

## 2. Proof of the rootwise budget

Apply R2 at a residual root \(r\) to the pair \(a,b\). If \(s_r>0\),
preservation fails because at least one endpoint edge has a nonzero entry in
the outside output column \(c\). R2 must therefore supply two distinct
pure-column witnesses, one for \(a\) and one for \(b\).

Every endpoint edge whose selected star is nonzero is disqualified by that
outside \(c\)-column. Thus at most \(2-s_r\) of the two endpoint edges can be
witnesses, and at least \(s_r\) witnesses must be internal. An internal
pure-column block has rank one and is singular, proving
\(\deg_S(r)\ge s_r\). Summing the degrees gives (1).

In particular:

* one nonzero endpoint star forces a singular internal neighbor;
* two nonzero endpoint stars force two distinct singular internal
  neighbors; and
* an invertible \(X_r\) has \(s_r=2\), so its singular degree is at least
  two.

The last statement retains rank-one \(X_r\); it is not a census only of
invertible and zero matrices.

## 3. A pure spoke fixes the neighbor's coordinate row

Suppose \(X_i\) is invertible and an internal witness has the form

\[
                         M_{ij}=u\,e_t^{\mathsf T}\ne0.               \tag{5}
\]

Equation (2) gives

\[
 X_iJX_j^{\mathsf T}
   =(\nu_i+\nu_j)u\,e_t^{\mathsf T}.                 \tag{6}
\]

If \(\nu_i+\nu_j=0\), invertibility of \(X_iJ\) forces \(X_j=0\). Otherwise
multiply (6) on the left by \((X_iJ)^{-1}\). The transpose \(X_j^{\mathsf T}\)
has only column \(t\) nonzero, so

\[
                         X_j=e_t\ell^{\mathsf T}                    \tag{7}
\]

for some row \(\ell^{\mathsf T}\). Thus a nonzero singular neighbor of an
invertible root is confined to the coordinate row named by the pure witness.
This is the missing rank-one refinement of the older live/dead argument.

An edge joining two invertible \(X\)'s cannot be pure: its left side in (2)
is invertible, whereas the right side is either zero or singular. Therefore
the two pure witnesses required at an invertible root must go to
noninvertible \(X\)-vertices.

## 4. Four invertible vertices reduce to two spoke patterns

Let \(0,1,2,3\) be the invertible vertices and \(4,5\) the two singular
ones. At every live root \(i\), R2 forces the two exceptional vertices to be
the two distinct pure witnesses. After naming the outputs \(0,1\), there is
an assignment \(\sigma\in\{0,1\}^4\) such that

\[
 M_{i4}=u_i e_{\sigma_i}^{\mathsf T},\qquad
 M_{i5}=v_i e_{1-\sigma_i}^{\mathsf T},\qquad u_i,v_i\ne0.          \tag{8}
\]

If \(\sigma\) is nonconstant, (7) forces \(X_4=0\): a nonzero \(X_4\)
cannot be supported in both coordinate rows. The complementary assignment
similarly forces \(X_5=0\). The calculation in the earlier pair-pencil note
then gives \(M_{45}=0\), and its rank-drop theorem gives
\(\operatorname{rank}d\Psi_M\le54\) (at most \(53\) in the balanced case).

It remains only to treat constant \(\sigma\). Swapping the binary colours if
necessary, assume

\[
                         M_{i4}=u_i e_0^{\mathsf T},\qquad
                         M_{i5}=v_i e_1^{\mathsf T}.                 \tag{9}
\]

The live-live blocks and \(M_{45}\) remain completely arbitrary. Section 5
proves the stronger bound (4) for every packet of this form.

## 5. Constant-spoke differential factorization

Index the 64 output rows of \(\Psi(M)\) by their colours at vertices \(4,5\),
giving four 16-row slices \(T_{00},T_{01},T_{10},T_{11}\). Let \(H\) be the
four-site binary matching tensor on vertices \(0,1,2,3\), let

\[
                         U=\operatorname{im}dH\subseteq\mathbb C^{16},
\]

and write \(g_{rs}=M_{45}[r,s]\).

Discard \(T_{01}\) temporarily. On the other three slices:

1. a live-live variation contributes
   \[
        (g_{00},g_{10},g_{11})\otimes u,\qquad u\in U;
   \]
2. the three corresponding cells of \(M_{45}\) contribute independent
   slice copies of \(H\);
3. the eight variations on the \(i4\) spokes with output \(1\) contribute
   only to \(T_{11}\); and
4. the eight variations on the \(i5\) spokes with output \(0\) contribute
   only to \(T_{00}\).

Euler's identity for the quadratic four-site tensor is

\[
                              dH_A(A)=2H,             \tag{10}
\]

so \(H\in U\). The first two families above therefore span at most

\[
                              \dim U+2\le18           \tag{11}
\]

dimensions in the three outer slices. This remains true if the displayed
three-vector \(g\) vanishes: then only the three copies of \(H\) remain.
Adding the two eight-column spoke families gives outer-slice rank at most

\[
                              18+8+8=34.              \tag{12}
\]

Every variation not yet counted is supported in \(T_{01}\), whose dimension
is \(16\). Hence

\[
                              \operatorname{rank}d\Psi_M\le34+16=50,
\]

proving (4), and with it the four-invertible closure.

## 6. Exact audit and sharpness

[verify_level_two_constant_spoke_rank_bound.py](../computations/verify_level_two_constant_spoke_rank_bound.py)
uses formal monomials for all 24 live-live cells, sixteen spoke coordinates,
and four arbitrary \(M_{45}\) cells. It verifies 624 matching identities:

* live-live cofactors factor as \(g_{rs}\) times the four-site cofactor on
  every slice except \(01\);
* the two forbidden spoke halves have exactly the claimed slice support;
* the \(M_{45}\) cofactor is exactly \(H\); and
* the four-site Euler identity (10) holds coefficientwise.

A deterministic integral specialization has rank exactly \(50\) modulo both
\(101\) and \(1{,}000{,}003\), so (4) is sharp. The checker is
standard-library only and passes normal, optimized, and isolated Python.

## 7. Revised frontier

On the rank-\(55\) generic-kernel branch, the number of invertible \(X_r\) is
now at most three. More generally, (1) turns every nonzero endpoint-star
column into singular-block incidence. The remaining two-sided target is
therefore the at-most-three-invertible stratum with rank-one coordinate-row
neighbors and its overlapping value equations; the four-live and fully
invertible residual patterns are closed.
