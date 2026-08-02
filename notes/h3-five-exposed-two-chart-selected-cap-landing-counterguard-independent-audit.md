# Independent audit: five-exposed selected-cap landing counterguard

Audit target: commit `7ed244e`, restricted to its checker and note.  The
certificate passes at its stated selected-coefficient scope.  This audit also
adds an executable scope guard: the base and tilted packets fail the full
tensor-valued `pq` EqSystem in exactly six and seven coefficients,
respectively.

No claim about a ternary source, the full eight-site EqSystem, the unified
full-nine theorem, SP-CLEAN-BRIDGE, or Krenn's conjecture follows from this
packet.

## 1. Independent reconstruction

The independent
[checker](../computations/verify_h3_five_exposed_two_chart_selected_cap_landing_counterguard_independent_audit.py)
does not import the primary checker.  Each packet is entered once as a table

\[
 (a,b,\alpha,\beta)\longmapsto w_{ab}^{\alpha\beta}\in\mathbb Q
\]

on the same eight physical sites.  The `pq` chart deletes sites $p=6,q=7$.
The `pr` chart deletes $p=6$ and the physical site $r$ (site $3$ in the
base packet and site $1$ in the tilted packet), while site $q=7$ becomes a
residual port.  Both chart blocks, stars, internal quadratics, caps, and
crossed coefficients are read from this one table.  There is no independent
chart relabelling or duplicated block from which compatibility could be
assumed.

For the base `pq` chart, the residual quadratic and labels reconstruct as

\[
q=01+02+04+05+12+14+23+34+35,
\qquad (0,1,2,0,1,2).
\]

The residual hafnian is $4$, and the endpoint-star cofactor matrix is

\[
H_\times=
\begin{pmatrix}0&1&2\\0&2&2\\1&1&1\end{pmatrix}.
\]

Consequently the independently read direct block is

\[
A_{pq}=-\frac14H_\times=
\begin{pmatrix}
0&-1/4&-1/2\\0&-1/2&-1/2\\-1/4&-1/4&-1/4
\end{pmatrix}.
\]

For each of the nine endpoint-colour pairs, direct matching enumeration
checks the scalar cap formula

\[
A_{ij}\operatorname{Haf}(q)+
\sum_{u\ne v}p_i(u)s_j(v)
\operatorname{Haf}(q|_{[6]\setminus\{u,v\}})=0.       \tag{A1}
\]

The same enumeration is repeated for the nine `pr` cap rows.  In the base
packet the entire `pr` direct block and all nine responses vanish.  Thus all
18 selected coefficients vanish without treating a chart-local symbolic
matrix as independent data.

For the crossed target-zero row, the checker fixes the four boundary colours
$(p,q,r,s)=(2,0,0,2)$ in the base packet and $(0,1,1,2)$ in the tilted
packet.  It then enumerates every assignment on the four complementary sites.
All $3^4=81$ physical matching coefficients vanish in each packet.  All four
endpoint-star ranks (`pq` left/right and `pr` left/right) are three.

## 2. Overlap signs and Euler normalization

Write

\[
(A,B,C,E,F,U)
=(w_{pq},w_{pr},w_{qr},w_{ps},w_{qs},w_{rs}),
\quad D=At-By,
\quad \kappa=AU-BF.
\]

An independent squarefree-polynomial calculation gives, with no sign choices
imported from the primary checker,

\[
P_{pq}t-P_{pr}y=Dz,
\]

\[
L_{pq;r}-L_{pr;q}=-2D,
\]

\[
UP_{pq}+tH_{pq;s}-FP_{pr}-yN_{pr;s}=Dv+\kappa z,
\]

and

\[
M_{pq;rs}-M_{pr;qs}=-2\kappa.                 \tag{A2}
\]

The high Euler terms are $\kappa z^2$ and $-\kappa z^2$; the low terms are
$Dvz$ and $-Dvz$.  They cancel pairwise as polynomials.  Since the top
coefficient of $z^2$ is $2\chi$, the base values

\[
(A,B,C,E,F,U)=(-1/4,0,1,1,0,1),
\quad \kappa=-1/4,
\quad \chi=1
\]

