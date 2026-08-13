# The coefficient-one debt is the first matching eigenspace

## Outcome

The \(0/-1\) residual isolated by the full-endpoint transfer is not a new
terminal sector. On each ordered-endpoint fibre it lies in the centered
edge-incidence eigenspace

\[
                 E_1\simeq [\,2h-2,2\,]                         \tag{1}
\]

of the perfect-matching two-switch graph. If \(A_h\) is the switch
adjacency, its eigenvalues on constants and \(E_1\) are

\[
 d_h=h(h-1),\qquad \lambda_h=h^2-3h+1.                         \tag{2}
\]

The second eigenvalue never vanishes for integral \(h\). Therefore

\[
        \Pi_h^{\rm match}={A_h-\lambda_hI\over 2h-1}            \tag{3}
\]

is the rational projection from \(1\oplus E_1\) onto the constant line,
and \(A_h-\lambda_hI\) is its integral numerator.

Applying (3) to the negative Gram row of the all-role endpoint transfer
kills every matching-dependent coefficient while preserving total mass.
The marked delta is retained rather than switched. After clearing the
denominator this gives a centered integral candidate with nonzero marked
coefficient.

This is progress, but not the full occurrence projector. Five distinct
ordered-endpoint fibre constants survive already at \(h=3\). Moreover,
\(A_h\) is presently a coefficient switch, not a source-valid augmented
Hasse cell. Its two-edge product-rule commutator is the next physical
obligation.

Checker:
[verify_uniform_centered_occurrence_matching_eigenspace_correction.py](../computations/verify_uniform_centered_occurrence_matching_eigenspace_correction.py).

## 1. The matching-incidence eigenspace

Fix \(2h\) residual vertices. For every residual edge \(e\), let

\[
                    \phi_e(R)=1_{e\in R}.                       \tag{4}
\]

A switch chooses two edges of \(R\) and replaces them by either of the
other pairings of their four vertices. Every matching has

\[
                    2{h\choose2}=h(h-1)                         \tag{5}
\]

neighbors. If \(e\in R\), then \(e\) survives precisely when the chosen
two edges do not include it, giving \((h-1)(h-2)\) neighbors containing
\(e\). If \(e\notin R\), the endpoints of \(e\) lie in two distinct
matching edges, and exactly one switch creates \(e\). Hence

\[
 A_h\phi_e=1+\big((h-1)(h-2)-1\big)\phi_e
            =1+\lambda_h\phi_e.                                \tag{6}
\]

An edge occurs in a proportion \(1/(2h-1)\) of all perfect matchings, so

\[
 A_h\left(\phi_e-{1\over2h-1}1\right)
 =\lambda_h\left(\phi_e-{1\over2h-1}1\right).                   \tag{7}
\]

The centered functions in (7) span \(E_1\), of dimension

\[
                         h(2h-3),                               \tag{8}
\]

the dimension of the irreducible \(S_{2h}\)-module \([2h-2,2]\). The
checker verifies the exact incidence rank and eigenidentity for
\(h=3,4,5\). Formula (6) proves it uniformly.

The eigenvalue \(\lambda_h\) cannot vanish for integral \(h\), because
\(h^2-3h+1\) has discriminant five. At \(h=3\), \(\lambda_3=1\).

## 2. The common-edge residual lies in \(1\oplus E_1\)

Let \(F\) be the residual matching of the marked occurrence and put

\[
                    t_F(R)=|F\cap R|=\sum_{e\in F}\phi_e(R).     \tag{9}
\]

Summing (6) over the \(h\) edges of \(F\) gives

\[
 A_ht_F=h1+\lambda_ht_F,\qquad
 (A_h-\lambda_hI)t_F=h1.                                      \tag{10}
\]

Thus the exact \(0/1\) split from the previous theorem is the \(E_1\)
component of \(t_F\). Formula (10) kills it integrally. Division by
\(2h-1\) only restores the constant normalization, since

\[
                         d_h-\lambda_h=2h-1.                    \tag{11}
\]

Equivalently, \(1-\lambda_h^{-1}A_h\) kills \(E_1\) rationally. The
integral numerator in (10) is preferable.

## 3. The matching-flat candidate

Recall the full all-role transfer

\[
 K_{f,h}=R_he_f-k_f,\qquad R_h=7hN_h,                           \tag{12}
\]

where \(k_f(g)=\sum_Tm_T(f)m_T(g)\). Fix the ordered endpoints \((p,s)\)
of \(g\). Let \(q_{p,s}\) be the number of marked residual edges avoiding
both endpoints. Direct chart counting gives

