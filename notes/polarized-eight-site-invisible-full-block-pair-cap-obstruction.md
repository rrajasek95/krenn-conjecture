# Every single invisible full block misses the pair-cap locus

## 1. Statement and exact scope

Work in the eight-site ternary square-zero algebra and put

\[
\begin{aligned}
q={}&23_{00}+45_{00}+67_{00}
     +01_{11}+36_{11}+57_{11}\\
   &+02_{22}+14_{22}+56_{22},\\
z={}&01_{00}+24_{11}+37_{22}.
\end{aligned}                                                    \tag{1}
\]

For a physical pair \(u<v\) and a matrix
\(X=(x_{cd})_{0\leq c,d\leq2}\in\mathbb C^{3\times3}\), define the full
ordered endpoint-colour block

\[
             E_{uv}(X)=\sum_{c,d=0}^2x_{cd}\,uv_{cd},
             \qquad q_{uv,X}=q+E_{uv}(X).                       \tag{2}
\]

Let

\[
 \mathcal I=\{03,04,05,06,07,12,13,15,17,25,34\}.               \tag{3}
\]

Then, for every *single* pair \(uv\in\mathcal I\) and every matrix \(X\),

\[
                zq_{uv,X}^{[3]}=\Delta_{8,3},                   \tag{4}
\]

but for every \(a\in\mathbb C\) and all linear forms \(p,s\),

\[
 \boxed{\quad
 (a q_{uv,X}+4ps)q_{uv,X}^{[3]}\ne\Delta_{8,3}.
 \quad}                                                         \tag{5}
\]

No entry of \(X\) is assumed nonzero.  Thus (5) covers all \(2^9=512\)
support strata, all exceptional coefficient ratios, and the zero block in
one unsaturated affine calculation for each physical pair.

The standalone exact checker is
[`verify_polarized_eight_site_invisible_full_block_pair_cap_obstruction.py`](../computations/verify_polarized_eight_site_invisible_full_block_pair_cap_obstruction.py).
It imports no construction from the one-cell or support-reconnaissance
programs.

## 2. Why every block preserves the polarized identity

All nine cells in a block \(E_{uv}(X)\) use the same two physical sites.
Consequently

\[
                         E_{uv}(X)^{[2]}=0
\]

and hence

\[
 q_{uv,X}^{[3]}=q^{[3]}+E_{uv}(X)q^{[2]}.                       \tag{6}
\]

Direct square-zero multiplication gives

\[
                         zE_{uv}(X)q^{[2]}=0                    \tag{7}
\]

for exactly the eleven physical pairs in (3).  Combining (7) with the
literal sparse identity \(zq^{[3]}=\Delta_{8,3}\) proves (4).  The checker
does not infer this from a support table: it reconstructs the full
symbolic divided power for all nine independent \(x_{cd}\) and verifies
the polynomial identity coefficient by coefficient.

## 3. The unrestricted coordinate ideal

Write

\[
 R_{(i,c),(j,d)}=p_{i,c}s_{j,d}+s_{i,c}p_{j,d}.                  \tag{8}
\]

The checker generates divided powers directly as unordered selections of
pairwise disjoint quadratic cells.  Thus factorial normalization is built
in rather than applied after an ordered-power expansion.  For every full
colour word \(w\in\{0,1,2\}^8\), let

* \(F_{w,AB}(X)\) be the integer-polynomial incidence of the Gram entry
  \(R_{AB}\) in \(q_{uv,X}^{[3]}\), and
* \(Q_w(X)\) be the \(w\)-coefficient of \(q_{uv,X}^{[4]}\).

Because \(q_{uv,X}q_{uv,X}^{[3]}=4q_{uv,X}^{[4]}\), a hypothetical
identity in (5) is equivalent, coordinate by coordinate, to

\[
 4\sum_{A,B}F_{w,AB}(X)
      (p_A s_B+s_A p_B)
   +4aQ_w(X)-\delta_w=0.                                      \tag{9}
\]

Here \(\delta_w=1\) for the three constant-colour words and is zero
otherwise.  The program places every nonzero equation (9) in the
characteristic-zero polynomial ring

\[
 \mathbb Q[\,p_{i,c},s_{i,c},a,x_{00},\ldots,x_{22}\,],         \tag{10}
\]

which has \(48+1+9=58\) variables.  Crucially, there is no
Rabinowitsch variable, saturation, division, genericity hypothesis, or
case distinction.  A reduced Gröbner basis equal to \([1]\) therefore
excludes every complex specialization of \(X,a,p,s\) at once.

