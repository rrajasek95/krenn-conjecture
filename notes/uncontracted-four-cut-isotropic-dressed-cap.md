# An isotropic direct block exports a full dressed cap packet

## 1. Result

Retain the notation of
[the overlapping zero-star four-cut identity](overlapping-zero-star-four-cut-exchange.md).
Thus `p,q,i,j` are four distinct exposed sites, `D` is their even common
complement, `|B|=2m>=8`, and

\[
\begin{aligned}
 &a_{ab}u_{cd}z^{[m-2]}+a_{ab}t_cv_dz^{[m-3]}
 +u_{cd}x_ay_bz^{[m-3]}\\
 &\hspace{31mm}+x_ay_bt_cv_dz^{[m-4]}
       =\delta_{a=b=c=d}X_a^D.                         \tag{1}
\end{aligned}
\]

Here `A=(a_ab)` and `U=(u_cd)` are the direct blocks on `pq` and `ij`,
while `x_a,y_b,t_c,v_d` are the four stars into `D`.  Every product is in
the site-square-zero algebra on `D`.

Choose covectors `alpha,beta` with

\[
                         \alpha^{\mathsf T}U\beta=0,    \tag{2}
\]

and put

\[
 T=t(\alpha)=\sum_c\alpha_ct_c,qquad
 V=v(\beta)=\sum_d\beta_dv_d,qquad
 n_c=\alpha_c\beta_c,
\]

\[
                         F_{\alpha,\beta}=TVz^{[m-4]}. \tag{3}
\]

**Theorem 1.1 (isotropic dressed cap).**  All nine uncontracted `(a,b)`
rows of (1) become

\[
 \boxed{
 F_{\alpha,\beta}
   \left(x_ay_b+{a_{ab}\over m-3}z\right)
       =\delta_{ab}n_aX_a^D,
       \qquad0\le a,b\le2.}                            \tag{4}
\]

Every term in (4) comes from the complete 81-row system.  In particular,
the direct block remains in the dressed quadratic

\[
                         x_ay_b+{a_{ab}\over m-3}z,     \tag{5}
\]

and the multiplier `F` retains both contracted stars and the actual common
power.  There is no division by a source entry or tensor.

There is a symmetric packet obtained by choosing
`xi^T A eta=0` and leaving the `(c,d)` indices open.  With
`G=x(xi)y(eta)z^[m-4]`, it reads

\[
 G\left(t_cv_d+{u_{cd}\over m-3}z\right)
       =\delta_{cd}\xi_c\eta_cX_c^D.
\]

**Corollary 1.2 (uniform colour retention).**  The covectors in (2) can
always be chosen so that at least two of `n_0,n_1,n_2` are nonzero.  They
can all be nonzero unless `U` is a nonzero scalar multiple of a matrix
unit.  Thus (4) is a ternary dressed cap off that sharp matrix-unit
boundary, and a binary dressed cap on it.

## 2. Derivation from the 81 rows

Multiply (1) by `alpha_c beta_d` and sum over `c,d`.  If
`u=alpha^T U beta`, the result for each `a,b` is

\[
\begin{aligned}
 &a_{ab}u z^{[m-2]}+a_{ab}TVz^{[m-3]}
   +u x_ay_bz^{[m-3]}+x_ay_bTVz^{[m-4]}\\
 &\hspace{42mm}=\delta_{ab}\alpha_a\beta_aX_a^D.       \tag{6}
\end{aligned}
\]

Equation (2) kills exactly the first and third terms.  Divided powers give

\[
                         z z^{[m-4]}=(m-3)z^{[m-3]}.    \tag{7}
\]

Factoring `TVz^[m-4]` from the two surviving terms gives (4).  At the
smallest order `m=4`, (7) reads `z z^[0]=z`, so the formula includes the
eight-site boundary without a negative power or exceptional case.

The symmetric packet follows by contracting the `(a,b)` indices instead.

## 3. The exact torus-isotropy classification

The following elementary fact explains the sharp colour count.

**Lemma 3.1 (torus zero or matrix unit).**  For a matrix
`M in Mat_3(C)`, exactly one of the following holds.

1. `M` is a nonzero scalar multiple of a matrix unit `E_rs`.  Then
   `alpha^T M beta` is nonzero whenever all six coordinates of
   `alpha,beta` are nonzero.
2. There are `alpha,beta in (C^*)^3` with
   `alpha^T M beta=0`.

The zero matrix belongs to the second alternative.

**Proof.**  The bilinear form is the Laurent polynomial

\[
                         \sum_{r,s}M_{rs}X_rY_s         \tag{8}
\]

on the algebraic torus.  The units of
\(\mathbb C[X_0^{\pm1},\ldots,Y_2^{\pm1}]\) are exactly the nonzero
scalar monomials.  If
(8) has at least two terms, it is a nonunit and hence belongs to a maximal
ideal of the torus coordinate ring, giving a torus zero.  With one term it
is a nonzero scalar matrix unit and never vanishes on the torus.  The zero
form vanishes everywhere.  \(\square\)

If `M=lambda E_rs`, choose `alpha,beta` with identical two-coordinate
support

\[
                   H=[3]\setminus\{r\}
                   \quad\hbox{or}\quad
                   H=[3]\setminus\{s\}.                \tag{9}
\]

All coordinates on `H` may be nonzero, the bilinear form vanishes, and
`alpha_c beta_c` is nonzero exactly for `c in H`.  This proves Corollary
1.2.  Same support is a convenient normalized witness, not a claim that
every isotropic pair must have the same support.

