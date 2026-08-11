# The third cofactor creates the formal relative tail and obstructs its physical descent

## Outcome

The genuine unary third cofactor from `0a374ef` and the top of the
denominator-marked two-edge principal-parts/Bianchi square are the **same
coefficient**, not two independent faces.  If $t=a_{pq}^{22}$,
$M=\{a_{xv}^{0m_v}\}\cup N$ is a perfect matching of the six residual
sites, and $A=H_m$, then

\[
 q^{[3]}=\partial_tA,\qquad
 \boxed{J_M=\partial_Mq^{[3]}=\partial_{t,M}A=1.}       \tag{1}
\]

This identification gives a split verdict.

* In the complete squarefree Hasse prolongation, $J_M=1$ produces an
  explicit lower tail $C_{\rm rel}^{\rm Hasse}$ with exactly the desired
  coarse type

  \[
  (\operatorname{ainc},\widehat w,\operatorname{tgt},
       \operatorname{ores})=(-1,0,0,0).                 \tag{2}
  \]

  Its differential is the negative pure Eq face, every Leibniz ridge
  cancels, and the coupled tail/top/cap complex has $d^2=0$.
* The construction does **not** give a source-valid physical
  $C_{\rm rel}$.  The same unit in (1) says that the fourth operator sends
  the underived source equation $H_m=0$ to $1$.  It therefore cannot
  factor through a nonempty source quotient.  Moreover, the physical
  $22/0m_v$ cube and the zero-endpoint $00/00$ Bianchi cube agree only
  at their scalar top: two endpoint-decorated ridges differ.  Identifying
  the tops without new word-changing faces is not a chain map.

The primitive higher obstruction is the signed two-ridge class

\[
 \Omega_v=(a_{pq}^{22}-a_{pq}^{00})
           -(a_{xv}^{0m_v}-a_{xv}^{00}),               \tag{3}
\]

up to the orientation convention.  It has four unit coefficients and is
nonzero in the free source-labelled ridge module.  Across the five deleted
sites the five $\Omega_v$ are independent; the complete individual ridge
differences span rank six.

Finally, neither literal cube lies in the selected binary three/three
midpoint word summand.  Selector localization can repair endpoint character
but cannot alter this residual word label.  Thus a positive physical cell
still needs both endpoint-ridge homotopies in (3) and a source-labelled
residual-word comparison into the midpoint sector.

This constructs the formal relative cell and proves its first physical
obstruction.  It does not prove that no larger physical source resolution
can contain the missing faces, and it does not prove Krenn's conjecture.

## 1. The common third-cofactor face

Use the direct-free eight-site word

\[
                         m=01211222                     \tag{4}
\]

with exposed pair $p,q=6,7$, $x=0$, and odd sites
$D=\{1,2,3,4,5\}$.  For $v\in D$, choose a perfect matching
$N$ of $F_v=D\setminus\{v\}$.  The four physical marked cells are

\[
 a_{pq}^{22},\quad a_{xv}^{0m_v},\quad N.              \tag{5}
\]

Deleting $a_{pq}^{22}$ leaves the unary six-site hafnian $q^{[3]}$.
The remaining three cells in (5) form a perfect matching $M$ of those
six sites.  Hence the genuine third cofactor $J_M$ of the unary row is
literally the fourfold coefficient of the physical row, proving (1).

The zero-endpoint Bianchi chart instead uses

\[
 a_{pq}^{00},\quad a_{xv}^{00},\quad N.                \tag{6}
\]

and has the same scalar fourfold coefficient $1$.  This is the exact
meeting point between the unary cofactor tower and the denominator-marked
principal-parts square.  It is only a scalar meeting point: the cell labels
in (5) and (6) remain distinct source coordinates.

The checker reconstructs all fifteen choices $(v,N)$ from the literal
90-term direct-free rows and verifies (1) in each.

## 2. The smallest total complex and the formal relative tail

Put

\[
                         B=H_0-u,
 \qquad I=\{a_{pq}^{22},a_{xv}^{0m_v}\}\cup N.         \tag{7}
\]

For squarefree Hasse copies use the genuine differential

\[
\begin{aligned}
 d r_0[U]&=B\,e_{\rm Eq}[U],\\
 d r_m[U]&=\sum_{S\subseteq U}
              (\partial_SA)e_{\rm Eq}[U\setminus S].
\end{aligned}                                          \tag{8}
\]

The complete translated Koszul chain is

\[
 s_I=\sum_{S\subseteq I}(\partial_SA)r_0[I\setminus S]
          -B r_m[I],\qquad ds_I=0.                     \tag{9}
\]

By (1), its unique target-carrying top is $r_0[\varnothing]$.  Split (9)
as

\[
 s_I=r_0[\varnothing]+C_{\rm rel}^{\rm Hasse},         \tag{10}
\]

where