## 4. Exact eleven-pair audit

The complete calculation gives the following deterministic counts.  The
two divided-power columns count distinct words, while the equations column
counts all nonzero coordinate equations (9).

| physical pair | \(q_{uv,X}^{[3]}\) words | \(q_{uv,X}^{[4]}\) words | equations | variables | reduced basis |
|---:|---:|---:|---:|---:|---:|
| 03 | 55 | 2 | 401 | 58 | \([1]\) |
| 04 | 55 | 2 | 401 | 58 | \([1]\) |
| 05 | 55 | 11 | 401 | 58 | \([1]\) |
| 06 | 55 | 11 | 401 | 58 | \([1]\) |
| 07 | 73 | 11 | 536 | 58 | \([1]\) |
| 12 | 46 | 2 | 338 | 58 | \([1]\) |
| 13 | 64 | 11 | 482 | 58 | \([1]\) |
| 15 | 46 | 2 | 338 | 58 | \([1]\) |
| 17 | 73 | 11 | 545 | 58 | \([1]\) |
| 25 | 55 | 2 | 419 | 58 | \([1]\) |
| 34 | 73 | 2 | 563 | 58 | \([1]\) |

In particular, the independently reconstructed pair-\(17\) ideal has the
same 545 equations and 58 variables as the initial discovery computation.
All eleven exact jobs reduce to the unit ideal.  The equation-count
histogram is

\[
\begin{array}{c|rrrrrrr}
\#\text{ equations}&338&401&419&482&536&545&563\\ \hline
\#\text{ pairs}&2&4&1&1&1&1&1.
\end{array}                                                     \tag{11}
\]

The checker hashes the exact Singular program for each pair, then hashes
the ordered rows consisting of the pair, equation and variable counts,
program digest, and verified unit result.  The resulting ledger SHA-256 is

```text
409ff093b5d461d6ce61a234ce2a84656589afcd1c465fad6de8bf9f17ee585f
```

The pair-\(17\)-only ledger SHA-256 is

```text
f690b30afc82c6882ec401707136471d81a19103d6b5b023409b59d5c7ddb45d
```

Since all arithmetic is over \(\mathbb Q\), these are exact algebraic
certificates rather than floating-point rank tests.  The equality
\(1\in I_{uv}\) remains true after base change from \(\mathbb Q\) to
\(\mathbb C\), proving (5).

## 5. Supplemental support audit

The optional `--support-census` mode revisits pair \(17\) without using
Gröbner bases.  Unlike the earlier reconnaissance, it first collects
repeated identical matching contributions; an integer multiple of one
invertible parameter monomial times one Gram entry is still a singleton
constraint in characteristic zero.  The resulting projective
orthogonality closure handles 432 masks and leaves 80 masks, with minimal
open masks

\[
             261=\{00,02,22\},\qquad
             291=\{00,01,12,22\}.                              \tag{12}
\]

Its complete 512-row support ledger has SHA-256

```text
5d76c9aedfe86f07c56fa586f35b01ca2d24667787b14602bd9a074ce1b52a5e
```

This smaller support certificate is only a diagnostic refinement.  The
proof of the theorem does not depend on it: the single unrestricted unit
ideal already covers all 512 masks, including the 80 left open by (12).

## 6. Boundary and next frontier

This theorem allows one arbitrary \(3\times3\) endpoint-colour block on
one pair from (3).  It does **not** allow blocks on two or more physical
pairs simultaneously.  It is also a theorem around the fixed sparse
\((q,z)\) seed, not a uniform statement for arbitrary quadratics and not
the missing all-even descent in Krenn's conjecture.

Within the polarized route, the next genuine sparse frontier is therefore
simultaneous activation of two invisible physical blocks.  Such blocks can
interact in \(q_X^{[3]}\) and \(q_X^{[4]}\), so the one-block affine ideals
do not specialize to that problem.  A second route is to activate visible
cells in combinations whose polarized debt words cancel.  Globally, any
successful argument still has to connect these eight-site obstructions to
the shared-row or physical-pair compatibility imposed by an actual
collection of pair caps.

## 7. Reproduction

From the repository root, run the complete eleven-pair audit with

```sh
.venv/bin/python computations/verify_polarized_eight_site_invisible_full_block_pair_cap_obstruction.py --workers 3
```

The independent pair-\(17\) reconstruction plus the optional support census
is

```sh
.venv/bin/python computations/verify_polarized_eight_site_invisible_full_block_pair_cap_obstruction.py --pair17-only --support-census --workers 1
```
