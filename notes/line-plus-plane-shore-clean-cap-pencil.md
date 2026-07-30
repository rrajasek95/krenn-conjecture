# A line--plus--plane shore contains an exact clean-cap pencil

## 1. Outcome

Let \(W\) be the \(2h\)-site residual set of a physical pair cap,
\(h\geq 3\), and suppose its complete fixed-label rows are

\[
 a_{ij}q^{[h]}+p_i s_jq^{[h-1]}=\delta_{ij}X_i,
 \qquad 0\leq i,j\leq2.                                      \tag{1}
\]

Assume the two-site-complement shore produced by the uniform
selector-union theorem occurs.  Thus

\[
 W=A\sqcup B,\qquad B=\{u,v\},\qquad
 \operatorname {rank}P_A=1,\qquad
 \operatorname {rank}S_A=2.                                  \tag{2}
\]

Put

\[
 C_0=\ker P_A,\qquad \dim C_0=2,
 \qquad \ker S_A=\mathbb C d.                                \tag{3}
\]

This note proves that (2) already supplies a projective pencil of
**exact clean physical caps**:

\[
                         K_c=cd^{\mathsf T},qquad [c]\in
                         \mathbb P(C_0).                       \tag{4}
\]

Indeed, the response of every member of (4) is supported on the two
sites \(u,v\), so its second divided power is zero.  Its activity
polynomial is exactly

\[
 {\cal A}(c)=\bigl(c^{\mathsf T}ad\bigr)
                 \prod_{i=0}^2 c_i d_i.                       \tag{5}
\]

The complete target row rules out the only non-coordinate way for (5)
to vanish identically.  Consequently:

> **Clean-pencil reduction.**  If the source has no active clean cap,
> then at least one of the following fixed-coordinate degeneracies holds:
> \[
>       d_i=0\quad\hbox{for some }i,                           \tag{6}
> \]
> or
> \[
>       C_0=\{c:c_i=0\}\quad\hbox{for some }i.                \tag{7}
> \]
> In (7), the rank-one shore is literally one fixed row:
> \(P_A(c)=c_iU\), after scaling a nonzero linear form \(U\) on
> \(A\).

Thus the generic \(b=2\) shore is closed without a resultant, a selector
lift, or a support census.  The remaining \(b=2\) work is confined to
the two coordinate boundaries (6)--(7).  These boundaries are genuinely
smaller than the three alternatives in the abstract quotient
trichotomy: one kernel misses a fixed target label, or two fixed rows of
the rank-one endpoint live entirely on the two-site complement.

There is also a useful scalar-zero refinement.  For every
\(c\in C_0\) satisfying \(c^{\mathsf T}ad=0\),

\[
              \bigl|\{i:c_i d_i\ne0\}\bigr|\leq1.             \tag{8}
\]

If the set in (8) is a singleton \(\{t\}\), then the two-site response
and the top power on \(A\) are separately pure in label \(t\).  If it is
empty and \(q_A^{[h-1]}\ne0\), the response itself is zero.  These are
literal tensor-factor conclusions, not termwise inferences from a
cancelling matching sum.

The note does not claim that (6) or (7) is impossible.  It replaces the
previous unrestricted line--plus--plane shore by two fixed-label gates
which must be coupled to the remaining eight rows or to a one-site
quotient probe.

## 2. Cap notation and the clean error

Let \(C,D\cong\mathbb C^3\) be the fixed row and column label spaces and
write

