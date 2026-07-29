# The eighth split: the five-triple monic-quadratic theorem

## 1. Result

At \((h,k)=(8,4)\), suppose that the collision profile contains at least
five value classes of multiplicity exactly three.

**Theorem 1.1.**  This configuration is impossible on the
no-extra-singular stratum.

For every three-set of exact triple values, its three legal
\((3,3,2)\) roles make the fourth common-pole Bell equation affine in the
role drop.  The vanishing slope gives one cubic Boolean identity on every
three-set.  A two-direction rectangle, with the fifth value fixed, says
that sums of two secant slopes of the role-three second jet are prescribed
by the role-three first jet.

Those secant identities force the five points \((A_x,B_x)\) to lie on a
monic quadratic

\[
                              B=A^2+qA+r.                \tag{1}
\]

This conclusion remains valid when the degree-two map \(x\mapsto A_x\)
has one or two double fibres.  Substitution of the exact jets in (1)
gives a nonzero polynomial of degree at most four with the five distinct
triple values as roots, a contradiction.

## 2. The identity on every triple

Use the notation of the six-triple fourth-order theorem.  For an exact
triple value \(x\), the dimensionless role-three logarithmic jets needed
here are

\[
 A_x=-{x+7\mu\over x^2-\mu^2},\qquad
 B_x={3\over(x+\mu)^2}+{4\over(x-\mu)^2}.               \tag{2}
\]

There is also an additive third jet \(C_x\), whose explicit value will
cancel below.  Let \(\alpha,\beta,\gamma\) be the background jets.
These are genuinely global constants.  In the full-multiset
normalization the regular cofactor for a selected set \(Y\) is

\[
                   U(w)\prod_{x\in Y}\widehat\rho_{r_x,x}(w),
\]

where the same unit \(U\) is used for every \(Y\); unselected classes are
already absorbed into \(U\).  Thus changing the three-set changes only
the displayed additive role jets, not the background.

The affine fourth-Bell cancellation proves that every three-set \(Y\) of
exact triple values satisfies

\[
\begin{split}
0=E(Y):={}&\gamma+C_Y+T_Y^3-{3T_Y^2\over2\mu}
 +3T_Y(\beta+B_Y)-{3(\beta+B_Y)\over2\mu},\\
&\hspace{35mm}T_Y=\alpha+A_Y.                           \tag{3}
\end{split}
\]

Indeed, the three cores assign role two to one member and role three to
the other two.  Each core selects eight labels and leaves the singleton
mate of the partial triple, so its Hermite residual is a nonzero constant.
This legality check is separate for each \(Y\), and does not require a
sixth triple value.  The three role-drop parameters are distinct because

\[
 d(x)=-{2\mu\over x^2-\mu^2},\qquad
 d(x)-d(y)={2\mu(x-y)(x+y)\over
 (x^2-\mu^2)(y^2-\mu^2)}\ne0
\]

for distinct, nonopposite exceptional values.  The affine fourth Bell
coefficient therefore has zero slope.  Consequently (3) is available for
all ten three-subsets of any chosen five triples, with the same
\(\alpha,\beta,\gamma\).  No other multiplicity class enters except
through that fixed background.

## 3. The fixed-fifth rectangle

Choose five distinct exact triple values.  For four of them write
\(a,b,c,d\), and call the fifth \(e\).  Take the alternating sum of (3)
on

\[
 \{e,a,c\},\quad\{e,a,d\},\quad
 \{e,b,c\},\quad\{e,b,d\}.                             \tag{4}
\]

Put

\[
 \delta_1=A_a-A_b,\quad \delta_2=A_c-A_d,\qquad
 \eta_1=B_a-B_b,\quad \eta_2=B_c-B_d.                 \tag{5}
\]

All additive terms disappear.  Exact polarization of the cubic,
quadratic, and bilinear terms gives

\[
 \delta_1\delta_2
 \left(2T_0+\delta_1+\delta_2-{1\over\mu}\right)
       +\delta_1\eta_2+\delta_2\eta_1=0,               \tag{6}
\]

where \(T_0=\alpha+A_e+A_b+A_d\).

If both \(\delta_i\) are nonzero, division and collection of the five
first jets yields

\[
 {B_a-B_b\over A_a-A_b}+{B_c-B_d\over A_c-A_d}+A_e=K, \tag{7}
\]

where

\[
                  K={1\over\mu}-2\alpha-\sum_xA_x      \tag{8}
\]

is independent of \(e\) and of the pairing.  If, say,
\(A_a=A_b\) while \(A_c\ne A_d\), the undivided equation (6) instead
gives \(B_a=B_b\).

