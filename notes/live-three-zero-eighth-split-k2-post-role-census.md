# The eighth split at \(k=2\): post-role incremental census

## 1. Result

Start from the frozen sixteen-profile residual set in
[the updated \(k=2\) census](live-three-zero-eighth-split-k2-updated-census.md).
Two subsequent proved routes apply:

1. the order-two four-role common-pole theorem; and
2. the unique-bad-core exchange repair, using both endpoint branches of
   its exact criterion.

The first route closes eight of the sixteen profiles.  The second adds two
more, disjointly.  Therefore the current residual set at

\[
                  h=8,\qquad p=10,\qquad k=2,
                  \qquad M=20                              \tag{1}
\]

has exactly six profiles.

Including the frozen earlier categories, the sequential count is now

\[
\begin{array}{c|rrrrrrrrrrrrr}
 &H&S&C&L&Q&V&M&A&O&T&U&R&D\\ \hline
 (8,10)&263&270&22&14&12&3&5&18&3&8&2&6&1.
\end{array}                                                \tag{2}
\]

Here \(T\) is the four-role theorem and \(U\) is the new endpoint branch
of the unique-bad-core repair.  The earlier \(O\) category already
credited the \(n_1=8\) branch, so \(U\) records only genuinely new credit.

## 2. Audit of the four-role hypothesis

The algebraic theorem in
[the order-two common-pole closure](live-three-zero-eighth-split-443333-order-two-common-pole-closure.md)
requires four value classes of multiplicity at least three with the
following property: on every three of the four classes, all three
distinguished assignments

\[
                              (3,3,2)                     \tag{3}
\]

leave a singleton class in the complement.

Each core in (3) selects eight labels in three value classes.  Its Hermite
residual is therefore a nonzero constant.  The exact order-two residue at
the common pole, compared across the twelve assignments, forces the four
values into one fibre of

\[
                   \phi_3(x)=-{x+7\mu\over x^2-\mu^2}.   \tag{4}
\]

Every fibre of (4) has size at most two, including the degree-drop case,
whereas the four value classes are distinct.  The role-drop difference is

\[
 d(x)-d(y)=
 {2\mu(x-y)(x+y)\over
  (x^2-\mu^2)(y^2-\mu^2)},                               \tag{5}
\]

so no comparison silently divides by zero: \(\mu\ne0\), and distinct
exceptional value classes are nonopposite and separated from
\(\pm\mu\).

For the frozen sixteen profiles, literal search for the full twelve-core
legality condition is equivalent to having at least four classes of
multiplicity at least three.  It closes exactly

\[
\begin{gathered}
 4^2 3^4,\qquad 3^6 2,\qquad 3^4 2^4,\qquad 3^6 1^2,\\
 3^5 2 1^3,\qquad 3^4 2^2 1^4,\qquad
 3^5 1^5,\qquad 3^4 2 1^6.                               \tag{6}
\end{gathered}
\]

All eight profiles in (6) contain at least four exact triple classes, so
one may choose those four: the distinguished role-two class itself then
leaves the required singleton.  This gives a direct legality witness for
every application, rather than relying only on the numerical
high-class count.

For overlap bookkeeping, the four-role theorem applies to ten of the 42
old \(H/S/C/L/Q/V\) residuals.  One was already credited to the all-\(k\)
moving-role route and one to the original \(n_1=8\) repair; it has no
overlap there with the legal-exchange antiderivative route.  The remaining
eight are precisely (6).

## 3. The unique-bad-core increment

If \(n_1,n_2,n_{\ge3}\) denote the counts of singleton, double, and higher
classes, the number of illegal eight-cores is

\[
                 \binom{n_{\ge3}}{8-n_1}.                \tag{7}
\]

It is one exactly when

\[
                              n_1=8
                       \quad\hbox{or}\quad c-n_2=8.       \tag{8}
\]

The frozen census had already credited the first branch.  The second
branch, followed by the collision-excess theorem, newly closes

\[
                         3^2 2^4 1^6,qquad
                         3\,2^5 1^7.                     \tag{9}
\]

Both have excess at most eight.  Neither has four high classes, so (9) is
disjoint from (6).  The general repair is proved in
[the unique-bad-core note](live-three-zero-higher-split-unique-bad-core-repair.md).

## 4. The exact six-profile frontier

Ordering as before by \((c,e,\lambda)\), the profiles left after (6) and
(9) are exactly

\[
\begin{array}{c|c|l}
c&e&\lambda\\ \hline
10&10&2^{10}\\
10&10&3\,2^8 1\\
11& 9&2^9 1^2\\
11& 9&3\,2^7 1^3\\
11& 9&3^3 2^3 1^5\\
12& 8&3^3 2^2 1^7.
\end{array}                                                \tag{10}
\]

Thus the next unresolved profile is

\[
                              \boxed{2^{10}}.             \tag{11}
\]

This is the ten-double profile.  It has no singleton class, every
one-label-per-class eight-core selects eight double classes, and every
selected class leaves its mate as a singleton in the complement.  Thus
ordinary value-core exchange is legal.  Its obstruction is instead the terminal excess
\(e=10\), two beyond the present \(e\le8\) antiderivative bound.

## 5. Exact audit

[verify_live_three_zero_eighth_split_k2_post_role_census.py](../computations/verify_live_three_zero_eighth_split_k2_post_role_census.py)
reconstructs the frozen sixteen-profile set, searches the twelve-core
legality hypothesis literally, reruns the exact logarithmic-jet and
degree-two-fibre checks, verifies all route overlaps, applies the complete
unique-bad-core endpoint criterion, and compares the six profiles in (10)
term by term.
