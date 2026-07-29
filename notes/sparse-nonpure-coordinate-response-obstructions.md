# Two sparse non-pure common-square boundaries are impossible

## 1. Outcome and exact scope

Let $U$ be a six-set and work in the site-square-zero algebra

\[
 \mathcal R_U=\bigotimes_{u\in U}(\mathbb C\oplus V_u).
\]

Write $e_0^{(u)},e_1^{(u)},e_2^{(u)}$ for the three target axes and

\[
 X_i=\bigotimes_{u\in U}e_i^{(u)}.
\]

This note closes two exact sparse search classes for

\[
 F=q^{[2]},\qquad q^{[3]}=0,\qquad
 p_i s_jF=\delta_{ij}X_i.                              \tag{1}
\]

The first class permits arbitrary mixed endpoint colours but assumes that
the physical support graph of $q$ has no perfect matching and that the
sampled four-site coefficients are collision-free.  The second class
permits every complex cancellation and does not even need $q^{[3]}=0$,
but assumes that every cell of $q$ has the same target colour at its two
ends.  Both classes allow arbitrary zero patterns and aggregate complex
weights.  In both, the six response rows are one-site coordinate rows.

**Theorem 1.1 (termwise, mixed-endpoint boundary).** Suppose each $p_i$
and $s_i$ is supported at one site.  Suppose the physical support graph
$G(q)$ has no perfect matching.  Assume, on every four-site block sampled
by the nine products, that

\[
 G(q)[S]\text{ has a two-matching}
 \quad\Longrightarrow\quad
 q^{[2]}|_S\ne0.                                      \tag{2}
\]

Then equation (1) is impossible.  Hypothesis (2) holds, in particular, when every
coordinate word on a sampled block receives at most one nonzero decorated
matching term.  Endpoint colours may be mixed.

**Theorem 1.2 (same-colour common-square boundary).** Suppose

\[
 q=\sum_{c=0}^2\sum_{uv\in\binom{U}{2}}
       x_{c,uv}e_c^{(u)}e_c^{(v)},\qquad x_{c,uv}\in\mathbb C,       \tag{3}
\]

and each $p_i,s_i$ is a one-site coordinate row.  There is no solution
of the nine product equations in (1), even if the equation $q^{[3]}=0$
is dropped.  Thus arbitrary cancellations among two-matchings and perfect
matchings do not repair this class.

Theorem 1.2 is genuinely beyond a single local line field: all three
incompatible target line fields occur in (3), and their cross-products make
$F$ non-pure.  It remains only a search-class theorem.  It does **not**
cover mixed endpoint cells in $q$, rank-two edge blocks, or multi-site
response rows.

## 2. One-site rows and the seventeen directed orbits

A nonzero diagonal response forces the coordinate of $p_i$ and $s_i$
to be $e_i$.  Absorb their two nonzero scalars into the normalization and
write

\[
 p_i=e_i^{(a_i)},\qquad s_i=e_i^{(b_i)},\qquad a_i\ne b_i.           \tag{4}
\]

Thus a row configuration is a triple of directed edges

\[
             (a_0\mathbin\to b_0,
              a_1\mathbin\to b_1,
              a_2\mathbin\to b_2).                                \tag{5}
\]

There are $30^3=27{,}000$ labelled triples.  Site permutations,
simultaneous target-colour permutations, and the global swap
$p\leftrightarrow s$ preserves (1); the last operation reverses all three
arrows.  Canonical relabelling leaves exactly seventeen orbits.  Their
labelled sizes are

\[
\begin{split}
 &(30,720,90,720,1080,720,1440,720,4320,\\
 &\hspace{35mm}2160,2160,4320,1080,240,2160,4320,720),               \tag{6}
\end{split}
\]

which sum to $27{,}000$.  The checker reconstructs the orbits from all
labelled triples rather than taking the list on faith.

For $P=\{u,v\}$, multiplication by rows at $u,v$ samples exactly the
block of $F$ on $U\setminus P$.  If the two rows occupy the same site,
their product is zero.  Consequently the diagonal equations require

\[
 q^{[2]}|_{U\setminus\{a_i,b_i\}}=
     \text{a nonzero scalar multiple of }e_i^{\otimes4},            \tag{7}
\]

whereas, for $i\ne j$ and $a_i\ne b_j$, the off-diagonal equation
requires

\[
 q^{[2]}|_{U\setminus\{a_i,b_j\}}=0.                               \tag{8}
\]

These are full tensor equations, not merely statements about one selected
coordinate.

## 3. Proof of the termwise physical-graph obstruction

For a graph $G$ on $U$, put

\[
 C_G(u,v)=1
 \quad\Longleftrightarrow\quad
 G[U\setminus\{u,v\}]\text{ has a perfect matching}.                \tag{9}
\]

Equation (7) implies

\[
                         C_G(a_i,b_i)=1                              \tag{10}
\]

