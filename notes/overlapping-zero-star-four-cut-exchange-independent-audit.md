# Independent audit of the overlapping zero-star four-cut exchange

## Verdict

The four-cut identity and exchange statement in
[overlapping-zero-star-four-cut-exchange.md](overlapping-zero-star-four-cut-exchange.md)
are correct.  The two 27-row tensor packets obtained from
\(\{p,q,i\}\) and \(\{p,q,j\}\) are two coefficient gradings of the
same 81 four-colour rows.  They must not be counted as independent
constraints.

The row-and-column cap obtained from a common isotropic pair is also
correct, as is the repeated-pair \(K_4\) boundary model.  That model
satisfies only the five selected cap rows; it leaves the uncontracted
\((a,b)\) directions unspecified and is not a countermodel to the
complete 81-row system.

## Clean-room matching derivation

Let \(D=B\setminus\{p,q,i,j\}\), let \(z\) be the internal quadratic on
\(D\), and assume

\[
 A_{pi}=A_{qi}=A_{pj}=A_{qj}=0.                         \tag{1}
\]

After fixing colours \(a,b,c,d\) at \(p,q,i,j\), respectively, every
perfect matching belongs to exactly one of four classes.

1. It uses both \(pq\) and \(ij\), contributing
   \(a_{ab}u_{cd}z^{[m-2]}\).
2. It uses \(pq\), while \(i,j\) cross separately into \(D\), contributing
   \(a_{ab}t_cv_dz^{[m-3]}\).
3. It uses \(ij\), while \(p,q\) cross separately into \(D\), contributing
   \(u_{cd}x_ay_bz^{[m-3]}\).
4. All four named sites cross into \(D\), contributing
   \(x_ay_bt_cv_dz^{[m-4]}\).

The two other pairings of the four named sites, and every mixed layer
containing one of them, vanish because of (1).  Hence the exact
coefficient is

\[
\begin{aligned}
 &a_{ab}u_{cd}z^{[m-2]}
 +a_{ab}t_cv_dz^{[m-3]}
 +u_{cd}x_ay_bz^{[m-3]}\\
 &\hspace{35mm}+x_ay_bt_cv_dz^{[m-4]}.
                                                               \tag{2}
\end{aligned}
\]

The target coefficient is
\(\delta_{a=b=c=d}X_a^D\), proving the displayed 81-row identity in the
primary note.  Divided powers give coefficient one in every layer:
they enumerate unordered residual matchings, so no hidden factorial or
binomial coefficient occurs.

At the first order \(2m=8\), the compatible perfect matchings split as

\[
 3\quad+\quad12\quad+\quad12\quad+\quad24=51.
\]

The terms are respectively the direct-direct, \(pq\)-direct,
\(ij\)-direct, and four-star layers.  This gives a small
coefficient-free audit that the four classes are exhaustive and disjoint.

## Why the two packets are regradings

For the triple \(\{p,q,i\}\), the remaining named site is \(j\).  Its
internal quadratic and the \(i\)-star are

\[
 z_i=z+\sum_de_d^{(j)}v_d,\qquad
 \tau_c=t_c+\sum_du_{cd}e_d^{(j)}.                     \tag{3}
\]

Square-freeness at site \(j\) gives, for every \(r\),

\[
 \iota_{j,d}\bigl(\tau_cz_i^{[r]}\bigr)
   =u_{cd}z^{[r]}+t_cv_dz^{[r-1]}.                     \tag{4}
\]

Applying (4) to the direct term and the three-star term of the
27-equation triple packet produces (2) row by row.

For the triple \(\{p,q,j\}\), the same calculation uses

\[
 z_j=z+\sum_ce_c^{(i)}t_c,\qquad
 \upsilon_d=v_d+\sum_cu_{cd}e_c^{(i)},                 \tag{5}
\]

and extraction at colour \(c\) of site \(i\) again produces (2).
Equivalently, contractions at the distinct sites \(i,j\) commute.
The target indicators agree because

