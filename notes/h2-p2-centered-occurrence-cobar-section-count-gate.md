# The finite P2 cobar needs eight pointed tags, not three orbit representatives

## Result

The labelled two-direction Hasse square of `711f051` makes the `P2`
totalization finite. It does not reduce the number of pointed occurrence
sections needed by the fixed physical packet.

There are three distinct counts.

1. The eight one-root word blocks have three orbits of sizes `4,2,2` under
   the `V4` stabilizer of the **unmarked** word `0112`.
2. Exact transport of the actual private vectors needs `3+2+2=7` ambient
   covariance seeds, not three. Nontrivial transport moves the marked
   occurrence, so the transported vector generally differs from the fixed
   packet's target-word vector.
3. In the strict marked word/fine grade all eight blocks remain independent,
   so eight labelled sections are necessary.

The same number eight follows independently from the exact private
`B-4` preimage. In the canonical twelve-occurrence order,

\[
\begin{aligned}
z_{\rm priv}=(&101/432,-1/108,-1/27,101/432,-1/27,-1/108,\\
              &-1/108,-1/27,-61/432,-1/27,-1/108,-61/432). \tag{1}
\end{aligned}
\]

Modulo the complete response line, (1) requires at least eight literal
occurrence selectors, and eight suffice. Thus the shortest positive object
is one **universal family** of pointed sections natural in the marked tag,
not one fixed source column and not three orbit representatives.

Checker:
[verify_h2_p2_centered_occurrence_cobar_section_count_gate.py](../computations/verify_h2_p2_centered_occurrence_cobar_section_count_gate.py).

## 1. Exact selector minimum

The four coordinate values of (1) have multiplicities

```text
 101/432 : 2
   -1/108: 4
    -1/27: 4
  -61/432: 2.
```

If

\[
             z=b\mathbf1+\sum_{i\in S}a_i e_i,        \tag{2}
\]

then every coordinate outside `S` must equal `b`. The largest equal-value
fibre of (1) has size four, so `|S|>=12-4=8`. Taking `b=-1/108` gives the
sharp formula on indices

\[
                         S=\{0,2,3,4,7,8,9,11\}.      \tag{3}
\]

The checker also exhausts every support of size at most seven by exact
rational rank.

Let

\[
                         c_i=12e_i-\mathbf1.           \tag{4}
\]

These are exactly the order-two centered occurrence/global conormals. Since
`sum z_priv=0`, formula (2) becomes the explicit centered identity

\[
 z_{\rm priv}=
 {35\over1728}(c_0+c_3)
 -{1\over432}(c_2+c_4+c_7+c_9)
 -{19\over1728}(c_8+c_{11}).                         \tag{5}
\]

Thus the missing pointed cap of the P2 square and the lower centered
occurrence descent are the same **source type**. Formula (5) is not yet a
source construction: every `c_i` must exist as a physical pointed section
and commute with the root and reinsertion operators.

Because (1) is endpoint-even, a physical selector for an unordered
endpoint pair would reduce the conditional minimum to four pair selectors.
The endpoint-role groupoid does not provide that selector: its canonical
transport sends the bar boundary to zero, while the nontransported fold is
the open promoted-occurrence column. Four is therefore only a conditional
count, not a current physical reduction.

## 2. Why three orbit representatives do not suffice

Write the unmarked-word `V4` orbits as

\[
\begin{aligned}
 \mathcal O_4&=\{0012,0102,0122,0212\},\\
 \mathcal O_2'&=\{0110,2112\},\\
 \mathcal O_2''&=\{0111,1112\}.                      \tag{6}
\end{aligned}
\]

For a proposed set of seed faces, the checker transports both word and
occurrence coordinates under every element of `V4`, then asks whether the
actual fixed-packet private vector in each target word lies in the resulting
span. The exact minima are

```text
orbit O4       3 seeds
orbit O2'      2 seeds
orbit O2''     2 seeds
all words      7 seeds.
```

The two minimal seven-seed sets are

```text
0012 0102 0110 0111 0212 1112 2112
0102 0110 0111 0122 0212 1112 2112.                  (7)
```

This does not contradict the orbit partition. A group orbit classifies
which word label can be reached after transporting the entire marked
packet; it does not assert equality with the private vector produced by the
original marked packet. The latter is what a fixed physical source chain
must cancel.

## 3. What the labelled square supplies

For one fixed structural occurrence tag and two commuting roots on distinct
factors, `711f051` constructs the exact square

```text
0112 ---> 1112
 |           |
 v           v
0102 ---> 1102
```

with signed boundary

