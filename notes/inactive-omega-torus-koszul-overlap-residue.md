# The all-inactive Omega certificate leaves one torus-Koszul residue

## 1. Outcome

Let

\[
                         d=h-2\geq1
\]

and suppose a routed unary--complementary cap pencil has

\[
 {\cal E}(t,u)=tu\,\Omega(t,u),\qquad
 \Omega\in V\otimes\mathbb C[t,u]_d,
\]

with no clean point on the activity torus.  The proved bounded
certificate is

\[
 H\in V^*\otimes\mathbb C[t,u]_d,
 \qquad \langle H,\Omega\rangle=(tu)^d.                 \tag{1}
\]

Let \(C\) be the odd-site residue quotient and let
\(0\ne\zeta_c\in C\) be one physical boundary-polar defect transported
unchanged through the two-chart connection.  On
\(S_{2d}=\mathbb C[t,u]_{2d}\), use the boundary-torus Koszul operator

\[
                  {\mathscr D}=t\partial_t-u\partial_u.       \tag{2}
\]

Its cokernel is one copy of the weight-zero line:

\[
\boxed{
 {C\otimes S_{2d}\over {\mathscr D}(C\otimes S_{2d})}
       \ \cong\ C,\qquad
 [Q]\longmapsto [t^du^d]Q.}                                \tag{3}
\]

The displayed isomorphism uses the ordered endpoint coordinates and the
chosen generator \((tu)^d\) of the weight-zero line.  Intrinsically, the
cokernel is \(C\) tensored with that line; endpoint rescaling does not fix a
generator of it.  Thus the equalities below with \(\zeta_c\) and
\(-\zeta_c\) use the normalization (1), while their vanishing or
nonvanishing is independent of the remaining endpoint gauge.

Tensoring (1) with the physical defect therefore gives

\[
\boxed{
 [\zeta_c\langle H,\Omega\rangle]
       =[\zeta_c(tu)^d]=\zeta_c
 \quad\text{in the cokernel of }{\mathscr D}.}             \tag{4}
\]

In this normalization the class is nonzero, independent of the chosen
Bezout certificate, and uniform in \(h\).  No common matching power or
site-algebra factor is cancelled.  In coefficient language, (4) is exactly
the sole middle convolution coefficient of (1).

Consequently, two flatly transported certificates do **not** turn the
boundary-polar defect into a \({\mathscr D}\)-coboundary in this coefficient
complex.  Their difference is zero, but their common torus-Koszul class
remains (4).  Within this routed coefficient model, a source-faithful
overlap can satisfy the required coboundary equation only by supplying a
correction
\(G_c\in C\otimes S_{2d}\) whose one middle coefficient is

\[
\boxed{
 \mathfrak T_c(G_c):=[t^du^d]G_c=-\zeta_c.}                \tag{5}
\]

Equivalently, the sole obstruction is the named class

\[
\boxed{
 \mathfrak o_c(G_c):=[t^du^d]G_c+\zeta_c\in C,}            \tag{6}
\]

the **inactive Omega overlap residue**.  Once a literal source comparison
with the requisite chain properties constructs \(G_c\), vanishing of (6)
is equivalent to the full torus-Koszul coboundary equation.  Every
noncentral coefficient then has an explicit primitive obtained by division
by its nonzero torus weight.  There is no additional all-order coefficient
ledger inside this model.

Within the currently selected tilted/direct-free overlap packet, the
candidate physical carrier for (5) is explicit.  On an active tilted
auxiliary it is the curvature-normal term

\[
                 \Gamma_{bd}(K)z
        =(a\kappa+b\Gamma_{bd}(J))z,                       \tag{7}
\]

and on the intrinsic direct-free boundary it is

\[
                         C_4-Dv=AUz.                        \tag{8}
\]

What is not constructed is the source-filtered prolongation which sends
(7), or (8), to a degree-\(2d\) correction \(G_c\) satisfying (5).
The triangular recovery of \(z\) in (8) does not itself define that
prolongation.

