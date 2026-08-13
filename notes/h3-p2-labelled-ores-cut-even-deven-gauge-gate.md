# Every two-cut `P2` residue reduces to `d_even` after the complete-response gauge

## Verdict

After a same-labelled primitive cap cancels the `dq23` face of a pointed
occurrence square, its tied labelled ordinary-residue face is not literally

\[
                         d_{\rm even}={B_1+B_4\over2}.
\]

For each of the eight first-root word blocks, collapse the twelve ordered
occurrences to the six endpoint-hole labels and average the two physical
cuts by

\[
              \tau_B=(B_0\ B_5\ B_3\ B_2)(B_1\ B_4).
\]

Every result lies on the single line

\[
 \delta_+={B_1+B_4\over2}
       -{B_0+B_2+B_3+B_5\over4}.                    \tag{1}
\]

Thus bare `d_even` does not cancel the raw residue.  The important positive
point is that `dq23` cancellation is required only modulo the complete
response row.  If a word has residue `k delta_+`, replace its primitive-cap
coefficient `z` by

\[
                         z+{k\over8}{\bf1}_{12}.       \tag{2}
\]

Since the collapse of `1_12` is `2*1_6`,

\[
 k\delta_+ + {k\over4}{\bf1}_6
                  ={3k\over2}{B_1+B_4\over2}.        \tag{3}
\]

The `Q` cost of (2) is a complete response row, the labelled-residue face
in (3) is canceled by `(3k/2)d_even`, and the scalar-residue cost is canceled
by the existing aggregate scalar row.  Consequently, conditional on the
pointed occurrence family, same-labelled `p`, `d_even`, and the already
required mixed-target square, **no fourth labelled-residue source type is
needed for `P2`**.

Checker:
[`verify_h3_p2_labelled_ores_cut_even_deven_gauge_gate.py`](../computations/verify_h3_p2_labelled_ores_cut_even_deven_gauge_gate.py).

## 1. The eight exact residues

The six labels are the unordered endpoint holes

```text
B0=02, B1=01, B2=03, B3=13, B4=23, B5=12.
```

For each first-root face, project off its complete response line, apply the
exact inverse of `B-4` on the endpoint-even private `0,-2` eigenspaces, and
collapse the two endpoint orientations.  After cut averaging, the result is
`k delta_+` with

| word | `k` | gauge `k/8` | `d_even` coefficient `3k/2` |
|---|---:|---:|---:|
| `0012` | `2/27` | `1/108` | `1/9` |
| `0102` | `5/27` | `5/216` | `5/18` |
| `0110` | `5/27` | `5/216` | `5/18` |
| `0111` | `7/27` | `7/216` | `7/18` |
| `0122` | `2/27` | `1/108` | `1/9` |
| `0212` | `5/27` | `5/216` | `5/18` |
| `1112` | `7/27` | `7/216` | `7/18` |
| `2112` | `5/27` | `5/216` | `5/18` |

The three unmarked `V4` orbit sums are

```text
O_211 = {0012,0102,0122,0212}:  (14/27) delta_+
O_220 = {0110,2112}:            (10/27) delta_+
O_310 = {0111,1112}:            (14/27) delta_+.
```

The all-eight sum is `(38/27)delta_+`; its total response gauge is `19/108`
and its total `d_even` coefficient is `19/9`.

This is stronger than an orbitwise dimension count: every literal word
coefficient and every rational normalization is fixed.

## 2. Why bare `d_even` fails

Put

\[
 v={B_1+B_4\over2},\qquad
 w={B_0+B_2+B_3+B_5\over4}.
\]

Then `delta_+=v-w`.  The primitive covector

\[
                 \lambda_{\rm out}=B_0^*+B_2^*+B_3^*+B_5^*
\]

kills `v` and both committed Cartan residue lines `alpha,alpha'`, but reads
`-1` on `delta_+`.  Hence neither `d_even` alone nor its Cartan translates
cancel the raw residue.

The escape is not a new labelled section.  The exact identity

\[
                  \delta_+={3\over2}v-{1\over4}{\bf1}_6       \tag{4}
\]

shows that only the labelwise diagonal is missing.  In this particular
`P2` problem the diagonal is supplied for free as the collapse of the
complete response gauge in (2).  This use is source-faithful only after the
pointed occurrence/complete-response comparison is granted; it is not a
claim that an arbitrary labelwise diagonal residue section exists.

## 3. Full sign and augmented-face calculation

Let the original `dq23` coefficient be `z`, and let its cut-even collapsed
residue be `k delta_+`.  Use the primitive cap with coefficient
`z+(k/8)1_12`.  Since `p_Q=p_ores=-1`, the faces are

```text
Q:        +z -(z+(k/8)1_12) = -(k/8)1_12,
labelled ores:              -(3k/2)v,
scalar ores:                -3k/2.
```

The first line is a complete response row.  Add `(3k/2)d_even` to cancel
the second.  If scalar and labelled residue are retained as independent
augmented rows, add `(3k/2)d_ores` to cancel the third.  The latter is the
already available aggregate scalar correction, not a labelled section.

All added columns are target/protected zero under the hypotheses.  The
mixed-target proper faces still have to be supplied by the labelled Hasse
square isolated earlier; the present calculation does not manufacture that
square.

## Conditional `P2` closure

For the labelled-residue stage, the following inputs suffice:

1. a pointed occurrence/global `P_f` family in the required fixed grades;
2. the same-labelled `p_Q/p_ores` cap family;
3. complete response rows with their `q23` principal-parts translates;
4. the pure protected-zero `d_even` section;
5. aggregate scalar ordinary residue; and
6. the mixed-target labelled two-direction square.

Then all eight literal residues—and therefore all three covariance orbit
sums—cancel.  No additional `d_fixed`, `d_pair`, or outer-average labelled
section is needed here.

This is conditional closure, not a construction of the six inputs.  In
particular, the occurrence-to-`Q/ores` comparison and the mixed-target
totalization remain the load-bearing physical maps.

## Verification

```text
python3 computations/verify_h3_p2_labelled_ores_cut_even_deven_gauge_gate.py
python3 -O computations/verify_h3_p2_labelled_ores_cut_even_deven_gauge_gate.py
python3 -I -S computations/verify_h3_p2_labelled_ores_cut_even_deven_gauge_gate.py
```

Frozen ledger SHA-256:

```text
ad015c3e59df847fe977255e5ae4b26f418f514781dd44e8093f72821ef47639
```
