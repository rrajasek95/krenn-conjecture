# The five quadratic reset faces reduce to one primitive aggregate

## Outcome

For the degree-four mixed/pure Koszul cell

\[
 K_m=H_mr_0-(H_0-u)r_m,\qquad m=01211222,
\]

the bare reset at the internal word \(\bar m=12112\) has five genuinely
independent quadratic denominator faces. If \(D=\{1,2,3,4,5\}\), then

\[
 h_v=\operatorname {Haf}
       \left(q_{\bar m}|_{D\setminus\{v\}}\right)
     =\sum_{N\in\operatorname {PM}(D\setminus\{v\})}q_{v,N}.       \tag{1}
\]

The fifteen matching monomials in (1) are pairwise distinct. Hence the raw
mixed face matrix is

\[
                       I_5\otimes(1,1,1)^{\mathsf T}               \tag{2}
\]

and has rank five. The five analogous pure quadrics \(g_v\) have disjoint
colour support from every \(h_v\); the combined pure/mixed rank is ten.
Thus neither the pure row nor the \(H_0r_m\) correction cancels the
quadratic initial face of the \(u r_m\) term.

The raw quadrics in (1) live one grade below the repeated cap packet. After
multiplying by the selected incident cell \(t_v\), put

\[
                         Q_{v,N}=t_vq_{v,N}.
\]

Conditional on a source-valid common-tail/Rees lift carrying all product-rule
faces, the exact physical matching/Hasse routes are

\[
       b_{v,N}=-\Omega_v+Q_{v,N},\qquad
       \lambda_v=\Omega_v+\sum_NQ_{v,N},                         \tag{3}
\]

and the induced repeated-grade face matrix is exactly

\[
                         \lambda(h_v)=3e_v,\qquad
                         [\lambda(h_v)]_{v=1}^5=3I_5.             \tag{4}
\]

Bare matching switches, Hasse shuffles, and Bianchi differences do not
construct this grade transport or contract the raw reset. Once the
transported faces are in the repeated packet, the newer source-provenant
endpoint-odd Cartan/Hasse orbit supplies the cyclic standard directions

\[
 -e_1+e_3,\ -e_3+e_5,\ -e_5+e_2,\ -e_2+e_4,\ -e_4+e_1.           \tag{5}
\]

Their integral image is the saturated rank-four lattice
\(\ker(\epsilon:\mathbb Z^5\to\mathbb Z)\), where
\(\epsilon=\sum_v\lambda_v\). Therefore the transported version of (3),
together with the physical orbit (5), leaves exactly one primitive
aggregate class. This is a conditional cap reduction: bare multiplication
by \(t_v\) has additional Hasse product-rule faces and is not the missing
source-valid lift.

The dependency-pinned checker is
[verify_h3_degree4_koszul_reset_quadratic_face_aggregate_gate.py](../computations/verify_h3_degree4_koszul_reset_quadratic_face_aggregate_gate.py).

## 1. The literal five quadrics

Suppressing the fixed colour decorations on the ten internal edges,

\[
\begin{aligned}
h_1&=q_{23}q_{45}+q_{24}q_{35}+q_{25}q_{34},\\
h_2&=q_{13}q_{45}+q_{14}q_{35}+q_{15}q_{34},\\
h_3&=q_{12}q_{45}+q_{14}q_{25}+q_{15}q_{24},\\
h_4&=q_{12}q_{35}+q_{13}q_{25}+q_{15}q_{23},\\
h_5&=q_{12}q_{34}+q_{13}q_{24}+q_{14}q_{23}.
\end{aligned}                                                        \tag{6}
\]

Every \(q_{ij}\) carries colours \((\bar m_i,\bar m_j)\). A monomial in
\(h_v\) uses exactly the four sites \(D\setminus\{v\}\), so monomial
supports from different deletion sites cannot coincide. Replacing all
colours by zero gives the pure \(g_v\). Their variables are different
decorated physical edge variables, so the mixed and pure supports are
disjoint. Exact ranks are: mixed five, pure five, combined ten.

The coefficient of \(r_m\) in \(K_m\) is \(u-H_0\). Extracting the
coefficient of the independent homogenizer \(u\) sees (2) unchanged. The
\(H_0h_v\) term starts in degree six and cannot cancel the quadratic face.

## 2. First higher polynomial syzygies

There is no constant or linear-coefficient relation among the five
quadrics. Exact rational reduction gives

| coefficient degree | columns | rank | kernel |
|---:|---:|---:|---:|
| 0 | 5 | 5 | 0 |
| 1 | 50 | 50 | 0 |
| 2 | 275 | 265 | 10 |

The degree-two kernel is exactly the span of the ten pairwise Koszul
relations

\[
                         h_w e_v-h_v e_w,\qquad v<w.                \tag{7}
\]

Thus the smallest bare polynomial higher syzygies have total degree four,
but (7) supplies only quadratic-weighted comparisons. It contains no unit
coefficient and no primitive aggregate nullhomotopy. An abstract appeal to
Koszul syzygies does not construct the missing physical reset chain.

## 3. Exact conditional physical face quotient

Use the twenty cap rows