\[
 \delta_{a=b=c}\delta_{d=a}
 =\delta_{a=b=d}\delta_{c=a}
 =\delta_{a=b=c=d}.                                    \tag{6}
\]

Thus each 27-row packet, whose rows are tensors on an odd complement,
contains the same 81 four-colour tensor rows after resolving the remaining
named site.  More globally, each packet contains

\[
 27\cdot3^{\,|D|+1}=3^{2m}
\]

scalar top coefficients, exactly the complete residual tensor.  Adding
the equation counts or ranks of the two packets would double-count the
same coefficients.

The four literal zeros in (1) are essential to this presentation.  If
one is removed, additional named-pairing layers enter, and the reduced
formula (2) is no longer the complete four-cut expansion.

## Isotropic contraction

Choose nonzero \(\xi,\eta\) with common support \(H\) and
\(\xi^TA_{pq}\eta=0\), and set

\[
 P=\sum_a\xi_ax_a,\qquad S=\sum_b\eta_by_b,\qquad
 \kappa_h=(\xi_h\eta_h)^{-1}.
\]

Multiply (2) by \(\kappa_h\xi_a\eta_b\), sum over \(a,b\), and first fix
\(c=h\).  Both terms containing \(a_{ab}\) vanish by the displayed
bilinear equation; the other two give

\[
 \kappa_hPS\bigl(u_{hd}z^{[m-3]}+t_hv_dz^{[m-4]}\bigr)
   =\delta_{hd}X_h^D.
\]

Fixing \(d=h\) gives the analogous column identity.  These are five rows,
not six, because their diagonal is shared.  They are only five linear
combinations of the 81 rows and discard the complement of
\(\mathbb C(\xi\eta^T)\) in the \((a,b)\)-index space.

## Repeated-pair boundary

On sites \(0,1,2,3\), let \(z\) be the six edges of \(K_4\), with its
three one-factors coloured \(0,1,2\).  The only disjoint edge pairs are
the members of those one-factors, so exactly

\[
 z^{[2]}=e_0^{\otimes4}+e_1^{\otimes4}+e_2^{\otimes4},
 \qquad z^{[3]}=0.                                     \tag{7}
\]

Put \(P=e_0^{(4)}\), \(S=e_0^{(5)}\),
\(t_0=e_0^{(0)}\), and \(v_0=e_0^{(1)}\), with all selected entries of
\(u\) zero and all other selected \(t,v\) rows zero.  The edge \(01\)
meets five of the six cells of \(z\); its only disjoint mate is the
colour-zero edge \(23\).  Therefore

\[
 t_0v_0z=e_0^{\otimes\{0,1,2,3\}},\qquad
 PSt_0v_0z=X_0^D.                                      \tag{8}
\]

This proves the selected diagonal cap, while the other four selected
row/column entries vanish literally.  Equation (7), however, still has
three pure lifts on the same missing pair \(45\).  The construction
therefore demonstrates exactly the claimed common-power boundary and
nothing stronger.

## Independent exact probes

In addition to the hand derivation, I expanded a fresh integer aggregate
family at eight sites using the repository's pre-existing generic
site-square-zero engine, without importing the new verifier.  I used
scattered named endpoints

\[
 (p,q,i,j)=(6,1,4,3),\qquad D=\{0,2,5,7\},
\]

set precisely the four blocks in (1) to zero, and left every other
endpoint-ordered \(3\)-by-\(3\) block as an arbitrary seeded integer
matrix.  All 81 direct contractions of the full fourth divided matching
power agreed with (2); all 81 rows were nonzero in this specialization,
so the check was not vacuous and exercised both storage orientations.

An independent combinatorial replay gave the layer ledger
\((3,12,12,24)\), checked all 81 target-index equalities in (6), and
reconstructed (7)--(8) over the integers.  No flaw or missing coefficient
was found.  The exact remaining gate is therefore the one stated in the
primary note: use uncontracted \((a,b)\) directions of the full 81-row
system to rule out extension of the repeated-pair filter.

