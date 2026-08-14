# Complete-response private caps at support 16

## Result

Privacy must be tested in every literal cap response, not only in the
minimum two-RRX face that created the old directed-incidence register.  This
simple extension gives 110 additional active-clean exits, representing 153
of the 351 incidences left by the first two-cap classifier.

Together with the already proved two-cap route and the pure-normalization
closure of the sole same-colour collision, the 281-orbit register partitions
as follows.

| route | stabilizer orbits | directed incidences |
|---|---:|---:|
| forced distinct two-cap | 22 | 25 |
| complete private cap | 110 | 153 |
| pure-normalization collision exit | 1 | 1 |
| unresolved, at most one original prototype | 148 | 197 |

The final 148 split into 85 with no original prototype face and 63 with one.
This is the current finite frontier before enlarging the two-cap criterion to
all two-monomial residues.

The exact audit is

```text
python3 computations/verify_n8_support16_complete_private_cap_extension.py
python3 -O computations/verify_n8_support16_complete_private_cap_extension.py
python3 -I -S computations/verify_n8_support16_complete_private_cap_extension.py
```

## Uniform algebra lemma

Let `X` be a directed ternary source-star block occurring at endpoint `p` of
a physical cap `pq`.  Suppose every fully oriented monomial of the complete
cap response contains `X`.  Equivalently, the response lies in the
source-star contraction ideal `I_X`; this is the literal, source-labelled
meaning of a complete private cap.

Write the noncoordinate vector of `X` as `w`, whose support has size at least
two.  For every column `j`, choose a pivot

```text
p_j in supp(w),  p_j != j when j is in supp(w),
```

and set

```text
K_jj     = w_pj,
K_pj,j  += -w_j,
all other entries = 0.
```

Then column by column

```text
w^T K = 0,
```

while each diagonal entry `K_jj=w_pj` is nonzero on the chart.  If `X`
occurs at the right cap endpoint, transpose the construction to obtain
`K w=0`.  Thus every response monomial is killed through its literal `X`
factor while all three diagonal cap readouts stay active.

The checker verifies all four noncoordinate support charts and both endpoint
sides, for eight exact symbolic charts total.  No common-covector or
cross-cap identification is used.

## Finite support-16 census

Among the 259 same-colour-completion guards from the earlier classifier:

- 105 orbits have one complete private face;
- 5 orbits have two complete private faces.

The 115 physical private faces have expanded sizes

```text
 2 terms : 19 faces
 4 terms : 52 faces
 6 terms : 23 faces
 8 terms : 20 faces
10 terms :  1 face.
```

For each face the checker reconstructs the actual support graph, cap edge,
directed occurrence, factor-level response terms, and every oriented
source-star monomial.  It then verifies that every expansion contains the
same directed `X` and that the star-zero residue is literally empty.

## Scope and leverage

The algebra lemma is independent of support size: at higher support, any
complete cap response lying in one noncoordinate source-star ideal lands in
exactly the same way.  Only the counts `110/153` are special to the present
support-16 census.

The remaining obstruction is therefore sharper than “the chosen minimum
face was not private.”  A genuine survivor must have a nonzero companion
residue in every cap that sees the directed block, and—after the original
two-cap theorem—has at most one `(2 target, 2 companion)` prototype face.
The next useful generalization is to retain every crossed two-monomial
residue regardless of how many target-containing expansions accompany it.
