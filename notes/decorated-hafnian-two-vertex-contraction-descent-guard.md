# Two-vertex contraction has an unavoidable multi-effective-edge debt

## Exact identity

Let

\[
 W_X(A)=\sum_{M\in\operatorname{PM}(X)}\ \bigotimes_{ij\in M}A_{ij}
\]

be the decorated hafnian tensor. Choose vertices `p,q`, put
`U=X\setminus\{p,q\}`, and contract by arbitrary covectors `phi,psi`. Define

\[
\begin{aligned}
s&=(\phi\otimes\psi)(A_{pq}),\\
a_u&=(\phi\otimes1)(A_{pu}),\qquad
b_u=(\psi\otimes1)(A_{qu}),\\
R_{uv}&=a_u\otimes b_v+b_u\otimes a_v.
\end{aligned}                                             \tag{1}
\]

Partitioning matchings according to whether `p,q` are paired together gives

\[
 (\phi_p\otimes\psi_q)W_X(A)
 =sW_U(A)+DW_U(A)[R].                                  \tag{2}
\]

This keeps arbitrary endpoint colours, orientations, and parallel weights.
The checker verifies (2) by direct exact tensor enumeration on an independent
nontrivial six-vertex graph:
[`verify_decorated_hafnian_two_vertex_contraction_descent_guard.py`](../computations/verify_decorated_hafnian_two_vertex_contraction_descent_guard.py).

If `s!=0`, let `A'=A+R/s`. Then

\[
 sW_U(A')=(\phi\psi)W_X(A)
 +\sum_{k\ge2}s^{1-k}C_k(A,R),                       \tag{3}
\]

where `C_k` is the matching sum with exactly `k` effective `R` edges. Thus
the contraction is not generally the matching tensor of the absorbed graph.

For a set `S` of `2k` retained vertices, the special rank-two form in (1)
has the exact hafnian

\[
 \operatorname{Haf}(R_S)
 =k!\sum_{\substack{I\subset S\\|I|=k}}
 \bigotimes_{i\in I}a_i\otimes
 \bigotimes_{j\in S\setminus I}b_j.                 \tag{4}
\]

Indeed, after choosing which endpoint vector occurs at each vertex, the
`a` and `b` sites can be paired in `k!` ways. The checker verifies the full
oriented-matching count through `k=4`.

## A literal monochromatic contraction with nonzero debt

The local implication

```text
contracted tensor is Delta_r  =>  all C_k, k>=2, vanish
```

is false already for `r=3`.

Take four retained vertices and two endpoints. Use

```text
phi=psi=(1,1,1),  s=1,
a_u=b_u=e0 for every retained u.
```

Then every effective edge is

\[
                         R_{uv}=2e_0e_0,
 \qquad W_4(R)=12e_0^{\otimes4}.                     \tag{5}
\]

Let `B=A+R` be the four-site graph whose three matching products are

```text
(01)(23): 13 e0^4,
(02)(13):    e1^4,
(03)(12):    e2^4.
```

Equivalently, put weights `13,1` on the two colour-zero edges and unit
weights on each of the colour-one and colour-two matching edges. Define
`A=B-R` edgewise. Since the four-site hafnian is quadratic,

\[
\begin{aligned}
W_4(A)+DW_4(A)[R]
 &=W_4(A+R)-W_4(R)\\
 &=(13e_0^4+e_1^4+e_2^4)-12e_0^4\\
 &=\Delta_3.                                         \tag{6}
\end{aligned}

The checker lifts this interface to an honest decorated six-vertex graph
with the displayed endpoint edges and verifies by full matching enumeration
that its chosen two-vertex contraction is exactly `Delta_3`. But the
absorbed retained graph is

\[
                         \Delta_3+12e_0^{\otimes4}.   \tag{7}
\]

So even exact monochromaticity of the contracted tensor does not cancel the
first multi-effective-edge term.

## A normalized no-choice endpoint guard

There is also a sharp guard against choosing better covectors using only the
target normalization. Let every endpoint-to-retained edge induce the
identity map, so `a_u=phi` and `b_u=psi`. To contract `Delta_r` back to equal
monochromatic weights, normalize

\[
                         \phi_c\psi_c=1
\]

for every colour. On any four retained vertices, the all-`c` coordinate of
every `R` edge equals two. Therefore

\[
                    [e_c^{\otimes4}]W_4(R)=3\cdot2^2=12. \tag{8}

No normalized covector choice kills this cross term. This is an exact
endpoint-factor guard for every `r>=3` (indeed every positive `r`).

It is deliberately not claimed to extend to a global `W_n=Delta_r` source.
The complete GHZ equations may force identity endpoint maps—or this whole
guard—to exit by an active, coloop, or terminal theorem. Proving that is the
additional global input a successful contraction descent needs.

## Direct-edge access is a separate gate

On the normalized torus write `phi_c=t_c`, `psi_c=t_c^{-1}`. For direct edge
matrix `E=A_pq`,

\[
                         s(t)=\sum_{c,d}E_{cd}t_c/t_d. \tag{9}

The offdiagonal Laurent characters are distinct, while all diagonal terms
have the trivial character. Hence `s` vanishes identically on every
normalized choice exactly when `E` is diagonal and traceless. In that case
absorption cannot even start. Otherwise a normalized choice with `s!=0`
exists, but (3)--(8) show that nonzero `s` does not remove the cross debt.

## Consequence for descent

The contraction route is reduced to a precise global theorem, not an
automatic identity:

> For some pair `p,q` and normalized covectors, the complete parent
> `W_n=Delta_r` equations must force `s!=0` and every `C_k(A,R), k>=2`, to
> vanish or land in an already accepted source-terminal branch.

Equation (2) alone cannot prove this. The six-vertex construction above is
a minimal exact counterguard to contraction-only descent, not a
counterexample to the Krenn conjecture and not a full `Delta_3` parent
source.

Run normally, optimized, and isolated/no-site. The checker freezes a ledger
digest.
