# A finite Hilbert--Cauchy moment tower kills the scalar-unit carrier class

## 1. Outcome, orientation, and the degree correction

Work over a characteristic-zero field and fix \(h\geq3\).  Use first the
orientation in the certified scalar-unit normal jet:

\[
 B_j=q^{[h-j]}r^{[j]}\quad(0\leq j\leq h),\qquad
 u_{\mathrm{jet}}=\sum_{j=2}^hB_j,\qquad
 x_{\mathrm{jet}}=B_0+B_1.                              \tag{1}
\]

Thus \(u_{\mathrm{jet}}\) is the clean unary error and
\(x_{\mathrm{jet}}=q^{[h]}+q^{[h-1]}r\) is its exceptional adjacent
endpoint class.  For \(s\geq0\), put

\[
 H_s=\int_0^1t^s(q+tr)^{[h-2]}\,dt
     =\sum_{\ell=0}^{h-2}{1\over s+\ell+1}
       q^{[h-2-\ell]}r^{[\ell]},
 \qquad c_s=(r-2q)H_s.                                  \tag{2}
\]

There is an essential degree correction to the proposed span:
\(c_s\) has degree \(h-1\), whereas (1) has degree \(h\).  The meaningful
degree-\(h\) consequences are

\[
 {\cal R}_h(S)=\operatorname {span}\{qc_s,rc_s:s\in S\}
              \subseteq V_h,                            \tag{3}
\]

where \(V_d\) is the space of binary forms of degree \(d\).  Raw \(c_s\)'s
cannot literally lie in the same homogeneous span as \(u_{\mathrm{jet}}\).
The multiplications in (3) are operations in the formal polynomial ring.
Using them in a source quotient is a separate, presently missing datum;
Theorem 1 does not silently assert such a source-level operation.
Concretely, if \(E_j=q^{[d-j]}r^{[j]}\), ordinary degree-one
multiplication has the divided-power weights

\[
 qE_j=(d-j+1)q^{[d-j+1]}r^{[j]},\qquad
 rE_j=(j+1)q^{[d-j]}r^{[j+1]}.
\]

Define

\[
 S_h=\begin{cases}
       \{0,1\},&h=3,\\
       \{0,1,\ldots,h-3\},&h\geq4.
     \end{cases}                                        \tag{4}
\]

**Theorem 1 (certified-orientation moment tower).**  One has

\[
 \boxed{{\cal R}_h(S_h)=(r-2q)V_{h-1}},\qquad
 \boxed{\operatorname {span}\{u_{\mathrm{jet}},
              {\cal R}_h(S_h)\}=V_h}.                   \tag{5}
\]

In particular,

\[
 \boxed{x_{\mathrm{jet}}\in
   \operatorname {span}\{u_{\mathrm{jet}},qc_s,rc_s:s\in S_h\}.}    \tag{6}
\]

This is stronger than target membership: the clean row and the carrier
tower span every degree-\(h\) binary class.

The prompt uses the reversed indexing

\[
 M_k=q^{[k]}r^{[h-k]}=B_{h-k}.                           \tag{7}
\]

Consequently its displayed pair is not (1), but rather

\[
 u_M=\sum_{k=2}^hM_k=\sum_{j=0}^{h-2}B_j,\qquad
 x_M=M_0+M_1=B_h+B_{h-1}.                               \tag{8}
\]

The first equality in (5) is independent of the clean orientation.
Moreover neither \(u_{\mathrm{jet}}\) nor \(u_M\) is divisible by
\(r-2q\).  Hence the literal prompt pair also satisfies

\[
 \boxed{\operatorname {span}\{u_M,{\cal R}_h(S_h)\}=V_h,\qquad
 x_M\in\operatorname {span}\{u_M,{\cal R}_h(S_h)\}.}     \tag{9}
\]

The two pairs must not be mixed: the certified clean row paired with
\(x_M\), or the prompt clean row paired with \(x_{\mathrm{jet}}\), is not
the complementary clean/target ledger.

There is a sharp, carefully qualified minimality statement.

**Theorem 2 (sharp initial-prefix depth).**  For \(h\geq4\), both

\[
\begin{aligned}
 x_{\mathrm{jet}}&\notin
   \operatorname {span}\{u_{\mathrm{jet}},qc_s,rc_s:0\leq s\leq h-4\},\\
 x_M&\notin
   \operatorname {span}\{u_M,qc_s,rc_s:0\leq s\leq h-4\}.
\end{aligned}                                           \tag{10}
\]

