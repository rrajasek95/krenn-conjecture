# The all-singleton diagonal N=8 branch is already closed by recurrence

## Verdict

No new occurrence CNF is needed to close the proof branch.  The existing
characteristic-free diagonal hafnian recurrence theorem excludes a strictly
larger class: every exact diagonal three-colour source at eight sites, with
arbitrary field weights, arbitrary cancellation, and any number of diagonal
colours on a physical edge.

Therefore it excludes in particular the proposed chart in which

1. every live physical edge carries exactly one diagonal colour;
2. the target edge `01` is live only in colour zero;
3. all three pure rows have support; and
4. no mixed row has occurrence multiplicity one.

The interface checker is
`computations/verify_n8_all_singleton_diagonal_recurrence_interface.py`.  It
pins and runs
`computations/verify_diagonal_recurrence_obstruction.py --n 8` and verifies
the coefficient factorization independently on all 6,561 words.

## Exact embedding of the singleton chart

Write the singleton support as a partial edge-colouring `sigma` and attach a
nonzero weight `x_uv` to each live edge.  Define three symmetric scalar edge
matrices by

\[
 A_c[u,v]=
 \begin{cases}
 x_{uv},&\sigma(uv)=c,\\
 0,&\text{otherwise}.
 \end{cases}                                               \tag{1}
\]

This is literally a specialization of the arbitrary diagonal model used by
the recurrence theorem.  The target condition says only

\[
 A_0[0,1]\ne0,\qquad A_1[0,1]=A_2[0,1]=0,                 \tag{2}
\]

and hence restricts that model further.

For a word `w` let `S_c=w^{-1}(c)`.  A diagonal matching term can pair only
vertices with the same word colour.  Union and restriction of perfect
matchings give a coefficient-one bijection

\[
 \{M\text{ compatible with }w\}
 \longleftrightarrow
 \operatorname{PM}(S_0)\times
 \operatorname{PM}(S_1)\times
 \operatorname{PM}(S_2).
\]

Consequently the exact coefficient identity is

\[
 [X^w]H_A=\prod_{c=0}^2\operatorname{haf}A_c[S_c].         \tag{3}
\]

The checker reconstructs both sides as labelled monomial multisets for all
`3^8=6561` words.  There are 1,641 words with all colour classes even: three
pure words and 1,638 proper even ordered partitions.

## Why the recurrence hypotheses follow

For an exact GHZ source, the three pure coefficients are normalized to one,
so

\[
                   \operatorname{haf}A_c[V]=1\ne0.         \tag{4}
\]

Every proper even partition is a mixed word and has target coefficient zero.
Equation (3) therefore gives

\[
 \operatorname{haf}A_0[S_0]
 \operatorname{haf}A_1[S_1]
 \operatorname{haf}A_2[S_2]=0.                            \tag{5}
\]

Equations (4)--(5) are exactly the hypotheses of
`proofs/diagonal-hafnian-recurrence-obstruction.md`.  Its N=8 checker has
2,988 variables and 23,844 base clauses.  Exhaustive matching-symmetry
reduction gives nine branches, all UNSAT.

The proof is characteristic-free.  It does not assume positivity, generic
weights, or absence of cancellation.

## Relation to the proposed occurrence CNF

The pure-support and no-mixed-singleton conditions are necessary occurrence
shadows of an exact singleton-weight source.  In particular, a mixed row
with exactly one supported monomial cannot vanish because that monomial is a
product of nonzero live weights.

They are not, however, the full coefficient equations.  A relaxed occurrence
CNF could in principle be SAT and still have no field-valued exact lift.  The
recurrence theorem closes precisely the proof-relevant coefficient branch,
so proving the Boolean shadow UNSAT would be duplicative and unnecessarily
strong.  No claim about standalone occurrence-CNF satisfiability is made
here.

## Scope

This closes every all-singleton diagonal support at N=8, including the fixed
target-colour-zero chart, and indeed all arbitrary diagonal N=8 supports.
It does not constrain a genuinely bicoloured source with nonzero
`A_uv[a,b]`, `a != b`; those off-axis cells are exactly why the general
Krenn problem remains outside the diagonal recurrence theorem.

## Reproduction

```text
python3 computations/verify_n8_all_singleton_diagonal_recurrence_interface.py --mode structural
python3 -O computations/verify_n8_all_singleton_diagonal_recurrence_interface.py --mode full
python3 -I -S computations/verify_n8_all_singleton_diagonal_recurrence_interface.py --mode exhaustive
```

The wrapper invokes the pinned PySAT/CaDiCaL recurrence checker through the
repository's audited `.venv` and returns one mode-independent ledger.
