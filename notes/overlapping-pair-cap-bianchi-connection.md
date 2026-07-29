# Overlapping pair caps carry an exact flat Bianchi connection

## 1. Outcome

Complete pair slices of one top matching tensor are only reindexings.  The
source variables nevertheless satisfy a stronger compatibility before the
lower common power is applied.  This note records that compatibility as an
exact flat connection on the canonical pair-cap quadratics.

Let \(|B|=2m\) with \(m\geq2\), put \(R=m-1\), and fix three distinct exposed sites
\(p,q,r\), with endpoint colours \(a,b,c\).  On their common complement
write \(z\) for the internal quadratic and \(x,y,t\) for the corresponding
three stars.  Abbreviate the direct entries

\[
 A=A_{pq}(a,b),\qquad B=A_{pr}(a,c),\qquad C=A_{qr}(b,c).           \tag{1}
\]

The restrictions of the two unnormalized canonical pair caps are

\[
 P_{pq}=Rxy+Az,\qquad P_{pr}=Rxt+Bz.                              \tag{2}
\]

Define the transition form

\[
                             D_{pq,pr}=At-By.                     \tag{3}
\]

Then the source variables obey the exact, power-free identity

\[
 \boxed{\quad P_{pq}t-P_{pr}y=D_{pq,pr}z.\quad}                   \tag{4}
\]

The normal star rows of the same two caps obey a companion connection
identity.  If

\[
 L_{pq;r}=R(By+Cx)+At,\qquad
 L_{pr;q}=R(At+Cx)+By,                                           \tag{5}
\]

then

\[
 \boxed{\quad L_{pq;r}-L_{pr;q}=-(m-2)D_{pq,pr}.\quad}            \tag{6}
\]

Equations (4) and (6), rather than a second list of top coefficients, are
the source-variable content of the overlap.  Multiplication by the two
successive divided powers makes their contributions cancel exactly.

With a fourth exposed site \(s\), colour \(d\), and abbreviations

\[
 E=A_{ps}(a,d),\quad F=A_{qs}(b,d),\quad U=A_{rs}(c,d),            \tag{7}
\]

write \(v\) for its star into the four-site common complement and put

\[
\begin{aligned}
 L_{pq;s}&=R(Ey+Fx)+Av,\\
 L_{pr;s}&=R(Et+Ux)+Bv,\\
 \kappa_{pq,pr;s}&=AU-BF.
\end{aligned}                                                     \tag{8}
\]

Taking the coefficient at \(s,d\) in (4) gives the four-site curvature
identity

\[
\boxed{
 UP_{pq}+tL_{pq;s}-FP_{pr}-yL_{pr;s}
       =D_{pq,pr}v+\kappa_{pq,pr;s}z.}                            \tag{9}
\]

The scalar curvature \(AU-BF\) is the difference between the exposed
pairings \((pq)(rs)\) and \((pr)(qs)\).  Cyclic comparison with the third
pairing \((ps)(qr)\) gives the exact first Bianchi relation

\[
 (AU-BF)-(AU-EC)+(BF-EC)=0.                                     \tag{10}
\]

The connection and curvature formulas are polynomial over \(\mathbb Z\)
and valid whenever the displayed exposed-site configuration exists.  The
mixed-partial cancellation below starts at \(m=3\), and the full four-cut
reconstruction is stated for \(m\geq4\); the smaller orders are the bare
matching identities with the nonexistent negative divided powers omitted.
The formulas retain arbitrary endpoint order, zero blocks, and complex
cancellation.  No source entry, common power, or cofactor is divided out.
Every direct symbol in (1), (7), and their later analogues denotes one
fixed endpoint-ordered scalar entry after the endpoint colours have been
chosen.  In particular, the displayed products are commutative scalar
products, not uncontracted matrix multiplication.

## 2. Canonical caps and normalization

For one deleted pair \(p,q\), let \(q_{pq}\) be the internal quadratic,
let \(p_a,s_b\) be its two endpoint stars, and let
\(A_{pq}(a,b)=A\).  The raw pair slice is

