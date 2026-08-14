# The full relative Boolean presentation already contains the odd carrier

## Outcome

Keep both complete pointed Boolean mapping cylinders: the one based at

```text
f = P0|S1|23|45
```

and its endpoint/head-transpose copy based at

```text
tau f = P1|S0|23|45.
```

For every nonempty Boolean face `S`, the first cylinder has

\[
                  db_S=C_S-u_S,
\]

and the transpose cylinder has

\[
                  db_{\tau S}=C_{\tau S}-u_{\tau S}.
\]

Because the centered constants cancel,

\[
 {C_S-C_{\tau S}\over90}=1_S-1_{\tau S}.
\]

Therefore their normalized antisymmetric difference is already

\[
 d b_S^-=(1_S-1_{\tau S})-u_S^- ,
 \qquad
 u_S^-={1\over90}(u_S,-u_{\tau S}).                  \tag{1}
\]

This is an honest element of the **full relative two-object presentation**.
It requires no new source generator.  In particular, the new earliest datum
identified in the mixed-head audit is automatically present once both
mapping cylinders are retained.

The first genuinely missing datum is later: the relative odd carrier has no
termwise physical map to the selected six-term `db01` flag block.  The exact
centered 360-flag dual survives with value `174`.  Conditional on granting
that map, the two root-labelled sections are exactly the intended receiving
arrows from the relative carrier to the tied `r0` cap, but their physical
head/fine columns remain unconstructed.

Exact checker:
[`verify_h3_pf_boolean_odd_graph_db01_section_gate.py`](../computations/verify_h3_pf_boolean_odd_graph_db01_section_gate.py).

## Presentation safety versus fixed-object descent

One pointed cylinder has 105 degree-zero coordinates: 90 occurrence
coordinates and 15 private face carriers.  Its 16 named columns have rank
16, so

```text
H0 = 105 - 16 = 89.
```

The direct sum of the plus and transpose cylinders has

```text
coordinates     210,
rank             32,
H0              178.
```

All fifteen antisymmetric graphs (1) are already in this rank-32 column
span.  Thus adjoining the two mapping cylinders is presentation-safe and
supplies `u^-` automatically.

There is still no nonzero canonical collapse to one transported object.
Canonical transport applies endpoint transpose simultaneously to the
occurrence and its carrier label, so

\[
                     b_S^-\longmapsto0.               \tag{2}
\]

Equation (2) only says that the relative carrier is not an absolute
fixed-object `W_odd` boundary.  It does not prevent using that relative
carrier as the domain of `Phi`.

For comparison, a raw fixed-object display uses one 90-coordinate occurrence
block and two sets of 15 carrier coordinates.  It has rank 31 in dimension
120 and again H0=89.  In that display

\[
 u_S^-=(u_S-u_{\tau S})/90.
\]

This display is useful algebraically, but the proof does not need to assert
that raw object-forgetting is a physical chain map.

## The top and four first face families

The full relative presentation supplies the normalized odd graph on the top
and on all four codimension-one faces:

| face | plus fine label | transpose fine label |
|---|---|---|
| top | `P0|S1|23|45` | `P1|S0|23|45` |
| delete `P0`/transported `S0` | `S1|23|45` | `P1|23|45` |
| delete `S1`/transported `P1` | `P0|23|45` | `S0|23|45` |
| delete `q23` | `P0|S1|45` | `P1|S0|45` |
| delete `q45` | `P0|S1|23` | `P1|S0|23` |

Each row has differential

\[
           1_{\text{plus face}}-1_{\text{transpose face}}-u^-_{\text{face}}.
                                                               \tag{3}
\]

If one insists on replacing this relative pair by a single fixed-object
normal, the minimal top-plus-four-face model adds five coordinates and five
relations.  Its rank changes `16 -> 21` while H0 stays `89 -> 89`.  This is
an optional fixed-object model, not a new requirement for the relative
domain.

## The first next dual is selected `db01`

The physical first-PP block retains 180 response flags and 180 carrier
flags.  Grant all 180 monic termwise reinsertion graphs and both complete
rows.  Their rank is 181.  Direct-sum this maximally generous block with the
top-plus-four-face odd graph block of rank 21.  The exact ranks are

```text
odd graph plus named db01 inventory       202
+ selected six-term db01                  203.
```

The integral covector is

