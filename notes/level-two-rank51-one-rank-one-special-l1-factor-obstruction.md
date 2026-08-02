# The exceptional one-rank-one L1 incidence does not factor

Research evidence only. Krenn's conjecture remains open,
**SP-CLEAN-BRIDGE** is untouched, and no certified dependency changes.

## Outcome

Use the shared gauge-coupled residual packet of differential rank \(51/49\)
and activate only root \(2\), with selected rank-one matrix

\[
                         X_2=e_1e_0^{\mathsf T}.             \tag{1}
\]

This is the unique direction found in the small primitive output-vector
search for which both pure targets pass the necessary L1 linear-incidence
test.  The two selected-column L1 systems have exact profiles

\[
\begin{array}{c|ccccc}
\text{column}&\operatorname{rank}&\operatorname{nullity}
 &\dim(\text{star modes})&\operatorname{rank}(\text{star modes})
 &\dim(\text{vacuous modes})\\ \hline
0&20&7&5&5&2\\
1&13&14&12&12&2.
\end{array}                                                   \tag{2}
\]

The sixty images of products between the two star-mode spaces span a
40-dimensional subspace.  The allowed direct \(\Psi(M)\) direction already
lies in that subspace, and adjoining either or both pure targets leaves the
rank equal to \(40\).  Thus linear incidence alone cannot exclude this
direction.

The actual factorization equations do exclude it.  Parameterize the two
left stars by \(24\) coordinates, the two right stars by \(10\) coordinates,
and weaken the direct term to four independent slice coefficients.  The
four literal 64-entry slice equations then give \(256\) bilinear
polynomials in \(38\) variables.  Their ideal is the unit ideal:

\[
          I=(1)\quad\text{over }\mathbb Q,
          \qquad
          I_{\mathrm{rev}}=(1)\quad\text{over }\mathbb F_{32003}. \tag{3}
\]

Consequently the fixed root-2 direction (1) has no shared L1 source on this
rank-51 residual packet, despite passing every necessary direct-plus-product
span test.  This closes that exceptional direction only; it is not a
component-wide theorem for the full \(1R+5Z\) endpoint-rank stratum.

## Exact audit

The standard-library checker
[verify_level_two_rank51_one_rank_one_special_l1_factor_obstruction.py](../computations/verify_level_two_rank51_one_rank_one_special_l1_factor_obstruction.py)
reconstructs the packet and selected equations, verifies the literal four
slices and both root-2 R2 cofactors, derives the two rational L1 nullspaces,
and checks all linear-incidence ranks.  It then emits the full factor ideal
and verifies reduced basis \(1\) with Singular over \(\mathbb Q\) and,
independently, with reversed variables and generators over
\(\mathbb F_{32003}\).  Hashes pin the equation ledger and both CAS
programs.  The checker passes normally, with -O, and with -I -S.
