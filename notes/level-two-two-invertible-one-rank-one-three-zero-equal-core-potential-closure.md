# Equal core potentials close a \(2I+1R+3Z\) subcase

Research evidence only. Krenn's conjecture remains open,
**SP-CLEAN-BRIDGE** is untouched, and no certified dependency changes.

## Outcome

Let a binary six-site packet satisfy the generic-kernel equations

\[
                 X_uJX_v^{\mathsf T}=(\nu_u+\nu_v)M_{uv},
 \qquad J=\begin{pmatrix}0&1\\1&0\end{pmatrix},                 \tag{1}
\]

and residual R2. Suppose the endpoint ranks are

\[
                              (2,2,1,0,0,0).                     \tag{2}
\]

Call the invertible sites \(0,1\), the nonzero rank-one site \(r=2\),
and the zero sites \(Z=\{3,4,5\}\). If

\[
                              \nu_0=\nu_1=\nu_r,                \tag{3}
\]

then

\[
                              \operatorname{rank}d\Psi_M\le51. \tag{4}
\]

Thus this equal-core-potential subcase misses rank 55. The proof uses only
the generic-kernel equation, R2 at the two invertible roots, and exact
cofactor support. It invokes no L0 or L1 equation.

The complementary branch with distinct invertible-site potentials is now
closed by the
[distinct-potential theorem](level-two-two-invertible-one-rank-one-three-zero-distinct-invertible-potential-closure.md),
which gives rank at most 48.  The only multiplier boundary left between the
two results is \(\nu_0=\nu_1\ne\nu_r\).

## The core and the R2 consequence

Write the common potential in (3) as \(\lambda\). The numerators on the
three core edges \(01,0r,1r\) are nonzero; the first is invertible and the
other two have rank one. Hence

\[
                              2\lambda\ne0.                      \tag{5}
\]

In particular \(\lambda\ne0\), \(M_{01}\) is invertible, and both
invertible-to-rank-one blocks are nonzero. Write

\[
                              X_r=ab^{\mathsf T}.                 \tag{6}
\]

Then

\[
 X_iJX_r^{\mathsf T}=(X_iJb)a^{\mathsf T}\qquad(i=0,1).        \tag{7}
\]

A local change of basis at \(r\) sends \(a\) to \(e_0\), so both
blocks \(M_{ir}\) are supported in the same shore column. This change is
used only for the rank calculation and preserves differential rank.

At either invertible root, R2 requires two distinct internal pure-column
witness labels. The edge \(01\) cannot be one because its block is
invertible. If every invertible-to-zero block vanished, the single edge to
\(r\) would be the only remaining internal candidate and could not supply
two distinct witness labels. Therefore

\[
 A=\{z\in Z:\nu_z=-\lambda\}\ne\varnothing.                    \tag{8}
\]

Indeed, an edge from an invertible endpoint to a zero endpoint can be
nonzero in (1) only at this zero multiplier sum.

## Exactly seven support envelopes

Every edge touching a zero endpoint has zero numerator in (1). Its entire
binary block is therefore arbitrary precisely when its endpoint potentials
sum to zero, and otherwise it vanishes. Put \(C=Z\setminus A\). The support
is consequently determined by these elementary rules:

* the three core edges \(01,0r,1r\) are live, with the common fixed shore
  factor on the last two;
* every core-to-\(A\) block is arbitrary;
* every edge internal to \(A\) vanishes, since its multiplier sum is
  \(-2\lambda\ne0\);
* a vertex \(c\in C\) joins every member of \(A\) exactly when
  \(\nu_c=\lambda\);
* an edge \(cd\subset C\) is live exactly when \(\nu_c+\nu_d=0\).

The last two exceptions cannot coexist: if \(\nu_c=\lambda\) and
\(\nu_c+\nu_d=0\), then \(\nu_d=-\lambda\), so \(d\in A\), contrary
to \(d\in C\).

There is one envelope for \(|A|=3\). For \(|A|=2\), the remaining zero
site is isolated or has potential \(\lambda\) and joins both members of
\(A\). For \(|A|=1\), neither, one, or both complementary vertices may
join \(A\), or their mutual edge may be live. Thus the total census is

\[
                              1+2+4=7.                            \tag{9}
\]

## Cofactor-column bounds

A cell column of \(d\Psi_M\) obtained by varying an edge \(e\) vanishes
unless the support on the four complementary vertices admits a perfect
matching with the required local colours. Exhausting the fifteen edge
choices and sixteen complementary words gives the exact support counts

\[
\begin{array}{c|c|c|c}
|A|&\text{complement pattern}&\text{potentially active cell columns}
     &\text{rank bound}\\ \hline
3&-&48&48\\
2&\text{isolated}&20&20\\
2&\text{joined}&56&51\\
1&\text{no join}&4&4\\
1&\text{one join}&16&16\\
1&\text{two joins}&28&28\\
1&\text{complement edge}&28&28.
\end{array}                                                       \tag{10}
\]

Only the joined \(|A|=2\) envelope needs more than the direct count. Name
the two members of \(A\) by \(a_0,a_1\), and the remaining zero vertex by
\(c\), whose potential is \(\lambda\). Every one of the four cell columns
on edge \(a_0a_1\) is identically zero: after varying that edge, its
complement is the three-site core together with \(c\), and \(c\) has no
live edge to the core.

These four coordinate directions are independent of the five usual vertex
gauges

\[
                         \dot M_{uv}=(\mu_u+\mu_v)M_{uv},
                         \qquad\sum_u\mu_u=0.                    \tag{11}
\]

The base block on \(a_0a_1\) vanishes, so every gauge has zero coordinates
there. On the dense support-open set, the live graph is connected and
contains the core triangle, making the five gauges independent. Therefore

\[
                              \dim\ker d\Psi_M\ge4+5=9,          \tag{12}
\]

and the rank is at most \(60-9=51\). Polynomiality extends this bound from
the dense support-open set to its closure. All other rows of (10) are at
most 48 by their active-column counts, proving (4).

## Exact audit

The standard-library checker
[verify_level_two_two_invertible_one_rank_one_three_zero_equal_core_potential_closure.py](../computations/verify_level_two_two_invertible_one_rank_one_three_zero_equal_core_potential_closure.py)
verifies the R2 necessity, all seven potential representatives and support
envelopes, every complementary perfect matching and local-colour cofactor,
the four zero columns in the exceptional 56-column envelope, and the gauge
independence graph. It also records exact calibration ranks

\[
                              44,20,45,4,14,23,19
\]

over two prime fields. It passes normal, optimized, and isolated Python.