## 4. A five-point secant lemma

We isolate the elementary geometry used in (7).

**Lemma 4.1.**  Let \((A_i,B_i)\), \(1\le i\le5\), be five indexed
points.  Assume every \(A\)-fibre has size at most two.  Suppose (7),
with one constant \(K\), holds whenever both displayed secants are
nonvertical, and suppose equal \(A\)-coordinates have equal
\(B\)-coordinates.  Then there are \(q,r\) such that

\[
                              B_i=A_i^2+qA_i+r           \tag{9}
\]

for all five indices.

**Proof.**  Put \(C_i=B_i-A_i^2\).  For nonvertical pairs, (7) becomes

\[
 {C_a-C_b\over A_a-A_b}+{C_c-C_d\over A_c-A_d}=K_0,
 \qquad K_0=K-\sum_iA_i.                               \tag{10}
\]

If the five \(A_i\)'s are distinct, every two disjoint secants in (10)
have complementary slopes.  Fix any three indices and use the other two
as one edge.  Fixing in turn each member of the three-set makes each of
its three internal edges complementary to that fixed edge.  Their three
slopes are therefore equal.  Thus every three of the five points are
collinear, so all ten secant slopes have one value; (10) makes that value
\(K_0/2\).  Hence \(C\) is affine in \(A\).

There are only two remaining multiplicity patterns.  In pattern
\((2,1,1,1)\), call the repeated coordinate \(X\) and the other three
coordinates \(Y,Z,W\).  Fixing \(Y,Z,W\) in turn and pairing the two
copies of \(X\) with the other two singletons gives

\[
 s_{XZ}+s_{XW}=K_0,\qquad s_{XY}+s_{XW}=K_0,\qquad
 s_{XY}+s_{XZ}=K_0.
\]

Consequently \(s_{XY}=s_{XZ}=s_{XW}=K_0/2\).  In pattern \((2,2,1)\),
write \(s_{XY},s_{YZ},s_{XZ}\) for the three block slopes.  The rectangle
with the singleton fixed, followed by rectangles fixing one copy in the
first and second double blocks, gives

\[
 2s_{XY}=K_0,\qquad s_{XY}+s_{YZ}=K_0,\qquad
 s_{XY}+s_{XZ}=K_0.
\]

Thus all three slopes are \(K_0/2\).  Equal-coordinate indices already
have equal \(C\)-coordinates.  Hence \(C_i=qA_i+r\) in every case,
proving (9).  \(\square\)

The first-jet map in (2) satisfies the fibre hypothesis.  For a scalar
\(\lambda\), its cleared fibre equation is

\[
                 \lambda(x^2-\mu^2)+x+7\mu=0,          \tag{11}
\]

a nonzero polynomial of degree at most two because its coefficient of
\(x\) is one.  Equation (6) supplies the equal-\(B\) conclusion on a
double fibre, since among the other three indices there is a nonvertical
pair.

## 5. The impossible quartic pullback

Apply Lemma 4.1 to (2).  Clearing \((x^2-\mu^2)^2\) from (1) gives

\[
\begin{split}
P(x)={}&3(x-\mu)^2+4(x+\mu)^2-(x+7\mu)^2\\
 &\quad+q(x+7\mu)(x^2-\mu^2)
       -r(x^2-\mu^2)^2.                                \tag{12}
\end{split}
\]

It has degree at most four.  It is not identically zero: its quartic
coefficient would first give \(r=0\), its cubic coefficient would then
give \(q=0\), while the remaining polynomial is

\[
                    6x^2-12\mu x-42\mu^2\ne0.          \tag{13}
\]

But (12) vanishes at the five distinct exact triple values.  This is
impossible and proves Theorem 1.1.

## 6. Fourth-order census consequence and audit

On the current frozen \((h,k)=(8,4)\) frontier, the theorem newly closes

\[
                         3^5 2\,1^5,\qquad 3^5 1^7.     \tag{14}
\]

It also independently covers every already-removed fourth-order profile
with at least five exact triple classes.

[verify_live_three_zero_eighth_split_k4_five_triple_monic_quadratic_closure.py](../computations/verify_live_three_zero_eighth_split_k4_five_triple_monic_quadratic_closure.py)
checks the fourth-Bell affine cancellation, the exact rectangle (6), all
three possible first-jet fibre patterns, the monic-quadratic secant lemma,
the nonzero quartic pullback, every legal \((3,3,2)\) core, and the exact
two-profile sequential census increment.
