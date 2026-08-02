# Full sitewise \(\mathfrak{sl}_3\) separates the face polar from the denominator

Research counterguard only.  This note does not construct a physical
four-face homotopy or prove Krenn's conjecture.

## Outcome

Passing from the abelian lowering cube to the full sitewise Lie algebra

\[
                     \mathfrak g_F=\mathfrak{sl}_3^{\oplus4}
\]

does not promote a desired four-face polar \(h_vY_0\) to a boundary in the
old denominator sequence.  In the exact \(q\)-degree-two face module there
is a canonical identification

\[
 \operatorname {span}\{h_cY_d:c,d\in\{0,1,2\}^{F}\}
       \simeq \operatorname {End}(\mathbb Q^3)^{\otimes4},
 \qquad
 h_cY_d\longmapsto\bigotimes_{x\in F}E_{d_xc_x}.       \tag{1}
\]

Under this identification, the universal denominator matching tensor is

\[
              T_F=\sum_c h_cY_c\longmapsto I^{\otimes4},             \tag{2}
\]

whereas the desired mixed-to-pure polar is

\[
 h_mY_0\longmapsto
       E_{0m_1}\otimes E_{0m_2}\otimes E_{0m_3}\otimes E_{0m_4}
       \in\mathfrak{sl}_3^{\otimes4}.                               \tag{3}
\]

Every letter of the five face words `2112`, `1112`, `1212`, `1212`, and
`1211` is 1 or 2, so all four factors in (3) are off diagonal.  Thus (2)
lies in the trivial summand and (3) lies in
\(\operatorname {ad}^{\boxtimes4}\).  The two summands do not communicate
under any \(\mathfrak g_F\)-equivariant construction:

\[
 \operatorname {Hom}_{\mathfrak g_F}
       (\mathbf1,\operatorname {ad}^{\boxtimes4})=0.                 \tag{4}
\]

The quadratic Casimir makes this separation computationally explicit.  It
does provide the standard contraction of the positive-degree
Chevalley--Eilenberg complex on the nontrivial summand, but that contraction
does **not** make (3) a source differential of anything.  At CE degree zero
the identity is \(z=h_{\rm CE}d_{\rm CE}z\), not
\(z=d_{\rm source}(\text{old chain})\).  A Spencer realization would need
new jet/ghost source generators and a chain map into the full-nine complex.
Supplying the generator whose boundary is (3) is precisely supplying the
missing \(\tau_v\).

There is a second typing obstruction.  Full
\(\mathfrak{sl}_3^{\oplus4}\) is not the stabilizer of the four-site ternary
GHZ target.  Its stabilizer has dimension six and is abelian diagonal.
Consequently the full semisimple Casimir is not an operation on the
fixed-target augmented problem; after restricting to the actual stabilizer,
the semisimple/Whitehead argument disappears.

## 1. The exact face representation

Fix a labelled four-site face \(F\).  For
\(c=(c_x)_{x\in F}\in\{0,1,2\}^F\), let

\[
 h_c=\operatorname {Haf}(q_c)
     =\sum_{M\in\operatorname {Match}(F)}
          \prod_{xy\in M}q_{xy}^{c_xc_y}.                            \tag{5}
\]

There are three perfect matchings.  Fine edge-colour labels make the three
monomials for one word distinct, and also make the supports for two
different words disjoint.  Hence the 81 quadrics \(h_c\) are linearly
independent and contain 243 distinct fine-colour monomials.  If
\(W_x=\mathbb Q^3\), their span is canonically a copy of
\(W_F^*=\bigotimes_xW_x^*\), while the output words span
\(W_F=\bigotimes_xW_x\).  This gives (1).

Let \(L_{x;ab}\) act by the matrix unit \(E_{ab}\) on the output at site
\(x\), and let \(D_{x;ab}\) be the contragredient fine-colour derivation on
the \(q\)-coefficient.  With the conventions of the sitewise-covariance
calculation,

\[
 h_cY_d\longmapsto E_{d,c},\qquad
 (L_{x;ab}-D_{x;ab})E_{d,c}=[E_{ab},E_{d,c}].                         \tag{6}
\]

