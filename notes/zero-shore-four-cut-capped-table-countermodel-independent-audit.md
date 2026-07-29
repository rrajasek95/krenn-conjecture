# Independent audit of the twelve-port capped four-cut countermodel

## 1. Verdict and frozen inputs

**PASS, with no mathematical correction.**  The twelve-port construction in
[zero-shore-four-cut-capped-table-countermodel.md](zero-shore-four-cut-capped-table-countermodel.md)
really satisfies all 81 entries of the capped four-frame diagonal response
table, with four rank-three support-one row frames and exact coefficient one
on the three nonzero entries.  Lemma 4.1 is valid for an arbitrary nonzero
tensor block on every edge of one fixed physical perfect matching, and its
extension allowing zero blocks is also valid.

The exact primary files audited here had SHA-256 digests

    3b17c5c32a568c2cc79254d0f9ea2cfd5d33a5fe18cf832c75663405e0eef946  notes/zero-shore-four-cut-capped-table-countermodel.md
    957493414116870e6f541bf1f562ea53ba507903f259ea0f1ceecc4427bd64a1  computations/verify_zero_shore_four_cut_capped_table_countermodel.py

The independent checker is
[audit_zero_shore_four_cut_capped_table_countermodel_independent.py](../computations/audit_zero_shore_four_cut_capped_table_countermodel_independent.py),
with SHA-256 digest

    263b4161a0a823f22c91be1a5470bef3c80227c5edc4f7d0bb312b96d9c0da9e  computations/audit_zero_shore_four_cut_capped_table_countermodel_independent.py

It imports neither primary artifact and rebuilds the site-square-zero
products, frame ranks, physical matching sectors, zero-block masks, and
coordinate-line obstruction from scratch.

## 2. Reconstruction of the twelve ports and four frames

Label the twelve ports by

\[
             P=\{(c,j):c\in\{0,1,2\},\ 0\leq j\leq3\},
 \qquad H_c=\{(c,j):0\leq j\leq3\}.
 \tag{A1}
\]

The three sets \(H_0,H_1,H_2\) are disjoint four-sets and partition
\(P\).  In the algebra

\[
 {cal R}_P=\bigotimes_{x\in P}(\mathbb C\oplus V_x),
 \qquad V_xV_x=0,
 \tag{A2}
\]

put

\[
 p_c^{(j)}=e_c^{(c,j)},\qquad
 E_c=\bigotimes_{x\notin H_c}e_c^{(x)},\qquad
 \overline Q=E_0+E_1+E_2.
 \tag{A3}
\]

For fixed \(j\), the three rows \(p_0^{(j)},p_1^{(j)},p_2^{(j)}\)
are three different standard basis vectors in the direct sum
\(\bigoplus_{x\in P}V_x\).  Their matrix rank is therefore exactly three.
Each row has physical support exactly one, and its sole component is the
required nonzero \(e_c\)-coordinate anchor.  This verifies the four frames
individually; it does not identify rows belonging to opposite endpoints.

## 3. All 81 products and exact normalization

For a word \({\bf c}=(c_0,c_1,c_2,c_3)\), the row product occupies the
four distinct sites

\[
                    (c_0,0),(c_1,1),(c_2,2),(c_3,3).
\]

It can multiply \(E_g\) nontrivially exactly when all four occupied sites
belong to the hole set \(H_g\).  By (A1), this is equivalent to
\(c_0=c_1=c_2=c_3=g\).  Thus the calculation is termwise in the physical
multigrading, not an inference from a cancelling sum, and gives

\[
 \left(\prod_{j=0}^3p_{c_j}^{(j)}\right)\overline Q
 =
 \begin{cases}
   \bigotimes_{x\in P}e_g^{(x)},&c_0=c_1=c_2=c_3=g,\\
   0,&\text{otherwise}.
 \end{cases}                                             \tag{A4}
\]

Every factor used in a nonzero product has coefficient one and precisely
one sector \(E_g\) survives, so the output coefficient is exactly one.
There are three normalized diagonal products and seventy-eight literal
zero products.  The independent checker expands each of the 81 row words
against each of the three sectors separately before comparing their sum
with the target.

If four formal shore vertices are adjoined and their six mutual aggregate
blocks are set to zero, (A4) has exactly the form of the capped induced-zero
\(K_4\) interface

\[
 p_{c_0}^{(0)}p_{c_1}^{(1)}p_{c_2}^{(2)}p_{c_3}^{(3)}\overline Q
   =\delta_{c_0=c_1=c_2=c_3}X_{c_0}^P.                 \tag{A5}
\]

This verifies consistency of the **abstract capped table**.  It does not
supply the internal common quadratic whose divided power and subsequent
cap would have to produce \(\overline Q\) in an actual source.

## 4. Clean-room proof of Lemma 4.1

Fix a physical perfect matching \(M\) of the twelve ports and take

\[
                         q=\sum_{e\in M}B_e,
                  \qquad B_e\in V_x\otimes V_y.
 \tag{A6}
\]

Because two copies of one edge block repeat both of its physical sites,
\(B_e^2=0\).  Distinct matching edges have disjoint sites.  The divided
power therefore expands with coefficient one as

