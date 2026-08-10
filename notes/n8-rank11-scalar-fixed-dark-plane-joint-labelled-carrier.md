# The fixed dark plane has three labelled joint carriers

This is a source-level advance on the fixed-dark-plane scalar shore, not a
proof of Krenn's conjecture.  The separate one-site rows and every clean-cap
contraction are blind to the rational packet in
[`n8-rank11-scalar-fixed-dark-plane-one-site-guard.md`](n8-rank11-scalar-fixed-dark-plane-one-site-guard.md).
The individually labelled joint contractions are not blind: all three
natural completion fibres have ordinary units using at most three rows.
With every \(q\)-cell restored, they leave three overlapping finite carrier
ledgers.  Eliminating or routing those ledgers is the next fixed-plane
theorem.

## 1. Literal joint rows

Keep the notation and the rational \(p,s,a,q\) packet of the one-site guard.
Contract site \(5=z\) in colour zero and leave sites \(3=x,4=y\) visible.  Write

\[
                 x_{uv}^{ab}=q_{uv}(a,b).
\]

The natural joint completion fibre varies all fifteen cells
\(x_{u5}^{a0}\), \(0\leq u<5\), and all nine cells \(x_{34}^{ab}\), while
retaining the other coefficients of the guard.  Thus it is a literal
24-coordinate fibre, not an abstract response quotient.

Among its 360 nonzero source coefficients, take

* \(g_{00}\): the \((0,0)\) row at output word \(00000\), whose uncontracted
  six-site word is \(000000\); and
* \(g_{22}\): the \((2,2)\) row at output word \(00021\), whose uncontracted
  word is \(000210\).

Direct expansion gives

\[
             g_{00}=-1+x_{25}^{00}x_{34}^{00},
             \qquad g_{22}=x_{25}^{00}.                    \tag{1}
\]

Consequently

\[
             \boxed{x_{34}^{00}g_{22}-g_{00}=1.}           \tag{2}
\]

This is an ordinary polynomial source certificate over every complex
coefficient field.  It proves that the labelled normal found in the guard
cannot be repaired by changing the exposed \(z{:}0\) star and the entire
\(xy\) block.  It also explains the failed five-cell tangent repair: one row
requires \(x_{25}^{00}x_{34}^{00}=1\), while the other requires
\(x_{25}^{00}=0\).

## 2. The other two joint cuts

The same calculation works after contracting either of the other dark
sites in colour zero.  Contracting \(x=3\), let \(h_{ij}\) denote the
corresponding five-site rows.  Three literal coefficients are

\[
 h_{00}=-1+x_{23}^{00}x_{45}^{00}+x_{34}^{00},\qquad
 h_{21}=-x_{34}^{00},\qquad h_{22}=2x_{23}^{00},
\]

and hence

\[
              -2h_{00}-2h_{21}+x_{45}^{00}h_{22}=2.       \tag{3}
\]

Contracting \(y=4\), the analogous rows \(k_{ij}\) satisfy

\[
 k_{00}=-1+x_{24}^{00}x_{35}^{00}+x_{34}^{00},\qquad
 k_{21}=-x_{34}^{00},\qquad k_{22}=x_{24}^{00},
\]

so

\[
              -k_{00}-k_{21}+x_{35}^{00}k_{22}=1.         \tag{4}
\]

Thus every one of the three natural 24-coordinate joint fibres is empty.
The three selected visible edges are respectively \(45,35,34\), the dark
triangle of the guard.

## 3. The unrestricted escape ledger

Equation (2) is not automatically a global unit after the other 111
\(q\)-cells are restored.  The exact unrestricted combination is

\[
\begin{aligned}
x_{34}^{00}g_{22}-g_{00}
={}&1-H_{34}\\
 &-x_{34}^{00}\bigl(
      x_{02}^{00}x_{35}^{20}
     +x_{03}^{02}x_{25}^{00}
     +x_{05}^{00}x_{23}^{02}\bigr),                       \tag{5}
\end{aligned}
\]

where \(H_{34}\) is the sum of the twelve pure-zero perfect-matching
monomials avoiding the selected edge \(34\):

\[
\begin{aligned}
H_{34}={}&x_{01}^{00}x_{23}^{00}x_{45}^{00}
 +x_{01}^{00}x_{24}^{00}x_{35}^{00}
 +x_{02}^{00}x_{13}^{00}x_{45}^{00}
 +x_{02}^{00}x_{14}^{00}x_{35}^{00}\\
&+x_{03}^{00}x_{12}^{00}x_{45}^{00}
 +x_{03}^{00}x_{14}^{00}x_{25}^{00}
 +x_{03}^{00}x_{15}^{00}x_{24}^{00}
 +x_{04}^{00}x_{12}^{00}x_{35}^{00}\\
&+x_{04}^{00}x_{13}^{00}x_{25}^{00}
 +x_{04}^{00}x_{15}^{00}x_{23}^{00}
 +x_{05}^{00}x_{13}^{00}x_{24}^{00}
 +x_{05}^{00}x_{14}^{00}x_{23}^{00}.                     \tag{6}
\end{aligned}
\]