Thus the flat connection \(L-D\) is exactly the commutator action on each
local endomorphism factor.  The covariance identity
\((L-D)T_F=0\) is then the elementary statement \([E_{ab},I]=0\).

For a fixed deleted site \(v\), the old denominator column is

\[
             \delta_F(d_{v,0})=e_0^{(v)}T_F.                         \tag{7}
\]

The exposed factor is a spectator for \(\mathfrak g_F\).  Therefore (7)
generates a trivial face representation.  Including all three exposed
colours gives three spectator copies of the same trivial representation;
it does not change the argument.

Locally one has the split decomposition

\[
              \operatorname {End}(W_x)=\mathbf1\oplus\operatorname {ad},
 \qquad
 P_x(X)=X-\frac{\operatorname {tr}X}{3}I.                            \tag{8}
\]

Taking \(P_F=P_1\otimes P_2\otimes P_3\otimes P_4\) gives the exact
separating projector

\[
 P_F(I^{\otimes4})=0,
 \qquad
 P_F(E_{0m_1}\otimes\cdots\otimes E_{0m_4})
       =E_{0m_1}\otimes\cdots\otimes E_{0m_4}.                      \tag{9}
\]

In particular, the polar remains nonzero in the cokernel of the denominator
line.  Equation (9) is stronger than a failed ansatz: it is an equivariant
direct-summand certificate.

## 2. The Casimir is a separator, not the missing differential

Use the trace form on \(\mathfrak{sl}_3\).  On a local endomorphism the
quadratic adjoint Casimir has the exact matrix-unit expression

\[
 \Omega_x(X)=\sum_{a,b=0}^2[E_{ab},[E_{ba},X]]
             =6\left(X-\frac{\operatorname {tr}X}{3}I\right).       \tag{10}
\]

The central \(\mathfrak{gl}_3\) direction acts trivially by commutator, so
the displayed matrix-unit sum is the \(\mathfrak{sl}_3\) Casimir with this
normalization.  It has eigenvalue zero on the local identity and eigenvalue
six on the adjoint.  Consequently

\[
 \Omega=\sum_{x\in F}\Omega_x
 \quad\text{has eigenvalues}\quad
 0\text{ on }T_F,\qquad24\text{ on }h_mY_0,                          \tag{11}
\]

and

\[
                   P_F=\prod_{x\in F}\frac{\Omega_x}{6}.            \tag{12}
\]

So Casimir inversion cannot turn (2) into (3): it kills the denominator
component and fixes, rather than removes, the desired obstruction
component.

This also pinpoints the mismatch with the CE homotopy.  For a nontrivial
finite-dimensional semisimple summand \(V\), the standard Casimir argument
contracts \(C^{>0}(\mathfrak g_F,V)\).  On a zero-cochain \(z\in V\), the
homotopy formula reads

\[
                 z=h_{\rm CE}(d_{\rm CE}z),                          \tag{13}
\]

because there are no CE cochains in degree \(-1\).  Thus (13) recovers a
non-invariant vector from its infinitesimal orbit.  It does not express
that vector as a CE boundary, much less as a boundary for the unrelated
source differential \(\delta_F\).

A Spencer complex can reverse this bookkeeping only by adjoining the
exterior/jet variables on which its contracting homotopy lands.  To use it
here one must exhibit a typed chain map

\[
 C^\bullet_{\rm Spencer}(\mathfrak g_F,\operatorname {End}W_F)
       \longrightarrow C^\bullet_{\rm full\text{-}nine}             \tag{14}
\]

whose image of the relevant jet has boundary \(h_vY_0\), zero physical
target, zero ordinary residue, and controlled remaining components.  The
old denominator source has no such jet generator.  Adjoining one formally
is exactly the abstract repair

\[
                       d\tau_v=h_vY_0.                               \tag{15}
\]

Therefore CE acyclicity cannot be invoked as existence of (14).

## 3. Why semisimplicity and Whitehead do not close the gap

The relevant face sequence contains

