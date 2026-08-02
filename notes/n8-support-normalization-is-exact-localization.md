# Support normalization is the exact chart-localized problem

## 1. Outcome

Fix any one of the 31 eight-site pure-matching charts, with support monomial

\[
                         P=\prod_{e\in S}s_e,              \tag{1}
\]

where $S$ is the resulting perfect matching of the 24 vertex-colour
ports.  Localizing at $P$ and using the port torus gives an explicit
coordinate isomorphism

\[
 R[P^{-1}]
   \simeq
 \mathbb C[s_e^{\pm1}:e\in S]\otimes_{\mathbb C}\bar R,  \tag{2}
\]

under which every hafnian coefficient is a Laurent unit times a polynomial
in the 240 normalized off-support coordinates.  In particular, if
$\bar I_{\rm mix}$ is the ideal of the normalized mixed coefficients, then

\[
 \begin{aligned}
 H_0H_1H_2\in I_{\rm mix}R[P^{-1}]
 &\Longleftrightarrow
 \bar H_0\bar H_1\bar H_2\in\bar I_{\rm mix},\\
 H_0H_1H_2\in\sqrt{I_{\rm mix}R[P^{-1}]}
 &\Longleftrightarrow
 \bar H_0\bar H_1\bar H_2\in\sqrt{\bar I_{\rm mix}}.
                                                               \tag{3}
 \end{aligned}
\]

Thus the correct saturated calculation is obtained by setting the twelve
support variables to one and retaining all 240 other source coordinates.
This is not a heuristic affine slice.  It is the exact Laurent quotient,
and it automatically includes every support-exponent translation omitted
by a single balanced port-multidegree Macaulay component.

## 2. Explicit coordinates

Let

\[
                         \Omega=B\times\{0,1,2\}
\]

be the set of ports.  A source coordinate is an allowed edge $f=pq$ of
ports at distinct sites; write its variable as $x_f$.  The twelve support
edges $S$ pair every port exactly once.  For a port $p$, let $e(p)\in S$
be its support edge.  Choose one distinguished endpoint of every support
edge and put

\[
 \epsilon(p)=
 \begin{cases}
 1,&p\text{ is distinguished},\\
 0,&p\text{ is not distinguished}.
 \end{cases}
\]

For every off-support coordinate $f=pq\notin S$, define

\[
       y_f=x_f s_{e(p)}^{-\epsilon(p)}
                  s_{e(q)}^{-\epsilon(q)}.                \tag{4}
\]

For a support edge $e=pq$, exactly one endpoint is distinguished, so the
same formula would give $x_e s_e^{-1}=1$.  Conversely,

\[
       x_f=y_f s_{e(p)}^{\epsilon(p)}
                  s_{e(q)}^{\epsilon(q)},qquad
       x_e=s_e.                                            \tag{5}
\]

Equations (4)--(5) are inverse monomial changes of variables and prove (2).
They are the algebraic form of the port-torus normalization which scales
the distinguished endpoint of $e$ by $s_e^{-1}$ and leaves its other
endpoint fixed.

Localizing at the product $P$ really does invert every $s_e$: in
$R[P^{-1}]$,

\[
                         s_e^{-1}={\prod_{e'\ne e}s_{e'}\over P}.
\]

No additional localization is being assumed.

## 3. Every coefficient separates into a unit and a normalized polynomial

For a word $c:B\to\{0,1,2\}$, let

\[
                         T_c=\{(v,c(v)):v\in B\}\subset\Omega
\]

be its port transversal, and put

\[
             m_c(s)=\prod_{p\in T_c}s_{e(p)}^{\epsilon(p)}. \tag{6}
\]

Every matching monomial in $H_c$ uses every port of $T_c$ exactly once.
Substituting (5), its entire support-variable factor is therefore (6),
independently of which perfect matching of the eight sites is used.  Hence

\[
                         H_c(x)=m_c(s)\bar H_c(y),          \tag{7}
\]

