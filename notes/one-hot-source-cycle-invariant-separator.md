# Source cycle invariants separate the one-hot boundary orbit

## Outcome

The source quotient behaves strictly better than the target quotient on the
known Laurent boundary.  For every mixed perfect matching \(M\) of the
properly coloured one-hot support, there is an explicit polynomial invariant
of the affine GHZ-stabilizer port torus which

\[
                    \text{equals }1\text{ on the boundary source orbit}
 \quad\text{and}\quad
                    \text{vanishes on every exact GHZ source}.  \tag{1}
\]

The invariant is

\[
 \boxed{
 I_M(A)=H_{m(M)}(A)
          \prod_{e\in E(G)\setminus M}A_e^{c(e)c(e)}.}    \tag{2}
\]

Here \(H_{m(M)}\) is the complete matching-output coefficient on the full
arbitrary-matrix source space, not its restriction to the one-hot chart.
Thus (2) remains a regular invariant with arbitrary endpoint colours and
arbitrary complex weights.

Consequently the source affine quotient does **not** identify the finite
all-unit boundary orbit with a hypothetical exact GHZ preimage.  By
contrast, Hilbert--Mumford polystability alone does not separate them: the
all-unit boundary source is polystable, and any nonempty exact fiber contains
a polystable orbit.

This does not prove that the exact fiber is empty.  The factor
\(H_{m(M)}\) makes (2) vanish there by the defining mixed equation.  The
lemma shows that source GIT retains the zero-times-infinity datum erased by
the target quotient; using it to prove Krenn's conjecture would require a
second argument forcing some \(I_M\ne0\) on an exact source.

## 1. Full arbitrary-colour source action

Let \(B\) have even cardinality \(n\), let \(V_v=\mathbb C^3\), and use the
full source space

\[
                  W=\bigoplus_{u<v}V_u\otimes V_v.        \tag{3}
\]

Write \(a_{uv}^{ij}\) for its endpoint-ordered coordinates.  The affine
torus fixing ternary GHZ exactly is

\[
 T_\Delta=\left\{(\lambda_{v,c}):
                   \prod_{v\in B}\lambda_{v,c}=1
                   \quad(c=0,1,2)\right\}.               \tag{4}
\]

It acts by

\[
                 a_{uv}^{ij}\longmapsto
                 \lambda_{u,i}\lambda_{v,j}a_{uv}^{ij}.  \tag{5}
\]

For a word \(m\in\{0,1,2\}^B\), the full output coefficient is

\[
 H_m(A)=\sum_{N\in\operatorname{PM}(B)}
                  \prod_{uv\in N}a_{uv}^{m_um_v}.        \tag{6}
\]

Every summand in (6) uses exactly one port \((v,m_v)\) at every vertex.
Therefore \(H_m\) is a semi-invariant with character

\[
                         \chi_m=\sum_{v\in B}e_{v,m_v}.   \tag{7}
\]

No support, rank, same-colour, or reality assumption is used in (6)--(7).

## 2. Completing a mixed coefficient to a port cycle

Now fix a properly three-edge-coloured cubic graph \(G\), with edge colour
\(c(e)\), and put

\[
                         z_e=a_e^{c(e)c(e)}.              \tag{8}
\]

Every vertex has one incident edge of every colour.  Hence the support
product

\[
                         P_G=\prod_{e\in E(G)}z_e         \tag{9}
\]

uses each port \((v,c)\) exactly once.  Its ambient weight is

\[
                         \sum_{v,c}e_{v,c},               \tag{10}
\]

which restricts trivially to (4).

Let \(M\) be a perfect matching of \(G\), and let \(m=m(M)\) be its colour
word.  The matching monomial

