# Independent audit of the sole-defect distinct-lift obstruction

## 1. Verdict

The power-only theorem in
[the primary note](sole-defect-distinct-lift-common-power-obstruction.md) is
correct.  A clean-room reconstruction found the same three local matroids,
the same \(13+26+13=52\) orbit count, the same \(qF\)-rank ranges, and a unit
unsaturated ideal over \(\mathbb Q\) in every orbit.  The computation retains
all coordinates of \(q\); it does not make a support, nonvanishing, rank, or
generic-chart assumption.

The only delicate premise check in the field-selection corollary is handled
explicitly in the frozen primary.  If the bad-site selector kills a field
whose selected pair contains the bad site, that selected lift does not contain
the killed local vector.  Before applying the theorem, the zero image is
replaced by an arbitrary nonzero dummy vector.  This does not change the
selected lift, and it also handles the case in which all three selected pairs
contain the bad site.  The selector simulation in the independent checker
tests this point explicitly.

This audit was made against these frozen SHA-256 identities:

~~~text
d6429ece3ddaf7dc9337894ba32fdca92a6620636fe7293cb86eb2829010f620  notes/sole-defect-distinct-lift-common-power-obstruction.md
f0a5dafc1b7a48572ea8b82771969a1c40e1bf02885c8e04c0e7a31c1677f6c6  computations/verify_sole_defect_distinct_common_power.py
0c621375a6379a8760dc297003fed2aa53ec9bca78694c8bf359ee816688891e  computations/audit_sole_defect_distinct_common_power_independent.py
~~~

## 2. Reconstruction of the reduction

A sitewise linear projection extends to a unital endomorphism of the
site-square-zero algebra.  Projecting the five good sites onto their three
independent field axes and the bad site onto the field span fixes every target
lift and commutes with bracket powers.  The reduced dimensions are therefore
\((2,3,3,3,3,3)\) or \((1,3,3,3,3,3)\).

Three nonzero vectors of rank at most two have exactly the following
projective matroids: three distinct lines in a plane, one coincident pair in a
plane, or one common line.  Individual field rescalings and a bad-site linear
automorphism give the three rational models used in the primary proof.
Every target lift occupies at least three good sites, so its coefficient can
be normalized independently on one occupied good axis.  No root extraction
or bad-site scaling is needed.

The independent orbit construction begins with all 455 unordered triples of
distinct physical pairs.  It canonicalizes by taking the **maximal** image
under the \(S_5\) good-site action.  For the circuit and rank-one matroids it
also quotients by all field permutations, giving 13 orbits.  For the
coincident matroid it keeps field one distinguished and only swaps the equal
fields zero and two, giving 26 orbits among 1,365 labelled objects.

The necessary linear equation is exact:

\[
 q^{[2]}=F,\quad q^{[3]}=0
 \quad\Longrightarrow\quad qF=0,
\]

because \(q q^{[2]}=3q^{[3]}\).  Literal multiplication shows that only a
\(q\)-block on the missing pair of a lift can survive, but equal six-site
coordinate words must still be collected across fields.  Exact row reduction
then gives ranks

\[
\begin{array}{c|c|c}
\text{matroid}&\operatorname{rank}(qF)&\dim\ker(qF)\\ \hline
\text{circuit/coincident}&18,21,24,27&102,99,96,93\\
\text{rank one}&9,15,21,27&96,90,84,78.
\end{array}
\]

Substituting a complete kernel parametrization into every literal
four-site coefficient of \(q^{[2]}-F\) gives an affine, unsaturated ideal.
A unit ideal over \(\mathbb Q\) remains a unit ideal after extension to
\(\mathbb C\).

## 3. Clean-room calculation

The
[independent checker](../computations/audit_sole_defect_distinct_common_power_independent.py)
does not import the primary checker or any primary ledger.  Its construction
differs in all of the following ways:

* maximal rather than minimal orbit representatives;
* alternative rational coordinates
  \((1,1),(1,-1),(0,1)\),
  \((1,1),(1,-1),(1,1)\), and
  \((-2),(3),(5)\) at the bad site;
* reversed good axes, pair endpoints, cells, target terms, matchings, and
  coefficient equations;
* rightmost-pivot exact RREF instead of leftmost-pivot elimination;
* sparse monomial dictionaries and reversed variable order with Singular's
  `Dp` order rather than the primary polynomial strings and `dp` order.

It reconstructs all 120 or 105 endpoint-ordered \(q\)-coordinates and all
945 or 675 possible four-site coordinate words.  Singular 4.4.1 returned the
unit ideal in all 52 cases.  The independent combined ledger hashes are

| bad-site matroid | independent combined SHA-256 |
|---|---|
| circuit | `44030a6c1e715cef391076c048fcb95999048cb27b1e8433acb3a753f5beffbd` |
| coincident pair | `73931e0cd9b20455fc5a54d4bbf95e459ec847216596f6709620801a8e10f211` |
| rank one | `0706158f1d5883a2e0a75e32a34ac32765e27f5d0a13ee1924e36d44cd87f5d0` |

Run

    uv run python computations/audit_sole_defect_distinct_common_power_independent.py

for the full replay, or add `--ledger-only` to rebuild every exact stream
without invoking Singular.

## 4. Field-selection corollary

Let \(P_r\) be distinct active representatives and
\(K=\{r:o\in P_r\}\).  At each good site, kill the \(r\)-axis precisely when
that site lies in \(P_r\).  A candidate \(r\)-lift survives the good selectors
exactly when it contains the good part of \(P_r\) in its missing pair.

* If \(o\notin P_r\), the good part already has size two, so only \(P_r\)
  survives and the bad-site image must be nonzero.
* If \(o\in P_r\), the selected good part has size one.  Other pairs through
  that good site are nonincident at \(o\), so killing \(a_r^{(o)}\) eliminates
  them; the selected incident pair omits \(o\) and survives.

Thus the selected multiplier contains exactly the three chosen distinct
lifts.  At a good site, every killed \(r\)-axis is omitted by the selected
\(r\)-lift; restore its original axis as an unused declared field vector, which
also restores the independent good frame.  At the bad site, replace every
killed unused image by any nonzero dummy before invoking the theorem.  These
replacements change neither the multiplier nor either power equation.  The
local separability tables are therefore exactly

\[
\begin{array}{c|c}
\text{matroid}&\text{nonseparable }K\\ \hline
\text{circuit}&|K|=2\\
L_0=L_2\ne L_1&\{0\},\{2\},\{0,1\},\{1,2\}\\
\text{rank one}&\varnothing\ne K\ne\{0,1,2\}.
\end{array}
\]

This proves the corollary only for locally separable systems of distinct
representatives.  It does not assert that arbitrary active families possess
one, and it does not cover two or more deficient sites.