\[
 P(c)=\sum_i c_i p_i,
 \qquad
 S(d')=\sum_j d'_j s_j.                                      \tag{9}
\]

For a pair covector \(K\in C\otimes D\), its direct scalar, response,
and target coefficients are

\[
 \sigma(K)=\sum_{i,j}K_{ij}a_{ij},\qquad
 r(K)=\sum_{i,j}K_{ij}p_i s_j,
 \qquad \kappa_i(K)=K_{ii}.                                 \tag{10}
\]

Contracting (1) gives

\[
 \sigma(K)q^{[h]}+r(K)q^{[h-1]}
       =\sum_i\kappa_i(K)X_i.                                \tag{11}
\]

The homogeneous canonical clean error is

\[
 {\cal E}(K)=\sum_{j=2}^{h}
       \sigma(K)^{h-j}q^{[h-j]}r(K)^{[j]}.                    \tag{12}
\]

A cap is active precisely when

\[
        \sigma(K)\kappa_0(K)\kappa_1(K)\kappa_2(K)\ne0,      \tag{13}
\]

and it is clean when \({\cal E}(K)=0\).  These are the exact
hypotheses of the clean-pair descent theorem.

For the rank-one matrix (4), equations (9)--(10) specialize to

\[
 \sigma(K_c)=c^{\mathsf T}ad,qquad
 r(K_c)=P(c)S(d),qquad
 \kappa_i(K_c)=c_i d_i.                                     \tag{14}
\]

No change of the fixed physical colour coordinates has been made in
(14).

## 3. The whole projective line is clean

By definition of the two shore kernels,

\[
                         P_A(c)=0,qquad S_A(d)=0              \tag{15}
\]

for every \(c\in C_0\).  Hence both linear forms \(P(c)\) and
\(S(d)\) are supported on \(B=\{u,v\}\).  Their product has no
same-site part in the site-square-zero algebra, so

\[
                         r(K_c)\in V_u\otimes V_v.             \tag{16}
\]

Every product of two elements of \(V_u\otimes V_v\) repeats both
sites.  Therefore

\[
                         r(K_c)^{[2]}=0.                       \tag{17}
\]

All terms of (12) contain \(r(K_c)^{[j]}\) with \(j\ge2\), so

\[
                    \boxed{{\cal E}(K_c)=0
                       \quad(c\in C_0).}                      \tag{18}
\]

This remains true when the response in (16) is zero.  It uses the actual
common quadratic \(q\) through (12), and is uniform in \(h\); no lower
power has been cancelled.

Combining (13), (14), and (18), the clean pencil contains an active point
if and only if the degree-four polynomial (5) is not identically zero on
the two-dimensional vector space \(C_0\).

## 4. The target row removes the scalar-only degeneration

Suppose first that

\[
 d_0d_1d_2\ne0                                               \tag{19}
\]

and that no fixed coordinate vanishes identically on \(C_0\).  In other
words, each restriction

\[
                         c\longmapsto c_i\bigm|_{C_0}          \tag{20}
\]

is a nonzero linear form.  Since the coordinate ring of \(C_0\) is an
integral domain, (5) can vanish identically only if

\[
                         c^{\mathsf T}ad=0
                         \quad\hbox{for all }c\in C_0.         \tag{21}
\]

Choose \(c\in C_0\) away from the three coordinate lines.  Then every
\(c_i d_i\) is nonzero.  Equation (21) makes the direct scalar zero, so
the complete contracted row (11) becomes

\[
       r(K_c)q^{[h-1]}=\sum_{i=0}^2c_id_iX_i.                 \tag{22}
\]

Let \(q_A\) denote the restriction of \(q\) to the \(2h-2\) sites of
\(A\).  Since every nonzero term of \(r(K_c)\) uses both \(u\) and
\(v\), every term of \(q^{[h-1]}\) meeting \(B\) collides with it.
Thus (22) is the literal flattening identity

\[
 r(K_c)\otimes q_A^{[h-1]}
   =\sum_{i=0}^2 c_i d_i
       \bigl(e_i^{(u)}e_i^{(v)}\bigr)\otimes Y_i^A,            \tag{23}
\]

where

\[
                         Y_i^A=\bigotimes_{x\in A}e_i^{(x)}.   \tag{24}
\]

The left side of (23) has Schmidt rank at most one across \(B\mid A\).
The three left factors \(e_i^{(u)}e_i^{(v)}\) are independent, as are
the three right factors \(Y_i^A\).  Because all three coefficients are
nonzero, the right side has Schmidt rank three.  This is impossible.

Consequently (21) cannot occur under (19)--(20), and (5) has a nonzero
value.  By (18), that value gives an active clean cap.  Taking the
contrapositive proves (6)--(7): if there is no active clean cap, either
some \(d_i=0\), or some coordinate restriction (20) is zero.

Finally, a two-dimensional subspace of \(\mathbb C^3\) on which the
\(i\)-th coordinate vanishes is the whole coordinate plane
\(\{c:c_i=0\}\).  Since \(P_A\) has rank one and kernel that plane, it
factors as

\[
                         P_A(c)=c_iU                         \tag{25}
\]

after scaling a nonzero shore form \(U\).  This proves the fixed-row
interpretation of (7).

## 5. The scalar-zero member has at most one target colour

The flattening argument did not require all three coefficients to be
nonzero.  Let \(c\in C_0\setminus\{0\}\) satisfy

\[
                         c^{\mathsf T}ad=0.                    \tag{26}
\]

Such a \(c\) always exists because (26) is one homogeneous linear
equation on the plane \(C_0\).  Equations (11), (16), and the same
collision calculation give

\[
 r(K_c)\otimes q_A^{[h-1]}
   =\sum_i c_i d_i
       \bigl(e_i^{(u)}e_i^{(v)}\bigr)\otimes Y_i^A.            \tag{27}
\]

The Schmidt rank of the right side is exactly the number of nonzero
products \(c_i d_i\), while the left side has rank at most one.  This
proves (8).

If the unique surviving label is \(t\), equality of two nonzero pure
tensors in (27) gives scalars \(\lambda,\mu\ne0\) with

\[
       r(K_c)=\lambda e_t^{(u)}e_t^{(v)},qquad
       q_A^{[h-1]}=\mu Y_t^A,qquad
       \lambda\mu=c_td_t.                                    \tag{28}
\]

If every product \(c_id_i\) is zero, (27) says

\[
                         r(K_c)\otimes q_A^{[h-1]}=0.          \tag{29}
\]

Over \(\mathbb C\), a tensor product of two vectors is zero only if one
factor is zero.  Hence \(q_A^{[h-1]}\ne0\) forces \(r(K_c)=0\), as
claimed.

## 6. Exact remaining gate

The selector-union classification leaves the \(b=2\) shore in three
local quotient forms, but Sections 3--4 show that all non-coordinate
members of those forms already contain an active clean cap.  Under the
global no-descent hypothesis, the only remaining coefficient geometries
are:

1. \(d_i=0\): the kernel line of the rank-two endpoint misses a fixed
   diagonal target label;
2. \(C_0=\{c:c_i=0\}\): the rank-one endpoint uses only row \(i\) on
   the large shore, while its other two fixed rows are supported on
   \(\{u,v\}\).

Equation (27) supplies a canonical clean scalar-zero member on either
boundary and limits its target to one label.  A closing argument may now
use the two local quotient maps at \(u,v\), or one additional diagonal
row, to show that the missing label enters the clean pencil.  What is no
longer needed is a general analysis of arbitrary line--plus--plane
shores.

This is a strict reduction, not a proof that the two coordinate gates are
empty.
