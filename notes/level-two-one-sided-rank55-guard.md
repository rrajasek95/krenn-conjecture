# A selected level-two block has a one-sided rank-55 family

Research evidence only. Krenn's conjecture remains open,
**SP-CLEAN-BRIDGE** is untouched, and no certified dependency changes.

## 1. Outcome

The selected-block guard recorded in the August 1 checkpoint is not confined
to the point $P=Q=z=0$. It extends to an entire one-sided linear family on which

\[
                         Q=0,\qquad z=0,                 \tag{1}
\]

while $P$ and the internal binary system $M$ are arbitrary. In particular,
there are exact points on this family with every $P_x\ne0$,
$\operatorname{rank}X_x=1$ at all six residual vertices, and

\[
                         \operatorname{rank}d\Psi_M=55.  \tag{2}
\]

The same example has an everywhere-live slope $\Psi(M)$, distinct active
pure-column pair-pencil witnesses at every residual vertex, and a support
completion whose full eight-vertex live graph is $K_8$. Thus neither maximal
binary differential rank, the local R2 consequence used in the preceding
rank-drop theorem, nor the no-independent-four-set support theorem forces a
selected block to be two-sided.

This is a guard, not a counterexample, and “family” does not assert that the
displayed linear subspace is a maximal irreducible component. The support
completion is required to
preserve only the selected 64 equations, and is not claimed to solve the other
6,497 equations. Its role is to narrow the next proof target: a further
single-block rank-pattern classification cannot eliminate this family.
One must use an overlapping block or an L0/L1 value equation which sees the
missing endpoint star.

## 2. Why the family is exact

For rare colour $c$ at endpoints $p,q$, write the complementary colours as
$a,b$, and put

\[
 P_x=\binom{A_{px}[c,a]}{A_{px}[c,b]},\qquad
 Q_x=\binom{A_{qx}[c,a]}{A_{qx}[c,b]},\qquad
 N_{xy}=P_xQ_y^{\mathsf T}+Q_xP_y^{\mathsf T}.
\]

The exact selected-block equation is

\[
       z\Psi(M)+d\Psi_M(N)=0.                            \tag{3}
\]

Both terms in (3) vanish under (1), identically in $M$ and $P$. Hence the
block variety contains the linear family

\[
 \{(M,P,Q,z):Q=0, z=0\}\cong\mathbb A^{60+12}.          \tag{4}
\]

The endpoint-transposed family $P=0,z=0$ is identical. This is stronger than
the old zero-star point in two ways: it retains twelve arbitrary star
coordinates, and for generic nonzero $P_x$ the six matrices
$X_x=[P_x\ Q_x]$ have rank one rather than zero.

The family is not an artifact of a dead slope. The exact witness below has
all 64 entries of $\Psi(M)$ nonzero.

## 3. An integral maximal-rank witness

On residual vertices $0,\ldots,5$, put pure $E_{00}$-blocks on

\[
                    01\mid23\mid45
\]

and pure $E_{11}$-blocks on

\[
                    02\mid14\mid35.                     \tag{5}
\]

Their nonzero scalars and all four entries on the other nine edges are the
small positive integers defined in the checker. At every residual root, the
two incident edges in (5) are distinct pure-column witnesses for $0$ and
$1$. Their complementary four-site tensors are nonzero. Thus the precise R2
exit used in the four-invertible/two-dead argument is already present.

For this $M$, the $64\times60$ integer matrix of $d\Psi_M$ has rank $55$.
The proof is exact and two-sided:

1. the five trace-zero vertex scalings
   $K_{xy}=(\mu_x+\mu_y)M_{xy}$, $\sum_x\mu_x=0$, are independent integral
   kernel vectors, so the rational rank is at most $55$;
2. row reduction modulo $101$ gives rank $55$, exhibiting a $55\times55$
   integer minor nonzero modulo $101$, so the rational rank is at least
   $55$.

Choose, for example,

\[
                         P_x=(x+1,x+2)^{\mathsf T},qquad Q_x=0,qquad z=0.
                                                                  \tag{6}
\]

Every $X_x$ then has rank one. The checker verifies (3) on all 64 binary
words and independently evaluates the literal eight-vertex matching sum with
the two rare endpoints. Both calculations give zero in every selected row.

Finally, cells invisible to this selected block can be placed on every edge
through the endpoints: they use the wrong endpoint or tail colour and hence do
not move any of the 64 values. Together with the complete residual support,
this makes the full live graph $K_8$. This last completion is only a support
guard; no equation outside the selected block is asserted.

## 4. Consequence for the continuation

The local rank-pattern target should be split before any further census:

* genuinely two-sided packets, where the pair-pencil Bianchi rank drop may
  still extend beyond the invertible/dead cases; and
* one-sided isotropic packets (4), which a selected block cannot see at all.

The second locus is already maximal-rank and pair-pencil compatible. Its first
possible obstruction must therefore contain data from a block with a different
rare endpoint pair or rare colour, or a lower-level value fixing one of the
otherwise invisible star rows. In particular, proving more support activity
inside the same block cannot remove (4).

The follow-up
[overlap-collapse theorem](level-two-one-sided-overlap-collapse.md) supplies
exactly that first obstruction. On the cofactor-open rank-$55$ locus, the L1
rows kill the remaining direct column and the three-/four-$c$ value rows
force $P=0$. The integral witness (5)--(6) satisfies every open hypothesis,
so it cannot extend to a full solution with its nonzero star. This does not
invalidate the selected-block guard proved here; it sharpens the global
frontier from the one-sided family to the older $P=Q=z=0$ packet and to the
boundary strata where an open hypothesis fails.

The next follow-up,
[the zero-star four-$c$ obstruction](level-two-zero-star-four-c-obstruction.md),
closes the cofactor-open zero-star specialization as well. Together the two
follow-ups show that the full equations exclude this witness and the entire
one-sided rank-$55$ locus with connected nonbipartite deletion graphs. The
selected-block family remains an exact warning about what one block alone can
see, but it is no longer a generic global guard.

## 5. Audit

[`verify_level_two_one_sided_rank55_guard.py`](../computations/verify_level_two_one_sided_rank55_guard.py)
is standard-library only and checks:

* the cofactor matrix against all 60 literal finite differences;
* the five independent gauge kernels and exact rank $55$;
* all 64 nonzero slope coordinates;
* the twelve distinct active pure-column witnesses;
* all 64 differential equations and all 64 literal eight-site equations; and
* preservation of those equations after completing the live support to all
  $28$ edges.

Every check raises explicitly and remains live under normal, optimized, and
isolated Python.