where $\bar H_c\in\bar R=\mathbb C[y_f:f\notin S]$.  Since $m_c$ is a
unit in (2), the localized mixed ideal is exactly

\[
 I_{\rm mix}R[P^{-1}]
   =\bar I_{\rm mix}\,
      \mathbb C[s_e^{\pm1}:e\in S]\otimes\bar R.          \tag{8}
\]

The three constant words partition all 24 ports.  Exactly one endpoint of
each support edge is distinguished, and therefore

\[
                         m_0m_1m_2=\prod_{e\in S}s_e=P.    \tag{9}
\]

Combining (7)--(9) gives

\[
                         H_0H_1H_2
                           =P\bar H_0\bar H_1\bar H_2.    \tag{10}
\]

Laurent polynomial extension is faithfully flat, so ideal membership and
radical membership of an element of $\bar R$ are detected before or after
adjoining the $s_e^{\pm1}$.  Equations (8)--(10) prove both equivalences
in (3).

There is also a certificate form.  Any normalized identity

\[
       (\bar H_0\bar H_1\bar H_2)^r
          =\sum_{c\;\mathrm{mixed}}\bar Q_c\bar H_c       \tag{11}
\]

lifts through (4)--(7) to a Laurent identity in $R[P^{-1}]$.  Only
finitely many negative support exponents occur, so multiplying by $P^N$
for their maximum absolute size clears them all and gives

\[
             P^N(H_0H_1H_2)^r\in I_{\rm mix}.             \tag{12}
\]

This is exactly the polynomial certificate required by the 31-chart cover.

## 4. Why this is the next degree-six calculation

The current chart-26 lift was organized in the balanced degree-twelve,
24-port component.  That component is useful for exact source provenance,
but it fixes one representative of the support-exponent lattice.  A left
kernel there proves exponent-one nonmembership only if it also annihilates
all Laurent translations.  Formula (2) supplies the clean test: rebuild the
filtered system after setting the support variables to one.

In the normalized system every $\bar H_c$ has off-support degree at most
four and $\bar H_0\bar H_1\bar H_2$ has degree at most twelve.  This bounds
the input polynomials, but it does **not** by itself make the normalized
Macaulay component finite.  Some mixed coefficients have a constant support
term; multiplying an inhomogeneous relation can create a higher-degree tail,
whose cancellation can create another tail, and so on.  Equivalently, the
support-exponent lattice which has just been quotiented out can have
degree-zero translation loops.  A normalized computation is a proof only
after it supplies a finite certificate or a well-founded contraction
statistic; a degree-truncated rank is not enough.

The restricted 60-edge certificate supplies the starting lift, while the
192 restored off-carrier coordinates enter as filtration-raising
perturbations.  The filtered Morse contraction of
[`filtered-macaulay-morse-contraction-target.md`](filtered-macaulay-morse-contraction-target.md)
applies once its acyclicity and finite-path hypotheses are verified in this
normalized module.

There are two informative outcomes.

1. Additional normalized columns kill the balanced degree-six dual.  Then
   the dual was a missing-Laurent-translation artifact, and its repair paths
   identify the support shifts needed by a saturated contraction.
2. The dual survives the normalized system.  Then it is a genuine critical
   class for exponent-one localized membership; the next honest target is
   its pairing with a power of the normalized pure product, not a raw
   port-degree-two enumeration before quotienting by the support torus.

Neither outcome by itself resolves radical membership, but both address the
actual localized chart rather than a smaller balanced ansatz.

## 5. Scope

The argument is valid for every one of the 31 support charts and, with
$3n/2$ support coordinates, at every even order.  It uses only that the
selected three pure matching monomials form a perfect matching of all
vertex-colour ports.  It assumes no same-colour condition on any restored
coordinate and no restriction on complex coefficients.

This note proves the normalization equivalence, not membership in the
normalized ideal.  Krenn's conjecture remains open.