\[
 A q_{pq}^{[m-1]}+p_as_bq_{pq}^{[m-2]}
                       =\delta_{ab}X_a^{B\setminus\{p,q\}}.       \tag{11}
\]

Define the canonical unnormalized cap

\[
                     \mathcal P_{pq}^{ab}=R p_as_b+Aq_{pq}.       \tag{12}
\]

Since \(q_{pq}q_{pq}^{[m-2]}=R q_{pq}^{[m-1]}\), equation (11) is
equivalent to

\[
 \mathcal P_{pq}^{ab}q_{pq}^{[m-2]}
                =R\delta_{ab}X_a^{B\setminus\{p,q\}}.            \tag{13}
\]

This choice removes all fractions and is the reason the coefficient in
(6) is exactly \(m-2=R-1\).

On the common complement of \(p,q,r\), the internal restriction of
\(\mathcal P_{pq}^{ab}\) is the first quadratic in (2).  Its colour-\(c\)
star row at \(r\) is the first expression in (5): the two product terms
use respectively the direct blocks \(pr\), \(qr\), while the internal-cap
term contributes \(At\).  The formulas for the \(pr\) cap are symmetric.

Direct expansion now gives

\[
\begin{aligned}
 P_{pq}t-P_{pr}y
   &=(Rxy+Az)t-(Rxt+Bz)y\\
   &=(At-By)z,
\end{aligned}
\]

which proves (4), and

\[
 L_{pq;r}-L_{pr;q}
  =(R-1)(By-At)=-(m-2)D_{pq,pr},
\]

which proves (6).

## 3. Why the top exchange hides the connection

For \(m\geq3\), contract (13) at \(r,c\).  In one presentation the result is

\[
 L_{pq;r}z^{[m-2]}+P_{pq}t z^{[m-3]},                            \tag{14}
\]

and in the other it is

\[
 L_{pr;q}z^{[m-2]}+P_{pr}y z^{[m-3]}.                            \tag{15}
\]

Their difference is, by (4) and (6),

\[
 -(m-2)D_{pq,pr}z^{[m-2]}
       +D_{pq,pr}z z^{[m-3]}=0,                                  \tag{16}
\]

because

\[
                         z z^{[m-3]}=(m-2)z^{[m-2]}.              \tag{17}
\]

Thus mixed-partial exchange only sees the cancellation (16).  If the cap
quadratics have first been replaced by arbitrary representatives modulo an
annihilator of the lower power, (16) can remain true while the separate
source identities (4) and (6) are lost.  This identifies precisely what a
quotient-only overlap argument discards.

There is also a triangle cocycle.  With

\[
 P_{qr}=Ryt+Cz,
\]

the three transitions are

\[
 At-By,\qquad By-Cx,\qquad Cx-At,                                \tag{18}
\]

and their sum is zero before multiplication by any power.  This is the
flatness relation on the triangle of pair charts.

## 4. Four-site curvature and the raw four-cut tensor

Regard the triple complement as \(\{s\}\sqcup D\), and decompose

\[
 x'=x+e_d^{(s)}E,\quad y'=y+e_d^{(s)}F,\quad
 t'=t+e_d^{(s)}U,\quad z'=z+e_d^{(s)}v.                         \tag{19}
\]

The coefficient at \(s,d\) of the two sides of

