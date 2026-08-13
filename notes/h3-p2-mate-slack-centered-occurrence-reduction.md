# The mate slack is exactly the centered-occurrence face

## Verdict

Augmented `P2` face 1 has not produced a new independent source object.  In
the selected `h=3`, head/word `11:110000` response block, the mate aggregate
`G` satisfies

\[
 \boxed{
 G=\mathbf1_{90}-e_f
   ={89\over90}\mathbf1_{90}-{1\over90}c_f,
 \qquad c_f=90e_f-\mathbf1_{90}.}                    \tag{1}
\]

Therefore, modulo the complete response row,

\[
                  [dG]=-{1\over90}[c_f],
 \qquad [d(u_f-u)]={1\over90}[c_f].                 \tag{2}
\]

The mate-slack conormal is exactly the centered-occurrence descent already
isolated by the scaled anchor bridge.  The committed same-grade complete
response, Cartan/diagonal, word-preserving matching, and head-difference
rows have only the line `Q*1_90` in this block, so they do not fill (2).

Checker:
[`verify_h3_p2_mate_slack_centered_occurrence_reduction.py`](../computations/verify_h3_p2_mate_slack_centered_occurrence_reduction.py).

## 1. Literal expansion of `G`

A response occurrence is a choice of ordered `p,s` endpoint sites and a
perfect matching on the four residual sites.  Thus there are

\[
                         6\cdot5\cdot3=90
\]

terms.  The marked occurrence is

\[
              p_1[0,1]s_1[1,1]q_{23}[0,0]q_{45}[0,0]. \tag{3}
\]

The word stabilizer `S2 x S4` has five occurrence orbits of sizes

```text
6, 12, 24, 24, 24.
```

The marked term lies in the size-six orbit `O`.  Consequently the 89 terms
of `G` split as

```text
5 other terms in O  +  84 terms in O^c.
```

Equation (1) is coefficientwise: it is not an equality only after a
projection or specialization.

## 2. The mate class has two independent symmetry pieces

The centered class has the exact decomposition

\[
 c_f=15(6e_f-\mathbf1_O)
       +(14\mathbf1_O-\mathbf1_{O^c}).                \tag{4}
\]

Hence

\[
 G={89\over90}\mathbf1_{90}
   -{1\over6}(6e_f-\mathbf1_O)
   -{1\over90}(14\mathbf1_O-\mathbf1_{O^c}).         \tag{5}
\]

The first nontrivial term is the marked-within-orbit class.  The second is
the orbit-marginal class distinguishing the six-element endpoint/matching
orbit from the other four orbits.  They are independent modulo the complete
row, but one centered source cell can carry both; this is not evidence that
two new generators are necessary.

Two integral covectors expose the two pieces:

- `lambda_local`: coefficient `5` on `f`, `-1` on the other five terms of
  `O`, and zero elsewhere;
- `lambda_marg`: coefficient `14` on `O`, `-1` on `O^c`.

Both kill `1_90`, while

\[
                    \lambda_{local}(G)=-5,
 \qquad             \lambda_{marg}(G)=-14.           \tag{6}
\]

## 3. Complete physical rows do not split the mate aggregate

Every occurrence covers every output site once in the colour prescribed by
`110000`.  Therefore every target-compatible diagonal/Cartan operation has
one common character on all 90 terms.  Word-preserving permutations fix the
complete response sum, so their group-bar boundary on that row is zero.
Response-head differences live in separate complete blocks and project to
multiples of `1_90` in the selected block.

The complete matching/Cartan prism theorem gives the same conclusion in
the matching factor: complete prisms remain in the trivial occurrence
representation and do not create a matching-centered cut.  Thus the total
committed same-grade image is

\[
                         \mathbf Q\mathbf1_{90}.      \tag{7}
\]

Since `G` is absent already after forgetting fine and repeated labels, it
cannot be present in the stricter literal grade through these operations.

## 4. Boundary target and terminal status

The smallest positive cell remains one same-grade centered occurrence
comparison with occurrence boundary `c_f`.  The raw coefficient projector
is not source-valid: normalized at `f(x)=1`, its scalar zero-face is

\[
                            90f(x)=90.                \tag{8}
\]

So the physical cell must carry a scalar/target face `-90f(x)`, together
with the word/fine/repeated and augmented readouts.  Once constructed, (2)
fills the pointed face with coefficient `1/90`.

The covectors in (6) are exact occurrence-module separators, not physical
terminals.  They select monomials inside a complete source polynomial and
have not been identified with the physical `q`, anchor, target, word,
ridge, eta/sigma, or `W` rows.  After a source-valid augmented centered cell
exists, the already proved physical kernel-versus-Fredholm alternative is
exhaustive; before then, declaring either covector a terminal would be a
typing error.

## Frontier

The face-1 core is now one object:

> Construct the same-grade centered occurrence cell
> `c_f=90e_f-1_90`, including its scalar/target face and complete physical
> augmentations; or physically type its first nonlift in the augmented
> comparison cone.

This is simultaneously the mate-slack lift, pointed-anchor lift, and scaled
occurrence descent.  No separate `dG` theorem remains.

Run:

```text
python3 computations/verify_h3_p2_mate_slack_centered_occurrence_reduction.py
python3 -O computations/verify_h3_p2_mate_slack_centered_occurrence_reduction.py
python3 -I -S computations/verify_h3_p2_mate_slack_centered_occurrence_reduction.py
```

Frozen ledger SHA-256:

```text
1dca6416efb9719641eaae2a4869c4e4f922dc321a432ccff2d9dbe873f839c0
```
