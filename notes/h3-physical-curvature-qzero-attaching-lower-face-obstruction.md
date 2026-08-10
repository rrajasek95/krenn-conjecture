# The physical curvature square does not supply the invisible q-zero attaching face

## Outcome

The automatic full-nine overlap rows (3)--(5), the selected curvature
minor, and the order-four $q$-zero symbol do not yet construct the chain
$n_A$.  There is one exact fixed-label source obstruction and one exact
diagnostic obstruction for the committed old-cap landing.

First, every connection/normal/curvature row is homogeneous in the four
physical endpoint labels.  A curvature minor compares two different perfect
matchings of **one decorated four-vertex word**.  The endpoint bridge in the
order-four symbol instead compares two colour decorations of the **same**
physical matching:


\[
 \begin{array}{c|c|c}
 & (x,v,p,q)&\text{physical matching}\\ \hline
 \text{mixed physical top}&(0,m_v,2,2)&xv\mid pq\\
 \text{zero-endpoint Rees face}&(0,0,0,0)&xv\mid pq.
 \end{array}                                             \tag{1}
\]

Here $m=12112$, so $m_v\in\{1,2\}$.  The two rows in (1) lie in
different fixed-label curvature components for every $v$.  No global
target-colour permutation changes this fact.

Second, even if this label mismatch is ignored and one works inside a
single decorated word, the **committed old split-cap landing** sends the
three external matching polars to identical $q$-augmentation and
ordinary-residue readouts:

\[
                         q\operatorname{-aug}
                    =\operatorname {ores}=(1,1,1).      \tag{2}
\]

The curvature signs are exterior signs.  In that old landing a curvature
difference kills both readouts, while a weighted difference retaining the nonzero scalar

\[
                         \kappa=AU-BF                  \tag{3}
\]

retains the same $\kappa$ in ordinary residue.  It never yields
$(q\text{-aug},\operatorname {ores})=(\kappa,0)$.

All relevant residual four-site words are mixed, so physical target is
already zero.  No physical ordinary-residue map on a new attaching chain
has been constructed; its absence is part of, not evidence for, the desired
theorem.  The exact missing datum is therefore still a
**word-changing, residue-corrected source comparison**.  The automatic
fixed-label curvature packet supplies neither part.

This is a bounded obstruction to the proposed assembly of $n_A$, not a
nonexistence theorem for a larger source resolution and not a Krenn
counterexample.  A genuine higher Bianchi/Spencer cell could change the
decorated word and add an independent ordinary-residue correction; those
are precisely the operations excluded from the packet audited here.

## 1. The automatic rows are fixed-label curvature rows

On the common complement of four exposed sites, use the selected instance
of the automatic packet

\[
\begin{aligned}
 f&=Az+xy, &g&=Bz+xt,\\
 H&=Av+Ey+Fx, &N&=Bv+Et+Ux,\\
 D&=At-By, &\kappa&=AU-BF.
\end{aligned}                                           \tag{4}
\]

Direct expansion gives

\[
 ft-gy=Dz,                                              \tag{5}
\]

and

\[
 Uf+tH-Fg-yN=Dv+\kappa z.                              \tag{6}
\]

These are the selected coefficients of the automatic connection and normal
rows.  Every term in (5)--(6) uses the same endpoint labels at the four
exposed vertices.  Neither the adjugate contraction nor multiplication by
$\kappa$ changes that word.

For a fixed decorated word on the four vertices there are three decorated
perfect-matching monomials.  The three curvature differences join them in a
triangle.  Across all $3^4$ words, the exact curvature graph is therefore

\[
                         81K_3,                         \tag{7}
\]

with 243 decorated monomials and 243 curvature faces.  A decorated matching
monomial determines the four vertex colours uniquely, so distinct word
components cannot meet or cancel through a sum of fixed-label curvature
rows.

The order-four physical Koszul top uses endpoint cells

\[
 \widetilde u_v=A_{xv}(0,m_v),\qquad
 \widetilde t=A_{pq}(2,2),                              \tag{8}
\]

whereas the zero-endpoint Rees square uses

\[
                 u_v=A_{xv}(0,0),\qquad t=A_{pq}(0,0). \tag{9}
\]

