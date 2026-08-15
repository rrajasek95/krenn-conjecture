# The conditioned SP-K6 certificate is a pre-stratum mixed singleton

## Outcome

Conditioning the certified six-site obstruction on the ten-cell transverse
seed and its 225 support-minimum pure completions does not reach any of the
nineteen rank-defect strata.

* The ten-cell seed fails first because none of the three pure target words
  has a supported perfect matching.  Its six nonzero aggregate edge matrices
  are rank one and form one `C6`, so every site has rank-one degree two; the
  forced-incident theorem would require degree at least three.
* Every one of the 225 minimum three-pure support completions passes the pure
  support condition but has a mixed coefficient fibre with exactly one live
  matching.  This is support principle 4 in the internal SP-K6 proof, before
  rank graphs, Laurent lattices, rectangle minors, or SAT/LRAT strata.

The second certificate is source-labelled and occurrence-linear.  It lifts
to every even order when the global occurrence fibre is the Cartesian product

\[
   \{\text{local singleton}\}\times
   \{\text{one common labelled tail family}\}.             \tag{1}
\]

Then the mixed coefficient is (mT), where the local monomial (m) is a
support unit and the arbitrary tail sum (T) is assumed nonzero.  The first
failure of (1) occurs with two window/tail crossing edges.  An exact
eight-site two-term fibre then cancels, so common-tail factorization—not the
black-box SP-K6 theorem—is the load-bearing uniform hypothesis.

The checker is
`computations/verify_c6_transverse_seed_spk6_certificate_lift_gate.py`.

## 1. The ten-cell seed stops before rank stratification

Use the transverse fines

\[
 A=02|13|45,\qquad B=03|15|24,                             \tag{2}
\]

in the four words

```text
111001, 111021, 111201, 111221.
```

The seed has exactly the six underlying edges in (A\cup B).  Every
nonzero aggregate matrix has rank one:

```text
R={02,13,45,03,15,24},  d_R(v)=2 for every v.               (3)
```

All other nine matrices vanish.  More immediately, the pure matching counts
in words `000000`, `111111`, `222222` are `(0,0,0)`, contradicting their
target coefficient one.  Thus the exact conditioned certificate order is:

```text
pure-support failure
    before forced incident-edge degree >=3
    before the derived |F|<=6 bound
    before every named rank stratum.                         (4)
```

This certificate is not useful for uniform promotion by itself.  Absence of
a pure matching inside a chosen six-site window need not survive a larger
source: a matching may cross the window boundary and supply the global pure
coefficient.

## 2. Minimum completions: the exact SP-K6 clause

The support-minimum completion adds one colour-one cap cell and one pure
matching in each of colours zero and two.  There are (15^2=225) choices.
In every completion each pure word has exactly one occurrence, while at least
nine mixed rows are singletons.  The complete singleton-count histogram is

```text
 9:8, 10:15, 11:6, 12:10, 13:26, 14:22, 15:24,
16:4, 17:16, 18:14, 20:26, 21:4, 22:5, 23:8,
25:4, 26:9, 27:2, 28:4, 29:6, 33:8, 38:2, 44:2.            (5)
```

Across all completions the 4,002 singleton words have profiles

```text
5+1:360, 4+2:960, 4+1+1:360,
3+3:360, 3+2+1:1512, 2+2+2:450.                             (6)
```

Hence this is not a special `4+2` or binary boundary.  It is the universal
support clause

> a mixed coefficient cannot contain exactly one supported nonzero
> perfect-matching monomial.

For the canonical sharp completion the first witness is

```text
word       000001,
fine       01|23|45,
cells      a01^00, a23^00, a45^01,
operation  coefficient:000001.                              (7)
```

Its equation is one nonzero monomial equal to zero.  This is a literal unit
after localizing the three supported cells.  No matrix rank, minor, or
unlabelled toric equation is involved.

## 3. Exact common-tail lift

Let (m) denote the labelled monomial in (7), and let a disjoint spectator
packet have compatible matching family ({\cal T}), with total coefficient

\[
                         T=\sum_{\tau\in{\cal T}}q_\tau.    \tag{8}
\]

If the global compatible occurrence set is termwise

\[
                  \{M\}\times{\cal T},                    \tag{9}
\]

with word, fine, and coefficient operation retained, then the global mixed
row is exactly

\[
                             F=mT.                          \tag{10}
\]

At any putative source point with (T\ne0), (10) is impossible.  This is the
singleton analogue of the arbitrary-common-tail permanent lemma.  The tail
need not be one monomial or have all terms of the same sign.

The checker verifies (9) in two ways:

1. forced matching tails of one, two, and three spectator pairs, at orders
   8, 10, and 12, each give one global occurrence; and
2. a complete same-colour `K4` tail has three matching monomials, and the
   ten-site global fibre has exactly the three products of its tail matchings
   with the local singleton.

Thus the certificate is occurrence-linear and uniformly common-tail
liftable.  The exact hypothesis is the labelled Cartesian bijection (9), not
equality after collecting occurrences or projecting away operation labels.
The nonvanishing of the total (T) is also necessary.

## 4. First nonlift: two crossing edges

Adjoin spectator sites `6,7` and the intended tail cell `a67^22`.  Extend the
canonical word to

```text
00000122.                                                   (11)
```

With separated support, its only occurrence is

```text
01|23|45|67.                                                (12)
```

Now add the two crossing cells `a46^02,a57^12`.  The same physical word gains
the second occurrence

```text
01|23|46|57.                                                (13)
```

The complete coefficient becomes

\[
 a_{01}^{00}a_{23}^{00}
 \left(a_{45}^{01}a_{67}^{22}+a_{46}^{02}a_{57}^{12}\right). \tag{14}
\]

All cells may be units and the two terms cancel—for example take all values
one except (a_{57}^{12}=-1).  The second term is divisible by neither the
full local singleton (a_{01}a_{23}a_{45}) nor the spectator tail
(a_{67}).  Therefore (9) fails before any rank-one tail comparison can be
applied.

Two crossings are minimal: a perfect matching crosses an even window
boundary an even number of times.  This is the exact first nonlift term, not
an artefact of a chosen presentation.

## 5. Proof consequence and scope

The conditioned SP-K6 analysis gives the following usable statement:

> **Minimum-completion window lemma.**  Every support-minimum pure completion
> of the transverse six-site packet has a literal mixed-singleton unit.  The
> unit persists after reinserting any nonzero common spectator tail satisfying
> the labelled Cartesian occurrence factorization (9).

This closes the minimum completion branch uniformly.  It does not close a
nonminimum larger source containing window/tail crossing matchings.  For that
branch the shortest missing theorem must either isolate one rank-one common
tail or route the first crossing correction (13) into the already classified
common-tail `C4`/parent recurrence.

This result conditions and opens the SP-K6 proof rather than citing its final
nonexistence theorem.  The accepted certificate is exactly its elementary
mixed-singleton support clause.  The external Lean/LRAT corroboration is not
used.

Run:

```text
python3 computations/verify_c6_transverse_seed_spk6_certificate_lift_gate.py --mode structural
python3 -O computations/verify_c6_transverse_seed_spk6_certificate_lift_gate.py --mode full
python3 -I -S computations/verify_c6_transverse_seed_spk6_certificate_lift_gate.py --mode exhaustive
```

Frozen ledger SHA-256:

```text
4d89d7b8a5dfccbe20ee3756a1853ecf5245c6d56688ad038b7c715f9702a846
```
