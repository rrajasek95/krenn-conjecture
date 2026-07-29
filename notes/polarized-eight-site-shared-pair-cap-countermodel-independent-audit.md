# Independent audit of the eight-site shared pair-cap countermodel

## 1. Verdict

This is a clean-room audit of
[polarized-eight-site-shared-pair-cap-countermodel.md](polarized-eight-site-shared-pair-cap-countermodel.md).
The corrected primary snapshot is sound.

Over \(\mathbb Q\), its twelve-cell quadratic \(q\), two-cell product
\(ps\), and quadratic

\[
                             z=\tfrac14q+4ps            \tag{A1}
\]

satisfy exactly

\[
                             zq^{[3]}=\Delta_{8,3}.      \tag{A2}
\]

The independent checker verifies every one of the \(3^8=6561\) ternary
coefficients using sparse multiplication in the site-square-zero algebra,
not the primary distinguished-matching routine.

The full-nine fixed-\(q\) obstruction is also correct.  The displayed
site and colour maps identify the twelve decorated cells and both mixed
fourth-power words with the already registered Laurent border core in
[n8-border-pair-suspension-obstruction.md](n8-border-pair-suspension-obstruction.md).
Thus that obstruction is not a new route.

During this audit, equations (28)--(29) initially had a factor-four error
relative to the literal ten-site decomposition (26).  The primary artifact
was corrected before this verdict: its polarized overlap equation now has
target \(4\delta X\), while its raw matching equation has target
\(\delta X\).  The corrected equations (27)--(29) are exact.

The standalone clean-room checker is
[audit_polarized_eight_site_shared_pair_cap_countermodel_independent.py](../computations/audit_polarized_eight_site_shared_pair_cap_countermodel_independent.py).
It imports neither the primary checker nor any registered-border code.

## 2. Independent square-zero reconstruction

Represent a monomial by a word in

\[
                         \{0,1,2,\mathord\cdot\}^8,     \tag{A3}
\]

where a dot denotes an unoccupied site.  The product of two words is zero
if both occupy one site and otherwise is their disjoint union.  This
implements the tensor product
\(\bigotimes_u(\mathbb Q\oplus V_u)\) literally.

Insert the twelve unit cells on

\[
\begin{aligned}
P_0&=01\mid23\mid45\mid67,\\
P_1&=07\mid12\mid34\mid56,\\
P_2&=04\mid17\mid26\mid35.                             \tag{A4}
\end{aligned}
\]

The cells have twelve distinct physical edges.  Four repeated
multiplications give

\[
 q^{[4]}=\frac{q^4}{4!}
   =X_0+X_1+X_2+e_{21122200}+e_{22002112}.              \tag{A5}
\]

Every coefficient in \(q^4\) is \(24\), so the divided-power coefficients
in (A5) are exactly one.  No other word survives.  The three repeated
multiplications similarly produce \(42\) six-site words and verify
coefficientwise that

\[
 q^{[3]}=\frac{q^3}{3!},\qquad q^3=6q^{[3]}.            \tag{A6}
\]

This reconstruction uses algebra multiplication rather than a
precomputed list of the \(105\) perfect matchings.

## 3. The global product \(ps\) and the polarized identity

At the four active color-two modes, the row coefficient pairs are

\[
(p_u,s_u)=
(1,1),\ (1,-1),\ (-1/8,-1/8),\ (-1/8,1/8)
\quad (u=0,2,4,6).                                     \tag{A7}
\]

Multiplying the two complete linear forms automatically retains both
endpoint orders.  The resulting quadratic has exactly

\[
 (ps)_{04}(2,2)=-\tfrac14,\qquad
 (ps)_{26}(2,2)=\tfrac14,                              \tag{A8}
\]

and zero on every other physical and colour cell.  In particular, the
four cross-pair Gram entries vanish by exact rational cancellation; they
were not omitted by a support assumption.

The independently reconstructed cofactors have the following top-degree
extensions:

\[
\begin{aligned}
e_2^{(0)}e_2^{(4)}F_{04}
  &=e_{21122200}+e_{22002112}+X_2,\\
e_2^{(2)}e_2^{(6)}F_{26}
  &=X_2.                                                \tag{A9}
\end{aligned}
\]

Therefore direct multiplication gives

\[
 psq^{[3]}=-\tfrac14e_{21122200}
             -\tfrac14e_{22002112}.                    \tag{A10}
\]

The sparse checker also verifies the distinguished-edge identity

\[
                         qq^{[3]}=4q^{[4]}              \tag{A11}
\]

coefficientwise.  Combining (A1), (A5), and (A10) gives (A2).
Finally, the checker loops over all \(6561\) full ternary words, finding
coefficient one on \(0^8,1^8,2^8\) and zero on the other \(6558\).

The factorials are therefore:

\[
 q^3=3!\,q^{[3]},\qquad q^4=4!\,q^{[4]},\qquad
 qq^{[3]}=4q^{[4]}.                                    \tag{A12}
\]

Since \(z\) is distinguished, \(zq^3/3!=zq^{[3]}\); there is no additional
factor of four in (A2).

## 4. Exact border-core isomorphism and the full-nine obstruction

Let

\[
\sigma=(3,0,1,5,6,7,4,2),\qquad
\tau=(1,2,0)                                            \tag{A13}
\]

be respectively the site map and colour map from the present model to the
registered border core.  Applying them cell by cell sends

\[
P_0\longmapsto
 03\mid15\mid24\mid67,\quad
P_1\longmapsto
 01\mid23\mid47\mid56,\quad
P_2\longmapsto
 02\mid14\mid36\mid57,                                 \tag{A14}
\]

with image colours \(1,2,0\), respectively.  These are exactly the three
rows of the registered core.  The mixed words map as

