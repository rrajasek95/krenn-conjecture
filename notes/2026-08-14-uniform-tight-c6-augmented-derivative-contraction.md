# A tight-cut escape either deletes through the cap span or is an active outside channel

## Result

The physical derivative theorem of `c8bc02f` and the complete `C6` rank
calculation of `474d5ce` combine into a uniform source-level criterion.

Let `J` be the live endpoint-decorated cells of a physically tight cut and
let `C subset J` be the live cells in the selected cap block.  If a forced
pure escape crosses the cut through `j in J-C`, compare its **complete**
physical derivative `D_j` with

\[
                     S_C=\operatorname{span}\{D_c:c\in C\}              \tag{1}
\]

in all `3^N` coefficient rows, not merely in a pure projection or a free
label module.

* If `D_j in S_C`, joint tight-cut linearity gives an exact affine move
  deleting `j` and preserving every pure and mixed output row.
* If `D_j notin S_C` and its pure derivative coordinate is nonzero, `j` is
  a literal active outside boundary channel.  If instead a nonzero mixed
  coordinate is a private occurrence, the exact mixed row is a source unit.

For the seven-cell `C6` packet the complete cap span has rank zero after the
forced residual equation, while every one of the twelve minimal escapes
raises rank to one.  On the tight shore `{3}`, its unique outside cut cell
has exactly one pure-one cofactor occurrence and no mixed derivative
coordinate.  Thus the packet takes the active-outside branch uniformly; the
three killed cap cells, not the escape, delete.

The checker is
[`verify_uniform_tight_c6_augmented_derivative_contraction.py`](../computations/verify_uniform_tight_c6_augmented_derivative_contraction.py).

## 1. Uniform physical criterion

Let

\[
                         V_N=\mathbb Q^{\{0,1,2\}^N}.                    \tag{2}
\]

For a tight cut, every compatible perfect matching contains exactly one live
cut cell.  Grouping the literal matching expansion by that cell gives

\[
                       \Delta=\sum_{i\in J}q_iD_i,                      \tag{3}
\]

where `D_i in V_N` is the complete physical derivative with respect to
`q_i`.  Tightness is what makes every `D_i` independent of all cut
coefficients simultaneously.

Suppose the forced escape contribution to the pure word `b^N` is nonzero:

\[
                  E_b=\sum_{i\in J-C}q_i(D_i)_{b^N}\ne0.                \tag{4}
\]

Then at least one literal live outside cell `j` satisfies

\[
                         q_j(D_j)_{b^N}\ne0.                            \tag{5}
\]

No occurrence projector is used: (4) is the physical partition of a
complete coefficient row by its unique tight-cut cell.

Assume first that

\[
                         D_j=\sum_{c\in C}a_cD_c.                       \tag{6}
\]

Define

\[
 q'_j=0,\qquad q'_c=q_c+q_ja_c\quad(c\in C),\qquad
 q'_i=q_i\quad(i\notin C\cup\{j\}).                                   \tag{7}
\]

Equations (3), (6), and (7) give

\[
                         \sum_iq'_iD_i=\sum_iq_iD_i=\Delta.             \tag{8}
\]

No new decorated cell is introduced, while the occupied cell `j` is removed.
Some cap coefficients may also become zero.  Hence (7) is an exact
source-level support deletion at fixed order.

If (6) fails, `[D_j]` is a nonzero physical state in `V_N/S_C`.  Condition
(5) gives it a live normalized pure channel.  This is the precise
active-outside alternative.  It is stronger than a formal labelled
transfer state and weaker than an active **clean cap**: the latter still
requires a private or common-cofactor landing theorem.

In a support-minimal exact source, (6) is impossible.  Therefore every
forced pure escape uses a physically independent outside channel, and every
zero or dependent live cap derivative is itself support-deletable.  This
turns the rank of the complete cap derivative module into the correct
monotone, replacing local cell count.

## 2. Exact dependent-span branch

The checker includes a physical four-site local source showing (7) directly.
Across the tight shore `{0}`, take

```text
q01;00 =  2,   q23;00 = 1,
q02;00 = -1,   q13;00 = 1.
```

