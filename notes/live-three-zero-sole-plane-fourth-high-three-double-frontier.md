# The (2^3 1^7) sole-plane frontier: exact necessary ideal, open fibres

## 1. Status

This note refines the first dense-double residual in
[live-three-zero-sole-plane-fourth-high-frontier.md](live-three-zero-sole-plane-fourth-high-frontier.md):

\[
                             2^3 1^7.                         \tag{1}
\]

It does **not** close (1).  It constructs six denominator-free necessary
parameter polynomials for a counterexample and identifies their exact
parameter-at-infinity boundary.  The remaining affine fibres and the two
infinity directions are open.

The exact reproducibility audit is

```text
uv run python computations/verify_live_three_zero_sole_plane_fourth_high_three_double_frontier.py
```

It checks all identities in this note over \(\mathbb Q\).  In particular,
no finite-field UNIT is used as a characteristic-zero conclusion.

## 2. Cleared order-three row

Let \(a\) be a selected double value.  Write \(P\) for the effective first
logarithmic derivative and \(R=P^2+W\), where \(W\) is the effective second
logarithmic derivative.  With

\[
 d_a=x^2-a^2,
\]

the first two cleared order-three conditions are the row

\[
\begin{aligned}
 M_a={}&R d_a^2-2P d_a(x+3a)
          +4(x^2+2ax+3a^2),\\
 N_a={}&2P d_a^2-2d_a(x+3a)-aM_a.             \tag{2}
\end{aligned}
\]

The checker expands (2) against the earlier `triple_quadratic_row` formula.
It also verifies scale covariance.  Under

\[
 x=cX,\qquad a=cA,\qquad P=c^{-1}\widehat P,
 \qquad R=c^{-2}\widehat R,
\]

one has

\[
                    M_a=c^2M_A,qquad N_a=c^3N_A.             \tag{3}
\]

Thus a pair determinant scales by \(c^5\), and one repeated value can be
normalized to \(1\).

Changing the selected partner at anchor \(a\) from \(b\) to \(c\) uses

\[
\begin{aligned}
 \chi(a,s)&={2\over a+s}-{3\over s-a},\\
 \eta(a,s)&={2\over(a+s)^2}+{3\over(s-a)^2},\\
 \delta&=\chi(a,c)-\chi(a,b),\\
 \epsilon&=\eta(a,c)-\eta(a,b),                               \tag{4}
\end{aligned}
\]

and the exact exchange

\[
       P\longmapsto P+\delta,qquad
       R\longmapsto R+2P\delta+\delta^2+\epsilon.             \tag{5}
\]

## 3. Three pair determinants

Normalize the three double values to \(1,v,w\).  For a selected pair put

\[
                         F_{ab}=M_aN_b-N_aM_b.                \tag{6}
\]

This has degree at most eight.  It vanishes at the seven singleton values
and at the unselected double value.  If its leading coefficient vanished,
it would have degree at most seven and eight distinct roots, hence would be
identically zero.  The sparse two-double UNIT lemma from the preceding
frontier excludes that identity on the structural locus.  Therefore each
pair determinant is nonzero of degree eight, and for the singleton
polynomial \(S\),

\[
\begin{aligned}
 F_{1v}&=k_{1v}S(x)(x-w),\\
 F_{1w}&=k_{1w}S(x)(x-v),\\
 F_{vw}&=k_{vw}S(x)(x-1),                                    \tag{7}
\end{aligned}
\]

with nonzero \(k_{ab}\).  Consequently there are nonzero multipliers
\(\lambda,\mu\) for which

\[
\begin{aligned}
 C_1(x)&=(x-v)F_{1v}-\lambda(x-w)F_{1w}=0,\\
 C_2(x)&=(x-1)F_{1v}-\mu(x-w)F_{vw}=0.                        \tag{8}
\end{aligned}
\]

The local coordinates are

