# Independent audit: full-nine pure-slice channel routing

## 1. Verdict

**PASS, with one terminology clarification.**  The constant-word
scalarization, the support definitions \(I_d,J_d\), the two hafnian
branches, the exclusion of the displayed unary/common-hole stars for every
replacement \(q\) and every direct block with a nonzero off-diagonal entry,
and the stated residual cases in
[the source note](full-nine-pure-slice-channel-routing.md) all check.

The source now says **hafnian-zero** rather than **singular** in its residual
ledger.  The equation obtained is
\(\operatorname{haf}(Q_d)=0\); the proof neither assumes nor implies
\(\det Q_d=0\).  This wording change does not alter any deduction.

## 2. Scalarization and fixed-label support

On the constant word \(d^6\), divided-power matching enumeration gives

\[
 [q^{[3]}]_{d^6}=F_d:=\operatorname{haf}(Q_d),
 \qquad
 [p_i s_jq^{[2]}]_{d^6}
   =(P_d^{\mathsf T}H(Q_d)S_d)_{ij}.
\]

The second identity has no factor two: for every unordered residual edge
\(\{x,y\}\), its coefficient is
\((P_d)_{x,i}(S_d)_{y,j}+(P_d)_{y,i}(S_d)_{x,j}\), while the matrix product
uses the corresponding two ordered entries of the symmetric, zero-diagonal
cohafnian matrix.  Hence the nine pair rows give exactly

\[
 M_d:=P_d^{\mathsf T}H(Q_d)S_d=E_{dd}-F_da.
\]

With

\[
 I_d=\{i:(P_d)_{*,i}\ne0\},\qquad
 J_d=\{j:(S_d)_{*,j}\ne0\},
\]

every entry outside \(I_d\times J_d\) is zero term by term.  Cancellation
inside an entry can shrink the support of \(M_d\), but cannot create an
entry outside this rectangle.  No rank assumption on either scalarized
star is being used.

## 3. The two branches and the unary guard

Fix any nonzero off-diagonal entry \(a_{ab}=\alpha\), \(a\ne b\).
If \(F_d\ne0\), then

\[
 (M_d)_{ab}=-F_d\alpha\ne0,
\]

so necessarily \(a\in I_d\) and \(b\in J_d\).  This conclusion is immune
to cohafnian cancellation because the full-row identity has already fixed
the aggregate entry to a nonzero scalar.

If \(F_d=0\), then \(M_d=E_{dd}\).  Its nonzero \((d,d)\)-entry forces
column \(d\) of both \(P_d\) and \(S_d\) to be nonzero, hence
\(d\in I_d\cap J_d\).  The implication does not claim that either column
pair has a selected noncancelling summand; only column nonvanishing is
needed.

For the displayed guard, direct inspection of (A16)--(A17) in
[the common-power audit](curved-pure-binary-three-channel-common-power-independent-audit.md)
gives

\[
 I_1=J_1=\{0\},\qquad I_2=J_2=\{1\}.
\]

For either missing colour, the nonzero-hafnian branch would require two
distinct off-diagonal labels to equal the same singleton label, and is
therefore impossible.  Thus that branch first forces \(F_d=0\), after
which \(M_d=E_{dd}\) forces the absent correct label \(d\) into both
supports, a contradiction.  Equivalently, the displayed matrix-unit
calculation makes the entire direct block diagonal when \(F_d\ne0\).
This proves the advertised uniformity in \(q\) and in the choice and
location of a nonzero off-diagonal direct entry.

The conclusion is about the **displayed, fixed-label endpoint stars**.  An
arbitrary refactorization or independent channel-basis change need not
retain these singleton supports and is not excluded by this argument.

## 4. Exact residual scope

The proof leaves precisely the following support-level exits.

1. **Aligned hafnian-zero exit:** \(F_d=0\), with the correct label
   \(d\in I_d\cap J_d\).  In the singleton case this is
   \(I_d=J_d=\{d\}\) and \(M_d=E_{dd}\).
2. **Curvature-channel exit:** \(F_d\ne0\), with
   \(a\in I_d\) and \(b\in J_d\).  For singleton supports this forces
   \((I_d,J_d)=(\{a\},\{b\})\), and the direct block can have no other
   off-diagonal cell.
3. **Deconcentrated exit:** one or both support sets contain multiple
   labels, subject to the same branchwise routing constraints.

The one-word packet in the source correctly witnesses only the first
support-level possibility.  It is not asserted to extend to global stars
or all words.  Conversely, the selected mixed-word packet in
[the Shafiei obstruction note](shafiei-generic-hafnian-apolar-lift-obstruction.md)
does not test this lemma: at a mixed word its target matrix is zero, whereas
the present zero-hafnian branch is routed by the nonzero pure anchor
\(E_{dd}\).  Thus the top-apolar cancellation guard and this pure-row
routing statement are compatible.

No listed exit is proved globally realizable.  Closing the argument still
requires cross-word/source compatibility to exclude the aligned
hafnian-zero and curvature-routed possibilities, especially with
non-singleton supports.
