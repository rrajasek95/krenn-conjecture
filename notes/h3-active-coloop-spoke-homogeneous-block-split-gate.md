# Rank two reaches homogeneous blocks, but need not produce a private row

## Exact block classification

Fix the pure-zero coloop `01` and the three spokes

```text
x=(q23[00],q24[00],q25[00]).
```

In a response coefficient with output word `w`, the spoke `q2j[00]` can
occur only if

```text
w2=wj=0.
```

Endpoint choices and coefficient cancellation can shrink this structural
support, but cannot enlarge it.  Among all `3^6=729` output words, the
eligible spoke-mask sizes are

| eligible spokes | words |
|---:|---:|
| 0 | 558 |
| 1 | 108 |
| 2 | 54 |
| 3 | 9 |

For each fixed response head the same table applies.  A complete response
coefficient contains `15` direct `d*q^3` occurrences and `90` ordered
endpoint `p*s*q^2` occurrences.  No occurrence contains two selected
spokes: they all meet site `2`.  Thus every fine occurrence is a singleton
in `x`, but the physical source row is the **sum** of its `105` possible
occurrences.  A fine monomial tag cannot be used as a coefficient equation.

Checker:
[verify_h3_active_coloop_spoke_homogeneous_block_split_gate.py](../computations/verify_h3_active_coloop_spoke_homogeneous_block_split_gate.py).

## What quotient rank two does force

Let `T=<y>` be the target line in the three-spoke restriction space.  Split
the complete response rows into their literal word/head/fine blocks.  If

\[
 \dim\frac{T+\sum_B\operatorname{im}M_B}{T}=2,       \tag{1}
\]

then exactly one of the following holds.

1. Some homogeneous block already has quotient image of dimension two.
2. At least two homogeneous blocks contribute distinct nonzero quotient
   lines.

Consequently the transverse signal cannot be invisible in every block.
There is always a literal homogeneous row not proportional to the target
row.  This is the strongest promotion that follows from rank alone.

Neither alternative forces a singleton/private coefficient.  In the second
alternative each block can contain only a two-occurrence cancellation, and
combining the two transverse lines mixes output words.

## Smallest literal split counterguard

The failure of private promotion occurs in the physical response
polynomials, not only in an abstract matrix.  Put

```text
alpha=q01[00]=1
x=(q23[00],q24[00],q25[00])=(1,1,-1)
y=(q45[00],q35[00],q34[00])=(1,1,1)

q13[00]=-1, q14[00]=1, q15[00]=1
p2[5,1]=p2[3,1]=s1[0,0]=1
```

and set every other displayed endpoint/direct cell to zero.  Site `0` has
only the pure edge `01`, so every nonzero pure-zero target matching contains
the coloop.  Its cofactor is normalized:

\[
                    x\mathbin{\cdot}y=1+1-1=1.       \tag{2}
\]

The full `729`-word/four-head restriction scan has precisely two nonzero
response rows:

\[
\begin{aligned}
 D_xR_{21}[000001]&=(1,-1,0),\\
 D_xR_{21}[000100]&=(0,1,1).
\end{aligned}                                       \tag{3}
\]

Both coefficients vanish at `x=(1,1,-1)`.  Their literal occurrence sums
are

```text
R21[000001]:
  p2_5[1] s1_0[0] q23[00] q14[00]
 +p2_5[1] s1_0[0] q24[00] q13[00] = 1-1=0;

R21[000100]:
  p2_3[1] s1_0[0] q24[00] q15[00]
 +p2_3[1] s1_0[0] q25[00] q14[00] = 1-1=0.
```

Together with the pure target row `y=(1,1,1)`, the rows in (3) have rank
three, so their quotient rank is two.  Nevertheless:

```text
used word blocks                         2
local quotient rank in each block       1
fine spoke occurrences                  4
private response coefficients           0
```

This is sharp.  One scalar word/head row contributes at most one quotient
dimension, so a split rank-two packet needs at least two blocks.  If neither
row is private, each needs at least two spoke incidences.  The guard attains
both lower bounds.

The guard is a literal restriction packet, not a complete GHZ source.  It
does not impose the other constant-colour target normalizations or the
augmented anchor/ridge equations.  It is sufficient to disprove the formal
implication from evaluated quotient rank two to a private coefficient.

## Hall and four-good scope

All four residual `q` tails in (3) are pure `[00]`, and the displayed
endpoint cells are diagonal in their response heads.  Thus the
target-augmented offdiagonal private-site identity does not fire merely from
this packet.  The endpoint holes
are

```text
05 and 03,
```

both contained in the closed star at `0`.  Hence this packet alone supplies
neither

```text
an offdiagonal base-q cell for the private-site/four-good theorem, nor
an endpoint hole outside the current closed Hall shore.
```

Each displayed response coefficient already has two cancelling
occurrences.  Its zero equation therefore forces no new matching mate.  The
special processor of `93cf9ae`, which begins with the private rows

```text
R11[110000], R11[110011], R11[111100],
```

does not apply to (3).

## Sharp remaining theorem

The missing statement is now a block-synchronization theorem, not another
affine integration argument:

> Given two target-zero homogeneous word/head blocks whose spoke
> restrictions span the target quotient, either one complete coefficient is
> private modulo the closed shore and enters the `93cf9ae` processor, or the
> two cancellations admit a source-valid common-word Hasse/Cartan comparison
> that gives a typed outside-shore, four-good, or augmented-terminal exit.

The exact deletion theorem `4f7f104` already handles a common kernel of all
blocks.  What remains is to compare independent transverse lines that live
in different physical words without performing an illegal row reduction
across those words.

Run the checker normally, optimized, and isolated/no-site.  Its frozen
ledger digest is recorded in the script.
