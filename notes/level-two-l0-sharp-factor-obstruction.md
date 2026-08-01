# The sharp L0 tangent packet has no factored endpoint completion

Research evidence only. Krenn's conjecture remains open,
**SP-CLEAN-BRIDGE** is untouched, and no certified dependency changes.

## 1. Outcome

The sharp residual packet $M^\sharp$ in the
[binary L0 tangent-incidence note](level-two-three-invertible-l0-obstruction.md)
passes the linear screen

\[
 \operatorname{rank}d\Psi_{M^\sharp}=55,\qquad
 \operatorname{rank}(d\Psi_{M^\sharp})_{\rm mix}=53,
\]

and has literal tangent columns $e_{0^6}$ and $e_{1^6}$. Nevertheless it
has **no** endpoint stars realizing all four binary L0 slices. Thus the
linear incidence screen is sharp, but this particular sharpness packet does
not survive its required two-star factorization.

This is an obstruction to one exact packet, not to the general incidence
locus and not a proof of Krenn's conjecture.

## 2. Exact factor equations

Write $D=d\Psi_{M^\sharp}$. Exact elimination gives
$\operatorname{rank}D=55$. The five universal gauge tangents are
independent, so

\[
 \ker D=\{((\mu_r+\mu_u)M^\sharp_{ru})_{r<u}:\sum_r\mu_r=0\}.
 \tag{1}
\]

For endpoint colours $s,t\in\{0,1\}$, let
$U_r^s,V_r^t\in\mathbb C^2$ be the two endpoint stars. Euler's identity
absorbs the direct endpoint coefficient into the vertex scalars. Because
the pure target preimages are the cells $(01,00)$ and $(45,11)$, every
factored completion would obey

\[
 U_r^s(V_u^t)^{\mathsf T}+V_r^t(U_u^s)^{\mathsf T}
 =R^{st}_{ru}+(\alpha_r^{st}+\alpha_u^{st})M^\sharp_{ru},
 \tag{2}
\]

where $R^{00}_{01}=E_{00}$, $R^{11}_{45}=E_{11}$, and every other
$R^{st}_{ru}$ is zero.

## 3. A four-edge unit-ideal certificate

It is enough to retain vertices

\[
                         \{0,1,4,5\}
\]

and edges $01,04,05,45$. We further weaken (2), replacing every vertex sum
$\alpha_r^{st}+\alpha_u^{st}$ by an independent scalar
$\lambda_{ru}^{st}$. The retained packet blocks are

\[
\begin{aligned}
M_{01}&=\begin{pmatrix}2&3\\4&6\end{pmatrix},&
M_{04}&=\begin{pmatrix}5&6\\11&8\end{pmatrix},\\
M_{05}&=\begin{pmatrix}6&7\\13&9\end{pmatrix},&
M_{45}&=\begin{pmatrix}1&0\\0&0\end{pmatrix}.
\end{aligned}
\tag{3}
\]

There are $32$ star coordinates and $16$ independent edge scalars. The
four slices on four edges give $64$ quadratic equations in $48$ variables.
Exact degree-reverse-lexicographic Gröbner elimination gives

\[
                         \operatorname{std}(I)=(1).          \tag{4}
\]

over $\mathbb Q$. The independent-scalar system is strictly weaker than
(2), so (4) proves that no factored L0 completion of $M^\sharp$ exists.
The same calculation over $\mathbb F_{32003}$ is an independent arithmetic
audit.

## 4. Machine audit and scope

[verify_level_two_l0_sharp_factor_obstruction.py](../computations/verify_level_two_l0_sharp_factor_obstruction.py)

* reads but does not alter the committed $M^\sharp$;
* rechecks differential rank $55$, the five-dimensional gauge kernel, and
  the two literal pure tangent columns;
* constructs all $48$ variables and $64$ quadrics in memory, with an
  independent scalar on every retained edge and slice; and
* requires the exact Gröbner basis $(1)$ over both $\mathbb Q$ and
  $\mathbb F_{32003}$.

The checker uses standard-library Python but requires an external
`Singular` executable on `PATH`. Its conclusion concerns only the displayed
sharp packet. Other rank-$55/53$ tangent-incidence packets may still admit
factored endpoint stars.

An
[independent audit](level-two-l0-sharp-factor-obstruction-independent-audit.md)
uses no computer-algebra dependency. It reconstructs the packet and exact
kernel, retains only slices $00,11,01$ on the residual $K_4$ induced by
$\{0,1,4,5\}$, and verifies a sparse rational identity
$\sum_k c_kf_k=1$ involving 38 of the 72 local equations. Thus the final
no-completion conclusion has both a Gröbner audit of a weakened system and
an explicit standard-library Nullstellensatz certificate.
