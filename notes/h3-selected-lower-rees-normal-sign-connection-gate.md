# Target-normal Rees cells cannot hit the private sign quotient

## Result

Deformation to the normal cone of the fixed GHZ fibre does not by itself
construct the selected occurrence comparison. The obstruction is
representation-theoretic and survives every Rees/Koszul degree.

Let \(s=(0\;1)\) be the endpoint swap. The four independent normal tensors
obtained by applying the two tail roots at sites 2 and 5 are fixed by \(s\):
the roots never change the two equal endpoint entries of GHZ. Thus their
target-normal module \(N\) is an \(s\)-trivial four-dimensional module.

By contrast, the exact private packet

\[
p_\xi=\xi-\bar\xi-s\xi+s\bar\xi
\]

satisfies \(sp_\xi=-p_\xi\), and it generates the certified one-dimensional
quotient \(Q_\xi\). Hence

\[
\boxed{
\operatorname{Hom}_{\langle s\rangle}
 \bigl(\operatorname{ReesKoszul}(N),Q_\xi\bigr)=0.}
\]

Every symmetric, exterior, or mixed Rees--Koszul monomial in \(N\) remains
endpoint-even. In characteristic zero, an equivariant map from an even
generator to the sign line obeys \(a=-a\), so \(a=0\). This proves the
statement in every degree; the checker enumerates 560 finite states as a
mutation guard.

Executable certificate:
`computations/verify_h3_selected_lower_rees_normal_sign_connection_gate.py`.

## Relation to the Hasse/principal-parts totalization

The existing Boolean Hasse/cobar theorem gives a canonical complete
principal-parts **source** totalization. It explicitly leaves the
principal-parts-to-physical augmented comparison open. It does not adjoin
the target-normal Koszul generators, nor prove that its source resolution is
the deformation-to-the-normal-cone model of the fixed fibre.

Adjoining those target normals does not repair the gap: the parity theorem
above says their entire induced image in \(Q_\xi\) is zero. The useful
orbit-relative Weyl bar instead carries an endpoint-sign source factor.

## The smallest positive source type

The minimal chain extension is one generator \(\kappa_\xi\) with

\[
s\kappa_\xi=-\kappa_\xi,
\qquad
d\kappa_\xi=p_\xi.
\]

This is an equivariant chain equation because \(sp_\xi=-p_\xi\). The
orbit-relative group-bar construction supplies it canonically as

\[
\kappa_\xi=(1-s)[\tau\mid\widetilde Z_0].
\]

Thus the required new type is not “one of four target normals”; it is a
source-side sign connection, equivalently a relative Kodaira--Spencer cell
for the two endpoint lifts of the same target orbit.

Endpoint parity immediately gives

```text
D = W = target = anchor = pure-Eq aggregate = 0
```

on this connection. No separate cancellation of those protected rows is
needed.

There is an important Ext qualification. Over the rational group algebra
of the endpoint involution,

\[
\operatorname{Ext}^1_{\mathbf Q[\langle s\rangle]}(-,-)=0
\]

by Maschke averaging. So the missing object is not a non-split extension of
ordinary endpoint representations. If \(d_{\rm old}\) is the admitted
physically graded boundary map, the exact obstruction is instead

\[
 o_\xi=[p_\xi]\in
 H_0\!\left(\operatorname{Cofib}(d_{\rm old})\right)^-
 \cong Q_\xi.
\]

The complete old image has rank 12 and adjoining \(p_\xi\) raises it to 13.
The pinned covector \(\lambda_\xi\) reads one on this class. Adjoining a
degree-one generator with \(d\kappa_\xi=p_\xi\) kills this cofiber class.
This is the precise sense in which \(\kappa_\xi\) is a relative
Kodaira--Spencer/Atiyah attachment.

## The terminal summand and capped formal column

Attach the independent relative Kähler generator

\[
\gamma_v=-d\Omega_v.
\]

Its ordinary boundary, residue, `D/W/target/anchor` rows vanish, while

\[
\iota_{\eta_z}\gamma_v=1+\delta_{vz}u_z/t,
\qquad
\iota_\sigma\gamma_v=-q_{pq}^{22}.
\]

Therefore

\[
C_{\rm formal}=\kappa_\xi+\gamma_v
\]

has the entire protected and terminal packet in the orbit-relative
sign-cone plus shifted Kähler model. After the already physical
\(-O_\alpha\) cap, the required augmented target is the pinned column

