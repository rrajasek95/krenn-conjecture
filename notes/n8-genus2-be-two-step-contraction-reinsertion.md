# The first squarefree genus-two BE attachment is the zero identity

## Outcome

The sole two-step physical-degree case left by the one-step genus-two audit
does become squarefree, but it gives no new source row.

Let \(T\subset\{0,\ldots,7\}\) have size seven, let \(i\in T\) be the
doubled site of the odd-principal Buchsbaum--Eisenbud row, and choose
\(j\in T\setminus\{i\}\). If \(k\) is the unique site outside \(T\), then
contracting \(\{i,j\}\) leaves exactly the holes \(\{j,k\}\). The unique
physical reinsertion that restores squarefree \(K_8\) degree is the edge
\(\{j,k\}\). There are

\[
                         8\cdot7\cdot6=336.             \tag{1}
\]

For every path, spin sector, starting output word, and colour-labelled
reinsertion, the resulting row is

\[
 \boxed{
 x_{jk}\,\partial_{x_{ij}}\operatorname{BE}_{T,i}=0 .
 }                                                       \tag{2}
\]

This is not merely zero because the parent BE row was simplified first. The
checker retains its unsimplified \(90\) terms. Differentiation selects
exactly \(30\); after reinsertion these are fifteen \(K_8\) perfect-matching
monomials, each appearing once with coefficient \(+1\) and once with
coefficient \(-1\). Thus (2) is a deletion-stable, literal termwise
cancellation in every constituent Pfaffian.

The bounded census therefore closes the first genuinely possible derived
Pfaffian attachment:

* all \(336\) paths have squarefree physical degree;
* all \(336\cdot16=5{,}376\) sector rows vanish termwise;
* all \(336\cdot16\cdot3\cdot9=145{,}152\) decorated rows vanish termwise,
  where the last factor exhausts the nine colour-labelled cells on the
  reinserted physical edge; and
* no row carries a target, ordinary residue, normalized \(w\), or physical
  pure-anchor incidence.

Consequently the construction realizes neither the rootless \(C_{\rm rel}\)
signature nor the intrinsic one-edge cap input.

## Physical and literal grades

Before contraction the physical degree is two at \(i\), one on
\(T\setminus\{i\}\), and zero at \(k\). Contraction of \(\{i,j\}\) gives
degree zero at \(j,k\) and one elsewhere. Multiplication by \(x_{jk}\)
then gives degree one at all eight sites.

The decoration has one precise freedom. Contraction removes the cell
labelled by the original output word at \(i,j\); reinsertion may use any of
the nine colour-labelled cells on \(j,k\). Hence the six unaffected output
labels are preserved and only the two reinserted-site labels can change.
Starting from the three words 00000000, 11111111, and 01222222, the complete
census reaches \(387\) final output words. None is one of the twenty selected
binary midpoint words with endpoint order 01 and a 3+3 residual split:
changing two sites cannot repair the required six-site balance. The operation
therefore supplies no required endpoint/output-grade comparison, despite
repairing the coarse physical degree.

There are \(10{,}944\) sector-labelled cases whose final output happens to be
pure. “Pure output” must not be confused with pure-anchor incidence:
equation (2) is a homogeneous Pfaffian syzygy and does not invoke the
physical equation \(H_c-1=0\). It has no constant target and its physical
pure-anchor incidence is zero in every one of those cases.

## Arf character

Write \(\ell(e)\in\mathbb F_2^4\) for the pinned Kasteleyn edge label. The
contraction differentiates a sector-signed \(x_{ij}\), while reinsertion
multiplies by the sector-signed \(x_{jk}\). The exact net twist is

\[
                  \ell(ij)+\ell(jk).                    \tag{3}
\]

All sixteen characters occur. The complete histogram is

\[
\begin{array}{c|rrrrrrrrrrrrrrrr}
\ell&0&1&2&3&4&5&6&7&8&9&10&11&12&13&14&15\\
\#&82&18&30&6&26&2&22&14&22&6&10&10&34&34&2&18.
\end{array}                                             \tag{4}
\]

Thus \(82\) paths are untwisted and \(254\) are nontrivially twisted. Every
nonzero character takes both signs on the sixteen sectors and hence is not a
scalar multiple of the original Arf aggregate. More importantly, even the
\(82\) untwisted paths are the zero identity (2); trivial spin descent does
not turn them into a physical row.

## Comparison with the two required endpoints

The rootless Component-III lower face requires

\[
 \operatorname{anc}=-1,\qquad
 \operatorname{tgt}=\operatorname{ores}=w=0,             \tag{5}
\]

and a selected midpoint response grade. The two-step row has all four
readouts zero, changes at most the two reinserted-site labels, and is the zero
polynomial. It misses both load-bearing parts of (5): anchor incidence and
the selected midpoint grade.

The intrinsic single-edge cap theorem instead requires scalar \(s(K)=0\), a
nonzero diagonal target \(\Lambda e_a\), and response supported on one
physical edge. Before cancellation, (2) has the common reinserted edge
\(\{j,k\}\), but its diagonal target is zero and its entire response cancels.
It is only the inactive zero member, not an active cap input.

The first missing Pfaffian operation is therefore genuinely cross-word or
target-augmented. Ordinary contraction and reinsertion inside a principal BE
identity cannot provide it.

## Verification

Run the checker normally, optimized, and isolated:

computations/verify_n8_genus2_be_two_step_contraction_reinsertion.py

It pins the sixteen-Pfaffian probe, the complete one-step boundary, the
rootless typed signature, and the intrinsic one-edge cap theorem. It
reconstructs the Kasteleyn orientation and four-bit labels, exhausts (1),
checks (3) sector by sector, and expands every one of the \(145{,}152\)
decorated rows without numerical specialization.