\[
 \{\Omega_v:1\le v\le5\}
 \sqcup\{Q_{v,N}:1\le v\le5,\ N\in\operatorname {PM}(D\setminus\{v\})\}.
\]

The fifteen repeated-grade route columns (3) have rank fifteen and primitive cokernel
\(\mathbb Z^5\), detected by the \(\lambda_v\). Identifying the three
monomials of \(t_vh_v\) with its three labelled \(Q_{v,N}\) entries proves
(4), including the integral factor three, after the common-tail lift:

\[
                         \epsilon(h_v)=3.                            \tag{8}
\]

The physical endpoint-odd Cartan theorem is load-bearing after entry into
this repeated grade. It proves
that the cyclic paths inducing (5) are source-provenant in the complete
principal-parts orbit and preserve the canonical repeated grade. Merely
taking matching switches or formal Bianchi differences in the raw quadratic
packet neither constructs \(q_{v,N}\mapsto Q_{v,N}\) nor kills a cross-face
class. In the repeated packet, the additional Cartan/Hasse orbit kills the
standard four-space.

The combined route plus Cartan matrix has rank \(19\) in the
twenty-dimensional cap module. Its primitive dual is

\[
                          \epsilon=\sum_v\lambda_v.                  \tag{9}
\]

A single reduced cap entry, for example

\[
                          p=-Q_{1,N_0},\qquad\epsilon(p)=-1,          \tag{10}
\]

raises the rank to twenty integrally. Consequently \(3p\), together with
route and Cartan paths, fills any transported reset face \(t_vh_v\); cyclic
transport fills all five. Algebraically, after a typed Rees lift, one
primitive aggregate attachment is necessary and sufficient.

## 4. Direct-free guard: three bright tangents, one dark aggregate

At the direct-free guard only \(q_{12}=a\) and \(q_{14}=b\) are supported.
Linearizing (6) gives

\[
\begin{array}{c|l}
v&dh_v\\ \hline
1&0,\\
2&b\,dq_{35},\\
3&a\,dq_{45}+b\,dq_{25},\\
4&a\,dq_{35},\\
5&a\,dq_{34}+b\,dq_{23}.
\end{array}                                                     \tag{11}
\]

For \(ab\ne0\), this Jacobian has rank three. Its left kernel is

\[
             \left\langle e_1,\;a e_2-b e_4\right\rangle.        \tag{12}
\]

The intersection of (12) with the standard sum-zero lattice is the single
line

\[
                 (b-a)e_1+a e_2-b e_4.                           \tag{13}
\]

Therefore bright first-order exits remove three directions, the physical
standard comparison removes one more dark direction, and the quotient is
again one primitive aggregate. This is the tangent shadow of (9), not a
different obstruction.

Both directions in (12) begin in the two-new-cell layer. The first has the
three terms of \(h_1\). In the opposite-face direction the common
\(dq_{35}\) term cancels and

\[
\begin{aligned}
a h_2-b h_4
={}&a q_{13}q_{45}+a q_{15}q_{34}\\
 &-b q_{13}q_{25}-b q_{15}q_{23}.                    \tag{14}
\end{aligned}
\]

Every monomial in (14) uses two cells absent from the guard. The pinned E14
two-cell theorem makes every such fixed two-cell extension a literal source
unit; the pinned three-cell theorem does the same for every cubic proper
face which a Rees totalization can create, provided the lift retains the
same canonical internal E14 chart.

This is a conditional terminal handoff, not yet the lift. The unit witness
depends on the chosen support, and the three-cell theorem explicitly does
not supply a universal triangular order. A source-valid Rees/initial-form
cell must first isolate a leading two- or three-cell support while preserving
word, fine grade, target, and protected readouts. Once that is done, the
existing unit theorem terminalizes that branch. Without it, citing the
finite unit censuses would repeat the unresolved witness-gluing step.

## 5. The smallest remaining physical theorem

Equation (10) is only a cap vector. The missing theorem is:

> Construct one source-valid seven-occurrence relative total cell in word
> 01211222 and the labelled repeated P3+K2 grade whose induced cap face has
> \(\epsilon=\pm1\), and whose endpoint, pairwise-Hasse, mixed
> endpoint/matching, cubic-Hasse, ridge, Eq, W, target, anchor, physical-q,
> ordinary-residue, eta, and sigma faces are the specified packet or
> committed physical boundaries.

The theorem includes the common-tail/Rees totalization: it must carry the
raw quadrics into the repeated \(Q_{v,N}\) packet and absorb every Leibniz
face. Once that exists, multiplying the primitive cap by three and adding
the physical standard paths nullhomotopes every transported quadratic reset
face. No constant or linear polynomial correction can replace it, by the
syzygy calculation.

This note constructs neither the common-tail lift nor the aggregate cell.
It also does not promote the aggregate dual (9) to a complete physical
terminal. The exact advance is the classification: five raw quadrics; no
bare cross-face filler; and, conditional on source-valid repeated-grade
entry, rank four of physically filled standard directions plus one
primitive aggregate—not five unrelated source theorems.

## Verification

Run the checker normally, with Python optimization, and in isolated/no-site
mode. Frozen ledger SHA-256:

    c6a3e6df4b74ae52478bd2c32c3e61483751f8c879ad4832824da0d99a82ec3f
