# Character-twisted translation is a gauge, not a new slice

The search in `computations/search_f3_character_twisted_n8.py` chooses a
sign character \(\chi_c:F_2^3\to\{1,-1\}\subset F_3^*\) for each colour and
writes, on the oriented edge \((u,u+d)\),

\[
 A_{u,u+d}(a,b)=\chi_a(u)\chi_b(u)B_d(a,b),
 \qquad
 B_d(a,b)=\chi_a(d)\chi_b(d)B_d(b,a).
\]

This ansatz is exactly gauge-equivalent to ordinary translation invariance.
Let \(C_d(a,b)=C_d(b,a)\) be arbitrary and, for the stored orientation, set

\[
 B_d(a,b)=\chi_b(d)C_d(a,b).
\]

The signed-transpose relation supplies
\(B_d(b,a)=\chi_a(d)C_d(a,b)\), and character multiplicativity gives

\[
 A_{u,u+d}(a,b)
 =\chi_a(u)\chi_b(u+d)C_d(a,b).
\]

Thus this is the vertex/colour diagonal gauge
\(C_{uv}(a,b)\mapsto\lambda_{u,a}\lambda_{v,b}C_{uv}(a,b)\), with
\(\lambda_{u,a}=\chi_a(u)\).  For a colouring \(c\), every perfect-matching
monomial, hence its coefficient, is multiplied by the same factor

\[
 \prod_{v\in F_2^3}\chi_{c_v}(v).
\]

Mixed target coefficients remain zero.  For a pure colouring of colour
\(c\), the factor is \(\prod_v\chi_c(v)=1\): a nontrivial character is
\(-1\) at four vertices, while the trivial character is identically one.
Consequently the gauge preserves \(\Delta_{8,3}\), and every character
triple gives a SAT instance bijective to the untwisted translation-invariant
instance.  These searches should not be counted as independent slices.

Up to the simultaneous action of \(GL(3,2)\) on characters and \(S_3\) on
colours, the 512 ordered triples have exactly eight classes:

| Representative | Description | Ordered orbit size |
|---|---|---:|
| `(0,0,0)` | three zero characters | 1 |
| `(0,0,1)` | two zero, one nonzero | 21 |
| `(0,1,1)` | one zero, two equal nonzero | 21 |
| `(0,1,2)` | one zero, two distinct nonzero | 126 |
| `(1,1,1)` | three equal nonzero | 7 |
| `(1,1,2)` | exactly two equal nonzero | 126 |
| `(1,2,3)` | three distinct nonzero, rank two | 42 |
| `(1,2,4)` | three independent characters | 168 |

The standalone verifier exhausts all 512 triples, all 168 linear maps, every
edge and ordered colour pair, endpoint reversal, and pure-target preservation:

```text
python computations/verify_f3_character_twist_gauge.py
PASS character_triples=512 classes=8 linear_maps=168 edge_colour_checks=129024 pure_target_checks=8
```

This is an exact statement over \(F_3\).  It neither supplies a
characteristic-zero point nor turns an \(F_3\) search result into one.
