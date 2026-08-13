# Uniform Cartan readouts are covariant, not arbitrary-tail natural

## Outcome

The uniformly placed Cartan prism `G` does **not** acquire the canonical
ordinary-residue and eta/sigma packet under arbitrary matching-tail
multiplication or independent root/transposition choices.  There are two
exact obstructions.

1. For a tail `T`, the mixed Cartan boundary commutes with multiplication by
   `T` exactly when `T` is invariant under both the selected Weyl action and
   endpoint transposition.
2. The two halves of the Kähler ridge `-dOmega_v` have different site
   degrees.  Adding the same matching tail preserves that difference.

The positive statement is covariance: invariant tails transport the
four-corner residue as `T*(-1,1,1,-1)`, and simultaneous relabeling of
`Omega`, eta, and sigma transports the ridge law.  Fixed numerical terminal
values require a normalized labelled shifted lift, not ordinary tail
multiplication.

This does **not** block the Schur-unit branch.  That determinant uses the
complete target-zero source prism and its nonzero fine-label projection; it
does not use ordinary residue or eta/sigma.  Augmented grade typing remains
load-bearing only for the residual, generator, and separator branches.

Checker:
[`verify_uniform_cartan_augmented_grade_naturality_gate.py`](../computations/verify_uniform_cartan_augmented_grade_naturality_gate.py).

## 1. Exact ordinary-residue transport criterion

Use the four orbit labels

```text
1, w, s, sw
```

and put

\[
                         D=(1-s)(w-1).                 \tag{1}
\]

On the seed corner,

\[
                         D e_1=(-1,1,1,-1).           \tag{2}
\]

Let `M_T` multiply the four orbit corners by
`(T,wT,sT,swT)`.  In the regular four-corner representation every entry of
`D` is nonzero, and

