# Four ordinary equation generators do not cancel the Gate-II root target

## Exact verdict

The four ordinary source-equation/Koszul generators for the two mixed and
two pure words do **not** make the root-only `chi_w` Cartan face target safe.

Order the four target coordinates as

```text
mixed_i, mixed_c, pure_i, pure_c.
```

The simultaneous two-site Weyl defect is

\[
          (w-1)\Delta=(1,1,-1,-1).                  \tag{1}
\]

For the ordinary Tate generators

\[
                       d\theta_y=F_y-\tau_y,          \tag{2}
\]

the two mixed target values are zero and the two pure values are one:

\[
 \tau_{m_i}=\tau_{m_c}=0,\qquad
 \tau_{p_i}=\tau_{p_c}=1.                           \tag{3}
\]

Thus the augmented target map of all four generators has image

\[
                         \langle p_i,p_c\rangle.      \tag{4}
\]

Adding `theta_pure_i+theta_pure_c` cancels the last two entries of (1), but
leaves

\[
             \boxed{m_i+m_c=(1,1,0,0)}.              \tag{5}
\]

The mixed generators in (2) are source equations with target zero; their
word labels do not turn zero augmentation into the mixed target normals in
(5).  The six pairwise ordinary Koszul cells
`theta_y wedge theta_z` also have zero degree-one target at the GHZ point,
so they do not enlarge (4).

Checker:
[`verify_h3_gate_ii_four_equation_koszul_root_target_no_go.py`](../computations/verify_h3_gate_ii_four_equation_koszul_root_target_no_go.py).

## Literal source and common-tail audit

The four exact eight-site words are

```text
mixed_i = 11211211,
mixed_c = 22122122,
pure_i  = 11111111,
pure_c  = 22222222.
```

Every direct-free coefficient has `90` physical matching terms.  The local
root action at sites `2,5` transports the pure rows to the mixed rows
termwise, preserving all `90` matching skeletons and every decorated edge
outside the root sites.  So the obstruction is not a failure of root
covariance.

It is a failure of occurrence localization.  Each generator (2) contains
the aggregate of all `90` skeletons in its word.  In the resulting
`4*90`-coordinate occurrence module the four equation rows have rank four.
Adjoining one selected root-character occurrence raises the rank to five.
A difference of two skeleton selectors kills every complete equation row
and detects the selected occurrence.

Therefore the old equations do not provide a fixed-common-tail section or
the pointed anchor `P_f`.  Multiplying by or projecting to a chosen tail
would be exactly the missing occurrence-local principal-parts operation,
not an ordinary use of (2).

## Presentation safety

The four generators (2) are presentation safe: they are the ordinary Tate
resolution of the existing four source equations and preserve the physical
equation quotient in `H0`.

By contrast, simply adjoining a new source generator whose differential is
the selected `chi_w` relation is not safe.  In the occurrence-linear guard,

```text
dimension after the four aggregate relations       360-4 = 356,
dimension after declaring selected chi_w a relation 360-5 = 355.
```

It kills a new degree-zero class.  An `H0`-preserving repair must export
(5) to a relative target coordinate—a root-decorated target cylinder or
equivalent physical PP/mapping-cone cell—rather than declare it zero inside
the old source.

## Anchor and `q=M-a`

The committed coarse signature of a pure source-row generator is

\[
  (\operatorname{ainc},W,\operatorname{target},\operatorname{ores})
                         =(-1,0,+1,0),                \tag{6}
\]

while the mixed generators have zero anchor/target signature.  Hence the
best pure target correction also brings its aggregate incidence face; it
does not create the selected `P_f` face.

More importantly, (2)--(6) do not determine the external aggregate matching
row `M`.  The same source differential and target correction admit, at the
coarse level, `M=0` or `M=a`, giving different values of

\[
                              q=M-a.                 \tag{7}
\]

Thus literal physical `q` cannot be claimed on a hypothetical corrected
cell merely from the four ordinary equation generators.  It must be typed
on the new relative source domain, after which the existing `q`-defect
alternative applies.

## Sharp first missing cell

After using the old pure generators, the smallest new cell has:

```text
target             -(mixed_i + mixed_c),
source boundary     selected root-only chi_w modulo complete rows,
grade               literal fan word orbit and fixed decorated common tail,
presentation        H0-safe relative target cylinder / PP cell,
anchor              selected P_f,
augmented law        physical M and a with q=M-a.
```

The two mixed coordinate functionals are primitive cokernel witnesses for
the four-generator target map.  They are word-module duals, not yet
physical Fredholm terminals.  Promotion still requires the complete
protected/ridge/terminal typing.

This is exact for canonical `h=3`.  No uniform all-`h` claim is made.

Run:

```text
python3 computations/verify_h3_gate_ii_four_equation_koszul_root_target_no_go.py
python3 -O computations/verify_h3_gate_ii_four_equation_koszul_root_target_no_go.py
python3 -I -S computations/verify_h3_gate_ii_four_equation_koszul_root_target_no_go.py
```

Frozen ledger SHA-256:

```text
ce0b4936e3e0e92a8a99cd79b29fea88a86bf503fcc5d34641a6ab97c54fcc9a
```