\[
       (Rx'y'+Az')t'-(Rx't'+Bz')y'=(At'-By')z'                  \tag{20}
\]

is exactly (9).  This proves the curvature formula without a top-tensor
assumption.

For completeness, when \(m\geq 4\), (9) has the correct normalization for
the entire raw four-cut slice.  Put

\[
 Z_0=z^{[m-2]},\qquad Z_1=z^{[m-3]},\qquad Z_2=z^{[m-4]},         \tag{21}
\]

and let the direct double coefficients in the two pair charts be

\[
 M_{pq;rs}=R(BF+EC)+AU,
 \qquad M_{pr;qs}=R(AU+EC)+BF.                                  \tag{22}
\]

Their difference already records the scalar curvature:

\[
 M_{pq;rs}-M_{pr;qs}=-(m-2)(AU-BF)=-(m-2)\kappa_{pq,pr;s}.       \tag{22a}
\]

Thus (22a) is the direct-cap companion to the row-valued curvature
identity (9).

The double coefficient of the canonical \(pq\) cap is

\[
\begin{aligned}
 \mathcal B_{pq;rs}={}&M_{pq;rs}Z_0
 +(L_{pq;r}v+L_{pq;s}t+UP_{pq})Z_1\\
 &\quad+P_{pq}tvZ_2.                                             \tag{23}
\end{aligned}
\]

Using

\[
 zZ_1=(m-2)Z_0,\qquad zZ_2=(m-3)Z_1,                            \tag{24}
\]

one obtains

\[
\begin{aligned}
 \mathcal B_{pq;rs}=R\big[&(AU+BF+EC)Z_0\\
 &+(Atv+Byv+Eyt+Cxv+Fxt+Uxy)Z_1\\
 &+xytvZ_2\big].                                                \tag{25}
\end{aligned}
\]

The bracket is the complete four-site matching split: three two-direct
pairings, six direct-plus-two-star terms, and the four-star term.  The
\(pr\) and every other pair-cap presentation reduce to the same expression.
Equation (25) audits both factorial shifts in (23).

## 5. Exact constraint on simultaneous defect representatives

For an off-diagonal pair colour, the individual equation (13) generally
records \(\mathcal P_{pq}^{ab}\) only through its product with
\(q_{pq}^{[m-2]}\).  Suppose an elimination replaces the canonical caps by
candidate representatives \(\widehat P_{pq},\widehat P_{pr}\) having the
same individual Hessian products.  On a triple overlap define the raw
connection residual

\[
 \Omega_{pq,pr}
   =\widehat P_{pq}t-\widehat P_{pr}y-(At-By)z.                    \tag{26}
\]

A lift to one shared source requires the **literal cubic equation**

\[
                              \boxed{\Omega_{pq,pr}=0,}           \tag{27}
\]

not merely \(\Omega_{pq,pr}z^{[m-3]}=0\).  Its coefficient at every fourth
site is the curvature equation (9).  Around a triangle the three residuals
sum to zero with the natural orientations.

Consequently simultaneous E1/E2 defect coordinates cannot be selected
independently modulo \(\operatorname{Ann}(q^{[m-2]})\).  Their physical
quadratic representatives, normal star rows, and direct coefficients must
solve (27) on every triple and (9) on every fourfold overlap.  This is an
exact source-variable filter which the common-restriction and
common-\(q\) guards do not impose.

These identities are universal consequences of the source definitions,
not additional target equations.  Their value is that they exhibit the
exact Koszul-type homotopy which any quotient-level representatives must
lift.  They do not by themselves prove that all annihilator corrections
vanish.  The next precise lemma is acyclicity, or an adequate filtered
injectivity substitute, for the homogeneous overlap complex

\[
 (N_{pq})\longmapsto
       \bigl(N_{pq}|_{B\setminus\{p,q,r\}}t_c
             -N_{pr}|_{B\setminus\{p,q,r\}}y_b\bigr)_{p,q,r;a,b,c}.
                                                                    \tag{28}
\]

It would suffice to prove, on the active E1/E2 graph strata, that a family
of pair-Hessian annihilator corrections in the kernel of (28) is gauge or
forces the already registered sparse/low-rank alternatives.  That statement
is strictly smaller than reimposing all top coefficients, and (9) supplies
its first local curvature equations.

The dependency-free symbolic checker
[`verify_overlapping_pair_cap_bianchi_connection.py`](../computations/verify_overlapping_pair_cap_bianchi_connection.py)
expands (4), (6), (9), (10), the triangle cocycle, and both pair-cap forms
of (25) over \(\mathbb Z[R]\), reducing only by the two divided-power rules
in (24).