The two matching contributions are `2 e_0000` and `-e_0000`, so the complete
tensor is `e_0000`.  The two cut derivatives agree on all 81 rows:

\[
                         D_{01;00}=D_{02;00}=e_{0000}.                  \tag{9}
\]

The move

```text
q01;00' = q01;00 + q02;00 = 1,
q02;00' = 0
```

deletes one occupied cell and leaves all 81 coefficients unchanged.  This is
the positive span branch of the theorem, realized in the actual matching
polynomial rather than an abstract matrix.

## 3. Complete augmented `C6` matrix

Use cap `34`, residual edges

```text
core  05|12,
mate  01|25,
```

and the exact residual specialization

\[
                       H=1-1=0.                                       \tag{10}
\]

Take the one-vertex shore `{3}`.  It is tight for every perfect matching.
For each of the twelve matchings avoiding `34`, the live cut cells are
exactly

```text
34;00, 34;11, 34;22,
one colour-one escape edge incident with site 3.                        (11)
```

The complete output space splits into the three pure rows

```text
000000, 111111, 222222
```

and 726 mixed rows.  Direct expansion gives, in every case,

\[
 \operatorname{rank}(D_{34;00},D_{34;11},D_{34;22})=0,                 \tag{12}
\]

and

\[
 \operatorname{rank}(D_{34;00},D_{34;11},D_{34;22},D_j)=1.            \tag{13}
\]

The pure projection of `D_j` is `(0,+/-1,0)`, its 726-coordinate mixed
projection is zero, and multiplication by the actual cut-cell coefficient
always makes its `111111` value `1`.  Moreover that derivative entry contains
exactly one literal cofactor occurrence: the chosen escape matching itself.

Thus none of the twelve escapes is in the cap span.  Each is a literal active
outside channel.  Conversely all three cap columns are zero, so setting

\[
                     q_{34}^{00}=q_{34}^{11}=q_{34}^{22}=0             \tag{14}
\]

preserves all 729 output rows.  This is the exact support deletion already
visible in `474d5ce`, now placed in the uniform tight-cut criterion.

There are four possible outside cut cells among the twelve fine matchings:

```text
03;11, 13;11, 23;11, 35;11.
```

Fine matching, cap, shore, operation, and decorated cut-cell labels are
retained in every record.

## 4. Full-GHZ sharpness control

No full-GHZ counterguard to the criterion occurs.  The smallest nontrivial
exact target instead demonstrates that its outside alternative is necessary.
On the exact ternary `K4` one-factor source from `c8bc02f`, the three tight-cut
derivatives across `{0}` have pure projection `I_3` and rank three.  Removing
any chosen column leaves rank two, while the selected column has a private
pure word.

Hence no derivative deletes, but every derivative is a literal essential
active outside channel.  This refutes any stronger claim that pure
normalization alone forces deletion, while satisfying the span-or-active
criterion exactly.

## 5. Scope and remaining bridge

The theorem is uniform in the order, cut size, coefficient field, and number
of companion matchings, provided the cut is genuinely tight and derivatives
are compared after full physical augmentation.  It allows arbitrary
cancellation and does not require diagonal cells.

It does **not** contract two physical sites or show that every active outside
channel is a clean cap.  After the `C6` packet takes the outside branch, the
remaining structural problem is narrower:

> prove that an independent outside tight-cut channel has a private/common
> cofactor landing, or that its mixed companions contain a literal unit or
> lower the terminal-component rank/potential.

That is a boundary-state routing problem.  The coefficient-support deletion
part is now complete and needs no parent occurrence selector.

## Verification

```text
python3 computations/verify_uniform_tight_c6_augmented_derivative_contraction.py --mode structural
python3 -O computations/verify_uniform_tight_c6_augmented_derivative_contraction.py --mode full
python3 -I -S computations/verify_uniform_tight_c6_augmented_derivative_contraction.py --mode exhaustive
```

All modes have frozen ledger SHA-256
`99e2c0b7f8e67de0ca3b2b5038ec23437959968831b84154c6995c36ddbc0399`.
