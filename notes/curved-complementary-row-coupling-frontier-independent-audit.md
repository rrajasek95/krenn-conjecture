# Independent audit: complementary-row coupling frontier

## 1. Verdict

**PASS.**  The interpolation coefficients, divided-power normalizations,
activity classification, shore-flattening argument, old-guard response,
and every product in the deconcentrated packet in
[the primary note](curved-complementary-row-coupling-frontier.md) check
exactly.

During audit, Lemma 3.1 was restricted to \(h\geq2\).  That hypothesis is
necessary: at \(h=1\), the complementary shore is empty and a quadratic
\(R=\kappa_0X_0+\kappa_1X_1\) itself gives a two-colour target on the sole
pair.  All uses in the primary are at the \(8\to6\) boundary \(h=3\), so
the correction changes no promoted conclusion.

The audited primary has SHA-256

    591338736fc152b07eeb0cd40444e7d9501fd35201185f84e6c6f4d7f85aa0ae  notes/curved-complementary-row-coupling-frontier.md

The result is a frontier theorem, not a curved-branch closure.  It proves
that the concentrated unary guard cannot satisfy the complementary row and
that a deconcentrated clean scalar-zero packet is locally possible.  The
remaining two-chart lemma is explicitly conditional and remains unproved.

## 2. Independent polarization and factorial audit

At the six-site boundary, the physical row and clean error are

\[
 sq^{[3]}+rq^{[2]}=T,\qquad
 {\cal E}=F^{[3]}-s^2T,\qquad F=sq+r.                  \tag{A1}
\]

On \(tK_0+uK_1\), linearity gives

\[
 s=t\sigma,\quad F=tF_0+uR,\quad T=tT_0+uT_1.          \tag{A2}
\]

The divided-power binomial formula has no binomial coefficients:

\[
\begin{aligned}
 (tF_0+uR)^{[3]}
  ={}&t^3F_0^{[3]}+t^2u\,RF_0^{[2]}\\
    &+tu^2\,R^{[2]}F_0+u^3R^{[3]}.                    \tag{A3}
\end{aligned}
\]

Subtracting

\[
 (t\sigma)^2(tT_0+uT_1)
   =t^3\sigma^2T_0+t^2u\sigma^2T_1                  \tag{A4}
\]

and using \(F_0^{[3]}=\sigma^2T_0\) gives precisely

\[
 {\cal E}
 =t^2u\bigl(RF_0^{[2]}-\sigma^2T_1\bigr)
  +tu^2R^{[2]}F_0+u^3R^{[3]}.                         \tag{A5}
\]

For the scalar-zero physical row, \(T_1=Rq^{[2]}\).  Since

\[
 F_0^{[2]}
   =\sigma^2q^{[2]}+\sigma qr_0+r_0^{[2]},             \tag{A6}
\]

the first coefficient becomes

\[
 \Omega_0=R(\sigma qr_0+r_0^{[2]}),                   \tag{A7}
\]

while \(\Omega_1=R^{[2]}F_0\) and \(\Omega_2=R^{[3]}\).
Thus every coefficient and factorial in the primary's (5)--(6) is
correct.

There is an independent ordinary-power check.  Expanding (A1) first gives

\[
 {\cal E}=sqR^{[2]}+R^{[3]}
\]

when the response is denoted by \(R\).  Since
\(R^2=2R^{[2]}\) and \(R^3=6R^{[3]}\),

\[
                         6{\cal E}=R^2(R+3sq),          \tag{A8}
\]

which agrees with the primary's formula (7).

If \(K_0=E_{00}\) and \(K_1=E_{00}-I\), then

\[
 tK_0+uK_1=\operatorname{diag}(t,-u,-u),\qquad
 s=t\sigma.                                             \tag{A9}
\]

Hence the activity product is \(\sigma t^2u^2\), up to the two harmless
minus signs, and activity is exactly \(tu\ne0\).  When \(R^{[3]}=0\),

\[
 {\cal E}=tu(t\Omega_0+u\Omega_1).                     \tag{A10}
\]

Two nonzero dependent tensors have a unique projective kernel with both
coordinates nonzero; two zero tensors make the whole line clean.  Independent
tensors have no residual kernel, and if exactly one tensor vanishes the
only residual kernel is an inactive endpoint.  This proves the stated
four-way classification with no omitted activity case.

## 3. Shore-flattening rank

Assume \(h\geq2\) and \(R\) is supported on one residual pair \(xy\).
Every term of \(q^{[h-1]}\) meeting \(x\) or \(y\) dies in the
site-square-zero product, so

\[
 Rq^{[h-1]}
  =R\otimes
    \left(q|_{W\setminus\{x,y\}}\right)^{[h-1]}.        \tag{A11}
\]

This has flattening rank at most one across

\[
 (V_x\otimes V_y)\ \bigm|\!
   \bigotimes_{z\in W\setminus\{x,y\}}V_z.              \tag{A12}
\]

For

\[
 T=\sum_{c\in C}\kappa_c
   (e_c^{(x)}e_c^{(y)})
   \otimes e_c^{\otimes(W\setminus\{x,y\})},            \tag{A13}
\]

the displayed left factors are independent.  The right factors are also
independent because \(h\geq2\) leaves at least two sites on that shore.
Thus the flattening rank is \(|C|\), proving the contradiction for
\(|C|\geq2\).  This argument treats \(R\) as one arbitrary vector in
\(V_x\otimes V_y\); it does not separate cancelling entries or assume
rank one inside the physical block.

## 4. The old guard at \(E_{00}-I\)

For the \(pq\)-chart of the audited unary guard, the selected endpoint
rows are

