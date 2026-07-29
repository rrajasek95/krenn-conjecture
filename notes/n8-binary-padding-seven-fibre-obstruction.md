# A seven-fibre obstruction to padding the rational binary source

Let (B) be the thirteen-cell rational binary support in
`computations/verify_n8_pair_cap_obstruction.py`, shifted to vertices
(0,\ldots,7).  Adjoin the colour-2 perfect matching

\[
             03\mid12\mid47\mid56.                       \tag{1}
\]

Assume all seventeen displayed cells are nonzero, every other cell whose
two endpoint colours belong to \(\{0,1\}\) is zero, and place no restriction
on any remaining cell involving colour 2.  Then the support cannot realize
\(\Delta_{8,3}\), over any field.

This closes the entire padding chart, not merely a bounded-cell part of it.
The argument uses seven mixed coefficients.

## Six forced zeros

Write a cell as `uv;ab`.  For each colouring in the first column, exhaustive
enumeration of the 105 perfect matchings leaves exactly the matching in the
second column after the fixed binary zero pattern is imposed:

| colouring | sole possible decorated matching | forced zero |
|---|---|---|
| `00120000` | `01;00 23;12 46;00 57;00` | `23;12` |
| `11020000` | `02;10 13;12 46;00 57;00` | `13;12` |
| `11120100` | `05;11 12;11 37;20 46;00` | `37;20` |
| `11120111` | `05;11 12;11 34;20 67;11` | `34;20` |
| `11121000` | `04;11 12;11 36;20 57;00` | `36;20` |
| `11121011` | `04;11 12;11 35;20 67;11` | `35;20` |

Every factor other than the indicated forced-zero cell belongs to the fixed
nonzero seed.  Each colouring is mixed, so its target coefficient is zero.
Its unique possible monomial therefore forces the indicated cell to vanish.

## The final coefficient

Consider the mixed colouring `21120000`.  Exactly seven matchings survive
the binary zero pattern.  In the standard recursive enumeration their
numbers are

\[
                         1,16,31,46,62,75,91.             \tag{2}
\]

Matching 31 is

```
03;22 12;11 46;00 57;00,
```

so it is a nonzero monomial entirely inside the seventeen-cell seed.  The
other six matchings respectively contain one of

```
23;12, 13;12, 36;20, 37;20, 34;20, 35;20,
```

and consequently vanish by the first six coefficient equations.  Hence the
coefficient of `21120000` is the nonzero matching-31 monomial, contradicting
the required mixed coefficient zero.

The proof is independent of the values of all unrestricted colour-2 cells
and of the rational normalization of the binary source.  It only uses the
fixed nonzero/zero pattern.  Thus any ternary extension of this particular
binary source must activate at least one previously absent principal
\(0/1\) cell; adding arbitrary third-colour entries alone can never work.

`computations/verify_n8_binary_padding_seven_fibre_obstruction.py`
independently enumerates every perfect matching in all seven fibres and
checks the forced-zero cover in (2).

## One principal-binary excess cell is still impossible

The conclusion persists if at most one of the other 99 principal
\(0/1\)-cells is activated.  This strengthening has a finite, solver-free
monomial-propagation certificate.

For each choice of the exceptional binary cell (and also the case with no
exception), initially declare the seventeen seed cells nonzero, the other
98 or 99 absent binary cells zero, and every remaining cell unknown.  Use
the following thirteen mixed colourings:

```
00120000  11020000
11120100  11120111  11121000  11121011
20100000  21000000
21110100  21110111  21111000  21111011
21120000
```

Whenever all but one of the 105 matching monomials in one of these fibres
contain a known-zero cell, the coefficient equation reduces to one product.
If that product has exactly one factor not already known nonzero, that
factor is forced to zero.  Repeating this rule reaches a sole possible
monomial all of whose factors are known nonzero.  This is a contradiction
because every displayed colouring is mixed.

There are only 100 cases.  The same fixed ordering of the thirteen fibres
terminates after 11 steps in 10 cases, 12 steps in 12 cases, and 13 steps in
the remaining 78 cases.  The computation uses only exhaustive enumeration
of the 105 perfect matchings and the no-zero-divisors property; no numerical
weights or SAT solver enter it.  It proves