give the four top coefficients

\[
(-1/2,1/2,-3/4,3/4).
\]

This reproduces both the overlap signs and their normalization.

## 3. Formal diagonal anchor and rank jump

The anchor calculation uses formal retained target-frame inputs; it is not a
claim that the physical packet satisfies diagonal tensor equations at other
residual words.  The independent checker reconstructs the stated rational
matrices $X,Y$, verifies

\[
X^{\mathsf T}H_\times+H_\times Y=0,
\qquad
X^{\mathsf T}A_{pq}+A_{pq}Y=0,
\]

and recomputes all three defects

\[
\Delta_c=-X^{\mathsf T}E_{cc}-E_{cc}Y.
\]

Each defect is nonzero.  Their separately retained cycle contributions are

\[
-\frac9{64},\qquad -\frac3{32},\qquad \frac{15}{64};
\]

all three are nonzero and their sum is zero.  The resulting values are
$\Theta=0$ and $\Xi=0$.

On coordinates $(\Theta,\Xi,\kappa,C,D,L,N)$, exact rational elimination
recomputes

\[
\operatorname{rank}R=5,
\qquad
\operatorname{rank}\binom RT=6.
\]

The witness

\[
w=(0,0,-1/4,-1/2,1/2,-3/4,3/4)
\]

is killed by every retained row and has landing residual
$T(w)=1/4$.  This is the claimed selected-row-span obstruction.

## 4. Tilted coexistence calibration

The tilted packet independently reconstructs

\[
A_{pq}=
\begin{pmatrix}0&-3/2&-1\\0&-1&-1/2\\-1/4&-1/4&-1/4\end{pmatrix},
\qquad
A_{pr}=
\begin{pmatrix}0&1&1/4\\0&1&1/2\\-1/4&0&1/8\end{pmatrix}.
\]

The second block has rank three.  At the selected square,

\[
(A,B,F,U)=(-3/2,1,1,1),
\quad \kappa=-5/2,
\quad \chi=2,
\]

and the four Euler tops are $(-10,10,-5,5)$.  In particular $B=1$, so the
second chart is canonically active.  Its 18 selected cap rows and 81 crossed
coefficients still vanish.  This verifies coexistence only; it does not turn
the tilted packet into a landing separator.

## 5. Executable scope guard and verification

The independent checker finally enumerates all
$9\cdot3^6=6561$ coefficients of the `pq` tensor EqSystem.  It requires six
failures in the base packet and seven in the tilted packet.  This makes the
selected/full distinction machine-checkable and prevents the formal anchor
module from being mistaken for a tensor-valued source certificate.

More precisely, writing a failure as
`(residual word; endpoint colours; actual, target)`, with residual words in
physical-site order (0,1,2,3,4,5), the base failures are

```text
(000000; 00;    0, 1)     (111111; 11; 0, 1)
(222222; 22;    0, 1)     (012112; 22; 1, 0)
(012212; 21;    1, 0)     (012212; 22; 1, 0)
```

and the tilted failures are

```text
(000000; 00;    0, 1)     (111111; 11;    0, 1)
(222222; 22;    0, 1)     (002012; 22;  1/2, 0)
(022012; 02; -3/2, 0)     (022012; 20;  1/2, 0)
(022012; 22; -1/4, 0)
```

Thus each list consists of the three missing monochromatic anchor
coefficients plus, respectively, three and four mixed coefficients.  The
checker pins the words, endpoint colours, actual values, and target values,
not only the counts.

Both the primary and independent checkers pass under ordinary Python,
optimized mode, and isolated no-site mode; both compile; and the scoped diff
passes `git diff --check`.  The independent exact ledger is pinned by

```text
360e70817a8fac2f64adae0db09b89f9a00163a7e63646df8e22c97a06ebf056
```

The primary
[note](h3-five-exposed-two-chart-selected-cap-landing-counterguard.md) and
[checker](../computations/verify_h3_five_exposed_two_chart_selected_cap_landing_counterguard.py)
were scope-hardened accordingly; their mathematical selected-word
certificate required no correction.
