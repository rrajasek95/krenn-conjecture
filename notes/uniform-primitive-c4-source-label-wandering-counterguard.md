# Primitive `C4` boundary mates can wander between physical stars

## Outcome

Unique same-character mates for a primitive diagonal `C4` cancellation and
both of its mandatory `L/R` boundary fibres do **not** automatically lie in
one physical same-star four-port space.

The smallest source-labelled guard is on six sites.  It has all three
normalized constant-colour coefficients, and exactly cancels

```text
the repaired top word,
the left one-edge boundary word,
the right one-edge boundary word.
```

Each of those three fibres has exactly two live occurrences and hence a
unique mate.  Nevertheless their retained matching tails rotate as

```text
01 -> 23 -> 45,
```

and their primitive flip windows are

```text
2345, 0145, 0123.
```

The three windows have empty total intersection.  In particular there is no
fixed ordered endpoint pair whose two stars contain the complete move
packet.  Normalization, exact boundary factorization, unique mating, and a
common sign character are therefore insufficient for physical cap
placement.

Exact checker:
[`verify_uniform_primitive_c4_source_label_wandering_counterguard.py`](../computations/verify_uniform_primitive_c4_source_label_wandering_counterguard.py).

## The literal decorated packet

Use sites `0,...,5`.  The three pure anchor matchings are

```text
M0 = 01|23|45,
M1 = 02|14|35,
M2 = 03|15|24.
```

All cells not displayed are zero.  Give the pure-one and pure-two anchor
cells weight `1`.  On the pure-zero chart put

```text
01:00 =  1,    23:00 = -1,    45:00 =  1,
04:00 = -1,    15:00 =  1,
02:00 = -1,    13:00 = -1.
```

Finally add the diagonal repair cells

```text
23:21 = i,     45:21 = i.
```

There are `15` decorated cells in total.  Exact expansion over all `3^6`
words and all `15` perfect matchings gives the following three cancellation
rows.

### Top

At word `002121`,

```text
01|23|45 = -1,
01|24|35 =  1.
```

They share tail `01` and flip on the window `2345`.

### Left boundary

At word `002100`,

```text
01|23|45 =  i,
04|15|23 = -i.
```

They share tail `23` and flip on `0145`.

### Right boundary

At word `000021`,

```text
01|23|45 = -i,
02|13|45 =  i.
```

They share tail `45` and flip on `0123`.

After rescaling each coefficient row by its first nonzero monomial, all
three relations have the same signless form `X+Y=0`.  Thus the wandering is
not caused by unequal character weights.

## Boundary identity and normalization

For the selected occurrence, write as before

```text
B = pure base occurrence       = -1,
D = diagonal repaired top      = -1,
F = forced opposite top        =  1,
L = left boundary occurrence   =  i,
R = right boundary occurrence  = -i.
```

Then exactly

\[
                         LR=BD=-BF=1.                 \tag{1}

\]

The two new pure-zero mate occurrences each have weight `+1`, so the
complete pure-zero coefficient is

\[
                         -1+1+1=1.                   \tag{2}

\]

The pure-one and pure-two coefficients are also `1`.  This is why merely
retaining the three normalized anchors cannot forbid the tail rotation.

## It is a guard, not a Krenn source

The complete nonzero fibre ledger contains six further mixed singletons:

```text
010111 = -1,     020002 =  1,     022102 = -i,
101000 = -1,     101021 = -i,     202220 =  1.
```

They violate the ternary source equations.  In a full source each must gain
a mate or produce a Laurent unit.  The packet therefore does not show that
wandering survives complete boundary iteration.  It shows the precise
negative fact needed here: **the first total `L/R` mating step does not
preserve a physical endpoint pair**, even with normalized pure rows.

This distinction matters for the preceding flat-component theorem.  Its
alternating charge is occurrence-centred, but occurrence centring alone
does not identify the charge with a finite deformation in one star.

## Minimality

Only even orders carry perfect-matching coefficients.  At order four every
pair of distinct perfect matchings differs on the full vertex set
`{0,1,2,3}`.  Hence every family of primitive windows has four common sites;
one can always choose a common endpoint pair.  Order six is the first order
where primitive windows can have total intersection of size below two, and
the packet above attains intersection zero.

The claim is minimal in order, not in the number of decorated cells.

## Exact additional compatibility

The missing hypothesis is a **Cartesian physical port trivialization**, not
another unsigned incidence condition.  A sufficient source theorem must
retain all of the following.

1. **Fixed endpoint pair.** The same ordered sites `p,s` belong to every
   primitive `C4` window in the flat component.
2. **Path-independent port labels.** Every varying occurrence factors as
   one of the four products `p_i s_j`, with fixed row labels
   `p1,p2` on the `p` star and `s1,s2` on the `s` star.  Transport around a
   flat loop may not permute or replace those port rows.
3. **Cofactor transport.** After the chosen ports are deleted, every tail is
   a coefficient of one fixed residual quadratic family `q`; whenever the
   same residual complement reappears, its literal matching cofactor and
   orientation agree.
4. **One-site concentration.** Each of `p1,p2,s1,s2` is supported at at most
   one residual physical site.
5. **Response typing.** The complete retained rows are the normalized
   one-bad packet

   \[
       q^{[h]}=X_0,qquad
       p_i s_jq^{[h-1]}=\delta_{ij}X_i.               \tag{3}
   \]

The first three clauses put the abstract centred charge in one literal
bistar product space.  Clause 4 gives

\[
 p_1^{[2]}=p_2^{[2]}=s_1^{[2]}=s_2^{[2]}=0.           \tag{4}

\]

Together with (3), the pinned uniform theorem supplies the active clean cap

\[
 K=\begin{pmatrix}1&0&0\\0&1&1\\0&-1&1\end{pmatrix}. \tag{5}

\]

Thus the next proof obligation is now sharply physical:

> use all subsequent singleton/multiterm source rows either to produce a
> unit, or to prevent tail rotation and construct a fixed-endpoint Cartesian
> port trivialization satisfying clauses 1--5.

A theorem stated only in terms of total mate involutions, bipartiteness, or
flat Laurent character cannot supply this trivialization; the displayed
packet satisfies those local conditions at the first boundary and still
wanders.

## Reproduction

```sh
python3 computations/verify_uniform_primitive_c4_source_label_wandering_counterguard.py
python3 -O computations/verify_uniform_primitive_c4_source_label_wandering_counterguard.py
python3 -I -S computations/verify_uniform_primitive_c4_source_label_wandering_counterguard.py
```

Frozen ledger SHA-256:

```text
885b7de1169942f2ec316e06ebcc2291bd85048a02aed8d02c6c492a31647b7e
```