\[
 \boxed{\text{every ternary extension must activate at least two absent
 principal }0/1\text{ cells}.}                            \tag{3}
\]

`computations/verify_n8_binary_padding_one_binary_excess.py` checks all
100 propagation certificates directly.

## Exactly two excess binary cells

There are \(\binom{99}{2}=4851\) ways to activate exactly two absent
principal \(0/1\)-cells.  The same unique-monomial rule gives a nearly
complete classification while still treating every colour-2 cell as
unknown:

* the thirteen fibres above already contradict 4812 pairs;
* propagation using all 6558 mixed fibres contradicts 38 of the remaining
  39 pairs;
* the sole support-level survivor is

\[
                         47;00,\qquad56;00.                \tag{4}
\]

These two cells switch the lower pure-zero matching
\(46\mid57\) to \(47\mid56\).  Even this exceptional pair is impossible by
a short exact coefficient argument.  Put

\[
 B=x_{46}^{00}x_{57}^{00}+x_{47}^{00}x_{56}^{00}.         \tag{5}
\]

The complete pure-zero fibre consists of precisely its two displayed
matchings, so

\[
 [00000000]H=x_{01}^{00}x_{23}^{00}B=1.                  \tag{6}
\]

In particular \(B\ne0\).  The only possible terms of the two mixed fibres
`00120000` and `11020000` respectively give

\[
 x_{01}^{00}x_{23}^{12}B=0,
 \qquad
 x_{02}^{10}x_{13}^{12}B=0.                              \tag{7}
\]

The cells \(x_{01}^{00}\) and \(x_{02}^{10}\) belong to the nonzero seed;
hence

\[
                         x_{23}^{12}=x_{13}^{12}=0.        \tag{8}
\]

Four further mixed colourings have exactly one combinatorially possible
matching:

| colouring | sole possible decorated matching | forced zero |
|---|---|---|
| `11120111` | `05;11 12;11 34;20 67;11` | `34;20` |
| `11121011` | `04;11 12;11 35;20 67;11` | `35;20` |
| `21110111` | `04;20 12;11 35;11 67;11` | `04;20` |
| `21111011` | `05;20 12;11 34;11 67;11` | `05;20` |

Thus all four cells in the last column vanish.  Finally consider
`21120000`.  Fourteen matchings survive the fixed binary zero pattern.
Twelve contain one of the six cells forced to zero in (8) and the table.
The remaining two contribute exactly

\[
                         x_{03}^{22}x_{12}^{11}B,          \tag{9}
\]

which is nonzero because both prefactors are seed cells and \(B\ne0\).
This contradicts the mixed target coefficient zero.

Consequently the rational binary source cannot be extended to a ternary
source unless at least three previously absent principal binary cells are
activated:

\[
 \boxed{\text{every exact extension has principal }0/1\text{ excess at
 least three}.}                                           \tag{10}
\]

`computations/verify_n8_binary_padding_two_binary_excess.py` performs the
complete 4851-pair propagation using integer support masks, identifies (4)
as the unique exception, and independently checks every matching and every
factorization in (5)--(9).  It uses neither SAT nor numerical algebra.

## Three excess binary cells: a compact exact certificate

The lower bound strengthens once more:

**Theorem.**  Keep all seventeen cells of the binary-plus-colour-2 seed
nonzero.  If at most three of the other 99 principal \(0/1\)-cells are
nonzero, then arbitrary values and arbitrary support on every cell involving
colour 2 cannot realize \(\Delta_{8,3}\).

The proof is a finite exact support certificate, not a finite-field or
numerical test.  It contains 110 necessary conditions for any complex
realization.  One hundred are singleton implications of the form

\[
 \bigwedge_{e\in T} (x_e\ne0)
 \quad\Longrightarrow\quad
 \bigvee_{M\ne T}\ \bigwedge_{e\in M\setminus T}(x_e\ne0),              \tag{11}
\]

where \(T\) is one specified matching monomial in a mixed fibre.  Exactness
implies (11): if the left side holds and no second matching is supported,
the mixed coefficient is one nonzero monomial.

The other ten conditions are one-row pure-zero nogoods.  Their complete
data are:

