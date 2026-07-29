# Independent closure of a full invisible endpoint-colour block

## 1. Result

Retain the sparse eight-site quadratics

\[
\begin{aligned}
q={}&23_{00}+45_{00}+67_{00}
     +01_{11}+36_{11}+57_{11}
     +02_{22}+14_{22}+56_{22},\\
z={}&01_{00}+24_{11}+37_{22}.
\end{aligned}                                                   \tag{1}
\]

For one physical pair \(uv\), let

\[
                    H_{uv}=\sum_{a,b=0}^2h_{ab}\,uv_{ab}, \tag{2}
\]

where the nine coefficients \(h_{ab}\in\mathbb C\) are completely
arbitrary, including zero.  If

\[
 uv\in\{03,04,05,06,07,12,13,15,17,25,34\},              \tag{3}
\]

then

\[
                       z(q+H_{uv})^{[3]}=\Delta_{8,3},    \tag{4}
\]

but there are no scalar \(a\) and linear forms \(p,s\) satisfying

\[
 \boxed{\quad
 (a(q+H_{uv})+4ps)(q+H_{uv})^{[3]}=\Delta_{8,3}.
 \quad}                                                    \tag{5}
\]

Thus every arbitrary \(3\times3\) block on any one of the eleven invisible
physical pairs is separated from the pair-cap variety.

The standalone checker is
[verify_polarized_eight_site_invisible_block_projective_frontier_independent.py](../computations/verify_polarized_eight_site_invisible_block_projective_frontier_independent.py).
It imports no primary computation.  It combines a support-only projective
proof on ten pairs and most of pair \(17\) with an independently generated
unsaturated characteristic-zero ideal for the remaining pair-\(17\)
frontier.

## 2. Why the whole block remains polarized

Every two cells in \(H_{uv}\) occupy the same two physical sites, so
\(H_{uv}^2=0\).  Each of the nine individual cells on every pair in (3)
also satisfies

\[
                         z\,uv_{ab}\,q^{[2]}=0.            \tag{6}
\]

The checker reconstructs (6) by all disjoint choices of one displayed
\(z\)-cell and two base-\(q\) cells.  Therefore

\[
\begin{aligned}
(q+H_{uv})^{[3]}&=q^{[3]}+H_{uv}q^{[2]},\\
z(q+H_{uv})^{[3]}&=zq^{[3]}=\Delta_{8,3},
\end{aligned}                                                   \tag{7}
\]

for arbitrary values of all nine coefficients.

## 3. Support-only coefficient logic

Fix a support mask \(M\subseteq\{0,1,2\}^2\), and require
\(h_{ab}\ne0\) exactly for \((a,b)\in M\).  There are \(2^9=512\) masks
on each physical pair.  Every concrete complex block belongs to exactly one
such stratum.

Put

\[
 F_H=(q+H)^{[3]},\qquad Q_H=(q+H)^{[4]}.
\]

A pair-cap solution would imply

\[
                       aQ_H+psF_H={1\over4}\Delta_{8,3}.  \tag{8}
\]

For every top word, the checker independently lists each literal
\(psF_H\) contributor together with either coefficient \(1\) or one active
parameter \(h_{ab}\).  It marks a mixed Gram entry zero only when:

1. the complete \(Q_H\)-support is absent on that word;
2. exactly one literal \(psF_H\) contributor occurs; and
3. its coefficient is \(1\) or one active, hence nonzero, \(h_{ab}\).

For a pure target word, the sum of its contributors equals \(1/4\), so at
least one literal summand is nonzero.  The checker branches on every
contributor.  In a branch, both endpoints of each selected Gram pair are
known nonzero.

No two active block cells can occur in the same matching term.  No
coefficient ratio is normalized, and no cancellation between two
contributors is excluded by assumption.

## 4. Replayable projective certificates

For known nonzero mode vectors \(x_X=(p_X,s_X)\), use

\[
 \beta((r,u),(s,v))=rv+us,\qquad
 R_{XY}=\beta(x_X,x_Y).                                  \tag{9}
\]

On projective lines, a forced zero applies the involution
\(\tau(L)=L^\perp\).  A zero path of odd length joining a required-nonzero
pair is immediately contradictory.  An odd zero cycle forces its component
onto one isotropic line; a required-nonzero pair in that component is also
contradictory.

The checker uses graph bipartiteness directly.  Every certificate records
and replays the actual zero path, or the actual odd cycle together with
paths to both endpoints of the conflicting required pair.  It restricts the
graph to branch modes already known nonzero, so a possible zero vector
cannot create a false proportionality inference.

The exact support census is:

| physical pair | closed masks | projective-frontier masks | pure branches | open branches |
|---|---:|---:|---:|---:|
| 03 | 512 | 0 | 1152 | 0 |
| 04 | 512 | 0 | 1152 | 0 |
| 05 | 512 | 0 | 768 | 0 |
| 06 | 512 | 0 | 768 | 0 |
| 07 | 512 | 0 | 1152 | 0 |
| 12 | 512 | 0 | 1152 | 0 |
| 13 | 512 | 0 | 1152 | 0 |
| 15 | 512 | 0 | 768 | 0 |
| 17 | 432 | 80 | 1152 | 80 |
| 25 | 512 | 0 | 768 | 0 |
| 34 | 512 | 0 | 1152 | 0 |

