# Simultaneous diagonal flattenings need one source fusion square

## Outcome

Inverse rank-(r) factorizations of **every** bipartition flattening of

\[
                  \Delta_{B,r}=\sum_{a=1}^r e_a^{\otimes B}
\]

do not force an active clean pair or a deletion.  They recover only the
perfect pairing between the two diagonal Schmidt spaces.  Each unoriented
cut retains an independent \(GL_r\) gauge, and the checker gives a dense,
nonmonomial choice on all seven cuts of \(\Delta_{4,3}\) simultaneously.
Thus this inference is still output-only, even when all cuts are imposed at
once.

There is a sharp positive source-level statement.  If two disjoint shore
factorizations are full rank and their **columnwise physical product**
factors through the diagonal factorization of their union, then both shore
bases are aligned monomial palette bases.  Equivalently, one source-valid
Khatri--Rao fusion square kills the \(GL_r\) ambiguity.  Rank loss is the only
alternative.  In an occurrence-faithful minimum source, that is the precise
place where a deletion lemma could enter.

This does not yet give the conjecture's active clean cap.  The matching
source has a canonical large cut-Wick factorization, but no proved
rank-(r\), occurrence-faithful, multiplicative quotient.  Nor does an
aligned palette carrier by itself prove the homogeneous cap error
\({\cal E}_{p,q}(K)=0\).  The first missing datum is therefore one physical
fusion/provenance square, not another collection of flattening ranks.

## 1. What every target flattening really says

Let \(V=\mathbb C^r\), with its fixed palette basis
\((e_1,\ldots,e_r)\).  For a nonempty shore \(S\), define

\[
 D_S:\mathbb C^r\longrightarrow V^{\otimes S},\qquad
 D_S e_a=e_a^{\otimes S}.                                  \tag{1}
\]

The \(S\mid S^c\) flattening is

\[
             \operatorname{Flat}_S(\Delta_{B,r})
                    =D_S D_{S^c}^{\mathsf T}.                \tag{2}
\]

Suppose a minimal rank-(r\) factorization is written

\[
             F_S F_{S^c}^{\mathsf T}
                    =D_S D_{S^c}^{\mathsf T}.                \tag{3}
\]

The column spaces on the two sides agree.  Since the columns of every
\(D_T\) are independent, there are unique gauges \(G_S,G_{S^c}\in GL_r\)
with

\[
            F_S=D_SG_S,\qquad F_{S^c}=D_{S^c}G_{S^c},
            \qquad G_SG_{S^c}^{\mathsf T}=I.                 \tag{4}
\]

Thus complementary factors are inverse-transposes.  Nothing in (2)--(4)
relates \(G_S\) to \(G_T\) when \(T\ne S^c\).  Choosing an arbitrary
\(G\in GL_r\) on one orientation of each cut and \(G^{-\mathsf T}\) on
the other satisfies every inverse identity.

The checker makes this failure literal for \(|B|=4,r=3\).  On each of the
seven unoriented cuts it chooses a dense rational Vandermonde gauge (with a
dense inverse), forms (4), and verifies all fourteen oriented flattening
identities entry by entry.  No chosen factor column is a palette coordinate
line.  This is the smallest even-order, ternary all-bipartition counterguard.
It is a counterguard to the flattening inference, not a Krenn source.

## 2. The source fusion defect

For disjoint nonempty shores \(S,T\), write the columns as

\[
 f_{S,c}=\sum_a (G_S)_{ac}e_a^{\otimes S},\qquad
 f_{T,c}=\sum_b (G_T)_{bc}e_b^{\otimes T}.                   \tag{5}
\]

Their columnwise, or Khatri--Rao, product has columns

\[
 f_{S,c}\otimes f_{T,c}
   =\sum_{a,b}(G_S)_{ac}(G_T)_{bc}
       e_a^{\otimes S}\otimes e_b^{\otimes T}.              \tag{6}
\]

Let \(\pi_{\ne}\) retain the cross-palette rows \(a\ne b\), and put

\[
 \Omega_{S,T}=\pi_{\ne}(F_S\odot F_T),\qquad
 (\Omega_{S,T})_{(a,b),c}=(G_S)_{ac}(G_T)_{bc}\quad(a\ne b). \tag{7}
\]

This is the palette associator/fusion defect.  An invertible transition on
the column index cannot hide it:

\[
        \Omega_{S,T}C=0\text{ with }C\in GL_r
              \quad\Longleftrightarrow\quad\Omega_{S,T}=0.  \tag{8}
\]

Hence a square

\[
\begin{array}{ccc}
 \mathbb C^r &\xrightarrow{F_S\odot F_T}&
       V^{\otimes(S\cup T)}\\
 \downarrow C && \uparrow D_{S\cup T}\\
 \mathbb C^r&=&\mathbb C^r
\end{array}                                                   \tag{9}
\]

with \(C\) invertible exists exactly when \(\Omega_{S,T}=0\).  Equation
(9), unlike complementary inverse pairing, is a multiplication statement
and is the source-level compatibility the route needs.

## 3. Fusion rigidity

**Lemma (aligned palette axes).**  Let \(S,T\) be nonempty and disjoint.
Suppose \(F_S=D_SG_S\) and \(F_T=D_TG_T\), with
\(G_S,G_T\in GL_r\).  If \(\Omega_{S,T}=0\), then a permutation
\(\pi\in S_r\) and nonzero scalars \(\lambda_c,\mu_c\) exist such that