| mixed word | exact mixed terms | exact pure-0 terms |
|---|---:|---:|
| `21120000` | `31,32` | `1,2,16,17` |
| `00120000` | `1,2` | `1,2,16,17` |
| `01020000` | `16,17` | `1,2,16,17` |
| `01120000` | `31,32` | `1,2` |
| `00120000` | `1,2` | `1,2` |
| `11120000` | `31,32` | `1,2` |
| `11020000` | `16,17` | `1,2` |
| `21120000` | `31,32` | `1,2` |
| `00020000` | `1,2` | `1,2` |
| `10020000` | `16,17` | `1,2` |

Matching numbers use the standard recursive ordering of all 105 perfect
matchings.  In every row, the single mixed binomial makes the indicated
complete pure-0 polynomial identically zero in the signed Laurent quotient.
Such exact mixed/pure term sets are therefore forbidden in a realization
whose pure-0 coefficient is one.

Introduce one Boolean variable for each of the 252 aggregate cells.  Force
the seventeen seed variables, impose an at-most-three totalizer on the 99
absent binary variables, encode the hundred implications (11), and encode
the ten exact-term-set nogoods.  The resulting CNF is UNSAT.  Therefore any
putative exact realization in this chart violates either a mixed singleton
equation or one of the ten exact one-row identities.  This proves the
theorem and hence

\[
 \boxed{\text{every exact extension has principal }0/1\text{ excess at
 least four}.}                                            \tag{12}
\]

The semantic and Boolean audits are deliberately separate:

* `computations/verify_n8_binary_padding_three_binary_excess.py` enumerates
  the matching terms, verifies all 100 singleton schemas, proves each of the
  ten Laurent pure-zero reductions exactly, rebuilds the CNF, and checks it
  independently with CaDiCaL 3.0.0 and Glucose 4.2;
* `computations/verify_drup_certificate.py` checks every addition in the
  deletion-free DRUP transcript by reverse unit propagation.

The frozen certificate statistics are 11,891 variables, 41,506 clauses,
10,400 matching selectors, and 3,885 DRUP additions.  Artifact sizes and
SHA-256 hashes are:

| artifact | bytes | SHA-256 |
|---|---:|---|
| `cert_n8_binary_padding_excess3.cnf` | 567,034 | `484259598c2d3fc0d4bca37312894da02d33981055a35e95ce8e9c0b25fff25c` |
| `cert_n8_binary_padding_excess3.drup` | 8,305,978 | `f96b9704b4443f03b35ab69eb21c5a47d764acd521e511d00083e9f8429cd953` |
| `verify_n8_binary_padding_three_binary_excess.py` | source | `b8a096b2bf4a16dba4779aa758dc6e117c251f884f1f11a66a0f966369b34512` |

Taken alone, this three-excess certificate does not rule out an extension
after four or more absent principal binary cells are activated.  Like every
result in this note, it does not constrain an unrelated ternary source that
does not contain the seventeen-cell seed.

## Four excess binary cells: an exact signed-Laurent certificate

The same arbitrary-density conclusion also holds with an at-most-four bound.

**Theorem.**  Every exact ternary realization containing the seventeen-cell
seed activates at least five of the other 99 principal \(0/1\)-cells.

The certificate has 210 independently validated semantic schemas:

* 174 mixed-singleton implications of the form (11);
* 12 exact signed-binomial core nogoods; and
* 24 exact pure-product-zero nogoods.

For a signed-binomial core, each cited mixed fibre is required to have exactly
its displayed pair of matching terms.  The corresponding exponent rows are
inconsistent in the signed integer quotient lattice.  Hence at least one of
those exact fibre statuses must change.  For a pure-product-zero schema, the
cited mixed pairs generate a consistent signed quotient, but the cited
complete pure-colour polynomial reduces identically to zero in its group
algebra.  This contradicts its required constant coefficient one.  These are
Laurent identities over the integers, so the argument is exact over
\(\mathbb C\) and does not depend on numerical coefficient searches.

The verifier reconstructs all 105 matching monomials in each cited fibre,
checks every signed-lattice assertion, enforces the seventeen seed cells and
an at-most-four totalizer on the 99 absent binary cells, and encodes exact
fibre status with Boolean variables equivalent to matching-term support.  The
resulting CNF is UNSAT under both CaDiCaL 3.0.0 and Glucose 4.2.  The separate
DRUP checker replays all 13,188 deletion-free proof additions with both
CaDiCaL 1.9.5 and Glucose 4.2.