\[
 0\longrightarrow\mathbf1
   \xrightarrow{\ 1\mapsto I^{\otimes4}\ }
   \operatorname {End}(W_F)
   \longrightarrow\operatorname {coker}\delta_F
   \longrightarrow0.                                                \tag{16}
\]

Semisimplicity says that (16) splits as a sequence of
\(\mathfrak g_F\)-modules.  That conclusion makes the obstruction sharper:
\(\operatorname {ad}^{\boxtimes4}\) survives as a direct summand of the
cokernel, and (3) lies in it.  Splitting an extension does not enlarge the
image of its first arrow.

Likewise, the Whitehead lemmas concern \(H^1\) and \(H^2\) of the CE
complex, and their higher-degree analogue concerns CE cohomology.  The
question here is membership in the image of a different map, the physical
source differential.  No theorem identifying that differential with
\(d_{\rm CE}\), or providing the chain map (14), is present.  In short,
Whitehead kills representation-theoretic extension classes; it does not
manufacture a source-provenant preimage of a nonzero cokernel vector.

## 4. The fixed GHZ target leaves only an abelian stabilizer

Let

\[
                         \Delta_F=\sum_{a=0}^2e_a^{\otimes4}.         \tag{17}
\]

The exact action matrix of \(\mathfrak{sl}_3^{\oplus4}\) on \(\Delta_F\)
has 32 columns and rank 26.  This can also be seen directly.  For an
off-diagonal \(E_{ij}\) at site \(x\), the resulting word has colour \(i\)
at \(x\) and colour \(j\) at the other three sites.  These 24 words are
distinct, so no nonzero off-diagonal generator stabilizes \(\Delta_F\).

There are eight independent sitewise traceless diagonal parameters
\(\lambda_{x,a}\).  The stabilizer equations are

\[
                    \sum_{x\in F}\lambda_{x,a}=0
                    \quad(a=0,1,2).                                 \tag{18}
\]

Only two of (18) are independent after the four sitewise trace-zero
conditions.  The diagonal action therefore has rank two and kernel
dimension \(8-2=6\).  Hence

\[
 \operatorname {stab}_{\mathfrak{sl}_3^{\oplus4}}(\Delta_F)
       \cong\mathbb Q^6
       \quad\text{is abelian diagonal}.                             \tag{19}
\]

The full sitewise action is useful on the universal matching tensor, but it
is not a symmetry of the augmented complex with the GHZ target fixed.
Individual raising and lowering directions move (17), and the pure-output
ordinary-residue line is not a full \(\mathfrak g_F\)-subrepresentation
either.  Thus a full-Casimir homotopy has no automatic typed target/residue
behavior.  Restricting to (19) restores the target type but leaves an
abelian algebra, for which the semisimple Casimir/Whitehead contraction is
unavailable.

## 5. Consequence and scope

The full sitewise Lie algebra does reveal something conceptual about the
stubbornness of this case.  The desired polar is not hidden inside the old
denominator representation waiting for a better equivariant projector.  It
is the first vector in a different irreducible-direction summand.  The
natural Casimir detects exactly that missing summand.

Accordingly, a successful proof must break at least one premise of this
counterguard.  It may use a genuinely source-provenant full-nine row, a
non-equivariant cross-word cancellation, a specialization/Rees
transgression, or a derived construction equipped with the explicit chain
map (14).  What cannot work is a formal appeal to full sitewise
semisimplicity applied only to the old face denominator sequence.

## Exact verification

The dependency-free checker
[verify_h3_full_sl3_face_casimir_counterguard.py](../computations/verify_h3_full_sl3_face_casimir_counterguard.py)
uses exact rational arithmetic.  It verifies:

- the 81 face coefficient words and their 243 disjoint quadratic monomials;
- the local formula (10) on all nine matrix units;
- that (12) kills the denominator identity and fixes all five polars;
- Casimir eigenvalues zero and 24 in (11); and
- the exact target-action ranks \(26=24+2\) and the six-dimensional
  abelian stabilizer.

Its frozen ledger digest is

    56e193d6341ac45638ae5f85a01f2f17053e4addc0d05b536534ef1f2bc9a655