Equations (8)--(9) are two decorations of $xv\mid pq$, not two
matchings of one decorated word.  This is why the formal differential
operator

\[
 M_{u_vt}\partial_{\widetilde u_v}\partial_{\widetilde t}
                                                               \tag{10}
\]

from the Hasse-cone construction is not supplied by the physical curvature
minor.  A curvature rectangle changes matching topology while preserving
the vertex word; (10) preserves matching topology while changing the word.

## 2. Exact sign and the committed old-cap augmentation lock

Fix one of the mixed residual words $m|_{D\setminus\{v\}}$.  It contains
both colours 1 and 2, hence every external matching polar has physical
target zero.  For any one of the three external perfect matchings $M$,
the order-four face satisfies

\[
 \partial_M\partial_NH_{c_v}=1,                        \tag{11}
\]

where $N$ is the internal perfect matching.  The complete denominator
reset has the same polynomial coefficient $+1$.  If it is landed in the
already committed split cap, target invisibility forces the
ordinary-response generator $\rho$, whose ordinary residue is also $+1$.
Reversing the orientation of a face reverses both values.  Therefore,
**for that old landing**, on the whole three-face span,

\[
 (q\operatorname{-aug},\operatorname {tgt},
                       \operatorname {ores})(c_0,c_1,c_2)
       =(c_0+c_1+c_2,0,c_0+c_1+c_2).                   \tag{12}
\]

The old-cap readout rank is one.  Adjoining the desired invisible lower face
$(1,0,0)$ raises it to two.

The selected curvature minor takes the difference of two matching
channels.  With unit polar normalization its coefficient vector is, up to
orientation, $(1,-1,0)$, so both values in (12) vanish.  With physical
weights the same calculation reads

\[
 (AU-BF,0,AU-BF)=(\kappa,0,\kappa),                   \tag{13}
\]

not $(\kappa,0,0)$.  Any extra automatic connection/normal difference is
another fixed-label target-zero identity in the same component and does
not change the equality of the two readouts.

This is the smallest obstruction behind the earlier split-cap calculation:
the physical order-four face can carry the required boundary or lose its
ordinary residue, but the automatic curvature square makes those two events
happen together.  It does not prove that every possible enlarged physical
attaching complex has this ordinary-residue map.  Rather, the automatic
rows (4)--(6) define no replacement map, so invoking a different zero
ordinary residue would simply declare the missing structure.

## 3. Consequence for the primitive attaching class

The primitive source-relative row isolated in the recent audit requires a
chain

\[
 dn_A=\mathcal K=\alpha A,\qquad
 \operatorname {tgt}(n_A)=\operatorname {ores}(n_A)=0. \tag{14}
\]

The order-four $q$-zero polynomial symbol supplies the right boundary
coefficient.  Equations (7)--(10) show that the selected physical curvature
packet cannot attach its mixed $22$-endpoint top to the zero-endpoint
face.  Equations (12)--(13) show that even a forced label identification
retains ordinary residue under the only committed cap landing whenever the
lower boundary is nonzero.

Thus the next positive object must have two genuinely new properties:

1. a source-provenant face changing the decorated endpoint word in (1);
2. an independent ordinary-residue correction, not the same matching-face
   augmentation reused with curvature signs.

Those are exactly the missing endpoint-curvature side and augmented chain
map in the formal Hasse-cone construction.  Neither follows from the
automatic rows (3)--(5) or from $\kappa\ne0$.

## 4. Verification

The dependency-free checker
[`verify_h3_physical_curvature_qzero_attaching_lower_face_obstruction.py`](../computations/verify_h3_physical_curvature_qzero_attaching_lower_face_obstruction.py)
verifies (5)--(6) as sparse polynomial identities, constructs all 243
decorated matching monomials and all 243 curvature faces, proves their
component decomposition (7), and checks all five endpoint bridges under all
six global colour permutations.  It then verifies the exact rank-one
$q$-augmentation/ordinary-residue map in the old split-cap landing, every
curvature-sign difference, and three nonzero weighted probes of (13).  The
checker uses runtime failures
and runs unchanged under normal, optimized, isolated, and
optimized-isolated Python.