\[
                         A_0+B_1-A_1-B_0             \tag{8}
\]

and `d^2=0`. A pointed source-valid occurrence section functorial for those
roots generates the whole square. Multiplication by `q23` then forces

\[
                         d(q_{23}S)=q_{23}dS+dq_{23}S. \tag{9}
\]

Therefore one family

\[
                  i\longmapsto C_i                  \tag{10}
\]

would suffice, provided it is defined for every marked occurrence tag and
is equivariant for:

- site and colour relabellings as maps between labelled packet objects;
- ordered commuting root PP operators, including their mixed-target proper
  faces;
- endpoint-role transport without silently folding the retained label;
- residual restriction and same-edge reinsertion; and
- the complete `q` first-principal-parts coproduct, so the `dq` face in (9)
  is retained.

Its degree-zero boundary must be `c_i=12e_i-1`. Its full augmentation must
retain word/fine/repeated grade, target, Eq, labelled `Q/ores`, anchor,
physical `q`, `W`, eta, and sigma. Formula (5) then combines eight
instantiations of this one family into the required private preimage, and
(8)--(9) provide the finite cobar. This is genuinely one theorem schema,
but it is not one column.

## 4. Relation to the h=3 centered projector and primitive cap

The h=3 centered occurrence class restricts on each marked residual edge as

\[
 D_ec_{f,3}={15\over2}c_{f/e,2}+{13\over2}\mathbf1.  \tag{11}
\]

So a physical h=3 centered family satisfying restriction naturality would
indeed supply the order-two `c_i` source type used in (5), up to the common
complete row. This is the exact positive connection.

What is already pinned is weaker:

- the centered projector exists coefficientwise but has scalar face
  `90 f(x)` and no source-valid lift;
- its physical cap projection leaves the primitive class
  `p=(-Q,-ores)` in word `01211222` and repeated grade `P3+K2`; and
- `7e9467c` proves the pointed conormal `P_f=d(u_f-u)` and `p` are independent
  projected faces.

Consequently

\[
 \boxed{p+\text{coefficient identity }(11)
        \not\Rightarrow\text{the P2 pointed sections}.}          \tag{12}
\]

The primitive `p` remembers only the aggregate cap quotient. It carries no
twelve-tag occurrence section, no labelled root square, and no `dq23`
conormal. A single enriched family may contain `P_f`, `p`, and the sections
`C_i`, but these remain distinct faces of that family.

Even under the strongest formal same-label use of `p`, its `Q` face can
cancel the `dq23` coefficient while its labelled `ores` face remains, read
by the existing detector as `-35/72`. Hence the universal family must carry
the labelled `Q/ores` comparison, not just scalar ordinary residue.

## 5. Nonfill and conormal darkness

Let `J_aug` be the complete physical map projected to all eight lower
private word blocks and their `dq`/labelled-residue companions, retaining
every protected augmented row. Exact finite-dimensional duality gives

\[
 \begin{array}{ll}
 R_{P2}\in\operatorname{im}J_{aug}
   &\Longrightarrow\text{the physical section exists},\\[1mm]
 R_{P2}\notin\operatorname{im}J_{aug}
   &\Longrightarrow\exists\lambda:\lambda J_{aug}=0,
                                      \ \lambda R_{P2}\ne0.
 \end{array}                                           \tag{13}
\]

The second arm closes only after `lambda` is identified with an accepted
physical exchange, relative-generator, or Fredholm terminal. An arbitrary
occurrence covector is not such a terminal. The exact missing promotion is
to extend the first nonzero lower/`dq` private covector across every target,
Eq, labelled residue, anchor, physical-`q`, `W`, eta/sigma, and protected
column of the source.

If all eight lower private readouts and their forced conormals are dark at a
particular physical source, then the evaluated associated-graded P2 value
lands modulo the complete response rows at that point. This is useful but
strictly pointwise. It constructs neither the section in a neighbourhood
nor the chain homotopy required by the proof.

## Shortest next theorem

Construct the family (10) as a physical pointed PP module, or prove that its
first failure is always an already accepted full augmented terminal. The
family formulation reduces the eight fixed labels to one natural theorem;
it does not reduce them to one generator.

Run:

```text
python3 computations/verify_h2_p2_centered_occurrence_cobar_section_count_gate.py
python3 -O computations/verify_h2_p2_centered_occurrence_cobar_section_count_gate.py
python3 -I -S computations/verify_h2_p2_centered_occurrence_cobar_section_count_gate.py
```

Frozen ledger SHA-256:

```text
17ff7b657efbe8796ef78858731c27979b0b1bdd46fc19f5d513e360b941e2e2
```