\[
 P_0,R_0,P_v,R_v,P_w,R_w,P_{vw},R_{vw},P_{wv},R_{wv},
 \lambda,\mu,                                                \tag{9}
\]

where the four exchanged coordinates satisfy (5).

## 4. Exact coefficient-field lifts and specialization audit

For either polynomial in (8), use its values at

\[
                 v,w,1,-1,-v,-w,0                            \tag{10}
\]

and its first derivatives at \(-v,-w,0\).  The first identity gives ten
equations.  The two identities together with the four exchange equations
give twenty-four.

Over \(\mathbb Q(v,w)\), exact `liftstd` computations return a constant for
both systems.  A generic coefficient-field UNIT alone would not control
exceptional parameter values.  Here the lift matrices themselves were
audited coefficient by coefficient:

\[
\begin{array}{c|c|c|c}
\text{system}&\text{lift shape}&\text{coefficient terms}
             &\operatorname{lcm}(\text{coefficient denominators})\\ \hline
C_1&10\times1&34&1\\
C_1,C_2,\text{ exchanges}&24\times1&48&1.
\end{array}                                                   \tag{11}
\]

Moreover, the denominators already present in the input equations factor
only into

\[
 v,\ w,\ v\pm1,\ w\pm1,\ v\pm w.                            \tag{12}
\]

These are structural nonzero factors.  Thus clearing the input
denominators in the two lift identities introduces no hidden
nonstructural specialization locus.

Let \(H(v,w)\) and \(B(v,w)\) be the two constant lift outputs.  Remove all
factors from (12), which is legitimate on the characteristic-zero
structural locus, and apply the three cyclic changes of normalized anchor.
This gives six denominator-free necessary polynomials

\[
                    h_1,h_2,h_3,b_1,b_2,b_3,                 \tag{13}
\]

with exact total degrees

\[
                   30,30,30,48,48,48.                        \tag{14}
\]

Every putative counterexample to (1) must satisfy all six equations in
(13).

## 5. Exact parameter-infinity boundary

Homogenize each polynomial in (13) and restrict it to the line at infinity.
Over \(\mathbb Q\), the gcd of the six resulting binary leading forms is

\[
                              v^6w^6.                         \tag{15}
\]

Hence the six necessary conditions have only two possible common parameter
directions at infinity:

\[
                            [v:w]=[1:0],\qquad[0:1].           \tag{16}
\]

Equation (15) is only a boundary reduction.  It does not exclude either
direction, and it does not settle the affine fibres of (13).

## 6. Discovery computation that is not a proof

Modulo \(32003\), the six-polynomial ideal in (13) is zero-dimensional and
has a 19-element reduced basis in the order used by the exploration
script.  Adding the full twenty-four equations and localizing at the
structural product in (12) gives a UNIT modulo \(32003\).

This is useful discovery evidence but is not a characteristic-zero
certificate.  Two losses remain:

1. an affine UNIT after reduction modulo one prime does not imply a UNIT
   over \(\mathbb Q\); for example,
   \(\langle 32003z-1\rangle\) is proper over \(\mathbb Q\) but reduces to
   the unit ideal modulo \(32003\);
2. the structural product can be nonzero in characteristic zero while its
   reduction vanishes, and local coordinates can reduce on a projective
   infinity chart.

An exact modular-reconstruction attempt over \(\mathbb Q\) timed out, and
the no-localizer projective affine-fibre computation did not finish in a
bounded window.  Neither result is promoted here.

## 7. Concrete next steps

A closure of (1) now has two reasonably sharp routes:

1. compute a characteristic-zero certificate for the affine fibres of
   (13), retaining the full twenty-four equations; or
2. give a proper modular certificate: cover all local projective charts,
   including reductions on the eight structural divisors in (12), and
   separately exclude the two parameter directions (16).

Until one route succeeds, the correct registry status of \(2^3 1^7\) is
**open**.  The later dense-double profiles \(2^4 1^5,2^5 1^3,2^6 1\)
remain open as well.
