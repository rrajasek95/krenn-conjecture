# Independent audit of the order-eight large-core obstruction

## 1. Verdict

**PASS.**  The proofs excluding \(|C|=3\) and \(|C|=4\) in
[the primary note](flat-n8-large-c-matching-cut-obstruction.md) are valid
under the stated order-eight globally flat boundary-core hypotheses.  The
arguments distinguish selected occurrences from physical aggregate pairs,
retain arbitrary complex cancellation, and terminate only at residual size
zero or two.  No repair to the primary proof or checker is required.

The audited files had SHA-256 digests

```text
486d1105a2daec300c343165fbe4eeab6a869d084d90c6160990e74b7ee4c8b5  notes/flat-n8-large-c-matching-cut-obstruction.md
d8523f1044f58bbc7ec4d91117c72e289ad5ecbf1e7eab71541e7b87518a3204  computations/verify_n8_flat_large_c_matching_cut_lemma.py
```

The audit treats as dependencies the already proved conclusions of
[the boundary-core reduction](flat-cubic-boundary-core-order-eight-reduction.md):

1. a vertex of \(C\) has three distinct bad physical neighbours;
2. its colour-\(a\) port is the entire pure block
   \(\lambda e_a\otimes e_a\), not merely one selected cell;
3. every zero block is good, so every bad pair is aggregate-active;
4. each selected constant-colour matching contains every forced port of
   that colour; and
5. each \(x\in X\) has at least \(|C|-2\) bad neighbours in \(C\) and
   total bad degree at least five when \(N=8\).

## 2. Occurrence and physical-edge ledger

The equality

\[
             b=\sum_a k_a=\sum_{x\in X}r_x
\]

is an equality of physical crossing-edge counts despite being obtained
from selected occurrence matchings.  Indeed, at a fixed \(u\in C\), its
three colour ports have three distinct physical neighbours.  Moreover the
whole block on such a pair is monochromatic pure.  Consequently no
physical \(C\!-!X\) pair is represented by two selected colours, and every
bad \(C\!-!X\) edge is represented exactly once among the three selected
fibres.  This justifies both equalities without silently counting a
parallel source twice.

Parallel differently coloured occurrences on a physical \(X\!-!X\) pair
are allowed.  They do not enter \(b\), \(k_a\), or \(r_x\).  When a
two-site residual is reached, the conclusion is that the complete
aggregate block \(A_{xy}\) is zero, so it kills every parallel occurrence
on that physical pair at once.

For an internal \(C\!-!C\) bad edge, the pure block descriptions at its
two endpoints force the same diagonal colour.  It is therefore one
physical bad edge and one selected occurrence, counted twice in the sum
of bad degrees over \(C\).  This validates

\[
                         3|C|=2e_C+b.
\]

## 3. Audit of the two-residual factorization

Let a disjoint selection of forced ports cover \(C\) and \(Z\subseteq X\),
and let \(Y=X\setminus Z\).  Once the endpoint colours on the selected
ports are fixed, every compatible full matching contains those ports, so
the complete coefficient factors as

\[
 [e_\xi]H_B(A)=w(F_\xi)[e_{\xi|Y}]H_Y(A),\qquad w(F_\xi)\ne0.
\]

If the colours already used on \(C\) are mixed, the left side is zero for
*every* assignment of the remaining endpoint colours.  Thus \(Y=\varnothing\)
is impossible, while \(Y=\{x,y\}\) forces every endpoint-ordered entry of
\(A_{xy}\) to vanish.  This is a statement about the full aggregate block,
not the selected monomial.  No uniqueness or termwise noncancellation is
used.  Reversing the fixed global endpoint order merely transposes the
two-site coordinate table and does not affect the zero-block conclusion.

## 4. The case \(|C|=3\)

Here \(|X|=5\) and \(r_x\ge1\), hence \(b\ge5\).  Each selected cut size
\(k_a\) is odd and at most three, so the three possibilities \(k_a\in
\{1,3\}\) force at least one all-cross selected fibre.  This establishes
the required all-cross fibre without any case classification of
\(b\in\{5,7,9\}\).

