# Nonarchimedean GIT and projective properness: an exact bridge criterion

This note isolates what a nonarchimedean compactness argument would actually
have to prove.  There is a clean positive statement: good reduction whose
special output is still in the GHZ orbit is equivalent, up to an integral
change of basis, to normalization by the projective stabilizer of the GHZ
tensor.  There is also a clean negative statement: projective properness and
ordinary GIT semistable replacement do not guarantee either primitive output
or membership in that orbit.  The one-color rational example from
`notes/nonarchimedean-route.md` already violates the first missing condition.

Throughout, let (n=2m\ge 4), let

\[
 V_R=\bigoplus_{u<v}R^q\otimes_R R^q,
 \qquad W_R=\bigotimes_{v=1}^nR^q,
\]

and let

\[
 H:V_R\longrightarrow W_R
\]

be the matching map.  It is homogeneous of degree (m) and equivariant for
(G_R=\prod_v GL_{q,R}).  Put

\[
 \Delta_R=\sum_{a=0}^{q-1}e_a^{\otimes n}.
\]

We use a Henselian discrete valuation ring (R), with fraction field (K),
residue field (k) of characteristic two, and valuation (\nu).  Passing to
a finite extension of (K), and hence enlarging the value group and residue
field, is allowed.

## 1. Algebraization is not specialization

If the affine fiber (H^{-1}(\Delta)) has a complex point, then it has a
point over a number field.  Indeed, the fiber is a finite-type scheme over
(\mathbb Q); a complex point makes its coordinate ring nonzero, and any
closed point has residue field finite over (\mathbb Q).  We may therefore
choose a place above two and regard an exact solution as a (K)-point.

This observation supplies a nonarchimedean point, but not an integral one.
A nonempty generic fiber of a finite-type (R)-scheme need not have a point
in the special fiber: the elementary scheme
(\operatorname{Spec}R[1/2]) is already a counterexample.  Some properness or
boundedness input is indispensable, and it must preserve the affine equation
rather than merely a projective limit.

## 2. What projective properness loses

Homogeneity gives only a rational projective map

\[
 \phi:\mathbb P(V_R)\dashrightarrow\mathbb P(W_R),
 \qquad [A]\longmapsto[H(A)].                              \tag{1}
\]

Its base scheme is the common zero scheme of all coordinates of (H).  The
closure of the graph of (1) is projective, so the valuative criterion extends
a generic graph point after finite base change.  However, the special source
can lie in the base scheme.  The resulting target point records the first
nonzero common-order term of (H(A)), not the value of (H) on the reduced
source.  In particular, it need not produce a nonzero tensor in
characteristic two.

The exact one-color example makes this loss visible without any geometry
hidden in notation.  On six vertices take

\[
 A_{01}=\tfrac12,\quad A_{02}=-\tfrac12,
 \quad A_{23}=A_{45}=A_{13}=A_{05}=A_{12}=A_{34}=1,        \tag{2}
\]

with all other edges zero.  Its three supported perfect matching products
are (1/2,-1/2,1), so (H(A)=1).  A primitive integral representative of
the same projective source is (2A).  Modulo two it has only the two edges
(01) and (02), hence

\[
 H(\overline{2A})=0,
 \qquad H(2A)=2^3H(A)=8.                                  \tag{3}
\]

Projectively, ([H(2A)]=[1]) still extends.  For (q=1) the target is the
single point (\mathbb P^0), so the rational map even extends as a constant
morphism across its polynomial base locus.  Thus projective extension alone
cannot imply affine nonvanishing; it has forgotten the common factor (8)
in (3).

Nor can one repair this merely by asking that the target remain in the
projective orbit closure of (\Delta).  The projective (G)-orbit of the
GHZ tensor is not closed.  For example, acting at one vertex by
(\operatorname{diag}(1,t,t)) gives

\[
 [e_0^{\otimes n}+t e_1^{\otimes n}+t e_2^{\otimes n}]
 \longrightarrow [e_0^{\otimes n}],                       \tag{4}
\]

and the limit is not in the GHZ orbit.  Properness supplies an orbit-closure
point, whereas the characteristic-two argument needs an actual orbit point.

## 3. A precise bounded-modulo-stabilizer theorem

Let

\[
 \mathcal O_R=G_R\mathbin{\cdot}[\Delta_R]
       \subseteq\mathbb P(W_R)                             \tag{5}
\]

denote the locally closed projective orbit.  For (n\ge3), the projective
stabilizer of ([\Delta]) consists of tuples

\[
 h_v=D_vP,                                                  \tag{6}
\]

where (P) is one common permutation matrix, every (D_v) is diagonal, and