\[
                  q^{[4]}=
       \sum_{\substack{S\subseteq M\\|S|=4}}\prod_{e\in S}B_e. \tag{A7}
\]

If all six blocks are nonzero, every tensor product in (A7) is nonzero.
The \(\binom64=15\) terms have fifteen distinct physical four-hole sets,
so already the physical multigrading prevents equality with
\(\overline Q\), which has only three nonzero sectors.  This is a direct
strengthening of the contradiction used in the primary proof.

To audit that proof itself, a required coefficient \(E_c\) can occur only
if \(H_c\) is the union of the two omitted matching edges.  Requiring this
for all three colours partitions \(M\) into two edges inside each \(H_c\).
The coefficient with holes \(H_c\) is then

\[
                         \bigotimes_{e\not\subset H_c}B_e. \tag{A8}
\]

Regroup \(E_c\) by those same four edge factors.  Equality in (A8) is an
equality of two nonzero simple tensors in the four vector spaces
\(V_x\otimes V_y\), one space for each edge.  Uniqueness of nonzero simple
tensor factors forces

\[
                 B_e\in\mathbb C^*(e_c^{(x)}\otimes e_c^{(y)})
                 \qquad(e\not\subset H_c).             \tag{A9}
\]

This step does **not** assume beforehand that \(B_e\) is simple: contract
the other three factors by covectors nonzero on their target factors.  The
remaining equality makes \(B_e\) proportional to its target factor.

Now take an edge \(e\subset H_g\).  It occurs in (A8) for both colours
\(c\ne g\).  Those two equations force \(B_e\) into two distinct coordinate
lines

\[
 \mathbb C(e_c\otimes e_c)\quad(c\in\{0,1,2\}\setminus\{g\}), \tag{A10}
\]

whose intersection in the full nine-dimensional edge space is zero.  This
contradicts \(B_e\ne0\).  Hence the coordinate-demand proof covers arbitrary
nonzero tensor blocks, including entangled blocks and arbitrary complex
coefficients.

If zero blocks are allowed, the three nonzero required coefficients first
force the same alignment.  A zero edge in \(H_g\) occurs in each of the two
required products with hole colours \(c\ne g\), so at least one—and in fact
two—of the required diagonal coefficients vanishes.  Equivalently, if
exactly \(r\) matching blocks are nonzero, (A7) has \(\binom r4\) nonzero
physical sectors, and this number is never three for \(0\leq r\leq6\).
Thus allowing zero blocks cannot produce \(\overline Q\).

## 5. The exact \(10395/27\) ledger

The number of perfect matchings of twelve labelled ports is

\[
                         11!!=11\cdot9\cdot7\cdot5\cdot3=10395.
\]

For every \(H_c\) to be a union of matching edges, the matching must
restrict to a perfect matching on each four-set.  A labelled four-set has
three perfect matchings, giving exactly

\[
                              3^3=27                 \tag{A11}
\]

fully aligned matchings.  The independent enumeration further finds 9,504
matchings aligned with none of the three hole sets, 864 aligned with exactly
one, none aligned with exactly two, and 27 aligned with all three.

For each of the 27 fully aligned matchings, all \(2^6=64\) zero/nonzero
block masks were checked.  Only the all-nonzero mask leaves all three
required diagonal sectors structurally nonzero; the other \(27\cdot63=1701\)
masks fail before tensor coordinates are considered.  In each full mask,
all six edge blocks receive two incompatible coordinate-line demands,
giving \(27\cdot6=162\) separately checked conflicts.

## 6. Scope of the PASS

The construction is a countermodel to deductions that use only sparse
injective frames, coordinate anchors, and an arbitrary degree-eight capped
response tensor.  It is **not** a counterexample to Krenn's conjecture.
No source quadratic or full matching tensor is constructed.

Lemma 4.1 excludes only quadratics whose nonzero blocks lie on one fixed
perfect matching of these twelve physical ports.  Neither this audit nor
the primary note decides whether a general quadratic on the twelve ports
can have the required fourth divided power, or whether a common power on a
larger internal site set can produce \(\overline Q\) after a decomposable
cap.  It also does not exclude arbitrary block graphs, cancellation among
many physical matchings in one cofactor sector, or auxiliary capped-away
sites.  Those common-power provenance constraints are exactly the remaining
mathematical content that the abstract 81-entry table omits.

## 7. Executable result

Both the frozen primary checker and the independent checker return
**PASS**.  The latter reports

    independent twelve-port capped-table audit: PASS
    81 products: 3 unit diagonal responses, 78 literal zeros
    four support-one coordinate-anchored frame ranks: 3, 3, 3, 3
    fixed matching ledger: 10395 total; 27 fully aligned
    zero-block masks: 27 full masks survive structurally; 1701 fail
    arbitrary nonzero edge blocks: 162 incompatible coordinate demands

The finite enumeration audits the ledgers.  Equations (A1)--(A10) give the
uniform characteristic-zero proof of the table and the precisely scoped
fixed-matching no-lift statement.