for all $i$.  Under the faithfulness hypothesis (2), equation (8)
implies

\[
 a_i=b_j\quad\text{or}\quad C_G(a_i,b_j)=0
                 \qquad(i\ne j).                                   \tag{11}
\]

There are only $2^{15}$ labelled simple graphs on six vertices.  Literal
matching enumeration gives $7{,}945$ with no perfect matching.  Across
the seventeen directed-row representatives, $8{,}911$ graph/orbit pairs
satisfy all three conditions (10).  None satisfies all six conditions
(11).  Since every labelled row triple lies in one of the reconstructed
orbits, this is exhaustive and proves Theorem 1.1.

No weight or colour assumption enters this enumeration.  Its only
coefficient hypothesis is (2), precisely the point at which an additional
decorated matching could cancel the first one.  Section 4 removes that
hypothesis for the three-line same-colour model by granting all such
cancellations.

## 4. Necessary support calculus for the three-line model

For (3), define the support bits

\[
 z_{c,e}=1\quad\Longleftrightarrow\quad x_{c,e}\ne0.                 \tag{12}
\]

Fix a missing pair $P$.  The pure colour-$c$ coefficient on its
four-site complement is the three-term hafnian

\[
 H_c(P)=
 \sum_{M\in\operatorname{PM}(U\setminus P)}
       \prod_{e\in M}x_{c,e}.                                      \tag{13}
\]

Only the following weak support consequences are used.

1. If $H_c(P)\ne0$, at least one matching in (13) is supported.
2. If $H_c(P)=0$, the number of supported matching terms is not exactly
   one.  Zero or two/three supported terms are all allowed; the latter are
   granted arbitrary complex cancellation.
3. A four-site word using colour $c$ twice and a different colour $d$
   twice has exactly one possible matching under (3): the edge joining the
   two $c$-sites and the edge joining the two $d$-sites.  Its vanishing
   therefore forbids those two support bits from being simultaneously one.

Rule 3 is where the common-square origin is used.  Cross-products between
the three line fields are genuine non-pure terms of $F$, but each such
$2+2$ word has a unique provenance.

Apply rules 1--3 to every block in (7)--(8).  For a fixed row orbit this is
a Boolean system in the $45$ bits (12).  The checker introduces $135$
auxiliary variables, one for each triple

\[
 (c,P,M),\qquad c\in\{0,1,2\},\quad
 P\in\binom{U}{2},\quad M\in\operatorname{PM}(U\setminus P),          \tag{14}
\]

and makes that variable equivalent to the conjunction of the two support
bits in $M$.  Rule 1 is one positive three-literal clause.  Rule 2 is

\[
 Z_k\Longrightarrow\bigvee_{\ell\ne k}Z_\ell                         \tag{15}
\]

for each of the three matching indicators.  Rule 3 gives binary negative
clauses.  These clauses are necessary for a complex solution but are not
sufficient: among other relaxations, they allow any two or three supported
terms in (13) to cancel without checking their weights.  Unsatisfiability
of this relaxation is therefore a valid obstruction.

After canonical deduplication, the clause counts for the seventeen row
orbits are

\[
 (435,462,435,486,513,489,489,489,540,540,516,567,567,489,564,615,642).
                                                                    \tag{16}
\]

A standalone deterministic DPLL routine proves every system UNSAT.  Its
search trees have respectively

\[
 (3566,1050,3566,1258,731,470,446,292,232,219,183,64,181,365,175,7,24)
                                                                    \tag{17}
\]

visited nodes.  When PySAT is available, CaDiCaL independently returns
UNSAT on the same clauses.  Dropping all rules (15) makes the first orbit
SAT, a positive control against a vacuous target encoding.  The SHA-256
ledger of the seventeen canonical CNF hashes is

```text
b71aa65a4a08354100e302acea5914de0e12808f8ca80a2539a1dccf52976afc
```

This proves Theorem 1.2.  Notice that neither the constant-colour
perfect-matching equation $q^{[3]}=0$ nor any support consequence of it
was inserted.  Perfect-matching cancellation is therefore allowed a
fortiori.

## 5. Reproducibility and the surviving next class

Run

```sh
uv run python computations/verify_sparse_nonpure_coordinate_response_obstructions.py
```

The checker independently reconstructs the seventeen row orbits, all
$7{,}945$ perfect-matching-free physical graphs, all $8{,}911$
diagonal survivors, every Boolean clause from literal matching provenance,
the internal DPLL proofs, the optional CaDiCaL cross-checks, and the hash
ledger.

The next exact sparse class is now sharply isolated: retain one-site
coordinate rows but allow a cell $e_a^{(u)}e_b^{(v)}$ with $a\ne b$,
or allow a rank-two edge block.  Mixed endpoint cells destroy the unique
$2+2$ provenance in rule 3, so they require a new cancellation-packet
classification rather than another same-colour support census.
