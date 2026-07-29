# Exact fibre obstructions for the arbitrary rank-one six-site shadow

## 1. Scope

Let $G$ be an arbitrary simple support graph on six sites.  On every
supported pair write the nonzero aggregate block as

\[
 A_{uv}=x_{u|v}x_{v|u}^{\mathsf T};
\]

the two endpoint factors are unrelated and may have arbitrary zero patterns.
Absent pairs are allowed.  This note records two exact algebraic obstructions
and a finite Boolean relaxation of

\[
                         H_6(A)=\Delta_{6,3}.             \tag{1}
\]

It does **not** assume pair-Hessian rigidity, distinct endpoint lines,
mutual coordinate edges, or full-support residual factors.

For an ordered supported half-edge put

\[
 S_{u|v}=\{c\in\{0,1,2\}:x_{u|v}(c)\ne0\}.              \tag{2}
\]

For a word $a\in\{0,1,2\}^6$ and perfect matching $P$, call $P$
compatible with $a$ when

\[
                         a_u\in S_{u|P(u)}\quad(u=0,\ldots,5). \tag{3}
\]

Its matching monomial $z_a(P)$ is then nonzero.

## 2. Necessary Boolean conditions

Here is a self-contained derivation of the two anchor conditions.  Fix a
centre $p$, set $y_u=x_{u|p}$ for a supported pair $up$ and $y_u=0$
otherwise, and independently choose covectors $\alpha_u$ with
$\alpha_u(y_u)=0$.  Contracting (1) at every site except $p$ kills every
source matching at the endpoint paired to $p$.  Consequently

\[
 \sum_{c=0}^2\left(\prod_{u\ne p}\alpha_u(e_c)\right)e_c=0. \tag{3a}
\]

If no $y_u$ were proportional to a fixed $e_c$, then each plane
$y_u^\perp$ would contain a covector nonzero on $e_c$.  Independent choices
of those covectors would make the $c$-component of (3a) nonzero.  Thus every
centre and colour has an incoming exact-coordinate anchor.

If $w$ is the unique such anchor for $(p,c)$, leave both $p,w$ uncontracted
and annihilate $y_u$ only for $u\notin\{p,w\}$.  The identical matching
argument gives

\[
 \operatorname {diag}(t_0,t_1,t_2)
   =h(\alpha)x_{p|w}x_{w|p}^{\mathsf T},\qquad
 t_r=\prod_{u\notin\{p,w\}}\alpha_u(e_r).                \tag{3b}
\]

Uniqueness lets us choose all factors in $t_c$ nonzero.  The left side is
then a nonzero diagonal matrix of rank at most one, hence a multiple of
$E_{cc}$.  Equality of the two nonzero rank-one matrices forces both
$x_{p|w}$ and $x_{w|p}$ to be proportional to $e_c$.  We have proved:

1. for every centre $p$ and colour $c$, some $u\ne p$ has
   $S_{u|p}=\{c\}$;
2. if this $u$ is unique, then also $S_{p|u}=\{c\}$.

Equation (1) gives two more immediate conditions:

3. every pure word $c^6$ has at least one compatible perfect matching;
4. every mixed word has either zero or at least two compatible perfect
   matchings.

Condition 4 is valid over arbitrary complex weights: if a mixed fibre had
one matching $P$, its coefficient would be the single nonzero number
$z_a(P)$, and so could not vanish.  It makes no termwise inference about a
fibre containing two or more matchings.

## 3. A nested binomial--trinomial obstruction

For two distinct perfect matchings $P,Q$, let

\[
 C(P,Q)=\{u:P(u)=Q(u)\}.                                  \tag{4}
\]

On six vertices, $C(P,Q)$ is the pair of endpoints of their common edge.

**Lemma 3.1.** Suppose mixed word $a$ has exactly the compatible
matchings $P,Q$, while mixed word $a'$ has exactly $P,Q,R$.  If

