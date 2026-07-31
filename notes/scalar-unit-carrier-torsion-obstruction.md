# Even complete scalar-unit curvature gives carrier torsion, not carrier cancellation

## 1. Outcome

Work over a characteristic-zero field.  Fix \(h\geq3\) and the intrinsic
scalar-unit row from a full-nine good-pair chart,

\[
 \alpha q^{[h]}+R q^{[h-1]}=X_a,
 \qquad \alpha\ne0,
 \qquad R=R_{aa}=p_as_a,
 \qquad X_a\ne0.                                      \tag{1}
\]

Put

\[
 Q=\alpha q,
 \qquad G=Q+R,
 \qquad
 \begin{aligned}
 U&=G^{[h]}-\alpha^{h-1}X_a,\\
 \Theta&=G^{[h-1]}-Q^{[h-1]}=RH,\\
 H&=\sum_{\ell=0}^{h-2}{1\over \ell+1}
          Q^{[h-2-\ell]}R^{[\ell]}.
 \end{aligned}                                         \tag{2}
\]

Here \(U\) is the unary clean error and \(H\) is the exact
divided-difference carrier from the
[scalar-unit normal-jet ledger](scalar-unit-full-normal-jet-unary-anchor-ledger.md).

At an ordered residual pair of sites and fixed physical colours, write

\[
 U_{rs}=q_{rs},\qquad
 B=(p_a)_{r},\quad E=(p_a)_{s},\quad
 T=(s_a)_{r},\quad F=(s_a)_{s}.                         \tag{3}
\]

The two endpoint-ordered curvature coefficients are

\[
        \kappa^\rightarrow=\alpha U_{rs}-BF,
        \qquad
        \kappa^\leftarrow=\alpha U_{rs}-ET,             \tag{4}
\]

while the coefficient of \(R=p_as_a\) at the same unordered physical
cell is \(BF+ET\).  Globally, after choosing an order on the residual
sites, this splits

\[
 R=R^\rightarrow+R^\leftarrow,
 \qquad
 K^\rightarrow=Q-R^\rightarrow,
 \qquad
 K^\leftarrow=Q-R^\leftarrow.                           \tag{5}
\]

Suppose, more strongly than the presently available four-cut statements,
that both complete oriented quadratic forms annihilate the same complete
carrier:

\[
                    K^\rightarrow H=K^\leftarrow H=0.   \tag{6}
\]

Adding (6), using \(R=R^\rightarrow+R^\leftarrow\), and multiplying by
\(-1\) gives exactly

\[
                         (R-2Q)H=0.                      \tag{7}
\]

If multiplication by \(H\) were cancellable on this quadratic span, then
\(R=2Q\).  In that hypothetical faithful-carrier quotient, cleanliness
would give

\[
 0=U=(3^h-1-2h)Q^{[h]},                                 \tag{8}
\]

whereas (1) would give

\[
              \alpha^{h-1}X_a=(1+2h)Q^{[h]}\ne0.        \tag{9}
\]

Thus cancellation would force

\[
                         3^h=1+2h,                       \tag{10}
\]

equivalently \(1+3+\cdots+3^{h-1}=h\), which is impossible in
characteristic zero for \(h\geq3\).  This is a useful conditional closing
lemma: a source-faithful proof that makes \(H\) cancellable would eliminate
the intrinsic scalar-unit branch without a support enumeration.

But (7), not \(R=2Q\), is the actual conclusion.  The site-square-zero
algebra has many zero divisors, and \(H\ne0\) does not make multiplication
by \(H\) injective.  In fact the clean relation and the carrier-torsion
relation do not even recover the exceptional target in the universal
two-variable polynomial module.  After clearing the divided-power
factorials, put

\[
 \begin{aligned}
 u_h&=(Q+R)^h-Q^h-hRQ^{h-1},\\
 w_{h-2}&={(Q+R)^{h-1}-Q^{h-1}\over R},\\
 v_{h-1}&=(R-2Q)w_{h-2},\\
 x_h&=Q^h+hRQ^{h-1}.
 \end{aligned}                                          \tag{11}
\]

