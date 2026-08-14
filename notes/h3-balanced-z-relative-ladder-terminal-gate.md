# The balanced dual reaches the mixed chart arrows; a full terminal is conditional

## Verdict

The pure-safe balanced detector from `0a684ce` extends through every
currently constructed presentation-safe relative family in the Gate-II
ladder.  Its new pure-target/`Eq` correction does not alter any of the
occurrence or principal-parts calculations:

```text
balanced z
  -> relative (t_R-R01, t_L-L01), forced values (-1,+1)
  -> selected dz01-db01, forced value 1 on dz01
  -> 18 direction terms, normalized value 1
  -> word-0102 relative carrier, forced dual C*d=12*d
  -> dq23 / Q / occurrence-labelled ores, values 35/72, 0, -35/72.
```

At every stage an **absolute** carrier column breaks the dual and belongs to
the filler branch.  A monic relative graph preserves the old `H0` and forces
the dual onto its retained carrier.

After granting relative `R01/U_C4` and selected `db01`, the first genuinely
new source-provenant rank-raising family is

\[
       DQ\longleftrightarrow P_0S_1,
       \qquad
       DQ\longleftrightarrow P_1S_0.                 \tag{1}
\]

Both mixed chart arrows are required.  The existing labelled two-root cobar
square cannot supply either one, because root action preserves the
`D/P/S/Q` operation profile while every arrow in (1) changes `DQ` to `PS`.

There is now a precise conditional terminal theorem.  If the selected
same-word/fine/repeated/common-tail physical map is exhausted by the audited
relative blocks and normalized restriction maps, contains no absolute
carrier and no arrow in (1), and its `Q/ores` tail is exactly the committed
conditional gauge/`d_even` closure, then the displayed normalized covector is
an augmented terminal detecting `z`.  Those exhaustiveness and cross-grade
gluing hypotheses are not currently proved for the full source.

Exact checker:

```text
computations/verify_h3_balanced_z_relative_ladder_terminal_gate.py
```

## 1. The pure-safe starting covector

The complete four-corner packet has thirteen cap--Cartan columns and the two
normalized pure-target columns.  On the resulting rank-`15` packet the
primitive detector is

```text
B                 ( 1,  1,-1,-1)
Eq                ( 0,  0, 1, 1)
target            (-1, -1, 0, 0)
W                 (-1, -1, 0, 0)
ordinary residue  ( 1,  1, 0, 0)
M, ainc, q, P_f    0,  0, 0, 0
ridge, eta, sigma  0,  0, 0, 0.
```

It reads `4` on the balanced `B` face, so division by four normalizes it.
The important point for the extension is that the `B` component remains

\[
                         \delta=(1,1,-1,-1).          \tag{2}
\]

Only the pure target/`Eq` correction has changed from the older
`psi_delta`.  The selected matching-PP face `db01` has target and central
`Eq` equal to zero, and the word-`0102` private block has zero target/`Eq`
projection.  Hence the correction in the last two pure corners is invisible
through the entire occurrence ladder below.

## 2. Relative `R01/U_C4`: extension, not filling

Write

\[
\begin{aligned}
 A&=Dq_{01}H, & B&=p_0s_1H, & C&=p_1s_0H,\\
 R_{01}&=A+B+C, & L_{01}&=2A-B-C,
\end{aligned}
\]

where `H` is the three-term residual `C4` sum on sites `2345`.  The
presentation-safe attachment is

\[
 d\Gamma_R=t_R-R_{01},
 \qquad
 d\Gamma_L=t_L-L_{01}.                              \tag{3}
\]

Normalize the occurrence covector by `psi(L01)=1`.  Its value on `R01` is
`-1`, so annihilating (3) forces

\[
                         \psi(t_R,t_L)=(-1,1).        \tag{4}
\]

The graph columns plus the complete response have rank `3`.  Adding the
absolute column `t_R` raises the rank to `4`; adding both `t_R,t_L` raises it
to `5`.  Therefore an absolute reinserted `U_C4/R01` column is not an
extension of the terminal covector.  It is precisely the positive
carrier-saturation/filler branch.  The relative graph (3) preserves the old
source algebra and carries the obstruction forward.

## 3. The selected six-term `db01` face

The literal vertical principal-parts face has six differentiated matching
terms.  Its presentation-safe graph uses coordinates

```text
(db01, dz01, all-D output endpoint)
```

and columns

```text
dz01-db01 = (-1,1,0),
all-D     = ( 0,0,1).
```

They have rank `2`.  The desired absolute `db01=(1,0,0)` raises the rank to
`3`.  The primitive covector `(1,1,0)` kills the relative graph and the
all-`D` endpoint, while reading one on `db01`; equivalently it is forced to
take value one on `dz01`.

Thus the normalized all-`D` endpoint is not the carrier.  It lies in a
different horizontal/vertical bidegree and has disjoint fine-colour support.
The alternatives are exact:

```text
physical absolute db01/dc01 source face -> breaks the dual / filler arm;
monic dz01-db01 graph                   -> extends dual onto dz01;
neither supplied                        -> first literal PP gap remains.
```

Because target=`Eq=0` on `db01`, the pure-safe correction of Section 1 adds
no new term here.

## 4. The eighteen direction terms and the first physical label obstruction

After granting selected `db01`, its endpoint mate, and the same-grade lower
`U_C4` tail, the remaining first-PP face has eighteen terms:

| chart | operation profile `(D,P,S,Q)` | terms | coefficient |
|---|---:|---:|---:|
| `A=D*q01` | `(1,0,0,1)` | 6 | `2` |
| `B=p0*s1` | `(0,1,1,0)` | 6 | `-1` |
| `C=p1*s0` | `(0,1,1,0)` | 6 | `-1` |

Its six marginals are

\[
 (6,6,-3,-3,-3,-3)=3(2,2,-1,-1,-1,-1),             \tag{5}
\]

and the normalized Gate-II dual reads one on this face and zero on the
eighteen residual-tail terms.

The exact fixed-block counterguard has four two-root words times three chart
tags.  Every tag-preserving root edge has rank `9`; adding all complete
response rows gives rank `10`; adjoining the direction charge
`(2,-1,-1)` at one word gives rank `11`.  The detector constant across the
word square with chart values

\[
                         (A,B,C)=(2,-1,-1)            \tag{6}
\]

kills every old column and reads `6` on the charge.

At coefficient level the missing flat `C4` has two projected mate types
`A+B` and `A+C`.  The rank tests are

```text
base + only A+B: rank 11 -> 12 after the direction charge;
base + only A+C: rank 11 -> 12 after the direction charge;
base + both:     rank 12 -> 12 after the direction charge.
```

Thus neither switch alone fills the class; both are necessary and
sufficient at coefficient level.  These are exactly the two arrows in (1).
All four proposed two-root mate edges change the operation profile, so zero
are literal edges of the existing site-root cobar square.  This is the first
source-label obstruction after the strongest `R01/U_C4/db01` grants.

## 5. What lies downstream if the mixed arrows are supplied

Once the eighteen-term section is physically placed, the labelled descent
reaches word `0102`.  On its twelve occurrence coordinates the primitive
detector

\[
                         d=e_0^*+e_3^*-e_1^*-e_6^*   \tag{7}
\]

kills the complete response and reads `-13/6` on the first private
representative.  The target/`Eq` cone has zero private occurrence
projection.

The presentation-safe relative `P2` graph has

\[
                 d\Gamma_i=t_i-(Cu)_i,
                 \qquad C=12I-J.                    \tag{8}

Annihilating every graph column in (8) forces the carrier covector

\[
                              d_t=Cd=12d.            \tag{9}

On the exact second private preimage its normalized value is `35/72`.  The
`q23` product rule transports that value into the independent `dq23` block.
The best same-labelled primitive-cap cancellation makes the `Q` value zero
but leaves occurrence-labelled ordinary residue

\[
                              -35/72,                \tag{10}
\]

with scalar ordinary residue zero.

The residue calculation is exhaustive **after** its physical hypotheses are
granted.  A complete-response gauge moves every one of the eight labelled
residues to the pure protected-zero `d_even` line, and the aggregate scalar
row cancels the scalar cost.  No new labelled residue direction remains.
The calculation does not construct the occurrence-to-`Q/ores` comparison,
mixed-target square, `d_even` section, or their source labels.

## 6. Conditional exhaustive terminal theorem

The checker forms the direct sum of four exact quotient blocks:

1. the cap--Cartan packet plus both pure targets;
2. the selected `db01` relative graph;
3. the tag-preserving direction square plus complete rows; and
4. the word-`0102` complete-response quotient.

The four detectors are normalized to value one on their selected class.
Adjoin three formal normalized bridges identifying the selected class in
blocks 2--4 with the old balanced class.  Their direct-sum covector kills
every block column and every bridge and reads one on `z`.

This gives a genuine terminal on the resulting exact finite complex.  It
becomes a physical same-grade augmented terminal under the following
precise hypotheses:

1. those four blocks exhaust the selected word/fine/repeated/common-tail
   physical map;
2. the only cross-block columns are the audited normalized
   restriction/reinsertion and relative product-rule columns;
3. `R01/U_C4` and `db01` occur only relatively—there is no absolute carrier
   column;
4. the direction block contains no mixed chart-switch arrow (1); and
5. the lower `P2/Q/ores` block is exactly (8)--(10) plus the committed
   conditional response-gauge/`d_even`/scalar closure.

These hypotheses are stronger than the presently constructed source map.
In particular, hypothesis 2 is the missing cross-grade physical gluing, and
hypothesis 1 is the missing exhaustive same-grade census.  Therefore this
is a sharp conditional terminal, not yet the accepted unconditional
physical terminal.

The first ways to falsify the terminal hypotheses are equally precise:

```text
absolute R01/U_C4 carrier -> top filler;
absolute db01/dc01 face   -> PP filler;
both mixed DQ<->PS arrows -> fills the eighteen-term chart charge;
another unlisted column   -> must be tested against the normalized dual.
```

## Scope and verification

This result is exact for canonical `h=3` over the rationals.  It combines
the literal cap--Cartan/pure packet, 105-occurrence `R01/L01` block, selected
six-term matching PP face, 18-term direction block, word-`0102` occurrence
quotient, and the labelled `dq/Q/ores` calculation.  It does not construct a
complete GHZ source point, the mixed chart-switch bicomplex, or an
unconditional full physical terminal.

Run:

```text
python3 computations/verify_h3_balanced_z_relative_ladder_terminal_gate.py
python3 -O computations/verify_h3_balanced_z_relative_ladder_terminal_gate.py
python3 -I -S computations/verify_h3_balanced_z_relative_ladder_terminal_gate.py
```

Frozen ledger SHA-256:

```text
89b68179775d0677fe50e836ebbcfd02bd46b416ff9dd9cfb939edcec78bc2ef
```