Thus projective closure alone proves \(5552\) of all
\(11\cdot512=5632\) support strata.  It certifies \(11056\) pure branches
and leaves exactly \(80\), one in each remaining mask.  The certificates
split as

\[
 10880\text{ isotropic-component certificates}
 \quad+\quad176\text{ odd-path certificates}.             \tag{10}
\]

Among the former, \(10864\) use triangles and \(16\) use five-cycles.
The full replayable branch-ledger SHA-256 is

    258a5e409eeced43ea4e777c46d72ab0e761de29df9f1bafeeab27ef13fcf757

and the support-classification SHA-256 is

    661e57a22c1eb5f308e09d5cd2fc8a9360fe16dbe01aee0fb65d30ed0495359a

## 5. A sharper pair-\(17\) frontier

Bits are ordered row-major:

\[
\begin{array}{c|ccccccccc}
\text{bit}&0&1&2&3&4&5&6&7&8\\ \hline
\text{cell}&00&01&02&10&11&12&20&21&22.
\end{array}                                                \tag{11}
\]

A weaker union--find reconnaissance left \(256\) pair-\(17\) masks and
reported minimal masks

\[
                         33,\ 38,\ 258,\ 261.              \tag{12}
\]

The independent projective-parity reconstruction strictly improves this:
masks \(33,38,258\) themselves close.  Its exact frontier consists of the
\(80\) masks containing at least one of

\[
\begin{aligned}
261&=\{00,02,22\},\\
291&=\{00,01,12,22\}.                                    \tag{13}
\end{aligned}
\]

These are the only minimal projective-frontier masks.  Every such mask has
one open branch; all its other pure-contributor branches have replayable
certificates.  This discrepancy is benign: the earlier union--find test was
sound but incomplete, while projective path parity captures further forced
orthogonality.

## 6. Uniform exact closure of the final \(80\) masks

The remaining pair-\(17\) cases are closed without support assumptions.
For the full symbolic block

\[
                  H_{17}=\sum_{a,b}h_{ab}\,17_{ab},       \tag{14}
\]

the checker reconstructs every coordinate of (8) directly.  There are:

- nine affine block variables \(h_{ab}\);
- the scalar \(a\);
- \(24\) coefficients of \(p\) and \(24\) coefficients of \(s\);
- \(545\) nonzero top-coordinate equations in \(58\) variables.

After multiplying (8) by four, these equations generate an ideal

\[
 I_{17}\subset
 \mathbb Q[h_{00},\ldots,h_{22},a,p_{00},\ldots,p_{72},
                         s_{00},\ldots,s_{72}].            \tag{15}
\]

The ideal is deliberately **unsaturated**: the \(h_{ab}\) are ordinary
affine variables, and none is inverted.  The independent checker orders
the variables as all block weights, then \(a\), then all \(p\)-coordinates,
then all \(s\)-coordinates, and calls Singular's exact
\(\operatorname{slimgb}\) routine with a reduced degree ordering.  It
returns

\[
                              I_{17}=(1).                  \tag{16}
\]

Consequently there is no solution for any specialization of the nine block
coefficients, including all \(512\) support masks and all exceptional
complex ratios.  This closes the \(80\) projective-frontier masks and proves
(5) for pair \(17\).

The ordered independent equation ledger has SHA-256

    1b4777acae6a7db26a51cc613cce1be34a8d16af8e94678d40bf8fed59c3cb2e

This algebra route is independent of the support ledger and uses a
different variable block order and Gröbner call from the primary exact
calculation.

## 7. Scope boundary

The theorem allows one arbitrary physical \(3\times3\) block, on any one
pair in (3), and includes endpoint-asymmetric entries, zero entries, and
all coefficient ratios.  It does not allow two invisible physical blocks
simultaneously: cross terms between distinct blocks can survive in both the
polarized cubic and the pair-cap coefficient system.

The nine-cell interior \(q\) is still fixed.  This is therefore a strict
local thickening of the eight-site polarized model, not an arbitrary
eight-site pair-cap theorem, not a Krenn counterexample, and not the missing
all-even descent.

## 8. Reproduction

Run

    .venv/bin/python computations/verify_polarized_eight_site_invisible_block_projective_frontier_independent.py

The checker prints the eleven rows of the support table above and ends with

    10 physical pairs: all 512 supports closed
    pair (1, 7): 432 closed, 80 projective-frontier supports
    weaker discovery minima superseded: (33, 38, 258, 261)
    minimal pair-17 frontier masks: (261, 291)
    certificate kinds: {'isotropic_component': 10880, 'odd_zero_path': 176}
    odd-cycle sizes: {3: 10864, 5: 16}
    closed/open branches globally: 11056/80
    classification SHA-256: 661e57a22c1eb5f308e09d5cd2fc8a9360fe16dbe01aee0fb65d30ed0495359a
    branch-ledger SHA-256: 258a5e409eeced43ea4e777c46d72ab0e761de29df9f1bafeeab27ef13fcf757
    pair-17 equation SHA-256: 1b4777acae6a7db26a51cc613cce1be34a8d16af8e94678d40bf8fed59c3cb2e
    pair-17 unsaturated 545-equation ideal is [1]: PASS
    all 11 invisible blocks and all 512 support masks excluded: PASS