Write its crossing ports as \(c_i y_i\).  The \(y_i\) are distinct because
they lie in one perfect matching.  If \(p,q\) are the other two vertices
of \(X\), a bad crossing edge \(c_i p\) cannot have the all-cross colour.
Together with the other two all-cross ports it is a disjoint mixed
selection leaving exactly \(\{q,y_i\}\).  Hence \(A_{q y_i}=0\).  Different
bad neighbours of \(p\) correspond to different \(i\), and therefore to
different forced-good neighbours \(y_i\) of \(q\).  This gives

\[
 \deg_{\rm nonbad}(q,X)\ge r_p,
 \qquad
 \deg_{\rm nonbad}(p,X)\ge r_q.
\]

The total bad-degree lower bound five gives, independently for every
\(x\in X\),

\[
 \deg_{\rm bad}(x,X)\ge5-r_x,
 \qquad
 \deg_{\rm nonbad}(x,X)\le4-(5-r_x)=r_x-1.
\]

Applying the latter inequality to \(q\) and \(p\) yields the incompatible
pair \(r_p\le r_q-1\) and \(r_q\le r_p-1\).  The argument remains valid if
unselected or selected differently coloured entries share an
\(X\!-!X\) physical pair, because the forced-zero statements concern
aggregate blocks.

## 5. The case \(|C|=4\)

A fourth occurrence matching exists in the union of the three selected
one-factors and is mixed.  Under exact core factorization, a mixed fourth
matching cannot leave zero or two residual vertices.  Since \(|X|=4\),
its uncovered set is exactly \(Y=X\).  It therefore has no crossing
occurrence and uses two disjoint internal \(C\)-edges.  In particular
these are two distinct physical edges even if parallel colours elsewhere
are allowed.

The crossing-degree bound gives \(b\ge8\), while

\[
                         12=2e_C+b.
\]

The fourth matching gives \(e_C\ge2\), and the degree equation gives
\(e_C\le2\).  Thus \(e_C=2\), \(b=8\), and the four inequalities
\(r_x\ge2\) sum to equality, so every \(r_x=2\).  Each \(x\in X\) still
has total bad degree at least five; its three other vertices in \(X\) are
therefore all bad neighbours.  Every residual \(X\)-pair is consequently
active.

