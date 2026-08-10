# Each bright pure preimage flags the whole cofactor kernel

## 1. Support-free site-flag theorem

Let (S) be the five common sites, let

\[
 Phi:\bigoplus_{z\in S}V_z\longrightarrow
       \bigotimes_{z\in S}V_z,
 \qquad B=\ker\Phi,
\]

and suppose a row (a=(a_z)) is a preimage of a nonzero pure tensor,

\[
                       \Phi(a)=X_i=\bigotimes_{z\in S}e_i^{(z)}. \tag{1}
\]

For a site (z), write

\[
 L_z(a)=\{b\in B:b_z\in\mathbb C a_z\},\qquad
 Z(a)=\{z:L_z(a)=B\}.                                  \tag{2}
\]

Then one of the following holds:

1. some local entry (a_z) is zero;
2. (|Z(a)|\ge2), so at least two sites carry a line containing the
   evaluation of the **entire** kernel (B);
3. (Z(a)=\{r\}) and (a_r\parallel e_i).

This is independent of source support, endpoint-colour sparsity, or a
chosen kernel basis.  It applies separately to the two bright rows

\[
                    \Phi(Q_c)=X_c,\qquad \Phi(R_a)=X_a. \tag{3}
\]

The checker is
`computations/verify_shared_reciprocal_two_bad_bright_whole_kernel_site_flag.py`.

## 2. Proof from the two-star lemma

Package the common cofactors as the degree-four element (G) in the
five-site square-zero algebra.  Equations (1) and (Phi(b)=0) are

\[
                         aG=X_i,\qquad bG=0.             \tag{4}
\]

The two-star pure-response lemma says that for every (b\in B),

\[
 D(a,b)=\{z:\dim\langle a_z,b_z\rangle\le1\}\ne\varnothing. \tag{5}
\]

Assume every (a_z\ne0).  Then (D(a,b)\ne\varnothing) says exactly

\[
                              B=\bigcup_{z\in S}L_z(a). \tag{6}
\]

Each (L_z(a)) is a linear subspace of (B).  A finite-dimensional vector
space over the infinite field (mathbb C) cannot be a finite union of
proper linear subspaces.  Hence some (L_z(a)=B), so (Z(a)\ne\varnothing).

If (Z(a)=\{r\}), every (L_z(a)), (z\ne r), is proper.  Apply the same
finite-union fact to choose

\[
                       b\notin\bigcup_{z\ne r}L_z(a).   \tag{7}
\]

Now (D(a,b)=\{r\}).  The singleton clause of the two-star lemma gives

\[
 e_i^{(r)}\in\langle a_r,b_r\rangle=\mathbb C a_r,     \tag{8}
\]

which is the third branch.

The infinite-field hypothesis is essential.  Over (mathbb F_2), the
three proper lines of (mathbb F_2^2) cover the whole space; the checker
freezes this exact mutation guard.

## 3. Refinement of the common-radical branch

In branch (iii) of the bright-pairing radical dichotomy,

\[
 W=\pi_t(B)
\]

is two-dimensional and the target-projection theorem puts it on one fixed
pair.  Let (T\subset S), (|T|=2), be the **minimal** coordinate support
of (W).

In the unique-site branch for (Q_c), equations (2) and (8) give

\[
                    \operatorname{ev}_r(B)\subseteq\mathbb C e_c. \tag{9}
\]

Every kernel vector therefore has zero (t)-coordinate at (r), so

\[
                              r\notin T.                \tag{10}
\]

The same conclusion holds for a unique (R_a) flag, with (e_a) in
place of (e_c).  Thus each zero-free bright row is reduced to one of two
source-independent geometries:

* at least two whole-kernel evaluation lines; or
* one literal bright-axis line at a site outside the target pair.

For five sites and a fixed target pair there are 26 multi-site flag sets
and three allowed unique sites.  Applying the result to both bright rows
leaves the finite pattern split

\[
  9\ \text{unique/unique},\qquad
  156\ \text{unique/multiple},\qquad
  676\ \text{multiple/multiple}.                       \tag{11}
\]

These counts are bookkeeping, not a support enumeration: every flag
constrains the evaluation of the full kernel, including arbitrary
non-target tails.

## 4. Interface with the private-row chart cover

The new lemma is the support-free normalization missing before the sparse
private-row calculations.  A proof can now choose leading cofactor
matchings only after entering one of the flag branches (9)--(11), rather
than assuming a tilted sparse kernel at the outset.

On the canonical first-transgression chart, the first apparent rewrite
two-cycle is already source-rigid.  With localized mate scale (x\ne0)
and switch weights (r,s,t\ne0), its two defect coefficients are

\[
  W=\pm {2r\over x}-s+t,\qquad Z=-s+t.                  \tag{12}
\]

Simultaneous cancellation gives (2r/x=0), impossible in characteristic
zero.  This is the first signed-holonomy critical-pair resolution, not a
counterexample to a well-founded matching filtration.

What remains is genuinely theorem-level: in each whole-kernel flag branch,
show that leading matching normalization produces the two private residues
and one of the four mate charts, and that every later critical cycle either
has a Laurent monomial holonomy as in (12) or creates a rank-14 pivot.  The
present lemma supplies the missing basis-free entry to that argument; it
does not yet prove the complete chart cover.
