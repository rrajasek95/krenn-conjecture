# Every weighted three-term same-colour support misses the pair-cap variety

## 1. The finite theorem

For each colour \(c\in\{0,1,2\}\), choose a perfect matching \(P_c\) of
eight labelled sites and a distinguished edge \(d_c\in P_c\).  Assign
arbitrary nonzero complex coefficients
\(\alpha_{c,uv}\) and \(\zeta_c\), and define

\[
\begin{aligned}
 q&=\sum_{c=0}^2\ \sum_{uv\in P_c\setminus\{d_c\}}
       \alpha_{c,uv}e_c^{(u)}e_c^{(v)},\\
 z&=\sum_{c=0}^2 \zeta_c e_c^{(d_c)}.                    \tag{1}
\end{aligned}
\]

Thus \(q\) has nine weighted same-colour cells and \(z\) has three.  Suppose
the literal decorated expansion has exactly the three intended matching
terms and is normalized so that

\[
                              z\,{q^3\over3!}=\Delta_{8,3}. \tag{2}
\]

Then the same \(q\) has no preimage of pair-cap form:

\[
 \boxed{\quad
 (a q+4ps){q^3\over3!}\ne\Delta_{8,3}
 \quad\text{for all }a\in\mathbb C
 \text{ and all linear }p,s.
 \quad}                                                   \tag{3}
\]

The theorem exhausts the full natural class of weighted same-colour
polarized models supported on exactly three decorated matching terms.  It
strictly contains the particular sparse model treated in the preceding
fixed-\(q\) note.  The weights are not normalized away; only their
nonvanishing is used.

The exact verifier is
[verify_polarized_eight_site_three_term_pair_cap_exhaustion.py](../computations/verify_polarized_eight_site_three_term_pair_cap_exhaustion.py);
its explicit enumerator and certificate constructor is
[explore_polarized_three_term_pair_cap_gram_patterns.py](../computations/explore_polarized_three_term_pair_cap_gram_patterns.py).

## 2. Reduction to six nonzero mode vectors

Put

\[
             Q={q^4\over4!},\qquad F={q^3\over3!}.
\]

If (3) failed, then \(qF=4Q\) would give

\[
                         aQ+psF={1\over4}\Delta_{8,3}.    \tag{4}
\]

For every support satisfying the three-term hypothesis, exact enumeration
verifies two facts for each colour \(c\).

1. The pure word \(c^8\) has exactly one contributor in \(psF\): the
   \(R\)-entry on the two colour-\(c\) modes of \(d_c\).
2. The same word is absent from \(Q\).

Here

\[
 R_{(u,i),(v,j)}=p_{u,i}s_{v,j}+s_{u,i}p_{v,j}.          \tag{5}
\]

The coefficient of the first contributor is the nonzero product of its
three \(\alpha\)-weights.  Thus (4) forces the corresponding \(R\)-entry to
be nonzero, although its value need not be \(1/4\).  Consequently the six
endpoint modes of \(d_0,d_1,d_2\) are nonzero vectors
in the two-dimensional Gram realization

\[
 x_X=(p_X,s_X),\qquad
 \beta(x_X,x_Y)=R_{X,Y},\qquad
 \beta((r,t),(r',t'))=rt'+tr',                           \tag{6}
\]

and the three distinguished pairs have nonzero Gram value.

Every mixed top word which has one \(psF\) contributor and is absent from
\(Q\) has a nonzero monomial coefficient multiplying its Gram entry, so it
forces that entry to zero.  Retaining only zero
entries whose two endpoints belong to the six distinguished modes gives a
finite labelled zero graph.

## 3. The orthogonality-closure certificate

The verifier applies the following elementary closure lemma.

**Lemma.**  Let six nonzero vectors lie in a two-dimensional vector space
with a nondegenerate symmetric bilinear form.  Mark some pairs as
orthogonal and three disjoint pairs as having prescribed nonzero product.
The following inference rules are sound.

1. All orthogonal neighbours of one nonzero vector are proportional.
2. Proportional vectors have the same orthogonal line.
3. If a proportionality class contains an orthogonal pair, its line is
   isotropic; every vector orthogonal to that class is then proportional to
   it.
4. A contradiction occurs if a prescribed nonzero pair is forced onto an
   orthogonal class pair, or into an isotropic class.

**Proof.**  The orthogonal complement of a nonzero vector in a
two-dimensional nondegenerate space is one-dimensional, proving the first
two rules.  For an isotropic line \(L\), one has \(L^\perp=L\), proving the
third.  The last rule is immediate. \(\square\)

The implementation records proportionality by union--find, repeatedly
merges all zero-neighbours of every class, detects isotropic classes from
internal zero edges, and then checks the three required nonzero pairs.
Every merge is therefore a literal application of the lemma, rather than a
heuristic graph rule.

The shorter seven-entry pattern from the fixed-\(q\) theorem already closes
most supports.  The general closure is needed for the rest.

## 4. Exhaustion and exact counts

There are \(105\) perfect matchings of eight labelled sites and \(420\)
flagged pairs \((P,d)\).  The symmetric group on the sites acts transitively
on flagged matchings, so normalize

\[
 P_0=01\mid23\mid45\mid67,\qquad d_0=01.                 \tag{7}
\]

The other two colours give exactly

\[
                              420^2=176{,}400             \tag{8}
\]

labelled cases.  For each case the verifier enumerates all decorated
perfect matchings of the complement of each \(d_c\).  Because every cell
is required nonzero, the expansion has exactly three decorated terms
precisely when each complement has one decorated matching and it has colour
\(c\).  The target normalization is then
\(\zeta_c\prod_{uv\in P_c\setminus\{d_c\}}\alpha_{c,uv}=1\), independently
for each colour.  Running the support enumeration at unit weights therefore
loses no weighted support.

The exact ledger is

\[
\begin{array}{c|r}
\text{class}&\text{count}\\ \hline
\text{combinatorially three-term supports}&9{,}888\\
\text{short seven-entry Gram certificate}&7{,}968\\
\text{additional orthogonality-closure certificate}&1{,}920\\
\text{uncertified supports}&0.
\end{array}                                               \tag{9}
\]

The SHA-256 hash of the ordered normalized certificate ledger is

5f42b78f2f972ed25a96f6ea01a25dcaf2b1c108174ba0fe2d0804132dddb639.

All matching enumeration, word multiplicities, \(Q\)-support tests, and
closure steps use integers and exact finite combinatorics.

## 5. Scope boundary and next target

This theorem is not an eight-site Krenn obstruction.  It assumes:

- exactly nine nonzero cells in \(q\), organized as three same-colour
  near-perfect matchings;
- exactly three nonzero distinguished cells in \(z\);
- no endpoint-asymmetric \(q\)-cells, additional cells, or cancellation
  among several decorated terms.

It does show that every three-term unrestricted polarized model of this
natural type, with arbitrary nonzero complex weights, is separated from the
actual pair-cap equations even after
the whole kernel of \(z\mapsto zq^3/3!\) is allowed.  A surviving
eight-site pair-cap model must therefore use a genuinely different
quadratic: extra or endpoint-asymmetric cells, nontrivial complex
cancellation, or more than three polarized terms.

For the uniform conjecture, compatibility among several shared rows and
overlap among distinct physical-pair identities remain untouched.  No
all-even descent is claimed.