```text
29 on the six selected positions in each 180-flag half,
-1 on the other 174 positions in each half,
0 on every Boolean occurrence/carrier coordinate.
```

It kills all 180 monic graphs, both complete rows, and the entire odd
Boolean presentation.  It reads `174` on the selected response vector.
Hence the four face carriers in (3) do not yet carry the termwise
reinsertion/PP incidence

\[
 p_0s_1\sum_{23|45,24|35,25|34}
      (dq_e q_{e'}+q_e dq_{e'}).                       \tag{4}
\]

The shortest new map is precisely a source-labelled map from the existing
relative odd top/face packet to (4).

### Minimal constructor/API

The exact smallest source constructor can be named

```text
PSQJet_01
```

with interface

```text
domain       existing relative u_f^- Boolean top/four-face packet
top          (p0*s1-p1*s0)*q01*H2345
top type     endpoint-odd P4+2K2 first jet
word/head    11:110000, ordered response heads 01/10
operation    absolute PS-over-q01 restriction/insertion
repetition   sites 0 and 1
chart        q01*H2345=1.
```

Put `B=p0*s1` and `C=p1*s0`.  The complete response supplies `B+C`; the
new constructor supplies `B-C`.  Therefore

\[
                         B={1\over2}((B+C)+(B-C)),     \tag{5}
\]

and the `q01*dH` projection of (5) is exactly selected `db01`.

The complete first product rule of the required top is

\[
\begin{aligned}
d((B-C)q_{01}H)={}&
 [(dp_0)s_1+p_0(ds_1)-(dp_1)s_0-p_1(ds_0)]q_{01}H\\
 &+(B-C)dq_{01}H +(B-C)q_{01}dH .                    \tag{6}
\end{aligned}
\]

In literal labelled pairs, (6) has:

| family | signed pairs | cofactor | status |
|---|---:|---|---|
| endpoint `dB-dC` | 6 | `P3+2K2` | may be granted fan exits |
| tail `q01*dH` | 6 | `P4+K2` | absent from old collision fan |
| `dq01*H` | 3 | `4K2` | absent from old collision fan |

On the nine paired tail/`dq01` coordinates, the strongest old recurrence
and even rows have rank 27.  Selected `B` raises it to 28.  Adjoining the
single aggregate odd source row `B-C` also raises it to 28, after which
selected `B` causes no further rank increase.  Thus `PSQJet_01` is exactly
the missing column at this interface.

This classifies the obstruction:

- scalar localization fails at the operation idempotent (`DQ` does not
  become selected `PS`);
- physical endpoint insertion repairs that operation tag but necessarily
  enters the repeated-site `P4+2K2` fine block;
- arbitrary termwise reinsertion graphs preserve endpoint orientation and
  leave the odd class;
- the first genuine missing atom is therefore an **absolute endpoint-odd
  `PS/q` restriction-insertion cell**, with the nine mandatory signed
  companion pairs in (6).

It is not merely another relative graph or an unlabelled Kähler identity.

## Conditional landing in the minimal `Phi` bicomplex

Grant (4).  The next block is the two-root operation/word section block.  Its
rank changes

```text
207 -> 209
```

when the two root-labelled sections are adjoined.  The paired operation
dual kills the old block and reads one on their sum.

The source interface is the correct one:

```text
relative carrier word       11110000 = 11:110000
relative carrier operation  response occurrence / P_f graph
section operation            response occurrence/KS -> AugP2/K_Eq cap r0
section word                 11110000 -> 01211222.
```

Thus the sections are exactly the formal receiving arrows for the two
root-labelled copies of `u^-`.  What remains missing is their physical
construction with the literal head/fine incidence.  The Boolean graph does
not itself map into the cap object.

So the attack order is now:

1. use the existing plus/transposed Boolean cylinders to supply `u^-` and
   its four first faces;
2. construct their termwise selected-`db01` incidence;
3. construct the two root-labelled receiving sections into `r0`;
4. continue with the already isolated mixed `K_Eq` square and shifted
   ridges.

## Verification

```text
python3 computations/verify_h3_pf_boolean_odd_graph_db01_section_gate.py
python3 -O computations/verify_h3_pf_boolean_odd_graph_db01_section_gate.py
python3 -I -S computations/verify_h3_pf_boolean_odd_graph_db01_section_gate.py
```

Frozen ledger SHA-256:

```text
3967fa82057b0693306972462cf52395e505c5388e90718864104d348eca4795
```