Let the two internal matching edges have colours \(k,k'\).  Keep the
\(k\)-edge.  At each endpoint of the other edge, the only internal port is
its \(k'\)-port, because the two displayed edges are the entire internal
bad graph on \(C\).  Hence:

- if \(k'=k\), either colour different from \(k\) crosses at both
  endpoints;
- if \(k'\ne k\), the third colour crosses at both endpoints.

Call this common colour \(\ell\).  Its two crossing endpoints in \(X\)
are distinct: otherwise the selected constant-\(\ell\) matching would
contain two incident forced ports.  The retained \(k\)-edge and the two
\(\ell\)-ports are thus a compatible mixed selection covering \(C\) and
two vertices of \(X\).  The residual pair is both bad and active, whereas
the two-residual factorization forces its entire block to zero.  This is
the desired contradiction.  The order in which a crossing block is
stored has no effect because its forced port is diagonal at both
endpoints.

## 6. Checker audit and parallel-colour stress test

The checker was run directly and returned

```text
|C|=4: 1232 normalized degree-feasible triples; 10 labelled cut profiles
|C|=3: 2388 normalized degree-feasible triples; 7 labelled cut profiles
order-eight large-C matching-cut obstruction: PASS
```

Its normalization is complete: for each possible parity-compatible cut
size of the first one-factor, the group
\(S_C\times S_X\) is transitive on one-factors of that cut size.  Fixing
one representative therefore loses no triple, while the other two
labelled one-factors are still enumerated without quotienting.  The
allowed first cut sizes are \(1,3\) for \(|C|=3\) and \(0,2,4\) for
\(|C|=4\), exactly as implemented.

Occurrences are stored as triples `(colour, u, v)`.  Consequently two
colours on the same physical pair are distinct recursion choices.  The
set of excluded selected matchings also retains the colour label.  Every
nonselected occurrence matching is automatically mixed: at every vertex
there is exactly one occurrence of each colour, so an all-\(a\) matching
is forced to be the selected factor \(M_a\).

As an adversarial test, among the feasible \(|C|=3\) triples the following
one has two parallel physical \(X\!-!X\) pairs:

```text
M0 = 03 12 45 67
M1 = 04 13 25 67
M2 = 06 17 23 45
```

Here \(C=\{0,1,2\}\), the cut profile is \((1,3,3)\), and the physical
pairs \(45\) and \(67\) each occur in two colours.  The checker retains
these as four occurrences, finds the forced-zero physical pairs \(36\)
and \(47\), and confirms that no bad graph on \(X\) avoiding those pairs
can meet total bad degree five.  Thus the intended occurrence semantics
is exercised, not merely documented.

For \(|C|=4\), every one of the 1,232 normalized feasible triples has a
nonselected occurrence matching with cut size two or four.  This is a
stronger finite contradiction than the human \(e_C,b\) argument: such a
matching would already have residual size two or zero.  The script is
therefore an independent audit rather than a line-by-line implementation
of Section 4, as the primary note correctly states.

## 7. Scope

The audited theorem only removes the large order-eight flat cores
\(|C|=3,4\).  It does not address curved transitions, and it imports the
entry-minimal globally flat cubic reduction.  Within that scope, the
argument is complete and no hidden assumption about unique matching
monomials, absence of parallel colours, or positive weights is present.

## 8. Sanity check of the unconditional curvature-line synthesis

I also audited
[the curvature-line synthesis](unconditional-curvature-line-selection.md),
at SHA-256

```text
a64dc29a6e88df96b47c0f5d64107d4cd4316cf8b3e1c230033dd988f7363e48  notes/unconditional-curvature-line-selection.md
```

The mathematical implication is valid with the minimum-support quantifier
stated in its first paragraph.  At a fixed order there are finitely many
aggregate coordinates, so the set of support cardinalities of exact
solutions is a nonempty subset of
\(\{0,1,\ldots,9\binom N2\}\) whenever a solution exists.  It therefore
has a minimum; no compactness or closed-image assertion is being used.
Replacing each nonzero aggregate coordinate by one decorated source is an
exact lift, so this minimization does not leave the original degree-two
source model.

For that minimum-support source, the bad graph is \(4\)-degenerate.  Thus
some centre has at least \(N-5\ge3\) good neighbours.  If *all* canonical
transitions at *all* centres with at least three good neighbours vanished,
flat-fan darkness would kill every good block at each such centre, and
minimum-support pure-port merging would make every such centre cubic.
The boundary-core theorem then excludes every even \(N\ge10\); at \(N=8\)
it leaves \(1\le|C|\le4\), the small-core theorem excludes \(|C|=1,2\),
and the audited theorem above excludes \(|C|=3,4\).  Therefore the
universal vanishing assumption is false and one actual transition is
nonzero.  This is the correct negation; vanishing only on one chosen fan
would not suffice.

A nonzero transition has a nonzero coefficient at some fourth site and
colour, giving the displayed physical determinant.  A nonzero
determinant has a nonzero entry in its first row after interchanging its
two columns, so the selected pair satisfies \(A_{pq}(a,b)\ne0\).  On the
line \(K_z=E_{ab}+zI\),

\[
 s(K_z)=A_{pq}(a,b)+z\operatorname{tr}A_{pq}
\]

is consequently a nonzero polynomial.  If \(a=b\), the target activity
product is \(z^2(1+z)\); if \(a\ne b\), it is \(z^3\).  Hence
\(s(K_z)\prod_i\kappa_i(K_z)\) is nonzero in \(\mathbb C[z]\), and its
nonvanishing locus is a nonempty cofinite subset of the line.  Endpoint
order is retained in the chosen coordinate determinant and has no effect
on this conclusion.

The audit requested one wording repair, now applied in the hashed version
above.  Its formal theorem was already about a chosen minimum-support
solution, but the former title and an unqualified use of “the flat
alternative is empty” could be read as claims about every arbitrary,
nonminimal presentation.  The exact proved statement is

\[
 \boxed{\text{at every order admitting a solution, a minimum-support
 solution has a physical curvature line}.}
\]

Equivalently, every minimum-support exact source has such a line.  It does
not show that an arbitrary redundant presentation has one, because the
port-merging surgery can change its transitions.  The revised title says
that every hypothetical realization admits such a representative, and the
flat alternative is explicitly qualified as empty after minimum-support
selection.  The prose now matches the proved quantifiers.
