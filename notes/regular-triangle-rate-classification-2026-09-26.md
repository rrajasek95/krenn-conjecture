# Every regular disconnected-triangle limit has a local square-root bound

September 26, 2026. **Written proof with supporting exact identities;
awaiting independent audit. The unrestricted square-root law remains open.**

[Guide](../explainers/BOUNDARY-STRUCTURE.md) ·
[Replay](../computations/boundary-structure-2026-09-26/README.md)

## 1. Scope of the extension

Split six sites into two triples. At a limiting source \(A_0\), assume all
cross-triple entries are zero, while the internal edge blocks may be arbitrary
complex 3-by-3 matrices. Let \(U_0,V_0:\mathbb C^9\to\mathbb C^{27}\)
be the two triangle response maps: choose an unmatched site and its color,
then fill the other two sites using their internal edge.

Call the split **regular** when both maps have rank nine.

**Theorem.** At every nonzero regular source of this form, one of the following
holds:

1. A whole neighborhood has GHZ fidelity bounded strictly below one.
2. Each triangle consists of three nonzero monochromatic edges, one in each
   target color. The source is an unequal-weight prism limit, and a whole
   neighborhood obeys \(\|E\|\ge c|\lambda|^3\) for some \(c>0\).

All perturbations in these neighborhoods may use all 135 complex source
entries. Thus this extends the local square-root result from one fixed prism
base to the entire class of regular disconnected-triangle limits. It does
not say that every zero-output limit admits such a split.

Here \(H=\lambda\Delta+E\), with \(\lambda\) the average of the three
pure amplitudes and \(\Delta=a^6+b^6+c^6\). The constants are local and can
depend on the base. They are uniform on a compact set of normalized bases
whose two least singular values are bounded away from zero.

## 2. Four-site exact GHZ sources are forced matching constructions

We first need the following consequence of the existing proof identities.

**Lemma.** A four-site complex ternary matching source whose only nonzero
outputs are \(\tau_h h^4\), with every \(\tau_h\ne0\), is diagonal in
the target basis. Each color occupies one perfect matching, and the three
colors occupy the three distinct perfect matchings of \(K_4\).

The whole-binary-response lemma in §2 of the
[frozen exact proof](../proofs/krenn-gu-all-orders-two-replica-proof.md) is stated
for odd cores of size at least three. Its even-omission argument in §3
explicitly includes the two-site omitted core. These identities therefore
apply to a four-site source; the later graph contradiction for more than
four sites is not being applied at four sites.

In that argument, for a target color \(h\), let \(C_h[r,q]\) be the
\(hh\) entry on the complementary pair, with diagonal zero, and let
\(B_{ih}[p,r]=A_{pr}(i,h)\). The identities give

\[
                    B_{ih}C_h=\delta_{ih}\tau_h I.
\]

Hence \(C_h\) is invertible and \(B_{ih}=0\) for \(i\ne h\), proving
diagonality. For \(i=h\), an off-diagonal entry of this same equation is
\(2A_{pr}(h,h)A_{ps}(h,h)=0\), where \(r,s\) are the other two sites.
Thus a vertex has at most one neighbor in each color. A nonzero pure hafnian
then forces one perfect matching per color. If two colors used the same
matching, choosing different colors on its two edges would give an uncancelled
mixed output. They therefore use distinct matchings. This proves the lemma.

The replay checks all 144 entries of the four-site cofactor formulas on a
complex example, and checks the finite classification constructions. The
universal whole-binary and omission identities are analytic dependencies of
the proof, not conclusions from that example.

**Triangle consequence.** If the image of a triangle response contains
\(a^3,b^3,c^3\), choose their three preimages as rows incident to a new fourth
site. This gives an exact four-site GHZ source. The lemma forces the original
triangle to have precisely three monochromatic edges, one of each color,
with nonzero weights. In particular, its response has rank nine.

## 3. A regular near-GHZ sequence forces this triangle condition

Across the split, every source has the exact decomposition

\[
                   H=UBV^T+K(B),
\]