\[
 21122200\longmapsto22101000,\qquad
 22002112\longmapsto01002102,                          \tag{A15}
\]

which are exactly its two registered mixed words.  Thus the isomorphism
holds at the decorated-cell and matching-tensor levels, not merely for the
underlying uncoloured graph.

For completeness, the independent checker reconstructs the entire linear
map

\[
                         R\longmapsto Rq^{[3]}.         \tag{A16}
\]

It obtains \(363\) nonzero output rows.  Exactly \(358\) are singleton
rows of coefficient one, and their distinguished columns are exactly the
\(240\) cells outside the twelve-cell core.  Restriction to the twelve
active cells leaves precisely the five words in (A5), each with a
four-cell incidence row; those rows have exact rational rank five.  The
twelve allowed port pairs form a perfect matching on all \(24\)
site-colour ports.

These counts reproduce the registered pair-suspension input independently.
The remaining common-rank-one-line argument is sound, including zero and
pure mode points:

* a nonzero active block has two nonzero endpoint points;
* if two active physical edges are disjoint, their four cross blocks are
  inactive and hence zero;
* if they meet, the three cross blocks on distinct sites are inactive and
  zero; and
* the zero-pair classification then makes every nonzero active value
  proportional to one common rank-one matrix.

The three pure target equations require differences proportional to
\(E_{00}-E_{11}\), which has rank two, giving the contradiction.

The registered theorem uses the raw physical normalization

\[
                    A Q+P S F=\delta X,                \tag{A17}
\]

where \(Q=q^{[4]}\) and \(F=q^{[3]}\).  The primary note uses

\[
                    C Q+p s F=\tfrac14\delta X.        \tag{A18}
\]

Besides the site-colour relabeling, these systems are equivalent under the
uniform parameter scaling

\[
                         A=4C,\qquad P=4p,\qquad S=s.   \tag{A19}
\]

Thus Proposition 5.1 is genuinely the registered fixed-core obstruction
in normalized coordinates.  Its mathematical content is not novel; the
new construction is the isolated aggregate solution (A1)--(A2).

## 5. Overlapping-pair formulas

For the literal ten-site decomposition

\[
 h=q+\sum_i e_i^{(r)}p_i+\sum_j e_j^{(t)}s_j
          +\sum_{i,j}a_{ij}e_i^{(r)}e_j^{(t)},          \tag{A20}
\]

delete \(r,0\).  Sorting every one of the \(45\cdot9=405\) possible
decorated ten-site cells by its role in the new decomposition gives:

\[
\begin{array}{c|r}
\text{new role}&\text{number of scalar cells}\\ \hline
\text{old--old internal on }1,\ldots,7&21\cdot9\\
\text{\(t\)--old internal}&7\cdot9\\
\text{direct \(r0\) block}&9\\
\text{\(r\)-star to \(t\)}&9\\
\text{\(r\)-star to old sites}&7\cdot9\\
\text{\(0\)-star to \(t\)}&9\\
\text{\(0\)-star to old sites}&7\cdot9.
\end{array}                                             \tag{A21}
\]

Reading the original coefficient attached to each class gives exactly

\[
\begin{aligned}
q^{(0)}
 &=q|_{\{1,\ldots,7\}}
   +\sum_{v=1}^7\sum_{j,\beta}
      s_{j,v,\beta}e_j^{(t)}e_\beta^{(v)},\\
b_{i\alpha}&=p_{i,0,\alpha},\\
\widetilde p_i
 &=\sum_j a_{ij}e_j^{(t)}
   +\sum_{v=1}^7\sum_\beta p_{i,v,\beta}e_\beta^{(v)},\\
\widetilde s_\alpha
 &=\sum_j s_{j,0,\alpha}e_j^{(t)}
   +\sum_{v=1}^7
      \bigl(e_\alpha^{(0)*}\mathbin{\lrcorner}q_{0v}\bigr).
                                                               \tag{A22}
\end{aligned}
\]

This verifies (27), including endpoint order in the last contraction.

A perfect matching with the removed colours \(i,\alpha\) either uses the
direct \(r0\) cell or uses one edge from each new star.  Hence its raw
coefficient equation is

\[
 b_{i\alpha}(q^{(0)})^{[4]}
 +\widetilde p_i\widetilde s_\alpha(q^{(0)})^{[3]}
 =\delta_{i\alpha}X_i^{U'_0}.                          \tag{A23}
\]

Since
\(q^{(0)}(q^{(0)})^{[3]}=4(q^{(0)})^{[4]}\), multiplying (A23) by four
gives

\[
 (b_{i\alpha}q^{(0)}
   +4\widetilde p_i\widetilde s_\alpha)(q^{(0)})^{[3]}
 =4\delta_{i\alpha}X_i^{U'_0}.                         \tag{A24}
\]

These are precisely the corrected equations (29) and (28).  The checker
audits the factors as polarized/raw \(=(4,1)\).

## 6. Novelty and scope

The result has a sharp but narrow consequence:

* it disproves any proposed obstruction based only on one isolated
  equation \(zq^{[3]}=\Delta_{8,3}\), even after retaining the literal
  factorization \(z=aq+4ps\);
* it does not provide a Krenn counterexample, because
  \(q^{[4]}\ne\Delta_{8,3}\);
* it does not provide a ten-site source, because the same \(q\) fails the
  full nine shared-row equations;
* it does not show that an arbitrary \(q\) fails those nine equations;
* the full-nine obstruction is the registered border-core theorem after
  relabeling and normalization; and
* formulas (27)--(29) are an exact compatibility filter for a hypothetical
  survivor, not an existence result or an obstruction theorem.

With those qualifications, the primary note makes no remaining novelty or
scope overclaim.
