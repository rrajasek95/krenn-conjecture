# The centered scalar normal is not canonically terminal after Segre--Tate completion

## Exact verdict

Let

\[
                         L=90f-R
\]

for the marked occurrence `f` and the complete selected response `R`.  At
the trapped normalization `R(x)=0`, `f(x)=1`, one has `L(x)=90`.

The relative Tate construction `d epsilon=L` therefore cannot itself be a
chain map to the fixed classical fibre: the target field has zero
differential, so it would require

\[
 0=d\phi(\epsilon)=\phi(d\epsilon)=\phi(L)=90.        \tag{1}
\]

A physical scalar/target correction is logically prior.  After granting
such a correction and adjoining the complete Segre Tate layer, the scalar
normal still does not acquire a canonical class in the existing
source-terminal/Macaulay quotient.  It has become exact, and every genuine
terminal cocycle must kill its image.

Checker:

```text
computations/verify_h3_centered_scalar_normal_terminal_extension_guard.py
```

Frozen ledger digest:

```text
190d537e5f24985505bece1677c24d85ff3275c8075bc69b88ac7ca5096dbcda
```

## Why the Tate layer does not produce a terminal

The occurrence Tate resolution and the physical terminal quotient live in
different complexes.  The former resolves the coefficient algebra and,
after adjoining `epsilon`, the relative quotient `A/(L)`.  The latter is a
quotient of the fully augmented physical output map.  No committed chain map
identifies the class of `L` with a target, residue, physical-`q`, ridge,
`W`, eta, or sigma class.

Moreover, if such a chain map contains `epsilon`, then for any terminal
cocycle `lambda`,

\[
              \lambda\Phi(L)=\lambda d\Phi(\epsilon)=0. \tag{2}
\]

A nonzero terminal pairing with `L` would instead be an obstruction to the
physical placement of `epsilon`.  It cannot simultaneously be a cocycle on
the complex after that cell has been admitted.  Thus the Segre--Tate lift
does not terminalize `L`; it makes `L` an exact proper face.

## Sharp two-completion guard after scalar correction

To show that all later output rows remain necessary, take five correction
columns

```text
placed base, corrected epsilon, Tate01, Tate02, Tate12.
```

Let the principal map pivot on the placed base and all three Segre Tate
directions.  Its sole kernel is the corrected `epsilon` line.  Give both
completions the identical rows

```text
anchor(epsilon)=90;
target = ordinary residue = W = shifted ridge = eta = sigma = 0;
matching M=(1,0,0,0,0).
```

The three Segre Tate columns are zero in all these augmented rows.  There
are nevertheless two exact completions of the physical law `q=M-ainc`:

\[
\begin{array}{c|c|c|c}
 &\operatorname{ainc}&q& q(\ker J)\\ \hline
 \text{dark}&(0,0,0,0,0)&(1,0,0,0,0)&0\\
 \text{bright}&(0,-1,0,0,0)&(1,1,0,0,0)&1.
\end{array}                                           \tag{3}
\]

In the dark completion, `q` is literally the first principal row and hence
factors through `J`, giving the Fredholm/factorization arm.  In the bright
completion, the corrected kernel vector has physical `q=1`, giving the
relative-generator arm.  Both completions agree on the principal map,
Segre Tate layer, scaled anchor, target, ordinary residue, `W`, shifted
ridge, eta, sigma, and aggregate matching row.

This is dimensionally minimal: one placed direction and one hidden
corrected kernel direction are required to distinguish factorization from
a kernel generator.  Adding the three quadratic Tate pivots does not change
the ambiguity.

## Shortest remaining theorem

Construct one physical scalar/target correction and a complete augmented
placement of the centered `epsilon` in the actual AugP2/E14 source, with

```text
word/fine/repeated grade,
target and ordinary residue,
anchor incidence and q=M-ainc,
W and shifted ridge,
eta and sigma.
```

Then the existing exact generator/Fredholm alternative is exhaustive: the
physical `q` either detects the protected kernel or descends to the actual
source-terminal quotient.  Failure of a proposed placement can be called a
terminal only after its surviving dual has been extended across every one
of these physical rows and every admitted Macaulay multiplier.

The guard is exact for the `h=3` relative-Tate packet.  It is a
complete-output linear guard satisfying all currently committed row
identities, not two complete GHZ source points and not a proof that no
physical augmentation exists.