\[
\begin{array}{c|ccc}
 &0&1&2\\ \hline
 p&r_0&s_1&s_2\\
 q&u_0&r_1&r_2 .
\end{array}                                                   \tag{A14}
\]

The direct block \(A_{pq}\) has only its \(00\)-cell, while
\((E_{00}-I)_{00}=0\).  Therefore the direct scalar really is zero and
there is no omitted \(sq^{[3]}\) term.  The response is

\[
 R_{pq}=-e_1^{(r)}e_1^{(s)}
        -e_2^{(r)}e_2^{(s)}.                             \tag{A15}
\]

Once \(r,s\) are occupied, the only internal matching on
\(\{u,v,w,x\}\) is \(uv\mid wx\), of weight \(1/2\).  Hence

\[
 R_{pq}q_{pq}^{[2]}
 =-\frac12(e_1^{(r)}e_1^{(s)}+e_2^{(r)}e_2^{(s)})
    e_0^{(u)}e_0^{(v)}e_0^{(w)}e_0^{(x)},               \tag{A16}
\]

exactly as claimed.  It is neither \(-X_1\) nor \(-X_2\).
The \(pr\)-chart is the endpoint-ordered relabelling with left shore
\(q,s\).

Changing only blocks inside \(D=\{u,v,w,x\}\) replaces the last factor
in (A16) by one arbitrary tensor \(Q_D\), while the left factor remains
\(R_{pq}\).  The result has rank at most one across \(rs\mid D\); the
binary target has rank two.  Thus no internal repair can work.  Also,
the two summands in (A15) occupy the same sites \(r,s\), so every product
of two response edges collides and \(R_{pq}^{[2]}=0\).  The old boundary
was clean; its exact failure was the physical complementary target row.

## 5. Complete deconcentrated-packet enumeration

Name the four internal edges

\[
 g_1=(bc)_1,\quad g_2=(ef)_1,\quad
 h_1=(ab)_2,\quad h_2=(de)_2.                           \tag{A17}
\]

Among their six unordered pairs, \(g_1h_1\) collides at \(b\) and
\(g_2h_2\) collides at \(e\).  The four terms of \(q^{[2]}\) are therefore

\[
 g_1g_2,\qquad h_1h_2,\qquad g_1h_2,\qquad g_2h_1,      \tag{A18}
\]

each with coefficient one.  There is no hidden factor \(2\): divided
powers list every unordered disjoint edge set once.

The endpoint rows in the primary give

\[
 R=-\rho_1-\rho_2,\qquad
 \rho_1=(ad)_1,\quad \rho_2=(cf)_2.                    \tag{A19}
\]

Every product is accounted for in the table:

\[
\begin{array}{c|cc|c}
q^{[2]}\text{ term}&\rho_1&\rho_2&\text{survivor}\\ \hline
g_1g_2&\text{disjoint}&\text{hits }c,f&-\!X_1\\
h_1h_2&\text{hits }a,d&\text{disjoint}&-\!X_2\\
g_1h_2&\text{hits }d&\text{hits }c&0\\
g_2h_1&\text{hits }a&\text{hits }f&0 .
\end{array}                                                   \tag{A20}
\]

It follows coefficientwise that

\[
                         Rq^{[2]}=-X_1-X_2.              \tag{A21}
\]

The response edges \((ad)_1\) and \((cf)_2\) are disjoint, so

\[
 R^{[2]}=(ad)_1(cf)_2\ne0.                              \tag{A22}
\]

There are only two response edges, and repeated use of either collides;
therefore \(R^{[3]}=0\).  The scalar-zero point is exactly clean.

The two endpoint-star maps are injective for the literal reason stated:
their rows land respectively at the three distinct sites
\((b,a,c)\) and \((e,d,f)\), with nonzero coordinate vectors.  Endpoint
order creates no transpose issue because each row is specified at its
named deleted endpoint and its output vector at the named residual site.

There is no missing direct contribution.  One may take the direct block
to have only an \(A_{00}=\sigma\) entry: \(E_{00}\) then has direct scalar
\(\sigma\), while

\[
 \langle E_{00}-I,A\rangle
 =A_{00}-\operatorname{tr}A=0.                         \tag{A23}
\]

The packet still does not supply the unary physical row—indeed it is
explicitly advertised only as the scalar-zero packet—so (A23) does not
silently complete the missing pair system.

## 6. Exact scope of the two-chart frontier

For one special line, absence of an active clean point is classified by
(A10) only under all of the following hypotheses:

1. \(K_0=E_{00}\) is a clean unary point with nonzero direct scalar;
2. \(K_1=E_{00}-I\) has zero direct scalar and its complete binary
   physical row;
3. \(K_1\) is also clean, equivalently \(R^{[3]}=0\).

The physical complementary row alone does not imply item 3; without it,
the \(u^3\Omega_2\) term remains.  The primary explicitly preserves this
distinction.

For two overlapping charts with \(AU-BF\ne0\), the proposed next theorem
would exclude the two bad residual patterns—independence or exactly one
zero—for both pairs \((\Omega_0,\Omega_1)\) simultaneously.  If proved,
at least one chart would fall into the nonzero-dependent or both-zero case,
and (A9)--(A10) would give an active clean point.  Neither the shore-rank
lemma nor the deconcentrated packet proves that simultaneous exclusion.
They only remove the old one-pair concentration and show that support
propagation by itself is consistent.

Accordingly, the primary makes no circular descent claim, no assertion
that a physical row is automatically clean, and no claim that the two
chart presentations are independent target equations.  Its final
two-chart statement is a precisely isolated missing lemma.