The frozen certificate has 19,795 variables and 97,119 clauses:

| artifact | bytes | SHA-256 |
|---|---:|---|
| `cert_n8_binary_padding_excess4_schemas.json` | 40,559 | `0d6677afeaa58226cde960fdb9ebe4badb55a5faee6affe89199187a3fd281cf` |
| `cert_n8_binary_padding_excess4.cnf` | 1,591,027 | `e9a0a69cf58c3ae381861a939dcc9f9d0c2622447499330b8855fd771974ae19` |
| `cert_n8_binary_padding_excess4.drup` | 42,314,675 | `7df2183bfacd6a31afbf303530125b6eab645e4e95180f54dd81faf437588aa2` |
| `verify_n8_binary_padding_excess_certificate.py` | 15,496 | `61938fa51aa189b1ff41c5a2d41e24cd6341522ac2f3e8d7098efe85081b3917` |

Run the semantic/Boolean verifier as

```
python computations/verify_n8_binary_padding_excess_certificate.py \
  computations/cert_n8_binary_padding_excess4_schemas.json
```

and pass the CNF and DRUP files to
`computations/verify_drup_certificate.py` for the proof replay.  As before,
this is a theorem about this fixed seed chart, not a global obstruction to an
unrelated ternary source.

## Five excess binary cells: compact quotient-monomial closure

The chart obstruction persists through five activated principal binary
cells.

**Theorem.**  Every exact ternary realization containing the seventeen-cell
seed activates at least six of the other 99 principal \(0/1\)-cells.

An exact arbitrary-density CEGAR enumeration terminates UNSAT.  Its frozen
SAT assumption core contains 851 necessary support conditions, a reduction
from 40,781 learned conditions in the independently recorded run:

* 741 mixed-singleton implications;
* 62 inconsistent exact signed-binomial core nogoods;
* 44 exact pure-product-zero nogoods; and
* 4 exact quotient-monomial nogoods.

The first three classes have the meanings described above.  For the fourth,
fix the listed exact mixed fibre polynomials.  The signed binomial fibres
generate a consistent Laurent quotient, but the listed four-term target
polynomial reduces to a single nonzero monomial in that quotient.  It
therefore cannot vanish on the algebraic torus.  Greedy exact row deletion
shrinks two such certificates to four binomial rows plus the target fibre and
the other two to nine rows plus the target.  The verifier reconstructs the
quotient over the integers and checks the monomial remainder directly; it
does not trust the search classification.

With an at-most-five totalizer, the 851 conditions yield a CNF with 64,105
variables and 319,309 clauses.  CaDiCaL 3.0.0 and Glucose 4.2 both return
UNSAT.  The deletion-free DRUP transcript has 21,889 additions, all replayed
successfully with both CaDiCaL 1.9.5 and Glucose 4.2.

| artifact | bytes | SHA-256 |
|---|---:|---|
| `cert_n8_binary_padding_excess5_schemas.json` | 153,434 | `a246630b71f070ee254d27eaf211192a7e8de9de890725e583f175b84d09d868` |
| `cert_n8_binary_padding_excess5.cnf` | 5,472,540 | `2b362425f866b38e2759ca530d68ef0805aaf8bd4bfe7962dec849ba44f088e3` |
| `cert_n8_binary_padding_excess5.drup` | 91,431,654 | `f69fe00842f467b93692fbe07318f5b9061d536cf749ee2b8d4de0d5cc15ed64` |
| `verify_n8_binary_padding_excess_certificate.py` | 15,496 | `61938fa51aa189b1ff41c5a2d41e24cd6341522ac2f3e8d7098efe85081b3917` |

The semantic and SAT audit is reproduced by

```
python computations/verify_n8_binary_padding_excess_certificate.py \
  computations/cert_n8_binary_padding_excess5_schemas.json
```

As in the lower-excess results, all cells involving colour 2 are unrestricted
and may be arbitrarily dense.  The conclusion is local to the fixed seed
chart and does not by itself settle the global ternary problem.