For \(h=3\), both nonmemberships hold with only \(s=0\).  Thus the last
moment in the prescribed nested initial tower is necessary, and every
shorter initial prefix fails.

This is not setwise or cardinal minimality among arbitrary moment indices.
That stronger reading is false.  At \(h=6\), the columns

\[
 u_{\mathrm{jet}},qc_0,rc_0,qc_1,rc_1,qc_3,rc_3          \tag{11}
\]

have determinant \(179/19600\ne0\) in the ordered divided-power basis
\((B_0,\ldots,B_6)\).  For the prompt's reversed \(u_M\), the corresponding
determinant is \(473/78400\ne0\).  Thus the nonconsecutive set
\(\{0,1,3\}\) already spans \(V_6\), while the initial prefix
\(\{0,1,2\}\) misses the corresponding target in both orientations.

The algebraic theorem is positive.  Its source-provenance audit is
negative: none of the existing normal-jet, pivot/path, or physical
four-cut results supplies (2) for every \(s\in S_h\) in one
source-faithful module.  Sections 4--6 state the exact gap.

## 2. Why the full tower spans

Put \(n=h-2\) and, for \(h\geq4\), let

\[
 W=\operatorname {span}\{H_0,\ldots,H_{n-1}\}\subseteq V_n.          \tag{12}
\]

The coefficient matrix is the \(n\)-by-\((n+1)\) Cauchy matrix

\[
                         C_{s\ell}={1\over s+\ell+1}.     \tag{13}
\]

Every square Cauchy minor is nonzero, so \(\dim W=n\).  The stronger
statement needed here is

\[
                         qW+rW=V_{n+1}.                  \tag{14}
\]

Rescale from divided powers to ordinary monomials, an invertible diagonal
change of basis.  Apart from a common factor \(1/n!\), the coefficient of
\(q^{n-j}r^j\) in \(H_s\) is

\[
                         {\binom nj\over s+j+1}.          \tag{15}
\]

Let \(\varphi\in V_{n+1}^*\), with value \(y_j\) on
\(q^{n+1-j}r^j\), annihilate \(qW+rW\).  Package the functional as

\[
                         Z(t)=\sum_{j=0}^{n+1}\binom{n+1}j y_jt^j.  \tag{16}
\]

Directly from (15), up to the common factor \(1/n!\),