Then

\[
 h!U=u_h,qquad (h-1)!H=w_{h-2},
 \qquad h!\alpha^{h-1}X_a=x_h,                          \tag{12}
\]

and the degree-\(h\) consequences of \(u_h=v_{h-1}=0\) form

\[
          I_h=\operatorname {span}\{u_h,Qv_{h-1},Rv_{h-1}\}.
                                                                  \tag{13}
\]

The exact universal two-variable obstruction is

\[
                         \boxed{x_h\notin I_h}.          \tag{14}
\]

Consequently, inside \(\mathbb K[Q,R]\), no degree-\(h\) manipulation
using only the clean equation and the summed carrier-torsion equation can
turn the exceptional row into zero: the only degree-one multipliers of the
latter are linear combinations of \(Q\) and \(R\).  The failure is
algebraic before one reaches the further physical occupancy and
source-provenance issues.

Actual four-cut layers are weaker than (6): after two sites are exposed,
an oriented curvature coefficient is paired only with the corresponding
coefficient restriction \(H_{rs}\), not with the complete \(H\).  Even
when \(H\ne0\), a given \(H_{rs}\) can vanish because the carrier terms
use an exposed site or because the surviving terms cancel.  Thus
even in the minimum-entry-support clean-unary case, where the normal-jet
ledger gives \(\Theta=RH\ne0\), that nonvanishing neither selects a
nonzero restricted layer nor currently transports to a nonzero physical
class \(\kappa H\).  A positive proof still needs an occupancy-separation,
carrier-faithfulness, or genuinely filtered restriction--insertion lemma.

This note is a reduction and a no-cancellation audit.  It does not prove
an active clean cap, a clean descent, or Krenn's conjecture.

## 2. Divided-power normalization and the conditional contradiction

Multiplying (1) by \(\alpha^{h-1}\) gives

\[
                  Q^{[h]}+RQ^{[h-1]}=\alpha^{h-1}X_a.   \tag{15}
\]

Therefore the first definition in (2) is equivalently

\[
 U=(Q+R)^{[h]}-Q^{[h]}-RQ^{[h-1]}
   =\sum_{k=2}^{h}Q^{[h-k]}R^{[k]}.                     \tag{16}
\]

The \(k=0\) term is removed by \(Q^{[h]}\), and the \(k=1\)
term is exactly \(RQ^{[h-1]}\); there is no missing binomial coefficient
in divided-power notation.  Similarly,

\[
 \begin{aligned}
 RH
 &=\sum_{\ell=0}^{h-2}Q^{[h-2-\ell]}R^{[\ell+1]}\\
 &=(Q+R)^{[h-1]}-Q^{[h-1]}=\Theta,
 \end{aligned}                                          \tag{17}
\]

because \(R R^{[\ell]}=(\ell+1)R^{[\ell+1]}\).  This
checks both the factor \(1/(\ell+1)\) and the power of \(Q\) in (2).

Under the additional cancellation of \(H\), equation (7) gives \(R=2Q\).
Substituting in (16) and using

\[
 (2Q)^{[k]}=2^kQ^{[k]},
 \qquad
 Q^{[h-k]}Q^{[k]}={h\choose k}Q^{[h]},                 \tag{18}
\]

gives

\[
 U=\left(\sum_{k=2}^{h}{h\choose k}2^k\right)Q^{[h]}
   =(3^h-1-2h)Q^{[h]}.                                  \tag{19}
\]

On the other hand,

\[
 Q^{[h]}+2Q Q^{[h-1]}=(1+2h)Q^{[h]}.                   \tag{20}
\]

Since \(X_a\ne0\), equation (15) and characteristic zero imply
\(Q^{[h]}\ne0\).  Finally,

\[
             3^h-1-2h=\sum_{k=2}^{h}{h\choose k}2^k   \tag{21}
\]

is a nonzero positive integer, hence a nonzero field scalar.  Equations
(19)--(21) prove the conditional contradiction with the exact
divided-power constants.