\[
                         z_M=\prod_{e\in M}z_e            \tag{11}

has character \(\chi_m\): at each vertex, the edge used by \(M\) has colour
\(m_v\).  Since \(M\subseteq E(G)\), the quotient

\[
                         Q_M=P_G/z_M
                             =\prod_{e\in E(G)\setminus M}z_e \tag{12}
\]

is a polynomial monomial, not a Laurent function.  Its character is the
restriction of (10) minus \(\chi_m\), hence \(-\chi_m\) on \(T_\Delta\).
Multiplying (6) by (12) proves that (2) is a regular
\(T_\Delta\)-invariant polynomial on all of \(W\).

There is a useful termwise description.  Every monomial of \(H_m\) uses
port \((v,m_v)\) once.  The complement monomial \(Q_M\) uses the other two
ports at \(v\) once each, because the one support edge omitted at \(v\) is
the matching edge of colour \(m_v\).  Thus every monomial of \(I_M\) has
incidence exactly one at all \(3n\) ports.  It is literally a balanced
source cycle invariant of degree

\[
                    \deg I_M={n\over2}+n={3n\over2}.       \tag{13}
\]

This proves invariance directly, including for the arbitrary endpoint-
colour terms in (6).

## 3. Exact separation

Let \(A_*\) be the all-unit one-hot source on \(G\).  Proper edge colouring
implies that a colour word determines a supported matching: at each vertex,
the word selects its unique incident edge of that colour.  Hence

\[
                         H_{m(M)}(A_*)=1,\qquad Q_M(A_*)=1,
\]

and therefore

\[
                              I_M(A_*)=1.                 \tag{14}
\]

For the Laurent source \(A(t)\), let \(d_M\) be the valuation of \(z_M\).
The normalized products of the three colour matchings give

\[
                         P_G(A(t))=1.                     \tag{15}
\]

Word uniqueness gives \(H_{m(M)}(A(t))=t^{d_M}\), while (12) and (15) give
\(Q_M(A(t))=t^{-d_M}\).  Thus

\[
                              I_M(A(t))=1                 \tag{16}

for every \(t\ne0\), making the pole compensation completely explicit.
This agrees with the fact that \(A(t)\) is one
\(T_\Delta\)-orbit of \(A_*\).

If \(A\) is any finite exact GHZ source in the full arbitrary-matrix space,
then every mixed output coefficient vanishes.  Since \(m(M)\) is mixed for
an extra non-colour matching,

\[
                         H_{m(M)}(A)=0,\qquad I_M(A)=0.   \tag{17}

Equations (14) and (17) prove (1).  In quotient language, if
\(\pi_W:W\to W/\!/T_\Delta\), then

\[
                  \pi_W(A_*)\notin
                  \pi_W\bigl(H^{-1}(\Delta)\bigr).       \tag{18}

This is a concrete polynomial separation, stronger than merely observing
that the two closed sets ought to have different quotient points.

At six sites, (2) is the invariant form of the familiar identity
\(rq=p_0p_1p_2\) on the sparse prism chart: \(H_m=r\), the complement
monomial is \(q\), and their product stays one along the Laurent arc.  The
construction above shows that this is not a special six-site accident.

## 4. What Hilbert--Mumford does and does not add

The all-unit source orbit is polystable.  The monomial \(P_G\) is invariant,
nonzero at \(A_*\), and contains every supported coordinate with positive
exponent.  It cannot remain nonzero at an orbit-boundary point which loses
one of those coordinates.  Inside the support coordinate torus the orbit is
a closed subtorus coset, so the full orbit is closed.

If the exact affine fiber \(H^{-1}(\Delta)\) is nonempty, it also contains a
closed torus orbit: choose an orbit of minimum dimension in that closed
invariant fiber; a nonclosed orbit would have a smaller-dimensional orbit in
its boundary.  Thus the Boolean statement “polystable or not” holds on both
sides and cannot separate them.

The cycle invariant (2) does separate their quotient points.  Its limitation
is equally precise: it belongs to the invariant part of the ideal generated
by a mixed output equation.  It proves that the known border degeneration
does not contaminate the source quotient, but it does not supply a
contradiction inside the exact fiber.  A source-GIT proof would still need a
reason, independent of the equation \(H_m=0\), that some completed cycle
\(I_M\) must be nonzero at a polystable exact representative.

## 5. Exact verification

The standard-library checker
[verify_one_hot_source_cycle_invariant_separator.py](../computations/verify_one_hot_source_cycle_invariant_separator.py)
uses the independently audited all-even graph generator and, through
\(n=18\), checks every mixed matching.  For each one it verifies:

- the complement monomial completes the word weight to incidence one at
  every port;
- \(\deg H_m=n/2\), \(\deg Q_M=n\), and
  \(\deg I_M=3n/2\);
- the Laurent orders \(d_M\) and \(-d_M\) cancel exactly; and
- the values are one on the all-unit boundary orbit and zero on the exact
  GHZ fiber.

The counts of explicit separators at orders
\(6,8,10,12,14,16,18\) are

\[
                         1,2,3,5,7,9,13.
\]

Normal, optimized, isolated, and no-site-library runs have digest

    1900ea5daa293e529a938ab388066908199890cf861216019eb0031e7487a547