\[
\begin{aligned}
 \varphi(qH_s)&=\int_0^1t^s
       \left(Z-{tZ'\over n+1}\right)dt,\\
 \varphi(rH_s)&=\int_0^1t^s{Z'\over n+1}\,dt.
\end{aligned}                                            \tag{17}
\]

Write \(I_s=\int_0^1t^sZ(t)\,dt\).  Integration by parts gives

\[
\begin{array}{ll}
 Z(1)-Z(0)=0,&s=0\text{ in the second line},\\
 Z(1)-sI_{s-1}=0,&1\leq s\leq n-1\text{ in the second line},\\
 (n+s+2)I_s-Z(1)=0,&0\leq s\leq n-1\text{ in the first line}.
\end{array}                                              \tag{18}
\]

Compare the last line at \(s=0\) with the middle line at \(s=1\).
They force \(Z(1)=0\), hence \(Z(0)=0\) and
\(I_0=\cdots=I_{n-1}=0\).  Write \(Z=t(1-t)P\), with
\(\deg P\leq n-1\).  Then

\[
 \int_0^1t(1-t)P(t)A(t)\,dt=0
 \quad\text{for every }A\in\mathbb K[t]_{\leq n-1}.      \tag{19}
\]

Over \(\mathbb R\), take \(A=P\); positivity gives \(P=0\).  Equivalently,
the rational Hilbert Gram determinant for the weight \(t(1-t)\) is
nonzero.  Since it is a nonzero rational number, the conclusion persists
over every characteristic-zero field.  Thus \(\varphi=0\), proving (14).

Multiplication by \(r-2q\) is injective, so (14) proves
\({\cal R}_h(S_h)=(r-2q)V_{h-1}\).  This is the hyperplane of degree-\(h\)
forms divisible by \(r-2q\).  In the ordinary basis scaled by \(h!\),

\[
\begin{aligned}
 h!\,u_{\mathrm{jet}}(1,2)
   &=\sum_{j=2}^h\binom hj2^j=3^h-1-2h\ne0,\\
 h!\,u_M(1,2)
   &=\sum_{j=0}^{h-2}\binom hj2^j
     =3^h-2^{h-1}(h+2)\ne0.
\end{aligned}                                            \tag{20}
\]

Both values are visibly sums of positive integers.  Either clean row
therefore complements the carrier hyperplane, proving (5) and (9).

When \(h=3\), the two moments \(H_0,H_1\in V_1\) have coefficient matrix

\[
                         \begin{pmatrix}1&1/2\\1/2&1/3\end{pmatrix},          \tag{21}
\]

whose determinant is \(1/12\).  Thus they span \(V_1\), so
\(qW+rW=V_2\), and the same hyperplane argument applies.

## 3. Rodrigues witnesses for sharp prefix depth

Assume \(h\geq4\), put \(n=h-2\), and retain only

\[
                         W^-=\operatorname {span}\{H_0,\ldots,H_{n-2}\}.     \tag{22}
\]

The Rodrigues polynomial

\[
 Z_n(t)={d^{\,n-1}\over dt^{\,n-1}}\bigl(t^n(1-t)^n\bigr)                  \tag{23}
\]

is equivalently
\((n-1)!t(1-t)P_{n-1}^{(1,1)}(1-2t)\), in shifted-Jacobi notation.  It
vanishes at both endpoints and is orthogonal to
\(1,t,\ldots,t^{n-2}\).  In the notation (16), after a common nonzero
rescaling, its functional is

\[
 y_0=0,\qquad
 y_j=(-1)^{j-1}\binom{n+j-1}{n}\quad(1\leq j\leq n+1).    \tag{24}
\]

Equations (17) and integration by parts show that this nonzero functional
\(\Phi_n\) annihilates \(qW^-+rW^-\).  For any
\(P(z)=\sum_{j=0}^{n+1}p_jz^j\), (24) is equivalently

\[
 \Phi_n(P)=-{1\over n!}
   \left.{d^n\over dt^n}\bigl(t^{n-1}P(-t)\bigr)\right|_{t=1}.       \tag{25}
\]

### 3.1 Certified orientation

Set \(q=1,r=z\), rescale by \(h!\), and write

\[
 X_{\mathrm{jet}}(z)=1+hz,\qquad
 U_{\mathrm{jet}}(z)=(1+z)^h-X_{\mathrm{jet}}(z),\qquad
 B_{\mathrm{jet}}=1+2h.                                  \tag{26}
\]

If the first membership in (10) held, evaluation at \(z=2\) would force
the coefficient of \(u_{\mathrm{jet}}\), and hence

\[
 P_{\mathrm{jet}}(z)=
 {3^hX_{\mathrm{jet}}(z)-B_{\mathrm{jet}}(1+z)^h\over z-2}          \tag{27}
\]

would belong to \(qW^-+rW^-\).  The numerator vanishes at \(2\), so this
is a polynomial.  In (25), the \((1-t)^h\) term has a zero of order
\(h=n+2\) and contributes nothing.  For the other term,

\[
 {t^{n-1}X_{\mathrm{jet}}(-t)\over -t-2}
   ={t^{n-1}(ht-1)\over t+2}.
\]

Using

\[
 [y^n]\,{(1+y)^{n-1}\over3+y}
       =-{2^{n-1}\over3^{n+1}},                          \tag{28}
\]

one obtains the explicit nonzero value

\[
                         \Phi_n(P_{\mathrm{jet}})
                         =-3(2h+1)2^{n-1}\ne0.            \tag{29}
\]

This contradicts membership and proves the certified half of (10).

### 3.2 The prompt's reversed \(M\)-orientation

For (8), the scaled target and clean polynomials are

\[
 X_M(z)=z^h+hz^{h-1},\qquad U_M(z)=(1+z)^h-X_M(z),\qquad
 B_M=2^{h-1}(h+2).                                      \tag{30}
\]

The same evaluation argument would put

\[
 P_M(z)={3^hX_M(z)-B_M(1+z)^h\over z-2}                 \tag{31}
\]

in \(qW^-+rW^-\).  Formula (25) instead gives

\[
 \Phi_n(P_M)=(-1)^{h+1}3^h c_n,\qquad
 c_n=[y^n]\,{(1+y)^{2n}(n+1-y)\over3+y}.                 \tag{32}
\]

This coefficient is strictly positive.  If \(c_k\) denotes the coefficient
of \(y^k\) and

\[
 R_k=(n+1)\binom{2n}{k}-\binom{2n}{k-1},
\]

then

\[
                         3c_0=R_0,\qquad3c_k+c_{k-1}=R_k.             \tag{33}
\]

For \(1\leq k\leq n\),

\[
 {R_k-R_{k-1}\over\binom{2n}{k-1}}
 ={(n+1)(2n-2k+1)\over k}
  -{2n-2k+3\over2n-k+2}>0.                              \tag{34}
\]

Indeed, the first term is at least \((n+1)/n>1\), while the second is at
most \(1\).  Thus the displayed strict inequality is uniform through the
endpoint \(k=n\).

Starting from \(0<c_0<R_0\), (33)--(34) inductively give
\(0<c_k<R_k\) through \(k=n\).  Thus (32) is nonzero and proves the
prompt-orientation half of (10).  Nesting proves failure for every shorter
initial prefix in both orientations.

### 3.3 The \(h=3\) threshold

Here

\[
 H_0=q+{r\over2},\qquad c_0={r^2\over2}-2q^2.            \tag{35}
\]

For the certified orientation,

\[
 U_{\mathrm{jet}}=r^3+3qr^2,\qquad
 X_{\mathrm{jet}}=q^3+3q^2r.
\]

In \(X_{\mathrm{jet}}=AU_{\mathrm{jet}}+Bqc_0+Crc_0\), the
\(q^3,q^2r,qr^2\) coefficients force
\(B=-1/2,C=-3/2,A=1/12\), but the remaining \(r^3\) coefficient is
\(A+C/2=-2/3\ne0\).  For the prompt orientation,
\(U_M=q^3+3q^2r\), \(X_M=r^3+3qr^2\); the equations force
\(B=6,C=2,A=12\), followed by the false coefficient
\(3A-2C=32\).  Thus \(H_0\) alone fails in both cases, while (21) proves
that \(H_0,H_1\) succeed.

## 4. What the algebra would close

On the clean unary branch, the certified normal jet supplies
\(u_{\mathrm{jet}}=0\), not the reversed clean row \(u_M=0\).  If a
source-faithful graded quotient also supplied \(c_s=0\) for every
\(s\in S_h\) and allowed legal multiplication by \(q,r\), Theorem 1 would
give

\[
                         x_{\mathrm{jet}}=B_0+B_1=0.      \tag{36}
\]

This is the actual exceptional adjacent class.  Any source statement
retaining it as nonzero would contradict the tower without cancelling a
single \(H_s\).  The prompt's reversed pair has the parallel algebraic
conclusion (9), but must not be substituted silently for the certified
source equations.

The theorem does not make formal polynomial identities survive physical
site restriction, insertion, or a source quotient.  Nor may one multiply
a coefficient-level four-cut equality by \(q,r\) unless those products
are legal operations in the same source complex.  Those are the remaining
provenance requirements.

## 5. Audit of the available data

### 5.1 Full normal jet

The
[full normal-jet ledger](scalar-unit-full-normal-jet-unary-anchor-ledger.md)
gives, after \(r=\alpha^{-1}R_{aa}\), exactly

\[
 H_a/\alpha^{h-2}=H_0,\qquad
 rH_0=(q+r)^{[h-1]}-q^{[h-1]}.                           \tag{37}
\]

Thus \(H_0\) is the only member of the moment family currently present in
the source data, and it is canonical as an endpoint divided difference.
Cleanliness and minimum-support goodness prove \(rH_0\ne0\); they do not
prove \(c_0=0\).  Even \(c_0=0\) follows only after granting the
stronger-than-physical pair of complete oriented annihilations.  The
higher normal polars are

\[
                         R_{D^{(1)}}\cdots R_{D^{(m)}}G_a^{[h-m]},            \tag{38}
\]

not the inverse-Hilbert rows \(H_s\).  The full normal jet therefore
supplies neither \(H_s\) nor \(c_s=0\) for any \(s\geq1\).

### 5.2 Stationary pivot or path

The
[one-sided stationary-pivot audit](scalar-unit-one-sided-stationary-pivot-path-no-go.md)
shows that its pivot is an exact discrete endpoint replacement
\(q\mapsto q+r\) under its unary equation and six complementary
first-endpoint response-row annihilations.  That endpoint/path audit is now
independently complete.  It does not make \(q+tr\) an exact source for
\(0<t<1\).  The one-sided stationary path has endpoint defects with a
factor \(t(t-1)\), but this does not create (2): its endpoint ordered-square
jet scales by \(\phi'(1)\) under reparameterization and can be killed by a
non-immersive endpoint parameter, while integrating the path derivative is
only the zero difference of equal endpoint defects.

Once the ordered affine segment \(q+tr\) is fixed, the algebraic \(H_s\)
is canonical.  Under \(t=\phi(\tau)\), its honest pullback is

\[
 \int \phi(\tau)^s\phi'(\tau)
       (q+\phi(\tau)r)^{[h-2]}\,d\tau,                  \tag{39}
\]

which equals \(H_s\).  A raw stationary jet or raw
\(\tau^s\,d\tau\) integral lacks this density and is parameter dependent.
No current pivot/path construction gives a canonical affine connection or
source-chain one-form whose pullbacks are (39).  Endpoint data gives (37),
but no independent \(c_s=0\) for \(s\geq1\).

### 5.3 Physical four cuts

A literal four-cut row sees an oriented curvature coefficient times a
carrier restricted away from exposed sites.  The two orientations can see
different restrictions, and either can vanish through occupancy or
evaluated cancellation.  The actual row is therefore weaker even than a
complete equation \((q-x)H_0=0\), let alone the common global tower.

The
[complementary-pivot packet](scalar-unit-complementary-pivot-essential-pair.md)
can detect a nonzero
restricted product \(\kappa^{\rm or}H_{0,\mathrm{comp}}\), but detection is
not annihilation or transgression.  The scalar-unit
[80-of-81 guard](uncontracted-four-cut-scalar-unit-eighty-row-injective-guard.md)
shows that injective stars can still miss the exceptional uncontracted row,
while the
[isotropic-packet guard](uncontracted-four-cut-scalar-unit-full-isotropic-packet-guard.md)
suppresses the exceptional coefficient used by
the unary Euler identity.  None of these data yields (2) for a common
carrier at all required moments.

## 6. Exact missing lemma and a source-safe stronger route

The positive bridge can be stated without carrier cancellation.

**Missing moment-transgression lemma.**  For a clean intrinsic scalar-unit
source, construct one source-provenant graded module \(Q\) and a physical
restriction--insertion or higher-cut chain operation such that:

1. \(u_{\mathrm{jet}}=0\) holds in \(Q_h\) and the exceptional
   \(x_{\mathrm{jet}}\) class is retained;
2. \((r-2q)H_s=0\) holds in the same \(Q_{h-1}\) for every \(s\in S_h\);
3. multiplication by both \(q\) and \(r\) is a legal source operation
   landing in \(Q_h\), with zero indeterminacy; and
4. every moment uses the same endpoint ordering, physical carrier, and
   affine density, so restriction, reparameterization, and evaluated
   cancellation do not change the class between moments.

Theorem 1 would then give (36) inside \(Q\).

A stronger, parameter-safe sufficient statement is the coefficientwise
higher-cut identity

\[
                 (r-2q)(q+tr)^{[h-2]}=0\quad\text{in }Q[t].           \tag{40}
\]

Canonical weighted integration gives every relation in item 2.  No
existing normal-jet or four-cut theorem proves (40).  Conversely, endpoint
stationarity, an unweighted path integral, or one exposed four-cut
coefficient cannot source-faithfully produce the tower.  This is the exact
present no-go.

## 7. Exact audit

The dependency-free checker
[verify_scalar_unit_carrier_moment_tower_hilbert_cauchy.py](../computations/verify_scalar_unit_carrier_moment_tower_hilbert_cauchy.py)
uses exact rational arithmetic and explicit exceptions.  It verifies the
Cauchy ranks, (5), (9), both sharp Rodrigues/Jacobi prefix witnesses, the
exact \(h=3\) residuals, and both determinants in (11) for
\(3\leq h\leq24\).  It rejects nine mutations: the moment denominator,
moment-basis reversal, the two-orientation factor, the clean endpoint,
deletion of the last initial moment, the two divided-power multiplier
weights, the target sign, and an inconsistent reversal of the certified
clean/target pair.  It runs unchanged under optimized Python.  The proofs
above are uniform; the finite range is a deterministic smoke audit.

This note is a conditional algebraic closing lemma and a provenance audit.
It does not modify the certified frontier, assert the missing
moment-transgression lemma, or prove Krenn's conjecture.
