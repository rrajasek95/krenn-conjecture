# The shifted order-two placement first fails on an occurrence-private Hasse face

## Outcome

Fix the literal lower cut

```text
sites                 0,1,4,5,
word                  0112,
residual              q45:12,
reinsertion           q23:21,
top grade             01211222 / repeated P3+K2.
```

The universal two-root Cartan/principal-parts square is source-valid on
this packet. It does not, however, map the exact endpoint-even `B-4`
preimage into the already constructed target/reduced-Eq three-term cone.
Its first one-root Hasse faces retain nonconstant coefficients on the twelve
ordered endpoint occurrences. Those coefficients survive modulo the
complete response row in their intermediate words.

The first missing physical datum is therefore an occurrence-local,
endpoint-even, one-endpoint principal-parts section. It occurs before any
remaining target or reduced-Eq normalization. The mixed-target Cartan cone
and the reduced-Eq Koszul face cannot cancel it because both have zero
projection to this occurrence-private word block.

Checker:
[verify_h2_p2_0112_one_endpoint_hasse_placement_gate.py](../computations/verify_h2_p2_0112_one_endpoint_hasse_placement_gate.py).

## 1. The exact lower input

Let `V` be the twelve-dimensional occurrence module on

\[
             (p,s;\text{the complementary residual edge})
\]

for four sites. Let `S` reverse the two endpoint roles and let `B` be
endpoint adjacency. For the marked occurrence `f=(0,1;45)`, put

\[
 c^+=6(e_f+e_{Sf})-\mathbf 1.
\]

The exact even preimage used by the lower proof is

\[
 z=-{1\over24}(B+6I)c^+,
 \qquad (B-4I)z=c^+,
 \qquad Sz=z.                                         \tag{1}
\]

Thus no coefficient inversion or endpoint-parity issue remains at this
stage.

## 2. The complete one-root Hasse boundary

For an occurrence `(p,s;{r,t})`, move one endpoint to one residual site.
When their colours differ, the physical word-returning path contains the
two-site colour Weyl action. Its principal-parts boundary has two one-root
faces: change the endpoint colour only, or change the selected residual
colour only. A colour root does not move the sites, so each face retains its
ordered occurrence label.

Summing these faces with the coefficients of (1) gives eight intermediate
words:

| word | contributing faces | coefficient sum | nonzero occurrences |
|---|---:|---:|---:|
| `0012` | 8 | `4/3` | 8 |
| `0102` | 8 | `-2/3` | 8 |
| `0110` | 8 | `-2/3` | 8 |
| `0111` | 16 | `2/3` | 12 |
| `0122` | 8 | `4/3` | 8 |
| `0212` | 8 | `-2/3` | 8 |
| `1112` | 16 | `2/3` | 12 |
| `2112` | 8 | `-2/3` | 8 |

The complete response equation in any fixed word has occurrence vector
`1=(1,...,1)`. Every vector in the table is nonconstant. Hence, separately
in every word,

\[
 \operatorname {rank}\langle\mathbf1,r_w\rangle=2.   \tag{2}
\]

Putting the eight words in distinct blocks, the eight complete response
rows have rank eight, while adjoining the actual Hasse faces raises the rank
to sixteen. Thus the displayed three-term cone misses eight word-labelled
private classes before symmetry identifications.

## 3. A representative exact obstruction

In the canonical occurrence order

```text
(01;23),(02;13),(03;12),(10;23),(12;03),(13;02),
(20;13),(21;03),(23;01),(30;12),(31;02),(32;01),
```

the intermediate word `0102` carries

\[
\begin{aligned}
r_{0102}=(&-13/12,0,1/6,-13/12,1/6,0,\\
          &0,1/6,5/12,1/6,0,5/12).                  \tag{3}
\end{aligned}
\]

This vector is endpoint-even. The primitive endpoint-even coordinate
covector

\[
                  \lambda=e_0^*+e_3^*-e_1^*-e_6^*   \tag{4}
\]

kills the complete row and satisfies

\[
                  \lambda(r_{0102})=-13/6.           \tag{5}
\]

Equations (3)--(5) are a literal source-presentation obstruction. The
covector is not yet a physical Fredholm terminal: it has only been extended
over the complete response, target, and reduced-Eq cone, not over the full
physical augmented source map.

## 4. Why the target/Eq triangle does not finish `P2`

The order-two diagonal identity and even Cartan cell already provide the
mixed target correction. The root-decorated Koszul/Spencer cell then
cancels its reduced-Eq face. In the projected rows their three columns form
the closed triangle

```text
lower endpoint path       target N       Eq 0,
even Cartan cone          target -N      Eq -N,
Koszul/Spencer face       target 0       Eq +N.
```

But the latter two columns have no occurrence coordinate in the word
`0102`. Therefore (5) survives unchanged after the target and Eq rows close.
Target equality cannot define the shifted source placement.

The smallest new column is a one-endpoint principal-parts section whose
boundary cancels (3) modulo the complete response row, with its root-word
translates. It must remain endpoint-even and must carry the literal
word/fine/repeated-grade data. Reinsertion by `q23:21` then invokes a further
Hasse product-rule face; that face is audited separately rather than being
silently omitted here.

## Scope

This is an exact one-cut, full twelve-occurrence calculation. The second
cut is its transport by `sigma=(2 5)(3 4)`. The result does not rule out the
needed principal-parts section, nor promote (4) to a terminal. It identifies
the first absent physical column in a construction of `P2`.

Run:

```text
python3 computations/verify_h2_p2_0112_one_endpoint_hasse_placement_gate.py
python3 -O computations/verify_h2_p2_0112_one_endpoint_hasse_placement_gate.py
python3 -I -S computations/verify_h2_p2_0112_one_endpoint_hasse_placement_gate.py
```

Frozen ledger SHA-256:

```text
9d3462fee3f24b2a73368f831240dbe6adedab8109c8716f928849b54ea8d323
```