\[
 f_{S,c}=\lambda_c e_{\pi(c)}^{\otimes S},\qquad
 f_{T,c}=\mu_c e_{\pi(c)}^{\otimes T}.                       \tag{10}
\]

Conversely, (10) makes \(\Omega_{S,T}=0\).

**Proof.**  Fix a column \(c\).  It is nonzero in both factors because the
two gauges are invertible.  Equation \(\Omega_{S,T}=0\) says the nonzero
simple tensor \(f_{S,c}\otimes f_{T,c}\) lies in

\[
 \operatorname{span}\{e_a^{\otimes S}\otimes e_a^{\otimes T}:1\le a\le r\}.
                                                                    \tag{11}
\]

If colour \(a\) occurs in the support of the first factor and colour \(b\)
in the support of the second, the coefficient of the \((a,b)\) word in
(6) is nonzero.  Equation (11) forces \(a=b\).  Since this holds for every
pair of support elements, both supports are the same singleton.  Thus every
column has the form (10).  Independence of the \(r\) columns makes the
singleton assignment a permutation.  The converse is immediate. \(\square\)

This proof is valid over every field; it uses no positivity, conjugation,
genericity, or simplicity of the decorated source.  The checker exhausts
the two smallest nontrivial finite cases as an independent audit:

\[
\begin{array}{c|c|c}
 (r,\mathbb F_q)&|GL_r(\mathbb F_q)|&
 \#\{(G,H):\Omega(G,H)=0\}\\ \hline
 (2,\mathbb F_3)&48&32\\
 (3,\mathbb F_2)&168&6.
\end{array}                                                   \tag{12}
\]

In each case the displayed count is exactly the number of aligned monomial
pairs.

There is also an immediate simultaneous form.  Put a graph on a collection
of shores and join two disjoint shores when their physical fusion defect
vanishes.  On every connected component whose shore factors are full rank,
the lemma propagates one common palette permutation (the column scalings may
vary).  Hence a spanning tree of physical fusion squares is enough; checking
all higher associativity polygons is unnecessary for palette alignment.
Conversely, a first rank-deficient shore is the only algebraic escape from
this propagation.  Turning that escape into deletion still requires the
factor columns to be source occurrences rather than quotient classes.

## 4. Why the matching source does not automatically supply (9)

The aggregate source is fully general: parallel decorated edges combine to
arbitrary endpoint-ordered matrices \(A_{uv}\), and the top tensor is

\[
 H_B(A)=\sum_{M\in\operatorname{PM}(B)}\bigotimes_{uv\in M}A_{uv}. \tag{13}
\]

Across a cut, the source-valid Wick expansion is indexed by the number and
endpoints of crossing matching edges: internal hafnians on both shores and
a cross permanent.  At six sites, even one balanced cut has nine one-cross
and six three-cross matching sectors.  This large factorization is physical
and functorial, but it is not the rank-(r) factorization in (3).

Passing from it to (3) quotients all cancellation directions after the
source has been evaluated.  Different cuts may use different kernels.
Complementary inverse gauges only describe the resulting target pairing;
they do not say that these kernels are stable under disjoint-shore product.
That stability is exactly the square (9), or equivalently the vanishing of
the source-provenant lift of \(\Omega_{S,T}\).

This distinction survives arbitrary parallel sources and complex weights,
because aggregation to the matrices \(A_{uv}\) is exact.  It also explains
why the known Laurent boundary defeats every output-only flattening
invariant: all its target limits satisfy (2), while the source data diverge
inside the unrecorded cut kernels.

## 5. Exact interface with deletion and clean descent

The strongest valid flattening theorem is therefore conditional:

> Suppose a rank-(r) cut compression is occurrence-faithful, its columns
> are tensor-active physical source channels, and it is multiplicative in
> the sense of one square (9).  Then either a shore factor loses rank, or all
> \(r\) channels are aligned pure palette carriers.  If source minimality
> turns rank loss into removal of the corresponding channel, this is the
> desired carrier-or-deletion alternative at the palette level.

Two promotions are still independent.

1. **Provenance.**  A column of the minimal Schmidt factorization is usually
   a linear combination of many crossing matchings.  One must lift it to an
   actual occurrence/cap channel before calling it active or deleting it.
2. **Cap cleanliness.**  Exact \(N\mapsto N-2\) descent requires a covector
   \(K\) with
   \(s(K)\kappa_0(K)\kappa_1(K)\kappa_2(K)\ne0\) and
   \({\cal E}_{p,q}(K)=0\).  Monomial palette axes alone imply neither the
   activity polynomial nor the homogeneous error identity.

Thus inverse pairs across all bipartitions do **not** presently shift the
global proof frontier.  The useful new reduction is that this route needs
only one additional kind of object: an occurrence-faithful physical fusion
square.  If it exists, palette alignment is automatic; if it does not, the
primitive cross-palette class \(\Omega_{S,T}\) is the exact minimal
counterguard to promote to a source terminal.

## 6. Exact audit

The dependency-pinned checker
[`verify_simultaneous_diagonal_flattening_palette_fusion_gate.py`](../computations/verify_simultaneous_diagonal_flattening_palette_fusion_gate.py)

* checks all seven unoriented (fourteen oriented) cuts of
  \(\Delta_{4,3}\) with dense rational gauges and their inverse-transposes;
* verifies a nonzero fusion defect on every disjoint proper shore pair;
* exhausts the finite fusion-rigidity cases in (12); and
* pins the global cut-Wick/output-boundary and target-flattening audits that
  fix the source/output scope used above.

It is standard-library only and is intended to pass identically under
normal Python, `python -O`, and `python -I -S`.
