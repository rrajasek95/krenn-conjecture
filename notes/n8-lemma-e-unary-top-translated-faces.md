# Smaller unary-top faces fail by one translated pure/zero row

## Outcome

The normalized one-bad Lemma-E packet has much smaller support-shadow faces
than the 39/46-cell odd-circuit packets previously frozen.  There is a
24-cell face in the shared-head `E11` case and a 25-cell face in the `E21`
case.  Both are source-faithful and irredundant under every one-cell deletion.
Their mixed binomial character systems are **consistent**, so the earlier odd
character obstruction does not explain them.  Instead, on each face one
mixed zero fibre is a Laurent translate of one required pure fibre.  A single
denominator-cleared identity makes the coefficient torus empty over every
field.

This is not a support-independent exclusion.  Extra matching terms break the
displayed translated-fibre equalities, and a bounded semantic CEGAR reached
larger faces rather than exhausting the packet.  No exact rational point was
found.  The full normalized packet remains open.

## Exact setting

Use sites `p=0,q=1,r=2`, residual sites `2,...,7`, essential arm

\[
                             A_{01}=E_{00},
\]

and the Lemma-E consequences

\[
 (A_{0x})_{0,*}=0\quad(x\ne1),
 \qquad H_{\{2,\ldots,7\}}=e_0^{\otimes6}.
\]

The second shared arm is either `A_02=E_11` or `A_02=E_21`.  As in the
previous packet audit, all 729 residual fibres and all 6,561 full pair-row
fibres are enumerated with literal endpoint-labelled cells and ordinary
site-square-zero perfect matchings.

The support histograms are:

| head | cells | residual target | residual zero | full targets | full zero |
|---|---:|---|---|---|---|
| `E11` | 24 | `1 x 2` | `713 x 0, 15 x 2` | `1 x 1, 2 x 2` | `6528 x 0, 30 x 2` |
| `E21` | 25 | `1 x 1` | `728 x 0` | `1 x 1, 2 x 2` | `6496 x 0, 62 x 2` |

Here `m x k` means `m` coefficient fibres with `k` supported matching
monomials.  Every nonfixed supported cell has a recorded fibre that violates
the necessary support shadow after deleting that cell alone.  This is only
deletion irredundancy, not a global minimum-support theorem.

## The `E11` translated row

On the 24-cell face the all-zero pure coefficient has exactly two monomials:

```text
01:00  27:00  35:00  46:00
01:00  27:00  36:00  45:00.
```

Call their sum `P0`; exactness requires `P0=1`.  The mixed word

```text
11100001
```

has exactly the two monomials

```text
02:11  17:11  35:00  46:00
02:11  17:11  36:00  45:00.
```

Call their sum `Z`; exactness requires `Z=0`.  Term by term,

\[
 (02{:}11)(17{:}11)P_0=(01{:}00)(27{:}00)Z.             \tag{1}
\]

Every displayed cell is nonzero on this support torus.  Equations `P0=1`
and `Z=0` therefore make (1) say that a Laurent unit vanishes, a
contradiction.  No division is required: (1) is checked as a literal
polynomial identity.

## The `E21` translated row

On the 25-cell face the all-one pure coefficient has two terms:

```text
07:11  16:11  24:11  35:11
07:11  16:11  25:11  34:11.
```

Call their sum `P1`, so `P1=1`.  The mixed word

```text
12111121
```

has the two terms

```text
07:11  16:22  24:11  35:11
07:11  16:22  25:11  34:11.
```

Thus, with its zero equation named `Z=0`,

\[
                     (16{:}22)P_1=(16{:}11)Z.            \tag{2}
\]

Again (2) is an exact polynomial identity and forces the supported cell
`16:22` to vanish.  This excludes the coefficient torus in every
characteristic.

## What the phase audit says

The zero fibres are all empty or binomial.  They contribute 45 rows on the
`E11` face and 62 on the `E21` face.  In each case there are 16 distinct
exponent-difference rows up to sign and GF(2) exponent rank 9.  More
concretely, an explicit sign assignment cancels every row: put `-1` on the
four `46:{00,01,10,11}` cells in the first face (respectively the four
`35:{11,12,21,22}` cells in the second), and `+1` on every other cell.  Thus
neither face has an odd Laurent circuit.  Its obstruction is instead the
nonzero-pure-product condition: one required pure polynomial is zero in the
signed quotient by a single translated mixed row.

This distinction matters for further search.  Adding only odd-circuit cuts
will rediscover these faces.  A sound semantic cut must preserve both the
mixed row and the exact pure-fibre support, while permitting any additional
matching term in either fibre.

## Support-independent residue

There is one genuine support-free consequence, but it does not finish the
packet.  Apply the two-star pure-response lemma from commit `cd77a7b` twice:

\[
 p_1(s_1Q^{[2]})=X_1,\quad p_2(s_1Q^{[2]})=0,
\]

and with colours exchanged, then do the same for `s1,s2`.  If

\[
D_p=\{z:\dim\langle(p_1)_z,(p_2)_z\rangle\le1\},\qquad
D_s=\{z:\dim\langle(s_1)_z,(s_2)_z\rangle\le1\},
\]

then each of `Dp,Ds` contains a site whose local dependent line is `e1`
and a distinct site whose line is `e2`.  The stronger line-hitting statement
follows by contracting every dependent site: if no local line contains the
corresponding pure target factor, the remaining sites form the no-defect
Hamming system already proved impossible.

This recovers two singular colour-carrying spokes at each endpoint.  It does
not force the p- and q-spokes to use common physical sites, exclude extra
rank-two blocks, or produce the missing source descent.  Accordingly it is a
structural reduction, not the requested support-independent contradiction.

## Reproduction and scope

Run

```text
.venv/bin/python computations/verify_n8_lemma_e_unary_top_translated_faces.py
.venv/bin/python -O computations/verify_n8_lemma_e_unary_top_translated_faces.py
```

The checker enumerates every residual/full fibre, verifies the complete
histograms and every one-cell deletion witness, checks signed-lattice
consistency, and expands (1)--(2) exactly.  It proves only that these two
displayed support tori are empty.  It does not exhaust arbitrary supports,
construct a rational packet point, or settle the one-bad selected-witness
branch.