\[
 C_{\rm rel}^{\rm Hasse}
 =\sum_{S\subsetneq I}(\partial_SA)r_0[I\setminus S]
       -B r_m[I].                                      \tag{11}
\]

Then the desired relative signature is literal:

\[
 dC_{\rm rel}^{\rm Hasse}=-B e_{\rm Eq}[\varnothing],
 \qquad
 (\widehat w,\operatorname{tgt},\operatorname{ores})=(0,0,0).
                                                               \tag{12}
\]

With $dT=-Yw$ and $\operatorname{tgt}(T)=1$, the top and total pieces
have signatures

\[
\begin{array}{c|rrrr}
 &\operatorname{ainc}&\widehat w&\operatorname{tgt}&
       \operatorname{ores}\\ \hline
 C_{\rm rel}^{\rm Hasse}&-1&0&0&0\\
 r_0[\varnothing]-T&1&1&0&0\\
 s_I-T&0&1&0&0.
\end{array}                                             \tag{13}
\]

The checker expands every face in (8), verifies $ds_I=0$, (12),
$d(s_I-T)=Yw$, and $d^2(s_I-T)=0$ on all fifteen cubes.  Thus the
candidate fails neither by a cubical sign nor by an omitted Leibniz term.

## 3. The first source-labelled bridge obstruction

A common total complex must also connect the physical cube (5) to the
zero-endpoint Bianchi cube (6).  At the fourfold top their coefficients are
both one.  At codimension one, differentiating all but one marked cell
returns the omitted decorated cell itself.  The two internal $N$-ridges
agree, while the two endpoint ridges are

\[
 a_{pq}^{22}\ne a_{pq}^{00},\qquad
 a_{xv}^{0m_v}\ne a_{xv}^{00}.                         \tag{14}
\]

Therefore the Hom differential of the proposed top identification is the
primitive class (3).  In a cubical chain map, its four monomials live in
separate source-labelled ridge coordinates; equality of their scalar top
derivatives does not cancel them.

For one $v$, (3) has coefficient gcd one.  Over all five $v$, the
$pq$ difference is common and the five $xv$ differences are distinct.
The complete ridge span has rank six, while the five oriented obstruction
vectors have rank five.  This is the smallest exact higher cell that a
positive construction must kill.

Automatic fixed-label curvature rows cannot do so: they exchange physical
matchings while preserving endpoint decoration.  A cell killing (3) must
instead be an endpoint-word-changing source comparison, with its companion
and target retained.

## 4. The unit is also the descent obstruction

The formal Hasse differential (8) is obtained by translating the
presentation as well as its coefficients.  It is square-zero, but it is not
a comparison on the underived source quotient.  The selected fourth
operator is

\[
 \Psi_I=\partial_{a_{pq}^{22}}
        \partial_{a_{xv}^{0m_v}}\partial_N,
 \qquad \Psi_I(H_m)=J_M=1.                             \tag{15}
\]

If $\Psi_I$ factored through a nonzero source ring, the zero class of
$H_m$ would map to the unit.  Equation (15) is therefore a primitive,
source-validity obstruction.  It is also exactly what makes the coefficient
of $r_0[\varnothing]$ in (10) equal to one.  The formal construction and
its failure of descent are two sides of the same coefficient, not separate
phenomena.

Equivalently, diagonal projection forgets (11) and leaves
$r_0-T$, whose chain-map defect is

\[
                         (H_0-u)e_{\rm Eq}.             \tag{16}
\]

The selected-$u$ coefficient of (16) is $-1$, so the obstruction is
primitive.  Adjoining a generator with differential (11) would solve it by
definition; deriving such a generator from the physical source is the open
theorem.

## 5. Endpoint and midpoint grade

The physical cube has six-site residual word `012112`, with colour counts
$ (1,3,2) $.  The five zero-endpoint chart words have counts either
$ (2,2,2) $ or $ (2,3,1) $, and the denominator reset is pure `000000`.
None is one of the sixty binary three/three midpoint words obtained by
choosing any two of the three colours.

Selector localization can shift endpoint character, as already proved, but
acts scalarly on the residual word module.  It cannot change any of these
counts or labels.  Thus even a future homotopy killing (3) must also carry a
literal residual-word comparison into the selected midpoint summand.  The
third cofactor is a scalar source coefficient and supplies no such map.

## Verification

Run

```text
python3 computations/verify_h3_rootless_third_cofactor_bianchi_total_complex_obstruction.py
python3 -O computations/verify_h3_rootless_third_cofactor_bianchi_total_complex_obstruction.py
```

The checker pins the unary third-cofactor, denominator-marked square, full
Hasse totalization, conormal, selector, and first-operation audits.  It
reconstructs all fifteen physical and zero-endpoint cubes, identifies their
third-cofactor tops, computes every ridge, builds the complete Hasse--Koszul
tail, verifies all four coarse readouts and $d^2$, proves the rank-six/rank-
five ridge obstruction, and checks the complete all-colour midpoint census.
