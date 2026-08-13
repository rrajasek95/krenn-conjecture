# The order-two diagonal trace jet cancels the even target and exposes reduced Eq

## Outcome

The natural endpoint-even \(B-4I\) path in the lower word 0112 has a
nonzero mixed target normal. On the generic diagonal open
\(\alpha\beta\ne0\), the order-two specialization of the diagonal cap
combination gives the exact target-bearing input

\[
 J_*^{(2)}=(\beta-\alpha)J_1+(\beta+\alpha)J_2
          =-2\alpha\beta I.                           \tag{1}
\]

Let \(S\) exchange endpoint roles, let \(w=w_{xt}\) be the two-site Weyl
return for one root-decorated endpoint move, and let \(P_2\) denote the
shifted diagonal-to-occurrence placement. Conditional on a source-labelled
physical \(P_2\), the even Cartan cell is

\[
\begin{aligned}
 C_{2,+}
  &={1\over4\alpha\beta}(1+S)H_wP_2(J_*^{(2)})\\
  &=-{1\over2}(1+S)H_wP_2(I).                         \tag{2}
\end{aligned}
\]

Its target is

\[
                    \operatorname{tgt}(C_{2,+})
                       =-2(w-1)\Delta_4.              \tag{3}
\]

This cancels exactly the \(+2(w-1)\Delta_4\) target of the two
endpoint orientations of the corresponding \(B-4I\) edge. Thus the mixed
target normal does have a uniform diagonal/Cartan correction on the generic
open. It is not obtained by adjusting the two old Cartan columns: target
cancellation inside their span forces the odd line. The diagonal trace jet
is the independent target-bearing input.

The Cartan formula computes the first residual exactly:

\[
\boxed{
 R_{2,+}=-{1\over2}(1+S)H_w\,d(P_2(I)).}               \tag{4}
\]

For the known canonical reduced-Eq target-cone candidate, a cell with target
\(-2D\), where \(D=(w-1)\Delta_4\), also carries

\[
                    -2D(H_0-u)e_{\rm Eq}.             \tag{5}
\]

Therefore the next required correction is

\[
\boxed{+2D(H_0-u)e_{\rm Eq}.}                          \tag{6}
\]

For the exact centered \(B-4I\) preimage, \(D\) is replaced by the explicit
eleven-word target normal \(N_v\) computed in the preceding gate. The
canonical cone candidate retains \(-N_v(H_0-u)e_{\rm Eq}\), and its required
correction is \(+N_v(H_0-u)e_{\rm Eq}\).

This is a positive target-level construction in the universal principal-parts
model, conditional on the source-labelled placement \(P_2\), and a sharp
physical interface. The derived reduced-Eq Koszul core already
exists. What remains is the single source-labelled, endpoint-even
comparison placing both \(P_2(I)\) and the root-decorated Koszul core in
the literal occurrence packet, with lower landing, residue, protected rows,
and physical \(q\). At \(\beta=0\), (1) vanishes and the normalized
construction has no regular specialization; the collision/unary branch is
still separate.

Companion checker:
[verify_h2_lower_even_cartan_jstar_target_cone_gate.py](../computations/verify_h2_lower_even_cartan_jstar_target_cone_gate.py).

## 1. Exact order-two trace identity

Let \(K_0=E_{00}\) and

\[
\begin{aligned}
 J_1&=(\alpha+\beta)K_0-\alpha I,\\
 K_2&=\alpha K_0-\alpha I,\\
 J_2&=-\beta K_0+K_2.
\end{aligned}
\]

Then

\[
\begin{aligned}
(\beta-\alpha)J_1+(\beta+\alpha)J_2
 &=[(\beta-\alpha)(\alpha+\beta)
     +(\beta+\alpha)(\alpha-\beta)]K_0\\
 &\quad-[\alpha(\beta-\alpha)+\alpha(\beta+\alpha)]I\\
 &=-2\alpha\beta I.
\end{aligned}
\]

The diagonal target values obey the same identity. In the three pure
coordinates,

\[
 T(J_1)=(\beta,-\alpha,-\alpha),\qquad
 T(J_2)=(-\beta,-\alpha,-\alpha),
\]

so \(T(J_*^{(2)})=-2\alpha\beta\Delta_4\). The intrinsic order-two
placement contributes a factor two, and endpoint evenization contributes
another factor two. Dividing by \(4\alpha\beta\) gives (3).

After substituting (1), every parameter cancels from the chain itself:

\[
 {1\over4\alpha\beta}P_2(J_*^{(2)})
                         =-{1\over2}P_2(I).            \tag{7}
\]

This is the \(h=2\) analogue of the universal \(h=3\) trace remainder
\(-\frac13(1+\rho)H_wd(P(I))\).

## 2. Literal cancellation of the lower target normal

For the marked occurrence \(f=(0,1;45)\), three moves are
root-decorated:

| move | root colours | defect |
|---|---|---|
| \(0\to4\) | \(0,1\) | \(D_{04}=(w_{04}-1)\Delta_4\) |
| \(0\to5\) | \(0,2\) | \(D_{05}=(w_{05}-1)\Delta_4\) |
| \(1\to5\) | \(1,2\) | \(D_{15}=(w_{15}-1)\Delta_4\) |

