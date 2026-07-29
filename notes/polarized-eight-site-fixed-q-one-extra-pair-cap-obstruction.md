# Every invisible one-cell extension of the sparse quadratic still has no pair-cap preimage

## 1. Result and scope

Work in the eight-site ternary square-zero algebra.  Let

\[
\begin{aligned}
q={}&23_{00}+45_{00}+67_{00}
     +01_{11}+36_{11}+57_{11}\\
   &+02_{22}+14_{22}+56_{22},\\
z={}&01_{00}+24_{11}+37_{22}.
\end{aligned}                                                    \tag{1}
\]

Here \(ij_{cd}\) denotes the cell \(e_{i,c}e_{j,d}\); thus endpoint
colour order is retained even when \(c\ne d\).  The earlier exact
countermodel says

\[
                         zq^{[3]}=\Delta_{8,3}.                   \tag{2}
\]

There are exactly 99 basis cells \(e\notin\operatorname{supp}(q)\) for
which

\[
                              zeq^{[2]}=0.                        \tag{3}
\]

For every one of those cells, every \(t\in\mathbb C^\times\), every
\(a\in\mathbb C\), and all linear \(p,s\),

\[
 \boxed{\quad
 (a(q+te)+4ps)(q+te)^{[3]}\ne\Delta_{8,3}.
 \quad}                                                          \tag{4}
\]

The case \(t=0\) is exactly the previously proved fixed-nine-cell
obstruction.  Thus (4), together with that inherited case, covers the
entire affine line through \(q\) in each of the 99 directions.

This is still a sparse fixed-\(q\), one-extra-cell result.  It is not a
uniform theorem for arbitrary quadratics, does not compare two shared
pair-cap rows, does not provide the all-even descent, and does not prove
Krenn's conjecture.

The exact checker is
[`verify_polarized_eight_site_fixed_q_one_extra_pair_cap_obstruction.py`](../computations/verify_polarized_eight_site_fixed_q_one_extra_pair_cap_obstruction.py).

## 2. Independent 99/144 census

There are

\[
                    \binom82 3^2-9=252-9=243                  \tag{5}
\]

endpoint-colour cells outside the support of \(q\).  Since a single cell
squares to zero,

\[
 (q+te)^{[3]}=q^{[3]}+t e q^{[2]},\qquad
 (q+te)^{[4]}=q^{[4]}+t e q^{[3]}.                              \tag{6}
\]

Consequently

\[
 z(q+te)^{[3]}=\Delta_{8,3}+tzeq^{[2]}.                         \tag{7}
\]

The checker reconstructs (1) directly and multiplies in the square-zero
algebra.  Condition (3) holds for all nine ordered endpoint-colour cells
on each of precisely the following eleven physical pairs:

\[
       03,04,05,06,07,12,13,15,17,25,34.                        \tag{8}
\]

This gives \(11\cdot9=99\) invisible cells.  On every one of the other
144 cells, \(zeq^{[2]}\) consists entirely of non-target words of
coefficient one.  The exact support-size histogram is

\[
             135\text{ cells with one debt word},\qquad
               9\text{ cells with two debt words}.              \tag{9}
\]

Thus every cell outside the 99 already destroys the polarized identity
for \(t\ne0\), while all 99 cells in (8) preserve it literally.  This
census is obtained without using the earlier discovery checkers.

## 3. The 66 unchanged seven-coordinate cases

Put

\[
\begin{array}{lll}
A=(0,0),&B=(1,0),&C=(2,1),\\
D=(4,1),&E=(3,2),&F=(7,2),
\end{array}
\]

and write

\[
 R_{XY}=p_Xs_Y+s_Xp_Y
       =\beta(x_X,x_Y),\qquad x_X=(p_X,s_X),                    \tag{10}
\]

for the split nondegenerate form

\[
              \beta((r,u),(r',u'))=ru'+ur'.                    \tag{11}
\]

For 66 of the 99 invisible cells, neither perturbation term in (6)
changes any of the seven decisive top coordinates.  Hence the proposed
identity still forces, literally,

\[
\begin{gathered}
 R_{AB}=R_{CD}=R_{EF}=\frac14,\\
 R_{AF}=R_{BF}=R_{AC}=R_{CF}=0.                                 \tag{12}
\end{gathered}
\]

For completeness, the contradiction is short.  The nonzero pairing
\(R_{EF}\) makes \(x_F\ne0\).  The three vectors \(x_A,x_B,x_C\) are all
in the one-dimensional line \(x_F^\perp\).  Since \(R_{AB}\ne0\), that
line is nonisotropic; hence \(R_{AC}=0\) forces \(x_C=0\), contrary to
\(R_{CD}\ne0\).  The default checker replays this proportionality
closure exactly.  Its optional full Gröbner audit also reduces the seven
equations over \(\mathbb Q\) to the unit ideal.

## 4. Exact treatment of the remaining 33 cells

Label the seven coordinates in (12), in order, by

\[
                 0,1,2,AF,BF,AC,CF.                             \tag{13}
\]

The other 33 cells split into the following 14 exact signatures.  A
signature records exactly which of those seven coordinate forms changes.

| signature | count | cells \(ij_{cd}\) |
|---|---:|---|
| \(0\) | 7 | \(04_{00},05_{00},06_{00},07_{00},12_{00},13_{00},17_{00}\) |
| \(1\) | 2 | \(04_{11},34_{11}\) |
| \(2\) | 3 | \(03_{22},13_{22},34_{22}\) |
| \(AC\) | 5 | \(03_{01},05_{01},06_{01},07_{01},12_{21}\) |
| \(AF\) | 3 | \(05_{02},06_{02},07_{02}\) |
| \(BF\) | 3 | \(12_{02},13_{01},17_{02}\) |
| \(CF\) | 3 | \(07_{12},17_{12},25_{10}\) |
| \(0,AF\) | 1 | \(03_{00}\) |
| \(0,BF\) | 1 | \(15_{00}\) |
| \(1,AC\) | 1 | \(25_{11}\) |
| \(1,CF\) | 1 | \(12_{11}\) |
| \(2,AF\) | 1 | \(17_{22}\) |
| \(2,BF\) | 1 | \(07_{22}\) |
| \(AF,AC\) | 1 | \(04_{02}\) |

