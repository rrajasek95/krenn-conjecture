# Hyperbolic root squares do not yet totalize physically

## Outcome

The two opposite-root identities of
[`a29eb69`](h3-balanced-c4-hyperbolic-root-return-gate.md) do not yet give a
physical relative Tate/cobar pair.  Restoring the complete response row
exposes an earlier face than the proposed `P2` landing: each formal root
leaves a signed 24-term collision splitter in its 45-term collision sector.
The existing collision cell is the symmetric 45-term row and cannot absorb
that splitter.  An exact centered functional kills the symmetric row and
reads one on the splitter.

Even if four such response-naturality cells are granted, the two root orders
are not flat on the complete unary row.  In each square their difference is
the selected three-of-fifteen block

\[
q_{01}H_{2345}.
\]

The two squares contribute this face with the same sign.  Thus they produce
`2*q01*H2345`, not a cancellation.  A second exact centered functional kills
the complete 15-term unary row and reads one on this selected block.

The full first-principal-parts census confirms that the lower topologies are
present, but not with the required physical types.  The first forward
`P3+K2` cofactor has operation type `DSQ`; the varied pair `DS` is absent
from the committed `DQ/PS/QQ/PQ/SQ` lower packet.  The reverse cofactor has
type `PQQ` and the associated-graded topology of `P2`, but remains in the
response word/fine degree rather than the canonical cap word/fine degree.
Consequently no existing collision, `P3+2K2`, or `P2` cell closes the two
root squares without an additional physical comparison.

Exact checker:
[`verify_h3_hyperbolic_root_collision_tate_cobar_totalization_gate.py`](../computations/verify_h3_hyperbolic_root_collision_tate_cobar_totalization_gate.py).

## The four roots in the complete response

Use the eight vertices

```text
P, S, 0, 1, 2, 3, 4, 5
```

and the operation edges

```text
D=PS, p0=P0, p1=P1, q01=01, s1=S1, s0=S0.
```

The four formal root derivations used in the coefficient identity are

```text
E01: p0 -> D,  q01 -> -s1
E02: p1 -> D,  q01 -> -s0
E10: D  -> p0, s1  -> -q01
E20: D  -> p1, s0  -> -q01.
```

On the selected chart monomial `A=D*q01*H2345`, their first faces are

```text
E01(A) = -D*s1*H2345,    E02(A) = -D*s0*H2345,
E10(A) =  p0*q01*H2345,  E20(A) =  p1*q01*H2345.
```

Each displayed block has three tail matchings.  It is not, however, the
derivative of the complete 105-matching response.  For example,
`-D*s1*H2345` from `E01(D*q01*H2345)` cancels term by term with
`+D*s1*H2345` from `E01(p0*s1*H2345)`.  The same adjacent-chart cancellation
holds for all four selected blocks.

After those cancellations, each six-coordinate root has exactly 24
remaining collision monomials: twelve with coefficient `+1` and twelve with
coefficient `-1`.  All lie in the appropriate 45-coordinate missing/doubled
sector:

| root | missing vertex | doubled vertex | selected chart face |
|---|---:|---:|---|
| `E01` | `0` | `S` | `-D*s1*H2345` |
| `E02` | `1` | `S` | `-D*s0*H2345` |
| `E10` | `S` | `0` | `+p0*q01*H2345` |
| `E20` | `S` | `1` | `+p1*q01*H2345` |

Write `C` for the complete symmetric collision vector, whose 45 entries all
have coefficient two, and `R` for the signed 24-term residual.  On the same
45 coordinates the functional

\[
\lambda_R=R/24
\]

satisfies

\[
\lambda_R(C)=0,\qquad \lambda_R(R)=1.
\]

Therefore the committed complete collision row and the required root
splitter are linearly independent.  A presentation-safe relative graph
`t_R-R` raises both the coordinate count and boundary rank by one, preserving
the sector value `H0=44`; it does not supply an absolute preimage of `R`.

This is the first missing typed face.  It can be repaired only by a
source-labelled cell whose boundary is this signed residual, or by extending
the root to the omitted incident-edge coordinates so that the residual
cancels.  Merely retaining the symmetric `P3+2K2` collision top does neither.

## Unary and opposite-root-order boundary