Notice that the impossible equality is (10), not
\(3^{h-1}=h\).  The latter is only a rough mnemonic for the growth gap;
the exact equivalent form is the geometric-sum equality following (10).

## 3. Exact polynomial-module nonmembership

Let \(S=\mathbb K[Q,R]\) with its ordinary grading.  The numerator in
\(w_{h-2}\) is divisible by \(R\), so every expression in (11) lies in
\(S\), with degrees \(h,h-2,h-1,h\), respectively.  The homogeneous
ideal \((u_h,v_{h-1})\) has degree-\(h\) piece exactly (13): the first
generator can only be multiplied by a scalar and the second by a linear
form in \(Q,R\).

Set \(t=R/Q\) only as notation for the coefficient vector in the ordered
monomial basis \(Q^h,Q^{h-1}R,\ldots,R^h\).  Write

\[
 \begin{aligned}
 u(t)&=(1+t)^h-1-ht,\\
 w(t)&={(1+t)^{h-1}-1\over t},\\
 v(t)&=(t-2)w(t),\\
 x(t)&=1+ht.
 \end{aligned}                                          \tag{22}
\]

Suppose, contrary to (14), that

\[
                     x(t)=a u(t)+b v(t)+c\,t v(t).      \tag{23}
\]

The relevant coefficients of \(v\) are

\[
 [t^{h-1}]v=1,\quad [t^{h-2}]v=h-3,\quad
 [t^0]v=-2(h-1),\quad [t^1]v=(h-1)(3-h).               \tag{24}
\]

Comparing \(t^h\), \(t^{h-1}\), and \(t^0\) in (23), in that order,
forces

\[
 c=-a,\qquad b=-3a,\qquad
 b=-{1\over2(h-1)},\qquad
 a={1\over6(h-1)},\quad c=-{1\over6(h-1)}.              \tag{25}
\]

The coefficient of \(t\) on the right of (23) would then be

\[
 b(h-1)(3-h)+c[-2(h-1)]
       ={h-3\over2}+{1\over3}={3h-7\over6},            \tag{26}
\]

whereas \([t]x=h\).  Their difference is

\[
                         {3h+7\over6}\ne0              \tag{27}
\]

in characteristic zero.  This contradiction proves (14) uniformly for
every \(h\geq3\).  It also proves that the universal quotient

\[
                   S/(u_h,v_{h-1})                     \tag{28}
\]

retains a nonzero degree-\(h\) exceptional target class.  This quotient
is an algebraic logical guard, not a claimed realization by a complete
site-square-zero matching source.

## 4. Physical scope

There are three successively stronger statements which must remain
separate.

1. A literal exposed four-cut coefficient may give
   \(\kappa^\rightarrow H_{rs}=0\) for one restricted carrier layer.
   It need not give \(K^\rightarrow H=0\) for the complete forms.
2. Even granting both complete equations (6) gives only the torsion
   relation (7).  The nonmembership theorem proves that this relation and
   cleanliness do not eliminate the exceptional target.
3. Cancelling \(H\) would give \(R=2Q\) and the contradiction (8)--(10),
   but no existing star-injectivity, minimum-support, same-power, or
   ordinary-residue theorem supplies that cancellation.

At a minimum-entry-support good pair with a clean unary cap, the audited
normal-jet ledger proves \(\Theta\ne0\), and hence \(H\ne0\).  This still
does not imply that multiplication by \(H\) is faithful.  The missing
positive input must distinguish a nonzero carrier component from the
annihilator created by site occupancy and evaluated-source cancellation.

The dependency-free checker
[`verify_scalar_unit_carrier_torsion_obstruction.py`](../computations/verify_scalar_unit_carrier_torsion_obstruction.py)
audits (11)--(27) with exact integer and rational arithmetic for
\(3\leq h\leq128\), verifies the ideal-degree nonmembership by an
independent exact rank calculation, and includes positive-span and
normalization mutations.  The finite range audits constants and signs;
the coefficient proof in Section 3 is uniform.