Section 6 gives an exact all-order guard: the bounded certificate, a
nonzero transported defect, a nonzero curvature coefficient, and the
direct-free triangular auxiliary coexist with
\(\mathfrak T_c=0\).  The guard is formal at the overlap-module level,
not a literal ternary source.  It shows that (5) is an additional
source-level requirement rather than a consequence of the certificate,
flat transport, or triangular split.  The conjecture remains open.

## 2. Exactness of the torus-Koszul coefficient complex

Use the monomial basis

\[
                     m_n=t^{2d-n}u^n,\qquad 0\le n\le2d.
\]

The operator (2) is diagonal:

\[
                       {\mathscr D}(m_n)=2(d-n)m_n.          \tag{9}
\]

Thus its kernel is \(\mathbb C\,(tu)^d\), and its image consists exactly
of the degree-\(2d\) forms whose \(t^du^d\)-coefficient is zero.  Tensoring
with \(C\) gives the exact sequence

\[
0\longrightarrow C\otimes\mathbb C\,(tu)^d
 \longrightarrow C\otimes S_{2d}
 \mathop{\longrightarrow}^{\mathscr D} C\otimes S_{2d}
 \mathop{\longrightarrow}^{\operatorname {mid}} C
 \longrightarrow0,                                        \tag{10}
\]

where

\[
                         \operatorname {mid}(Q)=[t^du^d]Q.
\]

The explicit primitive of

\[
 Q=\sum_{n=0}^{2d}Q_nm_n,\qquad Q_d=0,
\]

is

\[
                 K=\sum_{n\ne d}{Q_n\over2(d-n)}m_n,
                 \qquad {\mathscr D}K=Q.                    \tag{11}
\]

This is the homogeneous Koszul form of the logarithmic boundary
calculation.  On the activity torus, put \(z=u/t\).  After the harmless
scalar regrading by the central monomial, (2) becomes
\(-2z\partial_z\); its only Laurent cokernel is the constant term, or
equivalently the residue of the corresponding form against
\(dz/z\).  Equations (9)--(11), rather than this interpretation, prove
(3) without localizing or cancelling any factor.

The unary and complementary physical endpoints distinguish the two
coordinate axes.  Rescaling either endpoint preserves the central
weight-zero line, and exchanging the endpoints replaces
\({\mathscr D}\) by \(-{\mathscr D}\) while fixing that line.  Hence the
vanishing or nonvanishing of (4) is independent of the remaining endpoint
gauge.

## 3. The bounded certificate occupies the unique cokernel line

Write

\[
 \Omega=\sum_{k=0}^{d}t^{d-k}u^kE_k,\qquad
 H=\sum_{r=0}^{d}t^{d-r}u^rH_r.                            \tag{12}
\]

Equation (1) is equivalent to the full convolution ledger

\[
 c_n:=\sum_{r+k=n}H_r(E_k)=\delta_{n,d},
 \qquad 0\le n\le2d.                                      \tag{13}
\]

Tensoring (13) by \(\zeta_c\) leaves precisely

\[
                (0,\ldots,0,\zeta_c,0,\ldots,0),           \tag{14}
\]

with its nonzero entry at torus weight zero.  Equations (9)--(10) prove
(4).  This also explains why endpoint equations alone miss the
obstruction: every endpoint and noncentral convolution coefficient
vanishes, while the middle coefficient is normalized to one.