Thus every unrestricted labelled completion must satisfy

\[
 H_{34}+x_{34}^{00}\bigl(
      x_{02}^{00}x_{35}^{20}
     +x_{03}^{02}x_{25}^{00}
     +x_{05}^{00}x_{23}^{02}\bigr)=1.                    \tag{7}
\]

This is the cleanest of the three exact carriers forced by the joint rows.
After all cells are restored, the cuts at \(x,y,z\) each have twelve pure
cubic carriers avoiding their selected visible edge.  The \(x\)-cut also
has six mixed cubic terms; the \(y\)- and \(z\)-cuts each have three.  The
common pure quadratic row used in (3)--(4) vanishes separately in a full
source and is removed from these reduced carrier ledgers.  The \(z\)-cut is
displayed in (5).  The cap-plane quotient misses these
relations because the rational joint error has response-label
matrix \(\lambda\mu^{\mathsf T}\), but the labelled rows separate one
diagonal route from the pure anchor.

## 4. The common cross-block carrier

The pure parts of the three ledgers have a useful exact intersection.  Let
\(N_{uv}\) be the sum of pure-zero perfect matchings which avoid the dark
edge \(uv\), and let \(H\) be the full fifteen-term pure-zero hafnian.  A
perfect matching uses at most one of the dark-triangle edges, so

\[
 N_{34}+N_{35}+N_{45}-2H=P_{B,A},                           \tag{8}
\]

where

\[
 P_{B,A}=\operatorname {perm}
       \bigl(x_{ij}^{00}\bigr)_{i\in\{0,1,2\},\ j\in\{3,4,5\}}          \tag{9}
\]

is the six-term permanent of the residual-to-dark cross block.  Define the
three positive mixed ledgers by

\[
\begin{aligned}
M_{34}={}&x_{34}^{00}\bigl(
 x_{02}^{00}x_{35}^{20}+x_{03}^{02}x_{25}^{00}
 +x_{05}^{00}x_{23}^{02}\bigr),\\
M_{35}={}&x_{35}^{00}\bigl(
 x_{02}^{00}x_{34}^{20}+x_{03}^{02}x_{24}^{00}
 +x_{04}^{00}x_{23}^{02}\bigr),\\
M_{45}={}&x_{45}^{00}\bigl(
 x_{02}^{00}x_{35}^{02}+x_{03}^{00}x_{25}^{02}
 +x_{05}^{02}x_{23}^{00}\\
&\hspace{35mm}
 +x_{02}^{00}x_{34}^{01}+x_{03}^{00}x_{24}^{01}
 +x_{04}^{01}x_{23}^{00}\bigr).
\end{aligned}                                               \tag{10}
\]

Adding the three reduced joint carriers with weights \(1,2,2\), then
adding four copies of the pure top row \(H-1=0\), gives the ordinary
source identity

\[
       \boxed{2P_{B,A}+M_{45}+2M_{35}+2M_{34}=2.}           \tag{11}
\]

Thus the common pure escape is no longer twelve unrelated matchings: it is
one cross-block permanent.  Every completion must have either a nonzero
residual-to-dark pure matching or one of twelve explicit mixed carriers.
Equation (11) is particularly well matched to the second-chart problem,
because a cross edge becomes an endpoint-star or direct coefficient after
an overlapping deletion.

## 5. Proof impact and scope

The fixed-dark-plane problem is no longer an unspecified simultaneous-site
compatibility question.  It has become the following finite source-labelled
alternative:

> on each dark cut, either one of the twelve pure-zero matchings avoiding
> its selected edge survives, or one of the displayed mixed
> labelled carriers survives.

A theorem-completing argument must now use entry minimality and the second
chart to route every such carrier to an active clean cap, an already proved
descent, or another labelled unit.  Equation (5) alone does not show that
its fifteen carriers vanish, and the three unrestricted joint ideals have
not been claimed empty.  In particular this result does not promote the rational
guard to a full source point and does not close the unified two-chart
overlap theorem.

## 6. Exact audit

[`verify_n8_rank11_scalar_dark_plane_joint_labelled_carrier.py`](../computations/verify_n8_rank11_scalar_dark_plane_joint_labelled_carrier.py)
reconstructs all endpoint-coloured matching coefficients.  It checks all
three 24-variable fibres and their units (2)--(4), then reconstructs every
135-variable joint source.  The unrestricted carrier split is

\[
\begin{array}{c|ccc}
\text{contracted site}&\text{pure cubics}&\text{mixed cubics}\\ \hline
x&12&6\\
y&12&3\\
z&12&3.
\end{array}
\]

It also verifies (11) coefficientwise: its nonconstant support is exactly
the six cross-block permanent terms with coefficient \(-2\) and the twelve
mixed terms with coefficient \(-1\) or \(-2\).

Its deterministic ledger digest is

```text
96ba63403fc95b9363295f5f07a0bda9a4a9c24fb3cecf1d8ccdd31a9b26c70a
```