The fourth move \(1\to4\) exchanges equal colours and is a target-safe
site bar. For each root move, the two endpoint orientations have target
\(+2D_{xt}\), while (2) has target \(-2D_{xt}\). Summing gives

\[
 2(D_{04}+D_{05}+D_{15})
 -2(D_{04}+D_{05}+D_{15})=0.                          \tag{8}
\]

Thus the diagonal correction cancels all six mixed words and the pure
\(\Delta_4\) part simultaneously. No separate common-\(H_0\) target
normalization is needed after (2) is physically placed.

This does not yet identify the source modules. The diagonal input is a pure
cap trace jet; the lower \(B\) path is occurrence-local in word 0112 and
after reinsertion in the repeated P3+K2 grade. The map \(P_2\) in (2) is
exactly the shifted source-labelled comparison, not a relabelling inferred
from target equality.

## 3. Why an internal Cartan correction cannot replace \(J_*\)

Use the orbit basis \((H_w,SH_w)\). Since \(S\) fixes the Weyl target
defect, the target map is

\[
                             (a,b)\longmapsto a+b.     \tag{9}
\]

The even line is generated by \((1,1)\), while the target kernel is
generated by \((1,-1)\), the odd line. Their intersection is zero.
Starting from the signless vector and subtracting twice the first orbit
column gives

\[
                         (1,1)-2(1,0)=(-1,1),          \tag{10}
\]

which is merely the odd target-safe prism. Hence a nonzero target-safe even
cell needs an independent target-bearing source direction. Equation (1)
supplies its diagonal input.

## 4. The first principal-parts residual

Using \(dH_w+H_wd=w-1\), equation (2) gives

\[
 dC_{2,+}
 =-{1\over2}(1+S)(w-1)P_2(I)
  +{1\over2}(1+S)H_wd(P_2(I)).                        \tag{11}
\]

The first term is the target correction (3). Define \(R_{2,+}\) by (4).
Then (11) is target minus \(R_{2,+}\). This is the complete formal
principal-parts residual; assigning it a literal lower occurrence value
requires \(P_2\).

The first available universal two-row target-cone candidate is already
fixed. Put
\(F=H_0-u\), and use rows

    reduced Eq:  F e_Eq
    target:      Y w.

The canonical target cone carrying \(-2D\,Yw\) has projected boundary

\[
             (-2DF e_{\rm Eq},\,-2DYw),               \tag{12}
\]

whereas the desired boundary is

\[
                         (0,\,-2DYw).                  \tag{13}
\]

The difference is (5), proving the sign in (6). The canonical derived
Koszul cell \(K_{\rm Eq}\), with \(dK_{\rm Eq}=Fe_{\rm Eq}\), has exactly
the right abstract differential. The missing operation is its
root-decorated, endpoint-even physical placement. The existing master
comparison records this as one regular involution orbit, not as an
independent Eq generator for every root.

This calculation does not identify the literal image of \(R_{2,+}\) with
(12). That image is undefined until \(P_2\) is constructed. Formula (4) is
the exact formal residual; (12) is the first residual of the strongest
currently available target-cone filler.

For the exact centered preimage, the previous checker gives the primitive
normal

\[
\begin{aligned}
N_v^{\rm prim}={}&
2(X_{0011}+X_{1100}+X_{1122}+X_{2211})-2X_{1111}\\
&-(X_{0101}+X_{0220}+X_{1010}+X_{1212}
 +X_{2002}+X_{2121}).
\end{aligned}
\]

The coordinate \(X_{0011}^{*}\) reads two on both its target and reduced-Eq
decorations. Thus the known cone candidate has a genuinely nonzero residual
before the root-decorated Koszul comparison is added.

## 5. Generic and singular scope

The construction has two logically distinct hypotheses.

1. The diagonal input (1) is polynomial and physical whenever the two
   diagonal cap rows are available.
2. The normalized target cone (2) is defined only on
   \(\alpha\beta\ne0\), and only after a shifted source-labelled placement
   \(P_2\) transports its word, fine grade, and adjacent filtration.

At \(\beta=0\),

\[
                         J_2=J_1,\qquad J_*^{(2)}=0.   \tag{14}
\]

The formal parameter-free right side of (2) cannot be declared a regular
specialization: obtaining it requires division by the vanishing
\(\alpha\beta\).
The selected collision coordinate therefore still requires the unary
target jet or the integral beta/Bockstein comparison.

The present theorem constructs neither that special extension nor the full
physical \(P_2\). It proves that after \(P_2\), target cancellation is
automatic and leaves the formal residual \(R_2^+\). For the strongest known
target-cone filler, the next debt is exactly the root-decorated reduced-Eq
comparison (6), followed by the literal adjacent lower landing.

## Verification

    python3 computations/verify_h2_lower_even_cartan_jstar_target_cone_gate.py
    python3 -O computations/verify_h2_lower_even_cartan_jstar_target_cone_gate.py
    python3 -I -S computations/verify_h2_lower_even_cartan_jstar_target_cone_gate.py