If \(H'\) is another bounded certificate, then

\[
                    \langle H-H',\Omega\rangle=0.           \tag{15}
\]

Hence (4) is certificate-independent.  Likewise, if two charts have
certificates \((H_0,\Omega_0)\) and \((H_1,\Omega_1)\), then

\[
 \langle H_0,\Omega_0\rangle-\langle H_1,\Omega_1\rangle=0. \tag{16}
\]

Flat equality of their physical defects identifies the two copies of
(4); it does not annihilate either copy.  Reversing chart orientation
changes both the comparison and the chosen sign of \(G_c\), but does not
remove the weight-zero class.

## 4. One-coefficient criterion for a physical overlap

Suppose the literal source overlap, after retaining its direct/star/internal
grading and passing to the odd residue quotient, produces

\[
                         G_c(t,u)\in C\otimes S_{2d}.         \tag{17}
\]

The required coefficient coboundary is the existence of
\(K_c\in C\otimes S_{2d}\) such that

\[
 \zeta_c\langle H,\Omega\rangle+G_c
                              ={\mathscr D}K_c.              \tag{18}
\]

By (10), equation (18) holds if and only if

\[
                         [t^du^d]G_c+\zeta_c=0.              \tag{19}
\]

This proves the equivalence with the single class (6).  If (19) holds,
the primitive is the explicit weighted sum (11) applied to
\(\zeta_c(tu)^d+G_c\).  Thus the entire higher-degree coefficient problem
inside this torus-Koszul model is solved once the physical overlap
correction and its middle coefficient are known.  This does not construct
the source map that produces that correction or prove that exactness of the
coefficient model closes the literal full-nine branch.

Equation (18) is the precise torus-Koszul model of “the transported
boundary-polar defect becomes a boundary coboundary.”  It is not asserted
to follow from flat transport.  Constructing \(G_c\) from the literal
source rows, with the displayed source grading, and proving that this
construction is the relevant chain-level comparison are separate physical
requirements.  In particular, replacing the overlap by a second bounded
identity gives \(G_c=0\), and (19) fails whenever \(\zeta_c\ne0\).

## 5. Location of the missing class in the tilted and direct-free packets

Use the all-label power-free overlap identity

\[
\begin{aligned}
 \Gamma_{bd}(K)
   &=\sum_{i,k}K_{ik}(P_{ib}S_{kd}-R_{ik}Q_{bd}),\\
 \sum_{i,k}K_{ik}(&S_{kd}f_{ib}+t_kH_{ib;d}
       -Q_{bd}g_{ik}-y_bN_{ik;d})\\
   &=\sum_{i,k}K_{ik}(P_{ib}t_k-R_{ik}y_b)v_d
       +\Gamma_{bd}(K)z.                                  \tag{20}
\end{aligned}
\]

On the active tilted line \(K(a,b)=aE_{ac}+bJ\),

\[
                 \Gamma_{bd}(K)=a\kappa+b\Gamma_{bd}(J),
                 \qquad \kappa\ne0.                         \tag{21}
\]

Modulo the ordinary matrix-cap connection terms in (20), the unresolved
normal class is represented by \(\Gamma_{bd}(K)z\).  Therefore, if a
source-filtered prolongation

\[
 \Psi_c:\{\text{filtered overlap rows}\}
                   \longrightarrow C\otimes S_{2d}          \tag{22}
\]

is constructed and sends those ordinary connection terms to
\({\mathscr D}\)-boundaries, the required correction is represented by

\[
                         G_c=\Psi_c(\Gamma_{bd}(K)z).         \tag{23}
\]

This already-routed coefficient packet would then reduce exactly to

\[
             [t^du^d]\Psi_c(\Gamma_{bd}(K)z)=-\zeta_c.       \tag{24}
\]

This statement is conditional on the construction, grading, and chain-map
properties of \(\Psi_c\).  The power-free row alone does not supply that
map.  Nor does it route an arbitrary selected all-inactive line into the
diagonal unary--complementary Omega packet assumed in Section 1.

If the auxiliary direct block is identically zero, the selected overlap
is triangular:

\[
                 D=At,\qquad C_4=Dv+AUz,\qquad AU\ne0.        \tag{25}
\]

Hence the same candidate normal carrier is exposed without localizing the
auxiliary chart:

\[
                         C_4-Dv=AUz.                          \tag{26}
\]

This is the useful one-sided form.  It recovers \(z\) before any common
power is inserted, but it does not permit cancellation after insertion
into a top matching row.  The missing operation is the filtered
prolongation from (26) to (23).  Within an already-routed Omega packet,
once that prolongation has the stated chain and grading properties, the
torus-Koszul coefficient calculation reduces to (24), not to an \(h=3\)
endpoint-column census or a second-chart activity theorem.  Branch-specific
routing into the first-chart Omega packet remains a separate obligation for
the actual all-inactive branch.

## 6. A uniform guard for the abstract overlap interface

Let \(C=\mathbb Q\zeta\), and let \(V\) have independent vectors
\(A_0,B_0,Z\).  Define a boundary map

\[
             D(A_0)=D(B_0)=0,\qquad D(Z)=\zeta.              \tag{27}
\]

For every \(d\ge1\), put

\[
 \Omega=t^dA_0+u^dB_0,\qquad
 H=u^d\alpha,\qquad
 \alpha(A_0)=1,\quad\alpha(B_0)=\alpha(Z)=0.                \tag{28}
\]

Then

\[
                  \langle H,\Omega\rangle=(tu)^d,           \tag{29}
\]

and \(\Omega\) has no zero on \(D(tu)\).  Take the formal first polar
\(\Pi=A_0+Z\) and endpoint value \(E_0=A_0\).  Their defect is

\[
                         D(\Pi-E_0)=\zeta\ne0.                \tag{30}
\]

Use identical copies for two charts and identify their copies of \(C\).
This gives exact flat transport of the same nonzero defect.

Add the direct-free power-free auxiliary over
\(\mathbb Q[T,V,Z_0]\) by setting

\[
                         D_0=T,\qquad C_4=TV+Z_0,             \tag{31}
\]

so that

\[
                         C_4-D_0V=Z_0                         \tag{32}
\]

is (26) with \(A=U=1\).  The curvature coefficient is nonzero and the
triangular split is exact.  None of (27)--(32) prescribes a filtered map
from \(Z_0\) to \(C\otimes S_{2d}\); taking that map to be zero is
compatible with every displayed identity.  Thus \(G=0\), and

\[
                         \mathfrak o_c(0)=\zeta\ne0.          \tag{33}
\]

This guard retains more than the bare arbitrary-defect interface: it also
retains the nonzero-curvature direct-free triangular auxiliary.  It proves
that power-free recovery of the common quadratic does not automatically
give the middle coefficient (24).

The guard is not a literal full-nine matching source.  Its vectors and
first polar are formal, and it deliberately leaves the source-filtered
prolongation unspecified.  It therefore does not disprove (24) for a
physical source.  It shows that a positive proof must construct that map
from the decorated rows and compute its one torus-Koszul residue, rather
than infer a coboundary from the bounded certificates, flat transport, or
triangularity alone.

## 7. Exact remaining coefficient target for a routed packet

Assume first that the selected all-inactive line has been routed into the
first-chart diagonal unary--complementary clean pencil of Section 1, with a
surviving nonzero defect \(\zeta_c\).  This routing is not proved in general.
For such a packet, the uniform coefficient target can be stated without
assuming activity or a canonical unary--complementary pencil on the
auxiliary chart:

> Starting from the active first chart and its bounded Omega certificate,
> use the literal tilted overlap, or the direct-free triangular packet, to
> construct a source-filtered map \(\Psi_c\) for one surviving diagonal
> label \(c\).  Prove that its curvature-normal image satisfies (24).

The result would make (18) a genuine torus-Koszul coboundary inside the
displayed coefficient complex.  Since the certificate contributes the
nonzero physical class (4), the required source-normal contribution must
be exactly its negative.  Equation (24) is nevertheless a reduction target,
not by itself a closure theorem: to infer a contradiction to simultaneous
all-inactive behavior and obtain an active clean point, one must prove that
the literal source construction of \(\Psi_c\) is the required chain
comparison and that its exactness has that physical consequence.

Thus the actual all-inactive branch still has two distinct obligations:
branch-specific routing into the first-chart Omega packet, and construction
plus middle-coefficient evaluation of the source-filtered comparison (with
its closure implication).  Once the first routing is available, the
auxiliary need not satisfy a second activity theorem or carry its own
canonical Omega pencil, and no endpoint rank test replaces (24).
