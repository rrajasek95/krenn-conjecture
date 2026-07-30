# Pure target factors kill the scalar colon guard at its first polarization

## 1. Outcome

The all-27-row scalar packet in
[full-27-colon-cycle-macaulay-transfer-gap.md](full-27-colon-cycle-macaulay-transfer-gap.md)
cannot be the scalar shadow of a packet with even two independent target
directions at its distinguished site \(u_0\), while its data away from that
site are retained.

This is uniform on every odd common complement of size \(2h-1\), \(h\ge3\).
Replace the one-dimensional local space at \(u_0\) by an arbitrary
characteristic-zero vector space \(W\). Keep \(P,R,T\), every star component
away from \(u_0\), and every internal edge away from \(u_0\) equal to the
scalar guard. At \(u_0\), allow arbitrary vectors for all nine star
components and for **every** internal edge incident to \(u_0\), including
edges which were zero in the scalar packet. If the 27 rows hold with local
target factors

\[
                         E_0,E_1,E_2\in W,
\]

then necessarily

\[
                              \boxed{E_0=E_1.}             \tag{1}
\]

In fact, after imposing its 24 targetless off-diagonal rows, the complete
one-site coefficient map has compatible diagonal target image only

\[
             \mathbb Q(1,1,1)\subseteq\mathbb Q^3.        \tag{2}
\]

Thus \(E_0=E_1=E_2\). Equation (1) already excludes the physical target,
whose three local factors form a basis at every site.

The sparse certificate for (1) uses only four ordered rows. If
\(\mathscr L_{ijk}\) denotes the source side of the literal row, then the
coefficient of the fixed scalar top word away from \(u_0\) obeys

\[
 \boxed{
 \mathscr L_{000}-{8\over3}\mathscr L_{011}
       +{3\over8}\mathscr L_{100}-\mathscr L_{111}=0.}     \tag{3}
\]

The corresponding target side is \(E_0-E_1\). This is not a numerical
accident: (3) is the difference of the two normalized diagonal members of
the common-left-kernel packet.

Consequently the scalar full-27 packet remains a sharp guard against
**static cancellation**, but it is not a decorated purity guard. Target
decomposability is already active at one site. Its first general
consequence is that the common-kernel star must occupy at least two distinct
pure-colour sites. Removing those two slots leaves exactly \(2h-3\) target
factors, the odd degree missing from the proposed selector-to-Macaulay
transfer. Those factors are still a physical cofactor, not automatically a
binary clean-line covariant; constructing that latter map remains open.

The conjecture is not resolved by this note.

## 2. Uniform one-site polarization theorem

On the scalar packet use the labels

\[
                 e=0,\qquad a=1,\qquad b=2,
\]

and the common left kernel

\[
                 \xi=(-8,-3,0)^{\mathsf T}.              \tag{4}
\]

The scalar stars satisfy

\[
                    L=x(\xi)=\sum_i\xi_i x_i=u_0.         \tag{5}
\]

Let \(D_h=\{u_0,\ldots,u_{2h-2}\}\), and let

\[
                  \Omega'_h=\prod_{r=1}^{2h-2}u_r         \tag{6}
\]

denote the scalar top word on the complement of \(u_0\). In a one-site
polarization, write \(\widetilde L_0\in W\) for the remaining \(u_0\)
component of \(x(\xi)\). The off-site components still cancel by (5), so

\[
                      \widetilde L=\widetilde L_0^{(u_0)}. \tag{7}
\]

Contracting the full rows by \(\xi_i\), with no factor cancelled, gives

\[
 \widetilde L\left(y_jt_k+{T_{jk}\over h-1}z\right)
        z^{[h-2]}=\delta_{jk}\xi_jE_j\Omega'_h.           \tag{8}
\]

For \(j=k=0\) or \(j=k=1\), every summand in the parenthesis or in the
radial power which uses \(u_0\) dies on multiplication by
\(\widetilde L_0^{(u_0)}\). This includes every newly allowed internal
edge incident to \(u_0\). Hence only the unchanged off-site scalar
cofactor contributes.

In the original scalar guard, (8), (5), and the normalized target
coefficient one say that these two complementary cofactors are respectively

