# The fixed dark plane has a two-row labelled joint carrier

This is a source-level advance on the fixed-dark-plane scalar shore, not a
proof of Krenn's conjecture.  The separate one-site rows and every clean-cap
contraction are blind to the rational packet in
[`n8-rank11-scalar-fixed-dark-plane-one-site-guard.md`](n8-rank11-scalar-fixed-dark-plane-one-site-guard.md).
The first individually labelled joint contraction is not blind: its natural
completion fibre has an ordinary two-row unit.  With every \(q\)-cell restored,
the same identity leaves an exact finite ledger of twelve pure matching
carriers and three mixed carriers.  Eliminating or routing that ledger is the
next fixed-plane theorem.

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

## 2. The unrestricted escape ledger

Equation (2) is not automatically a global unit after the other 111
\(q\)-cells are restored.  The exact unrestricted combination is

\[
\begin{aligned}
x_{34}^{00}g_{22}-g_{00}
={}&1-H_{34}\\
 &-x_{34}^{00}\bigl(
      x_{02}^{00}x_{35}^{20}
     +x_{03}^{02}x_{25}^{00}
     +x_{05}^{00}x_{23}^{02}\bigr),                       \tag{3}
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
 +x_{05}^{00}x_{14}^{00}x_{23}^{00}.                     \tag{4}
\end{aligned}
\]

Thus every unrestricted labelled completion must satisfy

\[
 H_{34}+x_{34}^{00}\bigl(
      x_{02}^{00}x_{35}^{20}
     +x_{03}^{02}x_{25}^{00}
     +x_{05}^{00}x_{23}^{02}\bigr)=1.                    \tag{5}
\]

This is the first exact carrier forced by the joint rows.  The cap-plane
quotient misses it because the rational joint error has response-label
matrix \(\lambda\mu^{\mathsf T}\), but the two labelled rows separate one
diagonal route from the pure anchor.

## 3. Proof impact and scope

The fixed-dark-plane problem is no longer an unspecified simultaneous-site
compatibility question.  It has become the following finite source-labelled
alternative:

> either one of the twelve pure-zero matchings avoiding the selected anchor
> survives, or one of three displayed mixed carriers through the anchor
> survives.

A theorem-completing argument must now use entry minimality and the second
chart to route every such carrier to an active clean cap, an already proved
descent, or another labelled unit.  Equation (3) alone does not show that
the fifteen carriers vanish, and the unrestricted joint ideal has not been
claimed empty.  In particular this result does not promote the rational
guard to a full source point and does not close the unified two-chart
overlap theorem.

## 4. Exact audit

[`verify_n8_rank11_scalar_dark_plane_joint_labelled_carrier.py`](../computations/verify_n8_rank11_scalar_dark_plane_joint_labelled_carrier.py)
reconstructs all endpoint-coloured matching coefficients.  It checks the
24-variable fibre (360 rows, 508 terms), the two-row unit (2), and the full
135-variable joint source (1,359 rows, 17,173 terms).  The unrestricted
residual has exactly one constant, twelve pure negative cubics, and three
mixed negative cubics.  Its deterministic ledger digest is

```text
11731e55eac7c0d1b2431e3d9bc5e0d0681b1be0740099cf975bf96a10b07ff7
```