\[
 \prod_v(D_v)_{aa}=c                                      \tag{7}
\]

is independent of (a).  This description is valid scheme-theoretically in
characteristic two: the stabilizer is a torus extended by the constant
permutation group, hence is smooth.  One can prove (6) by viewing
(\Delta) as the multiplication tensor of the split algebra (R^q): for
three or more factors, preservation of its (q) primitive rank-one summands
forces the same permutation in every factor, and the remaining freedom is
diagonal.  Extra tensor factors only impose (7).

**Theorem 3.1 (orbit-valued good reduction).**  Let

\[
 \tau:\operatorname{Spec}R\longrightarrow\mathbb P(W_R)
\]

be a section such that its generic and special geometric points both lie in
(\mathcal O).  After a finite extension (R'/R), there is an element
(k_0\in G(R')) such that

\[
 \tau=k_0\mathbin{\cdot}[\Delta]
\]

as sections over (R').  Consequently, if
(\tau_K=g\mathbin{\cdot}[\Delta]) for (g\in G(K)), then

\[
                         g=k_0h,
 \qquad h\in\operatorname{Stab}_{G(K')}([\Delta]).         \tag{8}
\]

**Proof.**  Write the locally closed orbit as (Z\cap U), with (Z) closed
and (U) open in projective space.  The equations of (Z) vanish on the
generic point of the trait and therefore vanish in (R).  The inverse image
of (U) contains the closed point; an open subset of the spectrum of a DVR
which contains its closed point is the whole spectrum.  Hence (\tau)
factors through (\mathcal O_R).

The orbit morphism (G_R\to\mathcal O_R) is a smooth surjection because its
stabilizer is smooth.  Pulling it back along (\tau) gives a smooth scheme
over (R) with a geometrically nonempty special fiber.  After a finite
residue-field extension it has a rational special point, and Hensel lifting
gives an (R')-point (k_0); this is the standard lifting property for smooth
algebras over a Henselian pair ([Stacks Project, Lemma
15.13.3](https://stacks.math.columbia.edu/tag/0H74)).  This proves the first
assertion.  On the
generic fiber, (k_0^{-1}g) fixes ([\Delta]), proving (8).  (\square)

The theorem is a useful exact formulation of boundedness modulo the
stabilizer.  Its special-orbit hypothesis cannot be weakened to membership
in the orbit closure, as (4) shows.

## 4. Consequence for an integral source model

Fix an exact point (A\in V(K)) with (H(A)=\Delta).  Suppose that, after a
finite extension, there are (g\in G(K)) and (\mu\in K^*) for which

\[
                         B=\mu(g\mathbin{\cdot}A)\in V(R)  \tag{9}
\]

is primitive and integral.  Assume the two genuinely affine conditions

\[
 H(B)\text{ is primitive in }W(R),
 \qquad [H(\bar B)]\in\mathcal O_k.                        \tag{10}
\]

The first condition says exactly that evaluation has not fallen into the
projective base locus.  Apply Theorem 3.1 to the section ([H(B)]).  It
factors (g=k_0h), with (k_0\in G(R)) and (h) in the projective
stabilizer.  Since (k_0^{-1}) is an integral lattice automorphism,

\[
                         k_0^{-1}B=\mu(h\mathbin{\cdot}A)  \tag{11}
\]

is still primitive and integral, and its output is a unit multiple of
(\Delta).  Multiplication by the inverse unit at one vertex makes the
output exactly (\Delta).  Reduction then gives an exact solution over an
extension of (k).  Conversely, any stabilizer normalization with primitive
output plainly gives (9)--(10).  Thus allowing arbitrary local (GL_q)
does not enlarge the set of good models whose special output is in the
desired open orbit; the nonintegral part of the change of basis can be moved
into the projective stabilizer.

For completeness, this recovers exactly the valuation linear program from
`notes/nonarchimedean-route.md`.  Discard the common permutation in (6),
write

\[
 s_{v,a}=\nu((D_v)_{aa}),
 \qquad t_{v,a}=s_{v,a}+\tfrac12\nu(\mu),                  \tag{12}
\]

and pass to a ramified extension if necessary.  The valuation of a
transformed source entry is

\[
 \nu(A_{uv}^{ab})+t_{u,a}+t_{v,b}.                         \tag{13}
\]

If (h\Delta=c\Delta), primitivity of the output in (11) says

\[
 m\nu(\mu)+\nu(c)=0.
\]

Since (n=2m), equations (7) and (12) give

\[
 \sum_vt_{v,a}=\nu(c)+\frac n2\nu(\mu)=0                  \tag{14}
\]

for every color.  Integrality of (13), together with (14), is precisely the
linear program (2) in that note, up to a common relabeling of the colors.

## 5. The one-color example rules out even arbitrary good reduction

For the source (2), add the incidence vectors of its three perfect
matchings.  Every vertex has degree three, while the total valuation of the
nine edge occurrences is

\[
 (-1)+(-1)=-2.                                             \tag{15}
\]

If (t_v) were any local-scalar normalization with
(\sum_vt_v=0), summing the nine integrality inequalities would give
(-2\ge0), a contradiction.  The argument permits a global projective
source scalar because distributing half of its valuation to every vertex is
exactly the shift in (12).

For (q=1), every local (GL_1) transformation is already in the projective
target stabilizer, and every nonzero target is in the desired orbit.
Therefore (15), together with Theorem 3.1, proves the following precise
no-go statement:

> The rational exact point (2) has no finite extension and no arbitrary
> local change of basis for which a primitive integral source model has
> nonzero reduced matching output.

Equation (3) is its projective proper limit, so this is also a direct
counterexample to the assertion that projective extension forces a usable
specialization.  It does not claim that the whole one-color equation lacks
other characteristic-two solutions; it specifically refutes normalization
of a chosen exact point and any proof principle that treats projective
properness as sufficient for such normalization.

## 6. What semistable replacement would still need

Let (G^0=\prod_vSL_q) act on (X=\mathbb P(V)).  Over characteristic zero,
([\Delta]) is polystable.  Hence an exact source ([A]) is semistable: a
nonvanishing target invariant at (\Delta), pulled back along (H), is a
nonvanishing homogeneous source invariant at (A).  The semistable
replacement theorem can therefore, after finite extension and a
(G^0(K))-translation, produce an (R)-section of (X) with semistable
special point.  In strengthened formulations one may even choose a closed,
hence polystable, special orbit; this is the usual semistable-replacement
property of a projective GIT quotient ([Alper--Smyth--van der Wyck, Section
2](https://maths-people.anu.edu.au/~alperj/papers/weakly-proper.pdf)).

That theorem does not provide either condition in (10):

1. a semistable source point can lie in the base scheme (H=0); and
2. even when (H(\bar B)\ne0), its projective class can be a nonclosed
   orbit-closure point rather than a point of (\mathcal O_k).

The first failure already occurs in (2): for (q=1), the special linear
group is trivial, so every projective source point is semistable, while the
primitive reduction in (3) lies in (H=0).  In fact every source point is
already polystable in this example, so choosing a closed special source orbit
does not repair the failure.

Here is one concrete sufficient GIT package.  It would give the desired
bridge if all of the following were proved for the relevant integral model
and linearizations:

* every semistable special source reached by semistable replacement avoids
  the base scheme of (H);
* its nonzero target image is target-semistable; and
* ([\Delta_k]) is target-polystable, and every relevant image in its target
  GIT quotient fiber is polystable.

Indeed, the quotient morphism is separated.  Once the target images form an
integral semistable section, its generic quotient value is the value of
([\Delta]), so its special quotient value is the specialization of that
same point.  The last hypothesis upgrades S-equivalence to actual orbit
membership: a GIT quotient fiber has a unique closed orbit, so the image and
([\Delta_k]) have the same orbit.  Theorem 3.1 then applies.

A target invariant (F) with (F(\Delta)) a two-adic unit can help verify
the first two bullets if one can additionally prove
(F(H(B))\in R^*).  Generic nonvanishing is not enough: projective
renormalization can give this invariant positive valuation, exactly as the
factor (8) in (3) does.  Standard semistable replacement guarantees that
some source invariant is a unit, not that this particular pulled-back target
invariant is a unit.

## 7. Conclusion for the characteristic-two route

There is no unconditional bridge from a complex exact point to a
characteristic-two point via projective properness or standard GIT.  A
rigorous bridge must establish primitive output and prevent degeneration from
the GHZ orbit to its boundary.  If it establishes those facts, Theorem 3.1
shows that arbitrary local (GL_3) contributes no additional
nonarchimedean freedom: after an integral basis change, the problem is
exactly the target-stabilizing diagonal valuation program already isolated
in `notes/nonarchimedean-route.md`.

Finally, orbit-valued reduction is enough for the intended application.  If
(H(\bar B)=\bar g\Delta) with every component of (\bar g) invertible,
then equivariance gives

\[
 H(\bar g^{-1}\mathbin{\cdot}\bar B)=\Delta.
\]

The obstruction is therefore not the phrase “up to local (GL_3)”; it is
obtaining a primitive special output in that open orbit at all.
