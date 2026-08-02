# The (1I+5R) (K_{2,3}) antipodal pencil has rank at most (51)

Research evidence only. Krenn's conjecture remains open,
**SP-CLEAN-BRIDGE** is untouched, and no certified dependency changes.

## Outcome

The connected (K_{2,3}) residue left by the
[(1I+5R) potential reduction](level-two-one-invertible-five-rank-one-potential-reduction.md)
is closed by differential rank alone:

> **(K_{2,3}) antipodal-pencil rank theorem.** Every residual packet in
> the (1I+5R) (K_{2,3}) generic-kernel normal form satisfies
> \[
>                          \operatorname{rank}d\Psi_M\le51.       \tag{1}
> \]

The bound is sharp in the covariant residual class. In particular, no
rank-(55) packet reaches L0, L1, or the remaining literal R2 equations on
this branch. The six zero-multiplier cross blocks are completely arbitrary;
the theorem includes singular, zero, and R2-specialized choices.

Together with the independently proved
[(K_{1,4}) coordinate-core theorem](level-two-one-invertible-five-rank-one-k14-coordinate-core-closure.md),
this closes the full (1I+5R) endpoint-rank stratum.

## 1. Covariant normalization

Label the invertible root (0), and split the five rank-one sites as

\[
 A=\{1,2\},\qquad B=\{3,4,5\}.                                 \tag{2}
\]

The predecessor reduction gives nonzero vectors (h_i), two independent
root vectors (g_A,g_B), and nonzero scalars (c_A,c_B) such that

\[
\begin{aligned}
 M_{0i}&=g_Ah_i^{\mathsf T} &&(i\in A),&
 M_{12}&=c_Ah_1h_2^{\mathsf T},\\
 M_{0j}&=g_Bh_j^{\mathsf T} &&(j\in B),&
 M_{jk}&=c_Bh_jh_k^{\mathsf T} &&(j,k\in B),                 \tag{3}
\end{aligned}
\]

while every (M_{ij}), (i\in A,j\in B), is arbitrary. Independence of
(g_A,g_B) follows from the two distinct nonisotropic antipodal pencil
lines and invertibility of (X_0).

Independent binary changes of coordinates at the six residual sites act by

\[
                         M_{uv}\longmapsto L_uM_{uv}L_v^{\mathsf T}.
                                                                    \tag{4}
\]

They preserve differential rank. Choose nonzero (s_A,s_B\in\mathbb C)
with

\[
                         c_As_A^2=c_Bs_B^2=1.                     \tag{5}
\]

At sites (i\in A), send (h_i) to (s_Ae_0); at sites (j\in B),
send (h_j) to (s_Be_0). At site (0), send

\[
                         g_A\mapsto s_A^{-1}e_0,qquad
                         g_B\mapsto s_B^{-1}e_1.                  \tag{6}
\]

Equations (3)--(6) give the exact normal form

\[
\begin{array}{c|ccc}
\text{fixed triangle on }\{0,1,2\}&M_{01}&M_{02}&M_{12}\\ \hline
&E_{00}&E_{00}&E_{00}
\end{array}                                                     \tag{7}
\]

and

\[
 M_{03}=M_{04}=M_{05}=E_{10},qquad
 M_{34}=M_{35}=M_{45}=E_{00}.                                  \tag{8}
\]

The six blocks

\[
                 M_{13},M_{14},M_{15},M_{23},M_{24},M_{25}       \tag{9}
\]

remain arbitrary (2\times2) matrices. Thus the full covariant residue is
one affine (24)-parameter packet over the fixed blocks (7)--(8).

The use of square roots in (5) is harmless over (mathbb C). No physical
R2 coordinate statement is transported through this normalization; it is
used only for the invariant differential-rank calculation.

## 2. Exact generic differential

Introduce independent variables

\[
 x_{ij}^{ab},\qquad i\in A, j\in B, a,b\in\{0,1\},           \tag{10}
\]

for the (24) entries of (9), and work over

\[
 K=\mathbb Q\bigl(x_{ij}^{ab}:i\in A,j\in B,a,b\in\{0,1\}\bigr).
                                                                    \tag{11}
\]

Let (D(x)) be the (64\times60) matrix of (d\Psi_M). Every entry is
the matching tensor of a four-site complement, hence is an explicit
polynomial of degree at most two in (10). There are (512) structurally
nonzero cell entries.

Exact module computation over
(mathbb Q[x_{ij}^{ab}]) gives a polynomial matrix (Q(x)) with

\[
                            D(x)Q(x)=0.                           \tag{12}
\]

The Gröbner syzygy calculation returns eleven module generators. On the
exact specialization which sends the ordered variables in (10) to
(2,3,\ldots,25), their coefficient matrix has rank (9). Therefore at
least nine of the polynomial relations are independent over the function
field (K), and

\[
                       \dim_K\ker D(x)\ge9,qquad
                       \operatorname{rank}_KD(x)\le60-9=51.       \tag{13}
\]

This is a symbolic function-field statement, not a collection of random
rank tests. It implies that every (52\times52) minor of (D(x)) is the
zero polynomial. Consequently (1) holds after **every** specialization of
the six arbitrary cross blocks, including boundary specializations where
some blocks or entries vanish.

The five universal trace-zero vertex gauges account for only five of the
nine generic kernel dimensions. The additional four directions are the
genuine (K_{2,3}) pencil defect.

## 3. Sharpness

For a deterministic integral calibration, keep (7)--(8) and set

\[
 M_{ij}(a,b)
 =2+\bigl(17i+31j+7a+11b+3ij\bmod19\bigr)                    \tag{14}
\]

on every edge in (9). Exact row reduction gives

\[
\begin{array}{c|cccc}
\text{field}&\mathbb Q&\mathbf F_{101}&\mathbf F_{32003}&
\mathbf F_{1000003}\\ \hline
\operatorname{rank}d\Psi_M&51&51&51&51.
\end{array}                                                     \tag{15}
\]

Thus the covariant bound (1) is exact.

## 4. Consequence for L0, L1, and R2

The original (K_{2,3}) frontier already retained literal R2 in physical
coordinates: every root must have two distinct internal pure-column
witnesses, and root (0) forces two (h_i)'s onto the two physical axes.
None of that structure can restore four lost differential dimensions.
The rank theorem allows arbitrary values in all six blocks (9), so it
applies before imposing those R2 restrictions.

Likewise, L0 and L1 can only cut the residual family further. Since the
level-two rank-(55) branch is already impossible, no endpoint-star
incidence, factored-L0, or overlapping-L1 calculation is needed for
(K_{2,3}).

## 5. Exact audit

The checker
[verify_level_two_one_invertible_k23_antipodal_pencil_rank_closure.py](../computations/verify_level_two_one_invertible_k23_antipodal_pencil_rank_closure.py)

- imports and pins the covariant (K_{2,3}) and R2 conclusions of the
  predecessor potential reduction;
- constructs all (3840) entries of the generic (64\times60)
  differential over the (24)-variable polynomial ring;
- asks Singular for the exact syzygy module, then verifies all entries of
  (D(x)Q(x)) are zero;
- specializes the syzygy matrix exactly and verifies relation rank (9)
  and differential rank (51);
- independently reconstructs the integral calibration (14) and verifies
  (15) by rational and three modular row reductions.

The generated Singular program has SHA-256

```text
d18201acf82be051be1ed6a77e29f21af72c3649410dc64a4401668725da08f5
```

The Python driver uses only the standard library; Singular is its sole
external dependency. It passes normal, optimized, and isolated Python.
