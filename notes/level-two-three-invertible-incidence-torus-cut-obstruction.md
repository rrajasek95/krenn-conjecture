# A four-parameter three-invertible incidence family has no factored pure L0 slice

Research evidence only. Krenn's conjecture remains open,
**SP-CLEAN-BRIDGE** is untouched, and no certified dependency changes.

## Exact scope

Start with [the exact \(3I+1R+2Z\) tangent-incidence survivor](level-two-three-invertible-l0-incidence-survivor.md),
whose only change from the original R2 guard is

\[
 M_{34}=\begin{pmatrix}12&0\\0&0\end{pmatrix}.
\]

There is a four-parameter algebraic torus through this point on which

\[
 \operatorname{rank}D=55,\qquad
 \operatorname{rank}D_{\rm mixed}=53,
\]

both pure targets remain in \(\operatorname{im}D\), and the pure-zero
factored-L0 cut equations have no solution. Thus the base incidence
survivor and every member of this torus fail the factored pure-zero L0
screen. This result concerns only this four-dimensional subfamily; it does
not classify the full free-block incidence locus.

## The torus parameterization

Let

\[
 h_{4,0}=a_0,\quad h_{4,1}=a_1,\qquad
 h_{5,0}=b_0,\quad h_{5,1}=b_1
\]

be nonzero, and put \(h_{r,i}=1\) for \(r=0,1,2,3\). Define

\[
 M^h_{ru}(i,j)=h_{r,i}h_{u,j}M_{ru}(i,j).             \tag{1}
\]

Only the eight blocks joining \(\{0,1,2,3\}\) to \(\{4,5\}\) can change:
equivalently, every \(M_{r4}\) is multiplied on the right by
\(\operatorname{diag}(a_0,a_1)\), and every \(M_{r5}\) by
\(\operatorname{diag}(b_0,b_1)\). These are precisely zero-multiplier
blocks. The block \(M_{45}=0\) remains zero, while all determined blocks on
\(\{0,1,2,3\}\) remain fixed. Nonzero diagonal scaling also preserves the
complete zero pattern, hence all literal pure-column R2 witnesses.

For a residual word \(x\) and a tangent cell \(c=(ru,i,j)\), write

\[
 R_x=\prod_{v=0}^5h_{v,x_v},\qquad C_c=h_{r,i}h_{u,j}.
\]

Every perfect matching uses every residual vertex once, and every cofactor
matching uses every vertex except the two endpoints of its tangent cell.
Term by term this gives

\[
 \Psi(M^h)=R\Psi(M),\qquad D^h=RDC^{-1}.               \tag{2}
\]

Here \(R\) and \(C\) are invertible diagonal matrices over
\(\mathbb Q[a_0^{\pm1},a_1^{\pm1},b_0^{\pm1},b_1^{\pm1}]\). Therefore all
full and mixed differential ranks are unchanged. Each pure basis vector is
an eigenvector of \(R\), so (2) also preserves membership of both
\(e_{0^6}\) and \(e_{1^6}\) in the differential image.

## Uniform factored-L0 obstruction

Choose the exact base preimage \(K\) with \(DK=e_{0^6}\). If
\(R_0=a_0b_0\), then

\[
 K^h=C K/R_0,\qquad D^hK^h=e_{0^6}.                    \tag{3}
\]

The base differential has nullity five, and its five independent universal
vertex gauges span the kernel. Equation (2) transports that equality to
the whole torus. Hence every pure-zero preimage differs from (3) by a
sum-zero vertex gauge. It is enough, and slightly stronger, to allow all
six gauge scalars without imposing their sum-zero relation. The possible
factored pure-L0 packet is therefore contained in the enlargement

\[
 K^h_{ru}(i,j)+(\mu_r+\mu_u)M^h_{ru}(i,j).             \tag{4}
\]

On the cut \(\{0,1\}\mid\{2,3,4,5\}\), its \(4\times8\) flattening factors
entrywise as

\[
 \frac{h_{r,i}h_{u,j}}{R_0}
 \left(K_{ru}(i,j)+R_0(\mu_r+\mu_u)M_{ru}(i,j)\right). \tag{5}
\]

The prefactor splits into an invertible row factor and an invertible column
factor. The substitution \(\lambda_v=R_0\mu_v\) is an automorphism over the
Laurent parameter ring. Consequently the \(3\times3\) cut-minor ideal of
(5) is obtained from the base ideal by invertible row/column scaling,
Laurent base change, and an invertible change of gauge variables.

At the base point the 224 cubic minors have 80 nonzero generators and
generate the unit ideal over both \(\mathbb Q\) and
\(\mathbb F_{32003}\). Hence the family ideal is the unit ideal over the
entire four-parameter torus. In particular no torus member admits a
factored pure-zero L0 slice.

## Machine audit

[verify_level_two_three_invertible_incidence_torus_cut_obstruction.py](../computations/verify_level_two_three_invertible_incidence_torus_cut_obstruction.py)
checks the base \(55/53\) incidence and R2 certificates, all 3,840 matching
and cofactor monomial identities behind (2), the preimage and cut
transformations (3)--(5), and the exact base cut-minor Gröbner bases over
\(\mathbb Q\) and \(\mathbb F_{32003}\). It passes normal, optimized, and
isolated Python. Singular is the sole external dependency.