\[
                              \xi_0\Omega'_h,
                 \qquad      \xi_1\Omega'_h.             \tag{9}
\]

Substitution into the polarized equations therefore yields

\[
 \xi_0\widetilde L_0\Omega'_h=\xi_0E_0\Omega'_h,
 \qquad
 \xi_1\widetilde L_0\Omega'_h=\xi_1E_1\Omega'_h.         \tag{10}
\]

Coefficient extraction in the direct tensor factor
\(W\otimes\mathbb Q\Omega'_h\), followed by scalar division by the nonzero
numbers \(\xi_0,\xi_1\), proves (1). No element of the matching algebra,
no power of \(z\), and no component of \(\widetilde L\) has been cancelled.

To obtain (3), divide the \(j=0\) contraction by \(\xi_0=-8\), divide the
\(j=1\) contraction by \(\xi_1=-3\), and subtract. Explicitly,

\[
 {1\over\xi_0}\sum_i\xi_i\mathscr L_{i00}
 -{1\over\xi_1}\sum_i\xi_i\mathscr L_{i11}
 =\mathscr L_{000}+{3\over8}\mathscr L_{100}
   -{8\over3}\mathscr L_{011}-\mathscr L_{111}.          \tag{11}
\]

Both normalized source coefficients equal
\(\widetilde L_0\Omega'_h\), while the normalized target coefficients are
\(E_0\) and \(E_1\). This proves the sparse certificate uniformly.

## 3. Complete linear audit at the first boundary

At \(h=3\), scalarize the other four sites and allow the following thirteen
independent \(W\)-valued local data:

\[
 x_{0,0},x_{1,0},x_{2,0},
 y_{0,0},y_{1,0},y_{2,0},
 t_{0,0},t_{1,0},t_{2,0},
 z_{01},z_{02},z_{03},z_{04}.                             \tag{12}
\]

For one coordinate of \(W\), taking the top coefficient in each of the 27
rows defines a rational matrix

\[
                         \Phi_3:\mathbb Q^{13}\longrightarrow
                                  \mathbb Q^{27}.          \tag{13}
\]

Write \(\pi_{\rm diag}\) and \(\pi_{\rm off}\) for the diagonal and
off-diagonal row projections. Then

\[
 \operatorname {rank}\Phi_3=13,
 \qquad
 \operatorname {rank}(\pi_{\rm off}\Phi_3)=12.           \tag{14}
\]

The kernel of the 24 off-diagonal rows is the one-dimensional line

\[
 x_{1,0}={\lambda\over3},\qquad
 y_{0,0}=-\lambda,\qquad
 t_{2,0}=\lambda,                                         \tag{15}
\]

with every other coordinate in (12) zero. The three diagonal outputs on
this line are

\[
                              (-\lambda,-\lambda,-\lambda), \tag{16}
\]

and hence

\[
 (\pi_{\rm diag}\Phi_3)\bigl(\ker(\pi_{\rm off}\Phi_3)\bigr)
                  =\mathbb Q(1,1,1).
\]

This proves (2). (No claim is made that the unrestricted projection
\(\pi_{\rm diag}\Phi_3\) has rank one.) In particular, permitting arbitrary
formerly absent incident \(z\)-directions does not create a second target
direction.

Under the uniform suspension by disjoint matching edges, the same thirteen
columns tensor by the new top word. A new \(u_0\)-edge to one member of a
suspension pair strands the other member and has zero top coefficient.
Thus for every \(h\ge3\), the full one-site map still has rank thirteen,
its off-diagonal part has rank twelve, and its compatible diagonal target
image is (2). The proof in Section 2 is the coordinate-free reason for this
stability.

## 4. What purity supplies in a genuine packet

The one-site obstruction is not special to the numerical guard at the
level of its qualitative conclusion. In any genuine target-centred packet,
the two left anchors are

\[
 L C_e z^{[h-2]}=\xi_eX_e,
 \qquad
 L C_a z^{[h-2]}=\xi_aX_a,                               \tag{17}
\]

where \(\xi_e\xi_a\ne0\). The pure-factor lemma forces a site \(r_e\)
with \(L_{r_e}\in\mathbb C^*e_e^{(r_e)}\), and a site \(r_a\) with
\(L_{r_a}\in\mathbb C^*e_a^{(r_a)}\). Since the two target vectors at one
site are independent,

\[
                              r_e\ne r_a.                 \tag{18}
\]

This explains exactly why the scalar packet, where \(L=u_0\), cannot be
polarized. It also gives a naturally typed **physical** odd cofactor. For

\[
                         S=\{r_e,r_a\},
\]

target decomposability writes

\[
 X_c=X_{c,S}\otimes X_{c,D_h\setminus S},
 \qquad
 \deg_{\rm site}X_{c,D_h\setminus S}=2h-3.               \tag{19}
\]

The parity is exactly right: a selector covector has degree two, and the
Macaulay dual has degree \(2h-1\). But the cofactor in (19) lies in

\[
                  \bigotimes_{x\in D_h\setminus S}V_x,    \tag{20}
\]

not in \(\operatorname {Sym}^{2h-3}U^*\) for the binary clean-line
parameter space \(U\). To turn (20) into an odd binary covariant one needs
source-derived local maps

\[
                      \phi_x:V_x\longrightarrow U^*
                 \qquad(x\in D_h\setminus S),             \tag{21}
\]

compatible with the same clean line, the same ordered overlap, and every
Macaulay shift. Then, and only then, the product

\[
 \chi_{2h-3}=\prod_{x\notin S}\phi_x(e_c^{(x)}),
 \qquad
 \vartheta_{2h-1}=\vartheta_2\chi_{2h-3}                  \tag{22}
\]

is a well-typed Cartan candidate. Equations (17)--(19) do not construct
the maps (21), nor do they prove the Hankel equations for (22).

## 5. Three anchor labels do not force three distinct witness sites

There is a second incidence caveat at \(h=3\). The left packet gives
\(e,a\)-pure sites for \(L\), and the right packet gives \(e,b\)-pure sites
for its common factor. These facts do not imply that three distinct sites
can be selected.

Here is an exact guard in the site-square-zero algebra on any \(m\ge2\)
sites. At sites \(0,1\), put

\[
 L=e_0^{(0)}+e_1^{(1)},
 \qquad
 S=e_0^{(0)}+e_2^{(1)}.                                  \tag{23}
\]

For a colour \(c\), let \(H_c^{\widehat r}\) be the pure-\(c\) tensor on
all sites except \(r\). Then collision at the occupied site gives the four
literal identities

\[
 \begin{aligned}
 L H_0^{\widehat0}&=X_0,&
 L H_1^{\widehat1}&=X_1,\\
 S H_0^{\widehat0}&=X_0,&
 S H_2^{\widehat1}&=X_2.
 \end{aligned}                                           \tag{24}
\]

All three \(X_c\) are independent decomposable target tensors, but every
pure-factor witness in (24) lies at site \(0\) or \(1\). This guard does
not have the common radial power or the 27 ordered rows; its exact purpose
is to rule out an inference of a three-site cubic solely from the four
anchor factorizations. A source-derived cubic at \(h=3\) must use further
ordered-row or clean-line data.

## 6. Scope and checker

The positive result is the uniform one-site polarization obstruction
(1)--(3). It proves that the scalar colon-cycle packet cannot be promoted
to independent pure targets even at its first local factor. It does not
prove that an arbitrary target-centred packet has a one-site common-kernel
star; genuine packets must instead have the two-site incidence (18).

The remaining all-order question is now more precise: use the literal
ordered rows to construct the maps (21), and then prove that one nonzero
candidate (22) satisfies all common Hankel equations. Merely counting the
remaining \(2h-3\) target factors is insufficient.

The lightweight checker
[verify_pure_target_one_site_polarization_odd_cofactor.py](../computations/verify_pure_target_one_site_polarization_odd_cofactor.py)
reuses the audited scalar packet constructor and, over exact rationals,
verifies for \(3\le h\le8\):

* the imported scalar target normalization, all 27 literal rows, and their
  contracted forms;
* the complete one-site map with all incident internal-edge directions;
* ranks thirteen and twelve in (14);
* the sparse four-row certificate (3), including its target functional;
* the compatible diagonal target image (2) and the explicit line
  (15)--(16);
* exact suspension of the thirteen base columns and vanishing of every new
  incident-edge column; and
* the two-site collision identities (24).