\[
                 [D,M_T]_{ij}=D_{ij}(T_j-T_i).        \tag{3}

Therefore

\[
 [D,M_T]=0
 \quad\Longleftrightarrow\quad
                  T=wT=sT=swT.                       \tag{4}

The constraint matrix in (3) has rank three, so (4) is sharp.  If the tail
is supported away from the four chosen action sites, or is an invariant
aggregate there, then

\[
                   D(T\xi)=T D(\xi),                 \tag{5}

and the abstract ordinary residue transports as `T*(-delta)`.  A generic
matching-tail monomial involving the transposed or rooted sites has a
nonzero commutator (3); its extra orbit terms are the first residue-grade
obstruction.

Even with an invariant tail, (2) is oriented.  Reversing the endpoint
orientation sends `-delta` to `delta`.  Thus independent choices do not
preserve a fixed numerical vector.  The vector is natural only after its
corner labels and orientation are transported with the choice.

## 2. A common tail cannot type the Kähler ridge

In the canonical packet write

\[
 a=q_{pq}^{22},\quad t=q_{pq}^{00},\quad
 b=q_{xv}^{0m_v},\quad u=q_{xv}^{00},
\]

so

\[
                  \gamma_v=-d\Omega_v=-da+dt+db-du. \tag{6}

The two blocks have site degrees

\[
 \deg(-da+dt)=e_p+e_q,
 \qquad
 \deg(db-du)=e_x+e_v.                                \tag{7}

For every common tail degree `tau`,

\[
 (e_p+e_q)+\tau\ne(e_x+e_v)+\tau.                   \tag{8}

Site relabeling merely permutes both unequal vectors and cannot make them
equal.  This is the first exact terminal-grade obstruction.  It is already
visible before any support or component calculation.

There are two related product guards.  Contraction is coefficient-linear,
so

\[
 \iota_{\eta_z}(T\gamma_v)
     =T\left(1+\delta_{vz}{u_z\over t}\right),
 \qquad
 \iota_\sigma(T\gamma_v)=-Tq_{pq}^{22}.              \tag{9}

Thus the fixed normalized terminal law is scaled unless `T=1` in the
terminal quotient.  If one instead differentiates the tail-multiplied ridge,

\[
                    -d(T\Omega_v)=T\gamma_v-\Omega_v,dT, \tag{10}

so a nonconstant tail produces an extra Kähler face.  The smallest ordinary
homogenization is the known determinant

\[
 u(-a+t)+t(b-u)=tb-ua,                               \tag{11}

whose eta/sigma contractions are not (9) with `T=1`.

Consequently the correct positive object is still a **labelled shifted
Kähler lift** retaining the `pq` and `xv` halves as separate relative labels.
Ordinary multiplication by any common matching tail cannot replace it.

## 3. Dependence on root and transposition choices

The abstract constructions are equivariant.  If a site/colour relabeling
`phi` transports all of

\[
 (p,q,x,v),\quad \Omega_v,\quad \eta_z,\quad\sigma,
\]

then

\[
 \phi^*(-d\Omega_v)=-d(\phi^*\Omega_v),
 \qquad
 \iota_{\phi_*X}\phi^*\gamma_v=\phi^*(\iota_X\gamma_v). \tag{12}

This is covariance, not independence.  If the ridge is relabeled but the
old eta/sigma functionals are held fixed, its numerical values can change or
vanish.  For example, exchanging the `pq` and `xv` coordinate blocks sends
the coefficient vector `(-1,1,1,-1)` to its negative in the fixed basis.

Therefore a uniform augmented theorem needs an oriented label map from the
chosen Cartan sites to a physical ridge packet.  The ambient Cartan source
prism alone cannot supply that map.

## 4. What the Schur unit actually consumes

For a minimal zero-holonomy block,

\[
 \det\begin{pmatrix}M&g\\h^T&\alpha\end{pmatrix}
       =-\kappa(h^Tc)(\ell^Tg).                       \tag{13}

The nonzero-charge unit branch needs:

1. the complete physical source prism `G`;
2. its target-zero boundary;
3. the nonzero exact fine-label projection `g=pi_M G` constructed at the
   marked offdiagonal occurrence;
4. the rank-one critical-block and anchor amplitudes; and
5. `ell^T g != 0`.

Neither ordinary residue nor the eta/sigma ridge occurs in (13).  Hence
commits `346d76a` and `6824c9e` already make this Schur-unit arm uniform.
Augmented grade typing should not be inserted as an unnecessary hypothesis
there.

The terminal data are essential on the other arms:

* a dark residual `R=G-Cy` must be identified in the complete augmented
  grade before it is called a typed exit;
* a nonzero relative kernel becomes a physical generator only through its
  terminal value; and
* a terminal-dark class promotes to a physical separator only if the
  residue/ridge readouts descend on the exhaustive cone.

## 5. Shifted frontier

The result splits the global theorem cleanly:

```text
uniform source prism + nonzero placement
        |
        +-- ell^T g != 0 --> Schur unit
        |                     (no terminal typing needed)
        |
        `-- dark / relative branch
                    |
             invariant oriented residue transport
                    +
             labelled shifted Kähler lift
                    |
             typed exit / generator / separator
```

The next terminal construction should therefore target the shifted Kähler
label map in a saturated dark component grade.  Trying to prove naturality
under arbitrary common tails is impossible by (8), and trying to preserve
fixed readouts under independent choices contradicts (3) and (12).

## Scope

This is an exact naturality/no-go theorem.  It proves the invariant-tail
transport criterion, the persistent ridge degree obstruction, and the
minimal readouts actually used by the Schur determinant.  It does not
construct the labelled shifted Kähler lift outside the canonical `h=3`
grade or promote every dark residual to an exit/generator/separator.

Run:

```text
python3 computations/verify_uniform_cartan_augmented_grade_naturality_gate.py
python3 -O computations/verify_uniform_cartan_augmented_grade_naturality_gate.py
python3 -I -S computations/verify_uniform_cartan_augmented_grade_naturality_gate.py
```

Frozen ledger SHA-256:

```text
12be7e0141f24ae8cb2db689db118d8d42363a1d58705daca45ce17e0500d7de
```
