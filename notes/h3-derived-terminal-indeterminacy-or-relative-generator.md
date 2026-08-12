# The derived terminal cochain exists; its primitive ambiguity is either killed or is the relative generator

## Exact derived calculation

Let (k_v) be the primitive two-chart presentation syzygy and adjoin its
canonical free-resolution cell (b_v), so (db_v=k_v).  The marked
functional of `f872900` has

\[
                         \Lambda_v(k_v)=1.              \tag{1}
\]

The indexed Hasse/Koszul construction of `91041f7` supplies a target chain
(n_v) with

\[
 (d,\operatorname{tgt},\operatorname{ores})(n_v)
                   =(h_vYw,0,0).                       \tag{2}
\]

Consequently the terminal cochain extends across the total mapping cone:
assigning correction value (-1) to (n_v) gives the attaching equation

\[
                         1+(-1)=0.                      \tag{3}
\]

This is a derived chain-map homotopy.  It is not yet a physical relative
anchor.

The exact ambiguity is already nontrivial.  The strict chart difference

\[
                         z_v=N_v^{pq}-N_v^{pr}          \tag{4}

is closed in the complete indexed target.  Its \(T\)-terms cancel, it has
no \(\rho\)-term, and the two \(r_0\)-targets cancel.  Hence

\[
 (d,widehat w,\operatorname{tgt},\operatorname{ores})(z_v)
                         =(0,0,0,0).                    \tag{5}
\]

Its external face is the primitive chart square (S_v), so the normalized
marked readout gives

\[
                         \Lambda_v(z_v)=1.              \tag{6}

Every (n_v+c z_v) is another filler, and its correction value is
(-1+c).  Thus on the certified primitive summand
(mathbb Q[z_v]\subseteq H_1) the indeterminacy image is all of
(mathbb Q).  This is enough to disprove zero indeterminacy for the raw
chart readout.  It does not claim that (4) exhausts the full correction
homology of a larger resolution.

## Zero indeterminacy or relative generator

The ambiguity becomes useful once the missing physical typing is supplied.
Let

\[
 \widehat J:L\longrightarrow
 E_{\rm bdry}\oplus E_{\widehat w}\oplus
 E_{\rm tgt}\oplus E_{\rm ores}                       \tag{7}

be one physical augmented correction map in a fixed fine grade, and let
(q:L\to k) be the physically typed pure-anchor readout.  Then exactly one
of the following holds.

1. If (q(\ker\widehat J)=0), (q) is constant on every affine fibre of
   corrections.  The promoted polar is zero-indeterminate and the physical
   map (P) is well-defined.
2. If (q(z)\ne0) for some (z\in\ker\widehat J), then

   \[
                     z'=-{z\over q(z)}                 \tag{8}
   \]

   has the physical signature

   \[
    (\operatorname{ainc},\widehat w,
       \operatorname{tgt},\operatorname{ores})(z')
                         =(-1,0,0,0).                  \tag{9}
   \]

   Thus (z') is already the primitive relative anchor generator.

The proof is immediate: two corrections differ by (ker\widehat J), and
(8) preserves every augmented zero row while normalizing the only nonzero
readout.  The checker exhausts small binary matrices as a mutation guard.

Therefore Theorem B does not need an independent zero-indeterminacy lemma
after a physically typed comparison/readout is constructed.  Failure of
zero indeterminacy is its positive generator branch.  If zero
indeterminacy holds, the existing Fredholm generator-or-annihilator theorem
applies to the resulting (P).

## Scope guard

Neither ((b_v,-n_v)) nor (z_v) is presently a physical anchor face.
The chart value in (6) has not been identified with physical pure-anchor
incidence or with the pentagon aggregate.  A derived-to-physical comparison
must preserve the fine grade and all four readouts in (7).  Only after that
comparison does the dichotomy above promote the formal chart correction to
Theorem B.

Likewise, localizing (h_v) and scaling (n_v) produces a derived chain
with boundary (kappa Yw), but not by itself the literal Component-IV
physical cap column.  That use still requires the same physical (W)
identification and the Component-IV source-resolution typing.

## Verification

Run:

```text
python3 computations/verify_h3_derived_terminal_indeterminacy_or_relative_generator.py
python3 -O computations/verify_h3_derived_terminal_indeterminacy_or_relative_generator.py
python3 -I -S computations/verify_h3_derived_terminal_indeterminacy_or_relative_generator.py
```

The checker reconstructs the total-cone value (3), the complete indexed
chart cycle (4)--(6), the affine ambiguity, and the physical linear-algebra
dichotomy.  It pins `f872900`, `91041f7`, and the full indexed
Hasse/Koszul/cap totalization.

Frozen ledger SHA-256:

```text
dde75a89477549d7e04f3a26231bacbe5e48dbea653dc9e0dca2155bb9e06073
```