There need not be a two-coordinate torus zero on any principal support.
For example,

\[
                         E_{01}+E_{12}+E_{20}           \tag{10}
\]

restricts to one nonzero monomial on each principal two-set.  Nevertheless
`alpha=(1,1,1)` and `beta=(1,1,-2)` give a full-torus zero.  This is why the
matrix-unit classification, rather than a universal two-support claim, is
the correct statement.

## 4. Double isotropy and the pure four-star export

Choose additionally `xi,eta` with `xi^T A eta=0`, multiply (4) by
`xi_a eta_b`, and sum over `a,b`.  The dressed direct term disappears and
one obtains

\[
 \boxed{
 x(\xi)y(\eta)t(\alpha)v(\beta)z^{[m-4]}
      =\sum_{c=0}^2\xi_c\eta_c\alpha_c\beta_cX_c^D.}  \tag{11}
\]

Lemma 3.1 gives the exact maximum number of nonzero target colours in this
double contraction.

* If neither `A` nor `U` is a scalar matrix unit, all three survive.
* If exactly one is a scalar matrix unit, two survive.
* If `A=lambda E_rs` and `U=mu E_kl`, two can be retained exactly when
  `{r,s}` and `{k,l}` intersect; otherwise the sharp maximum is one.

For the last assertion, a two-coordinate witness for a matrix unit omits
one index from its endpoint-index set.  The two active sets have
intersection two precisely when the same index can be omitted from both;
otherwise their intersection has size one.  In every case at least one
colour survives.

## 5. Sharp consistency guards

Equation (11) is useful export data, but it is not by itself a
contradiction.

### 5.1 A binary four-star identity

On four cyclic sites, with indices modulo four, put

\[
                         L_j=e_0^{(j)}+e_1^{(j+1)}.     \tag{12}
\]

Then exactly

\[
                         L_0L_1L_2L_3=X_0+X_1.         \tag{13}
\]

Indeed, every nonconstant binary choice around the cycle contains a
`1 to 0` transition, and the corresponding two factors occupy the same
physical site.  Only the all-zero and all-one choices survive.  Thus even
the two-colour four-star output is attainable at `m=4`.

### 5.2 Ternary support algebra with an unstructured multiplier

Partition twelve sites into three four-sets
`S_c={s_(c,0),...,s_(c,3)}` and put

\[
 L_j=\sum_{c=0}^2e_c^{(s_{c,j})},
 \qquad
 R=\sum_{c=0}^2\bigotimes_{u\notin S_c}e_c^{(u)}.      \tag{14}
\]

Then

\[
                         L_0L_1L_2L_3R=X_0+X_1+X_2.   \tag{15}
\]

For the `c`-summand of `R`, square-freeness forces every `L_j` to choose
its unique remaining site in `S_c`.  This model does **not** represent
`R` as a divided power of one quadratic.  It shows that target support and
factor count alone cannot exclude the ternary version of (11).

## 6. The next exact gate

The stronger object is the entire dressed packet (4), not one further
rank-one contraction of it.  A continuation must use simultaneously

1. the shared multiplier `F=TVz^[m-4]`;
2. all six target-zero off-diagonal dressed quadratics;
3. the three normalized diagonal targets; and
4. the linkage of every quadratic in (5) to the same `A,x,y,z`.

The registered pure-lift obstructions concern codimension-two six-site
lifts with an additional next-power equation, while the aligned square
ideal arguments require a repeated marked form.  Neither hypothesis is
present automatically here.

Two subsequent boundary results sharpen the gate.  At \(m=4\), the
[four-site coordinate-monomial obstruction](four-site-coordinate-monomial-dressed-packet-obstruction.md)
proves that a multiplier \(TV\) whose local rows are coordinate monomials
can place at most two of the three pure targets in its quadratic response
image.  It therefore excludes the ternary packet in that exact stratum,
with arbitrary nonzero local weights.  Arbitrary local superpositions and
the higher common powers remain outside that theorem.

In the other direction, the
[scalar-unit full-isotropic-packet guard](uncontracted-four-cut-scalar-unit-full-isotropic-packet-guard.md)
gives an \(m=5\), \(U=E_{22}\) model with \(z^{[2]}\ne0\) which satisfies
every isotropic nine-row packet.  Core padding makes both opposite star
triples injective, all their rows supported on at least three sites, and every diagonal
product nonzero.  The model does not satisfy the full four-cut identity or
the connected-spanning-nonbipartite E1 provenance, so those omitted
conditions remain usable; the isotropic packet family alone cannot expose
the exceptional \(E_{22}\) coefficient.

Consequently (4) is a new exact export, not a proof of the remaining E1
chart.  The active split is to extend the four-site obstruction beyond
coordinate monomials and higher powers, or to use the full 81-row/provenance
equations to couple the scalar-unit row back to the isotropic packets.

## 7. Audit

The dependency-free checker
[`verify_uncontracted_four_cut_isotropic_dressed_cap.py`](../computations/verify_uncontracted_four_cut_isotropic_dressed_cap.py)
checks the 81-to-nine contraction, the divided-power factor in (7), every
matrix-unit support intersection, the sharp cyclic matrix (10), the binary
identity (13), and the arbitrary-multiplier ternary identity (15).  The
uniform statements remain algebraic proofs; the checker is a small exact
guard against index and boundary mistakes.