```text
literal boundary          360 seven-edge features
Eq                        (-1,+1,+1,-1)
ordinary residue          0
D,W,target,ainc            0
eta_z                     1+delta_(vz)u_z/t
sigma                     -q_pq^22.
```

This is a formal augmented construction, not yet a literal physical
repeated-grade cell. The shifted Kähler theorem itself records that its two
halves have different site multidegrees and that the labelled physical lift
is open. Thus adjoining \(\gamma_v\) fixes the desired readout, but does not
silently prove its physical grade placement.

## Tensoring with the sign connection does not fix the grade

The selected private packet has repeated-site profile

\[
 g_\kappa=(1,1,1,2,1,1,1,2).
\]

The two Kähler halves have site degrees

\[
 g_{pq}=e_6+e_7,
 \qquad
 g_{xv}=e_0+e_1.
\]

Consequently

\[
 g_\kappa+g_{pq}\ne g_\kappa+g_{xv}.
\]

Adding any common polynomial or divided-power tail preserves this
difference. The checker exhausts all 6561 tails with entries in
\(\{0,1,2\}\) as a mutation guard; the general statement is cancellation in
the grading monoid. The signed shift

\[
 g_{pq}-g_{xv}=(-1,-1,0,0,0,0,1,1)
\]

is not the degree of a coefficient monomial. The least two-sided polynomial
completion is still

\[
 u(-a+t)+t(b-u)=tb-ua,
\]

and the pinned Kähler calculation proves that it changes the eta and sigma
laws.

A mapping cone can retain the two labels, but only after adjoining an arrow
of exactly this signed shift. That arrow is the missing labelled shifted
Kähler lift; calling it a cone grading does not construct it from the
existing diagonal Hasse/principal-parts tails. Thus the source-sign
connection and the ridge shift are two independent source data.

## One scalar section test, then the augmented alternative

Let \(\lambda_\xi\) be the normalized private quotient functional. For any
admitted family of source-sign connections, the occurrence comparison is
decided by one scalar:

\[
\lambda_\xi(dc).
\]

- If it is nonzero for some \(c\), normalize
  \(\sigma_\xi=c/\lambda_\xi(dc)\). This constructs the occurrence section.
- If it is zero for every admitted \(c\), \(\lambda_\xi\) annihilates the
  complete admitted image and is the private associated-graded dual.

After adjoining the protected and ridge rows, the same statement becomes a
finite augmented-column alternative: either the capped column lies in the
complete physical image, or a functional on the complete augmented
cokernel detects it. This is the boundary/separator decision. No new
occurrence enumeration is involved.

## Physical \(q\)

The terminal relevant to the global dark alternative is

\[
q=\sum_{i=1}^6m_i-\mathrm{ainc}.
\]

Neither the target-normal Rees model nor the Kähler ridge defines this
physical cochain on the new source generator. That typing remains a real
requirement. More sharply, \(p_\xi\) is an output/cokernel class, while
physical \(q\) is a row on the source correction domain. Therefore a nonzero
\(o_\xi\) is not itself a terminal class and \(q(p_\xi)\) is ill-typed.

After adjoining \(\kappa_\xi\), one must choose \(q(\kappa_\xi)\) and prove
that the resulting row respects every source relation. The private boundary
does not determine that scalar: values \(-1,0,1\) give the same
\(d\kappa_\xi=p_\xi\). Once this physical \(q\)-cocycle and the comparison on
complete physical relative domains exist:

- a nonzero \(q\)-transport defect gives a protected-kernel witness with
  nonzero physical \(q\) on the source or canonical side, hence the relative
  generator;
- zero defect transports \(q\) modulo protected rows and passes to the
  generator/Fredholm alternative.

So the shortest positive proof lemma is:

> Construct one physically graded source-sign connection lifting
> \(\kappa_\xi\), construct one independent shifted labelled Kähler arrow
> carrying the two halves of \(\gamma_v\) into the repeated grade, and extend
> physical \(q\) as a cocycle on the resulting domain. Endpoint parity
> supplies the protected zeros and the ridge supplies eta/sigma. Membership
> of the capped column closes Gate I; failure gives the complete augmented
> cokernel dual, while later \(q\)-ambiguity has only the
> generator/transport alternatives.

The target-normal deformation is useful for identifying why ordinary fibre
pullback fails, but it is not the missing cell.