Let `U` be the complete 15-matching unary row on vertices
`0,1,2,3,4,5`.  Direct calculation gives

\[
E_{01}(U)=-s_1H_{2345},\qquad
E_{02}(U)=-s_0H_{2345},
\]

while `E10(U)=E20(U)=0`.  Hence

\[
E_{10}E_{01}(U)=q_{01}H_{2345},\qquad
E_{01}E_{10}(U)=0,
\]

and likewise

\[
E_{20}E_{02}(U)=q_{01}H_{2345},\qquad
E_{02}E_{20}(U)=0.
\]

Thus the two orders of either hyperbolic square disagree on the unary row.
The common defect is not the complete unary generator: it consists of the
three matchings containing `q01`.  On the 15 unary coordinates, the
functional with value `1/3` on those three matchings and `-1/12` on the
other twelve satisfies

\[
\lambda_q(U)=0,\qquad
\lambda_q(q_{01}H_{2345})=1.
\]

As at the response stage, a relative graph
`t_q-q01*H2345` preserves `H0=14` but retains the centered class.  A physical
occurrence-local Cartan/restriction cell, or an absolute preimage of the
retained `t_q`, is still required.

## Complete and selected PP families

Every complete 45-term collision sector has 180 labelled first-PP flags:

```text
90 of topology 3K2
90 of topology P3+K2.
```

The `3K2` flags split into six complete 15-matching unary cofactor rows,
indexed by the removed edge at the doubled vertex.  The `P3+K2` flags split
into fifteen six-term repeated-edge rows, indexed by the removed edge away
from the doubled vertex.  Across all four roots this is a literal family of
720 distinct flags: 360 of each topology.  In the two reverse sectors,
deleting `p0` or `p1` does expose the physical six-site unary row, but its
derivative and occurrence labels are not thereby forgotten.

The four selected three-term collision blocks have twelve flags apiece:
six `3K2` and six `P3+K2`.  All 48 are distinct once the root and removed
edge are retained.  Their lower typing is:

* Forward `-D*s_i*H2345`: deleting a tail edge leaves a `DSQ` cofactor.
  Its `DS` operation pair is not a committed lower idempotent, so no current
  `P2` packet receives it.
* Reverse `p_i*q01*H2345`: deleting a tail edge leaves a `PQQ` cofactor.
  This has the associated-graded `P2` topology, but the collision response
  word is `11:110000`, whereas the canonical cap word is `01211222`.  The
  word/fine mapping cylinder, reduced-Eq face, and shifted ridge remain
  unconstructed.

Topology alone therefore does not totalize the boundary.  The operation,
root, removed-edge, response-word, and fine labels are essential.

## Shortest remaining positive datum

The shortest constructive attack is ordered by where the exhaustive audit
first fails:

1. Give one source-natural formula for the signed 24-term response residual
   of a root, equivariant under the two root pairs.  Equivalently, extend the
   terminal/root action to all omitted cross edges and prove that the
   residual vanishes in the complete response.
2. Show that the same construction supplies the selected-unary return
   `q01*H2345` with opposite-root-order coherence.  The two current squares
   reinforce this face, so it cannot be discarded by pairing them.
3. Add the first genuinely new lower typed comparison: a `DSQ` restriction/
   insertion cell for the forward tail.  Then transport the reverse `PQQ`
   tail through an explicit response-to-cap word/fine cylinder.

Without item 1 there is no physical root square to totalize.  Without item
2 its unary boundary is not closed.  Existing `P3+2K2/P2` cells become
relevant only after both earlier conditions are met.

## Verification

Run

```text
python3 computations/verify_h3_hyperbolic_root_collision_tate_cobar_totalization_gate.py
python3 -O computations/verify_h3_hyperbolic_root_collision_tate_cobar_totalization_gate.py
python3 -I -S computations/verify_h3_hyperbolic_root_collision_tate_cobar_totalization_gate.py
```

The checker freezes the four complete-response residuals, both unary
commutators, all 720 complete and 48 selected labelled PP flags, the exact
centered separators, and the relative-graph `H0` ranks.

Frozen ledger digest:

```text
369c13561001f6dc4f1f18e1c1dd8543549cec346ebd7fb2f047c1f3ef85d7d4
```
