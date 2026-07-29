# Independent audit of the sole-extra-plane reductions

This note records an adversarial audit of the three all-order reductions

- `live-three-zero-extra-plane-common-beta-all-orders.md`,
- `live-three-zero-extra-plane-minority-exceptional.md`, and
- `live-three-zero-extra-plane-two-marked-transverse.md`.

No counterexample or coefficient defect was found.  The audit was done from
the complete marked-pair response, independently of the prose counts, and
then compared with all three checkers.

## Balance and coefficient checks

Write \(\kappa=1/2\).  In the common-beta argument, the two binary subset
families give exactly

\[
 K_r((r+2)p_1+rp_2),\qquad L_r(p_1+p_2),
\]

where

\[
 K_r=(r+1)r!\kappa^r,\qquad L_r=(r+2)K_r.
\]

The first coefficient splits into marked-pair contributions
\(rK_r(p_1+p_2)\) and \(2K_rp_1\).  The second family has only two
ordinary marked zeros.  The extra-star and coordinate-plane singleton
coefficients are \(L_r\); the two centre alternatives are
\(L_r(p_1+p_2)\) and
\(r(r+1)r!\kappa^r p_2\); and the live pair-sum coefficient is
\(2r!\kappa^r p_2=r!p_2/2^{r-1}\).  Direct recounting of labelled
bijections gives every displayed factorial and power of two.

For \(t\) minority exceptional sites, placing all exceptional sites on one
shore replaces the common matching factor by

\[
 \Lambda\kappa^{r-t},\qquad
 \Lambda=\prod_{j\in E}(1+\nu_j)^{-1}.
\]

Whether the extra row pairs with a common or exceptional zero, the same
monomial results.  Thus the coefficients in the note are exactly
\(K_{r,t},L_{r,t},M_{r,t}\), and the pair-sum coefficient is
\(2r!\Lambda\kappa^{r-t}p_2\).  Structural admissibility makes every
denominator actually used here nonzero; repeated exceptional values do
not introduce an exceptional--exceptional matching edge.

For two marked exceptional sites, source \(22\) forces that marked pair
when \(p_2=0\).  After removing the pair and a supported star, there are
\(r\) zeros, \(r-1\) ones, and the extra row, so the extra row is forced
onto a zero.  Summing its \(r\) choices and the remaining \((r-1)!\)
bijections gives

\[
 C_{r,t,B}=2r!\left(\prod_{j\in E\setminus B}(1+\nu_j)^{-1}\right)
                  \kappa^{r-t+2}.
\]

The binary, extra, centre, and common-live coefficients are respectively
\(C_{r,t,B}p_1\) (or \(C_{r,t,B}p_0\) after swapping),
\(C_{r,t,B}\), \(C_{r,t,B}p_1\), and
\(C_{r,t,B}p_1\).  Allowing an arbitrary contraction in the extra-star
row causes no contamination: the extra site is the star and therefore
cannot enter the marked pair; all other star variables have already been
killed.

## Subset ranks and endpoint checks

For the incidence matrix \(W_{n,k}\) of all \(k\)-subsets against points,

\[
 W_{n,k}^{\mathsf T}W_{n,k}
  ={n-2\choose k-1}I+{n-2\choose k-2}J.
\]

Its eigenvalues on the sum-zero subspace and the constant line are nonzero for
\(1\le k\le n-1\), so it has full column rank in characteristic zero.
The relevant sizes satisfy:

- common beta: \(k=r+1,r+3\) in \(n=2r+2\), with the second proper
  exactly for \(r\ge2\);
- minority exceptional: \(k=r+1-t,r+3\) in \(n=2r+2-t\), with the
  second proper exactly for \(t\le r-2\);
- two marked: \(k=r+3-t\) in \(n=2r+2-t\), where \(k\ge1\) is exactly
  \(t\le r+2\) and \(n-k=r-1\ge1\).

The two coefficient functionals in each binary row have determinant
\(2\), so no two-plane can annihilate both.  The intersection argument
used for the centre row is also nondegenerate: a nonzero
\(p\in R\cap\{p_0=0\}\) with \(p_1+p_2=0\) necessarily has
\(p_2\ne0\).

## Computational stress cases and conclusion

All three shipped checkers pass.  In addition to their recorded cases,
exact symbolic runs pass at common \(r=5\), minority \((r,t)=(5,1)\),
and transverse \((2,3),(3,2),(3,4)\).  Exact rational-beta runs with
symbolic \(p\) also pass at transverse \((4,2),(4,4),(4,6)\).

The contraction at the extra site ranges over its full two-dimensional
row plane, the coordinate-plane normalization uses only an invertible
output change, and all graph conclusions distinguish literal zero blocks
from the merely singular removed ports.  After adjoining the structurally
zero exceptional blocks, every possible rank-three edge at the shared zero
is therefore excluded as claimed.

The checkers are correct but not maximally redundant: some colour-swapped
off-support zeros are invoked by symmetry, and later off-star terms are
discarded using variables already proved zero rather than asserted again.
These are coverage choices, not gaps in the three arguments.
