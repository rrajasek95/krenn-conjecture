# N = 8 D1: exact minimal off-Sigma support cover

Date: 2026-08-08.

Checker:
[`computations/verify_n8_d1_minimal_off_sigma_support_cover.py`](../computations/verify_n8_d1_minimal_off_sigma_support_cover.py).

Committed input:
[`computations/verify_n8_d2_kill_and-monochrome-rigidity.py`](../computations/verify_n8_d2_kill-and-monochrome-rigidity.py),
pinned at SHA-256
`6320c3bdb795df3050952e52bd9c0fb9f4d5f2cdbf9eb543cd3467179630a745`.
No historical `scratch/` file is read or assumed.

## 1. Result

On the canonical D1 geometry, let \(m\) be the number of nonzero,
(E1)-admissible aggregate cells outside the a-column support class
\(\Sigma\).  Any exact D1 source must have

\[
                         \boxed{m\geq 6}.
\]

At the minimal layer \(m=6\), the two monochromatic anchors initially
give \(72^2=5184\) labelled support signatures.  The exact cover is

| certificate | signatures |
|---|---:|
| mixed residue-purity monomial | 864 |
| one-carrier six-site-purity monomial | 2400 |
| mixed full-word monomial | 1872 |
| support-level survivors | **48** |

The 48 survivors are one orbit under the D1-preserving group
\(C_2\times S_4\), of order 48.  Thus the minimal off-\(\Sigma\) layer is
reduced to one explicit support orbit.  This is a field-independent support
classification, not a finite-field sample.

It does **not** prove that the final orbit contains an exact source.  It also
does not address supports with \(m\geq7\).  Krenn's conjecture remains open.

## 2. Why six cells are necessary

On \(\Sigma\), every cell incident to a residue site is zero at the
monochromatic colours \(b,b\) and \(c,c\).  A nonzero matching term in
\(H(b^8)\) or \(H(c^8)\) must therefore cover all four residue vertices by
off-\(\Sigma\) cells of that colour.

The 105 perfect matchings split by their residue trace as follows:

| residue-residue edges | off-Sigma residue-incidence cells | matchings |
|---:|---:|---:|
| 2 | 2 | 9 |
| 1 | 3 | 72 |
| 0 | 4 | 24 |

The two colours use disjoint aggregate cells.  If \(m\leq5\), one colour
must cover the residue with two cells, necessarily two disjoint
residue-residue edges.  Among at most three active residue-residue edges,
that is the unique perfect matching: the coefficient of the corresponding
four-site monochromatic residue word is a nonzero monomial.  This
contradicts residue purity.  (The checker exhausts all 42 residue graphs
with at most three edges and verifies that none contains two perfect
matchings.)

At \(m=6\), the same argument excludes any two-cell colour trace.  Both
colours must use exactly three cells: one residue-residue edge and two
small-residue edges.  The latter meet the two residue vertices complementary
to the first edge.  Choosing the residue edge, the two small endpoints, and
their bijection gives

\[
                         6\cdot6\cdot2=72
\]

signatures per colour and no other off-\(\Sigma\) cell.

## 3. Exhaustive 5184-signature cover

For each pair of three-cell colour traces, the checker applies these
disjoint tests in order.

1. If the \(b\)- and \(c\)-residue edges are disjoint, the mixed residue
   word supported on those two edges has one nonzero matching term.  This
   kills 864 signatures.
2. If either colour's two small endpoints are the carrier pair
   \(\{0,2\}\) or \(\{1,3\}\), the corresponding six-site Lemma-F purity
   word has one nonzero term.  This kills 2400 further signatures.
3. Each anchor trace determines a fourth, small-small cell.  Its anchor
   equation makes that cell nonzero.  Together with the six off-\(\Sigma\)
   cells and the four nonzero D1 cells

   \[
   A_{01}(b,b),\ A_{23}(c,c),\ A_{02}(b,c),\ A_{13}(b,c),
   \]

   the checker searches all 105 matchings for a mixed full word having
   exactly one term on the whole allowed support.  It produces such an
   exact monomial certificate for another 1872 signatures.

The third test is not a blanket support rejection.  Without the two
anchor-determined small-small units it kills only 1632 signatures; those
units are load-bearing in 240 additional cases.  It deliberately leaves
48 signatures alive.

The simultaneous swap \((0\ 1)(2\ 3)\), together with every permutation of
the four residue sites, maps the survivor set transitively.  The
lexicographically canonical representative has the six off-\(\Sigma\)
cells

\[
\begin{split}
&A_{04}(c,c),\quad A_{15}(c,c),\quad A_{67}(c,c),\\
&A_{24}(b,b),\quad A_{36}(b,b),\quad A_{57}(b,b).
\end{split}
\]

## 4. Reproducible residual search input

The checker reconstructs, but does not solve, a conservative saturated-ideal
input for that representative.  It has:

- 95 variables: all 89 \(\Sigma\)-cells plus the six displayed cells;
- 616 distinct nonzero generators after exact deduplication;
- full 6561-word output exactness, both six-site purity systems, residue
  purity, the a-pendant identities (structural zeros on this support), both
  dagger identities, and the D1 harmful-minor equation;
- (E1) imposed by omission of its forbidden cells; and
- localization at 12 cells: the six displayed cells, the four live/harm
  cells above, and \(A_{02}(a,a),A_{13}(a,a)\).

The frozen generator digest is

~~~text
e63e5997eda920d62442aa20f702fac62ad2942077cea9a73f9059c08b241600
~~~

This is the exact next elimination target.  Its emptiness would finish the
minimal \(m=6\) layer only; it would not classify \(m\geq7\).

## 5. Verification

~~~text
python3       computations/verify_n8_d1_minimal_off_sigma_support_cover.py
python3 -O    computations/verify_n8_d1_minimal_off_sigma_support_cover.py
python3 -I    computations/verify_n8_d1_minimal_off_sigma_support_cover.py
python3 -S    computations/verify_n8_d1_minimal_off_sigma_support_cover.py
python3 -I -S computations/verify_n8_d1_minimal_off_sigma_support_cover.py
python3 -m py_compile computations/verify_n8_d1_minimal_off_sigma_support_cover.py
~~~

Frozen ledger digest:

~~~text
69166fa61fad7499bf991aa803c6e6a138a1f64a51ba6e9e26cc9e0a86db0a88
~~~