where \(B\) contains the 81 crossing entries and \(\|K(B)\|\le2\|B\|^3\).
Near a regular base, the least singular values of \(U,V\) have positive
lower bounds. Consequently

\[
 \|UBV^T\|\ge s\|B\|\qquad(s>0),
\]

and, for small enough crossing norm, \(\|H\|\ge s\|B\|/2\).

Suppose a sequence tending to the base has \(F\to1\). Then
\(\|H\|/|\lambda|\to\sqrt3\), so \(B/\lambda\) is bounded.
Pass to a convergent subsequence. Since
\(K(B)/\lambda=O(|\lambda|^2)\to0\), division by \(\lambda\) gives

\[
                       \Delta=U_0 B_* V_0^T.
\]

The column and row spaces of the GHZ flattening contain the three pure
triple words. They must therefore lie in the images of \(U_0,V_0\).
The triangle consequence above forces both triangles to be monochromatic
one-edge-per-color triangles.

If this condition fails, no such sequence exists. Equivalently, some
neighborhood has a strict fidelity gap. This implication uses all complex
perturbations and arbitrary approaches to the limit, not just analytic paths.

## 4. Unequal prism limits reduce to the already proved local bound

For each color \(h\), let its left and right internal weights be
\(l_h,r_h\ne0\). Apply invertible diagonal maps to the local color spaces:
multiply one endpoint of the left color-\(h\) edge by \(1/l_h\), one
endpoint of the right edge by \(1/r_h\), and the unmatched left color-\(h\)
coordinate by \(l_h r_h\). Leave the other coordinates unchanged.

Both internal weights become one, while the product of the six factors for
each fixed color is one. Thus the transformation preserves \(\Delta\),
every pure amplitude, and \(\lambda\). It maps the base to a canonical
prism limit, after site relabeling.

Let \(D\) bound the induced operator on source entries and \(M\) bound the
induced operator on output tensors. On a source ball small enough that
\(D\|A-A_0\|\le10^{-3}\), the
[existing full-complex prism theorem](complex-rate-bound-2026-09-26.md) gives

\[
 M\|E\|\ge\|E'\|\ge\tfrac12|\lambda|^3.
\]

This proves the asserted local square-root estimate. For non-prism regular
bases, a fidelity gap gives \(\|E\|\ge c_1|\lambda|\); boundedness of
\(|\lambda|\) on a neighborhood converts it to a cubic bound as well.
Compactness supplies uniform constants over any compact regular set as
specified in §1.

## 5. An exact third-order identity, with all higher jets free

At the canonical prism, consider
\(A(t)=A_0+tA_1+t^2A_2+t^3A_3+\cdots\), with first output
\(H_1=l\Delta\), \(l\ne0\). Injectivity of the crossing response forces
the crossing part of \(A_1\) to be the three vertical cells of weight \(l\).
Its 54 internal entries remain arbitrary.

Put \(q=bca\), and let \(L_h,R_h\) be the internal first-order coefficients
that fill the two sites complementary to the vertical color-\(h\) edge,
using the colors of \(q\). Direct coefficient extraction gives

\[
 E_{2,(q,h^3)}=lL_h,\qquad E_{2,(h^3,q)}=lR_h,
\]

\[
 E_{3,(q,q)}=l^3+l\sum_h L_hR_h.
\]

In particular,

\[
 \boxed{lE_{3,(q,q)}-
     \sum_h E_{2,(q,h^3)}E_{2,(h^3,q)}=l^4.}
\]

If second-order error vanishes, third-order error cannot vanish. The checker
verifies this as a polynomial identity in 325 formal variables: \(l\), all
54 internal first jets, and all 135 entries of each of \(A_2,A_3\).
It does not fix higher jets to zero or test only a single path. The analytic
local theorem remains stronger, since it also covers later leading orders
and nonanalytic approaches.

## 6. What remains outside the proof

Rank-deficient triangle responses can make \(B/\lambda\) unbounded and defeat
the compactness step. Sources with no vanishing-crossing three-versus-three
split are also outside this theorem. These are genuine remaining classes;
no claim of a global square-root bound follows from the regular classification.
