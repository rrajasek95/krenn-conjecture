# Coordinate-monomial obstruction for the five-hole response

## 1. Outcome

The common-annihilator specialization of the union-five full row asks for
an identity

\[
 \Delta_{5,3}=[X\,Y\,D\,Q]_{1^5}.                    \tag{1}
\]

Here `X,Y,D` are three site-graded linear families and `Q` is an arbitrary
site-graded quadratic.  This note excludes the boundary on which, at every
site, the three local vectors `x_i,y_i,d_i` occupy three distinct target
coordinate lines.  Arbitrary nonzero scalings and independent permutations
of the three lines are allowed at all five sites.

The obstruction is support-sensitive but cancellation-aware.  After local
normalization, the response in (1) is a 90-dimensional linear space.  Its
coefficients with colour multiplicities `(3,1,1)` occur in forced equal
pairs.  For each fixed `(2,2,1)` colour type, its coefficient vectors form
a directed-cut code of minimum support four.  A locally permuted diagonal
rank-three tensor has only three nonzero words, pairwise at Hamming distance
five, and violates one of these two conclusions (or has a nonsurjective word,
which the response cannot contain at all).

This is not yet the general union-five exclusion.  It does not cover a site
where `x_i,y_i,d_i` fail to span, nor a nonmonomial basis.  Its role is to
close the fully coordinate allocation boundary and isolate the genuinely
mixed local-basis case.

That qualification is sharp: an exact rational mixed-basis factorization is
given in
[`five-hole-factorization-counterexample.md`](five-hole-factorization-counterexample.md).
It has invertible local triples and the exceptional `011166` witness masks.

## 2. The normalized response space

Let the species labels `0,1,2` denote `X,Y,D`.  Normalize the three local
vectors to these coordinate vectors independently at every site.  For an
edge `ab`, a coefficient of `Q_ab` is multiplied by the sum over all six
bijections from the three species to the complementary three sites.  Thus a
basis word occurs only if it contains all three species.

The remaining words have two possible multiplicity types.

* For a word of type `(3,1,1)`, let `a` be its tripled species and let
  `i,j,k` be the three `a`-sites.  Its coefficient is
  \[
              q_{ij}^{aa}+q_{ik}^{aa}+q_{jk}^{aa}.      \tag{2}
  \]
  In particular it is unchanged when the two singleton species are swapped
  at their two sites.
* For a word of type `(2,2,1)`, fix the singleton site `k`, let `A` be the
  two sites carrying species `a`, and let `B` be the two sites carrying
  species `b`.  Its coefficient is
  \[
                         C(k;A,B)=\sum_{i\in A,j\in B}z_{ij},          \tag{3}
  \]
  where the twenty variables `z_ij` are the directed `ab` entries of `Q`.

The diagonal variables in (2) give three independent ten-dimensional
triangle-sum blocks.  The three unordered pairs of distinct species give
three independent twenty-dimensional copies of (3).  Hence the normalized
response space has dimension

\[
                         3\cdot10+3\cdot20=90.          \tag{4}
\]

The exact checker reconstructs the full `243 by 90` coefficient matrix and
verifies (2)--(4), rather than assuming this decomposition from a support
picture.

## 3. The directed-cut support lemma

**Lemma 3.1.**  Over a characteristic-zero field, a nonzero coefficient
vector `(C(k;A,B))` in (3) has at least four nonzero entries.

**Exact finite proof.**  Order the thirty triples `(k,A,B)` and the twenty
directed edges of `K_5`, and form their `30 by 20` zero-one incidence matrix
`M`.  For every choice of three omitted rows, the remaining `27 by 20`
matrix has rank twenty modulo `1,000,003`.  Its rank over the rationals is
therefore also twenty.  If `Mz` had support at most three, pad that support
to three rows and delete them.  The retained full-rank matrix would force
`z=0`.

The bound is exact.  An integral `+/-1` weighting of all twenty directed
edges, listed in the checker, has precisely four nonzero cut sums, with
values `(-4,-4,4,4)`. `QED`

There are only `C(30,3)=4060` rank checks.  Each is ordinary deterministic
finite-field elimination; a full modular column rank is itself a
characteristic-zero nonvanishing-minor certificate.

## 4. Exclusion of every local monomial allocation

Let the local species-to-target permutation at site `i` be `pi_i`.  After
the normalization above, the three target summands in `Delta_(5,3)` become

\[
                 \lambda_r e_{w_r},\qquad
 (w_r)_i=\pi_i^{-1}(r),\qquad \lambda_r\ne0.            \tag{5}
\]

At every site the three entries `(w_0)_i,(w_1)_i,(w_2)_i` are distinct.
Consequently the three words in (5) disagree at all five sites.

If some `w_r` omits a species, its coefficient must be zero in the response,
contrary to `lambda_r!=0`.  Suppose instead that `w_r` has multiplicity
type `(3,1,1)`.  Swapping its singleton species produces a word agreeing
with `w_r` at the other three sites.  It cannot be either of the other target
words, since those disagree with `w_r` everywhere.  Formula (2) equates its
zero coefficient to `lambda_r`, again a contradiction.

The only remaining possibility is that all three target words have type
`(2,2,1)`.  In each fixed species-multiplicity block the target has between
one and three nonzero coefficients, because it has only three nonzero words
in total.  Lemma 3.1 says that a nonzero response block has support at least
four.  This is the final contradiction.

For redundancy, the checker enumerates all `6^5=7776` local permutation
systems.  It separates them as

\[
 5316\text{ nonsurjective},\qquad
 1560\text{ with a }(3,1,1)\text{ word},\qquad
 900\text{ wholly }(2,2,1),                            \tag{6}
\]

and applies the corresponding exact obstruction above.

## 5. Exact audit

Run

```text
.venv/bin/python computations/verify_five_hole_monomial_factor_obstruction.py
```

The script reconstructs all response rows, checks the 90-dimensional block
decomposition, verifies all 4,060 rank certificates for the directed-cut
minimum distance, audits the sharp four-support example, and exhausts (6).