\[
                  \{u:a_u\ne a'_u\}\subseteq C(P,Q),     \tag{5}
\]

then (1) is impossible.

**Proof.** In the ratio $z_a(P)/z_a(Q)$, the common edge cancels.  At
all other vertices the colours in $a$ and $a'$ agree, so

\[
                    {z_a(P)\over z_a(Q)}
                  ={z_{a'}(P)\over z_{a'}(Q)}.            \tag{6}
\]

The binomial mixed equation at $a$ makes the first ratio $-1$.  Hence
the $P,Q$ terms cancel in the $a'$-equation, leaving the nonzero term
$z_{a'}(R)$, a contradiction. □

## 4. A Laurent rectangle obstruction

Introduce one formal variable $X_{u|v,c}$ for every directed half-edge
coordinate and put

\[
 d_a(P,Q)=\exp z_a(P)-\exp z_a(Q)\in\mathbb Z^{90}.       \tag{7}
\]

Only ratios of compatible monomials are used, so every variable which is
divided by is nonzero.

**Lemma 4.1.** Let $P,Q,R$ be distinct perfect matchings.  Suppose a
mixed target word $t$ has exactly the compatible matchings $P,Q,R$,
and each of three mixed words $b,d,e$ has exactly $P,Q$.  If

\[
              d_t(P,Q)+d_e(P,Q)=d_b(P,Q)+d_d(P,Q),       \tag{8}
\]

then (1) is impossible.

**Proof.** Rank-one factorization makes

\[
 \rho(a)={z_a(P)\over z_a(Q)}
         =\prod_{u=0}^5
           {x_{u|P(u)}(a_u)\over x_{u|Q(u)}(a_u)}.        \tag{9}
\]

Thus (8) is the exact Laurent identity
$\rho(t)\rho(e)=\rho(b)\rho(d)$.  The three binomial mixed
equations give $\rho(b)=\rho(d)=\rho(e)=-1$, hence
$\rho(t)=-1$.  The $P,Q$ terms in the target trinomial cancel and
leave $z_t(R)\ne0$, again a contradiction. □

Repeated choices among $b,d,e$ are allowed; the same calculation still
holds.  The word $t$ is necessarily different from them because its
compatible fibre has a different cardinality.

## 5. Checkable finite reduction

`computations/search_rankone_anchor_fibre_cegar.py` encodes exactly the four
necessary conditions of Section 2.  There is one symmetric presence bit for
each of the fifteen pairs, independent three-bit coordinate masks at its two
endpoints, exact-coordinate singleton bits, and compatibility bits for all
fifteen perfect matchings in all $3^6$ words.  A supported pair is forced
nonempty at both endpoints and an absent pair empty at both; no symmetry is
imposed between its two endpoint masks.  The base relaxation has 11,130
variables and 88,026 clauses.

Whenever a satisfying mask contains a Lemma 3.1 or Lemma 4.1 witness, the
search adds the single clause excluding precisely that conjunction of exact
fibre supports.  This is a semantic CEGAR step: the clause need not follow
from the Boolean base theory, but it follows from the complex coefficient
equations by the displayed lemma.

`computations/certify_rankone_anchor_fibre_cegar.py` records every witness in
JSON.  Its replay mode reconstructs rather than trusts every blocking clause,
checks (6) or the full 90-coordinate equality (8), checks the final DIMACS
hash, and resolves the augmented formula.  It can additionally emit a
standard DRUP trace using Glucose or Lingeling.  The terminating UNSAT run
below is therefore a finite exact certificate for the arbitrary-support
rank-one six-site shadow; by contrast, any intermediate SAT assignment is
only a support-mask candidate and is not claimed to satisfy the coefficient
equations.

The deterministic discovery run terminates after 828 refinements.  An
assumption core retains 789 of them (584 nested and 205 rectangle clauses),
giving an 88,815-clause DIMACS instance with SHA-256
`4b5b2977536b7db3856c426e6b87c069aeb56f88bc3b083ea76598d6b4c1582f`.
Glucose emitted a proof with 861,358 additions.  The independent upstream
`drat-trim` checker reports `VERIFIED`, with 83,443 input clauses and 692,618
proof lemmas in its backward core, 100,002,188 resolution steps, and zero RAT
lemmas.  Thus the trace is in fact a pure RUP certificate.

## 6. The nine-orbit finite lemma

Number the fifteen perfect matchings in the recursive order used by the
checker:

| index | matching | index | matching | index | matching |
|---:|---|---:|---|---:|---|
| 0 | `01|23|45` | 5 | `02|15|34` | 10 | `04|13|25` |
| 1 | `01|24|35` | 6 | `03|12|45` | 11 | `04|15|23` |
| 2 | `01|25|34` | 7 | `03|14|25` | 12 | `05|12|34` |
| 3 | `02|13|45` | 8 | `03|15|24` | 13 | `05|13|24` |
| 4 | `02|14|35` | 9 | `04|12|35` | 14 | `05|14|23` |

The following are the seven nested representatives.  The entries mean that
the first word has exactly the displayed pair and the second word exactly
the displayed triple.

| binomial word | pair | trinomial word | triple |
|---|---|---|---|
| `000001` | `0,1` | `010001` | `0,1,8` |
| `000011` | `1,2` | `010011` | `1,2,4` |
| `000011` | `1,2` | `110011` | `1,2,11` |
| `000011` | `1,4` | `000010` | `1,4,7` |
| `000011` | `1,4` | `000010` | `1,4,13` |
| `000012` | `1,2` | `010012` | `1,2,4` |
| `000012` | `1,4` | `000010` | `1,4,13` |

The two rectangle representatives are:

| target word/triple | distinguished pair | binomial words `(b,d,e)` |
|---|---|---|
| `000001 / 0,1,3` | `1,3` | `000100`, `001001`, `001100` |
| `000001 / 0,1,3` | `1,3` | `000101`, `001000`, `001100` |

In the rectangle rows the target triple contains the distinguished pair,
and the three listed words have exactly that pair.  Direct substitution in
(7) checks (8).

**Lemma 6.1 (finite shadow lemma).** Every collection of arbitrary
asymmetric endpoint masks on an arbitrary simple support graph on six sites
which satisfies the four necessary conditions of Section 2 realizes, after
a permutation of the six sites and one simultaneous permutation of the
three colours, at least one of the nine patterns in the two tables.

**Exact certificate.** The base CNF has 11,130 variables and 88,026 clauses.
For each table row the verifier generates all $6!3!$ relabelings, audits
the nested ratio identity or all ninety coordinates of the rectangle
identity, and removes duplicate clauses.  The nine clause-orbit sizes are

\[
 (4320,4320,1080,4320,4320,4320,4320,4320,4320),
\]

with 35,640 distinct clauses in total.  The resulting 123,666-clause CNF is
UNSAT.  This is checked directly by
`computations/verify_rankone_anchor_fibre_orbits.py`; its optional output is
a DIMACS file and a deletion-free DRUP trace, each proof addition of which is
checked by `computations/verify_drup_certificate.py`.  Since a blocker clause
is precisely the negation of one exact table pattern, UNSAT is equivalent to
the assertion of the lemma.  No arithmetic over a finite field and no
floating-point computation occurs.

The emitted orbit DIMACS has SHA-256
`dae187d355193735c93058954cb0723b7ef3798c5935f777ed513e8e1e8df634`.
Its 1,166,186-addition deletion-free DRUP trace has SHA-256
`0da0eb641968a56d0b6ba56854fcd0f91640efb5a5c7ba2f38c3ad13ba99abfe`
and ends in the empty clause.  The independent upstream `drat-trim` audit
reports `VERIFIED`: its backward core uses 88,169 input clauses and 934,397
proof lemmas, with 131,621,172 resolution steps and zero RAT lemmas.
Independently, the repository's streaming checker reconstructs the base CNF
and reports

```text
PASS deletion-free DRUP: variables=11130 cnf_clauses=123666 proof_additions=1166186
```

## 7. Exclusion of every rank-one six-site aggregate chart

**Theorem 7.1.** Let $A_{uv}$ be arbitrary complex $3\times3$
aggregate blocks on six sites, each of rank at most one.  Blocks may vanish,
and the rank-one factors at the two ends may have unrelated zero patterns.
Then

\[
                            H_6(A)\ne\Delta_{6,3}.        \tag{10}
\]

**Proof.** Suppose equality held.  Factor every nonzero block and form the
endpoint masks (2); omit the zero blocks.  The one-centre contraction and
unique-anchor equality case give conditions 1 and 2 of Section 2.  The pure
and mixed coefficients of the assumed tensor equality give conditions 3
and 4.  Lemma 6.1 therefore supplies one of the seven nested or two rectangle
patterns.  Lemma 3.1 or Lemma 4.1, respectively, contradicts the same tensor
equality. □

This theorem strictly removes the all-pair-Hessian-rigidity hypothesis from
the rank-one conclusion in `rank-one-complete-six-chart-obstruction.md`.
It still concerns aggregate blocks: parallel decorated source edges on one
pair have already been summed into $A_{uv}$, and the theorem applies when
that sum has rank at most one.