\[
                  k_f(g)=t_{F,p,s}(g)+C_{p,s},                  \tag{13}
\]

where \(t_{F,p,s}\) sums the \(q_{p,s}\) available marked-edge indicators,
and

\[
 C_{p,s}=\begin{cases}
 4h^2+4h,&(p,s)=(p_f,s_f),\\
 2h-1,&p=p_f\text{ or }s=s_f\text{, but not both},\\
 0,&\text{otherwise}.
 \end{cases}                                                   \tag{14}
\]

Equations (10)--(11) imply, fibrewise,

\[
 (A_h-\lambda_hI)k_f=q_{p,s}+(2h-1)C_{p,s},                    \tag{15}
\]

which is independent of the residual matching. Hence the rational
matching-flat centered candidate is

\[
              \widehat K_{f,h}=R_he_f-\Pi_h^{\rm match}k_f.     \tag{16}
\]

The delta coefficient \(R_h\) remains at \(f\); it is not spread to switch
neighbors. Since \(\Pi_h^{\rm match}\) preserves total mass, (16) has
augmentation zero. Its integral multiple is

\[
 K^{\mathbb Z,\rm match}_{f,h}
 =(2h-1)R_he_f-(A_h-\lambda_hI)k_f.                            \tag{17}
\]

The marked coefficient in (17) is

\[
 (2h-1)R_h-\big(h+(2h-1)(4h^2+4h)\big),                        \tag{18}
\]

which is positive for every \(h\ge3\). At \(h=3\), it is \(9207\). The
reversed-endpoint fibre which formerly contained \(0\) and \(-1\) becomes
uniformly \(-3\). Exact enumeration verifies that all residual matchings
in every ordered-endpoint fibre become constant.

## 4. The remaining endpoint debt

Equation (15) still depends on \((p,s)\). At \(h=3\) it assumes five
different values as the ordered endpoints move relative to the marked
endpoints and marked residual pairs. Consequently

\[
 K^{\mathbb Z,\rm match}_{f,h}
 \notin\operatorname {span}\{c_{f,h+1},1\}                     \tag{19}
\]

in general. The matching filter has reduced the full occurrence scheme to
the ordered two-point/marked-pair scheme; it has not solved that smaller
scheme. The next coefficient calculation should diagonalize endpoint
change operators on the remaining standard, symmetric-pair, and
alternating-pair sectors.

## 5. Product-rule faces

On a residual monomial, \(A_h\) performs

\[
 q_{ab}q_{cd}\longmapsto
 q_{ac}q_{bd}+q_{ad}q_{bc}.                                  \tag{20}
\]

The differential of the right side has four one-derivative terms. The
\(-\lambda_hI\) part retains the old-edge derivative faces. A source lift
of (17) must therefore contain the full two-edge Hasse/Spencer commutator,
not only the top matching switch.

Existing physical matching/Bianchi switches do not supply this lift. In
the pinned ridge/response module they are differences of already coupled
route columns and do not enlarge the physical image. Independently, the
pinned Reynolds audit exhibits nonzero Leibniz commutators on products.
Thus \(A_h\) is currently a coefficient operator, not a chain map on the
complete word/fine/repeated physical presentation.

There is a useful degree signal. Each switch face is quadratic in two edge
factors. Repeating corrected induction for \(h-3\) steps has the numerical
degree \(2h-6\) required of

\[
                \rho_{2h-6}\in\operatorname {Sym}^{2h-6}U.      \tag{21}
\]

This is evidence, not a construction. The two-edge face still needs a
common clean-line \(\operatorname {Sym}^2U\) typing, target/residue/physical
\(q\) protection, boundary independence, nonvanishing, and every common
Hankel equation before its iterated product can enter
\(\operatorname {Tr}_h\).

The exact next theorem is:

> Lift \(A_h-\lambda_hI\) to a source-valid augmented two-switch cell whose
> product-rule commutator is a boundary or an accepted physical terminal;
> then diagonalize and kill the remaining ordered-endpoint association
> classes without moving the marked delta.

## Scope

This theorem identifies and removes the first association-scheme residual
at coefficient level. It does not claim the matching-flat candidate is a
physical source row, a full centered projector, or a common-Hankel transfer.

Run:

~~~text
python3 computations/verify_uniform_centered_occurrence_matching_eigenspace_correction.py
python3 -O computations/verify_uniform_centered_occurrence_matching_eigenspace_correction.py
python3 -I -S computations/verify_uniform_centered_occurrence_matching_eigenspace_correction.py
~~~

Frozen ledger SHA-256:

~~~text
19fae004aa82be477cd91354387ad9e49473e481d7aefb764b5b709ee9607b97
~~~