In particular, this table retains both cross-colour orientations.  The 33
cases consist of 18 same-colour cells and 15 genuinely ordered
cross-colour cells.

For these cases the checker uses every top coordinate rather than trying
to preserve (12).  Set

\[
 F=q^{[3]},\quad H=e q^{[2]},\quad
 Q=q^{[4]},\quad K=e q^{[3]}.                                  \tag{14}
\]

If \(F_w^{XY}\) and \(H_w^{XY}\) are the integer incidences of the
abstract Gram entry \(R_{XY}\) in top word \(w\), then the \(w\)-coordinate
of the desired identity is exactly

\[
 4\sum_{XY}\bigl(F_w^{XY}+tH_w^{XY}\bigr)
       (p_Xs_Y+s_Xp_Y)
 +4a(Q_w+tK_w)-\delta_w=0.                                    \tag{15}
\]

There is a much smaller exact certificate inside this full system.  Call
a non-target coordinate a *safe singleton zero* if its direct
\(a(Q+tK)\) term vanishes and exactly one abstract Gram entry occurs,
entirely in \(F\) or entirely in \(H\).  Equation (15) then has the form

\[
                    cR_{XY}=0\quad\hbox{or}\quad
                    ctR_{XY}=0                              \tag{16}
\]

for a nonzero integer \(c\).  Hence it forces \(R_{XY}=0\) uniformly on
the \(t\ne0\) locus.  Entries occurring on both sides are deliberately
not called safe, because a coefficient such as \(1+t\) could vanish at an
exceptional parameter.

The closure rule for these zero entries is elementary.  Every endpoint of
a known nonzero Gram edge represents a nonzero vector in a nondegenerate
two-space.

1. Two nonzero vectors orthogonal to the same nonzero vector are
   proportional.
2. If a proportionality class contains an orthogonal pair, its line is
   isotropic.  In dimension two an isotropic line equals its orthogonal
   complement, so every zero neighbour belongs to the same class.
3. If a final pair of proportionality classes supports both a forced-zero
   and a forced-nonzero Gram edge, there is a contradiction.

Iterating rules 1 and 2 is a finite union-find closure; rule 3 is the
terminal check.  The checker reconstructs all safe singleton zeros and
finds:

* For each of the 15 cross-colour cells, every pure target word still has
  a single contributor.  These three contributors are nonzero, and the
  singleton-zero closure contradicts them.
* For each of the 18 same-colour cells, two pure target words have one
  contributor and the third has exactly two distinct contributors:
  \(R_0+tR_1=1/4\).  At least one of \(R_0,R_1\) is nonzero.  The closure
  gives a contradiction in each of the two branches separately.

The same-colour cases use between 151 and 185 safe zero edges, and the
cross-colour cases use between 153 and 194.  These are exact support
certificates, not generic-rank or numerical calculations, and the default
checker replays all 51 branches in under a second.

As a redundant exhaustive audit, the checker accepts
`--full-groebner`.  In that mode it reconstructs every nonzero equation
(15) in the 48 variables \(p_{i,c},s_{i,c}\), together with \(a,t\), then
adjoins a new variable \(u\) and the Rabinowitsch equation

\[
                              ut-1=0,                            \tag{17}
\]

so the resulting affine scheme is exactly the \(t\ne0\) locus.  Singular
computes over \(\mathbb Q\), in exact arithmetic, and returns the reduced
unit basis \([1]\) in every one of the 33 cases.  Therefore none has a
solution over \(\overline{\mathbb Q}\), and base change of the identity
\(1\in I\) excludes solutions over \(\mathbb C\) as well.

As a reproducibility checksum, the numbers of equations including (17)
have the following histogram:

\[
\begin{array}{c|rrrrrrrrrrr}
\#\text{ equations}&184&190&193&196&199&202&205&208&211&214&217\\
\#\text{ cases}&3&6&2&6&3&1&1&4&4&1&2.
\end{array}                                                    \tag{18}
\]

This is 6,582 exact equations across the 33 saturated ideals.  The
coordinate construction includes the direct \(a(Q+tK)\) contribution;
it does not silently discard the scalar multiple of the quadratic.

## 5. Consequence and next frontier

The unrestricted polarized model is not an isolated point: the same
three-cell \(z\) continues to solve \(zq_t^{[3]}=\Delta_{8,3}\) along 99
explicit one-cell affine lines.  Nevertheless, none of those lines meets
the literal one-pair-cap locus \(z'=a q_t+4ps\).  Therefore an eight-site
pair-cap countermodel near this sparse support, if one exists, must either
activate at least two of the 99 invisible cells simultaneously or change
cells that already create polarized debts and arrange their cancellation.

The concrete next sparse frontier is consequently a two-extra-cell
extension, preferably organized by the automorphism orbits of (1), while
retaining the full common-power equation and the shared pair-cap form.

## 6. Reproduction

From the repository root, the fast exact support/Gram certificate is

```sh
.venv/bin/python computations/verify_polarized_eight_site_fixed_q_one_extra_pair_cap_obstruction.py
```

The redundant full saturated-ideal audit is

```sh
.venv/bin/python computations/verify_polarized_eight_site_fixed_q_one_extra_pair_cap_obstruction.py --full-groebner
```
