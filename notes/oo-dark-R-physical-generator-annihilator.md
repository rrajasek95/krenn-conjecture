# A dark complete-lift class has a physical generator/annihilator trichotomy

## Result

Let `C=(C_1,...,C_m)` be complete physically typed source lifts for a
critical block, let `G` be the placed physical Cartan connector, and suppose
the component charge is dark.  Thus

\[
                         My=g,
\]

where `M,g` are the critical-component projections.  In the source domain
form

\[
                    r=G-\sum_i y_iC_i.                \tag{1}
\]

The old identity gives only `pi_M(r)=0`.  Assume the stronger, physically
typed statement

\[
                         J_0r=0,                       \tag{2}
\]

where `J_0` is the complete protected map in one word/fine/repeated grade.
It retains literal boundary, `D`, `W`, target, ordinary residue, `Eq`, and
every other row required to vanish on a relative anchor.

Let

\[
               q=\sum_{i=1}^6m_i-\operatorname{ainc} \tag{3}
\]

be the physically typed six-term anchor readout.  Then there are exactly
three local descriptions, but only two final Fredholm outcomes.

1. If `q(r)!=0`, then `r/q(r)` is the protected-zero relative anchor.
2. If `q(r)=0` but `q` is nonzero on another element of `ker J_0`, that
   other class—not `r`—normalizes to the relative anchor.
3. If `q` kills all of `ker J_0`, then

   \[
                              q=\lambda J_0,           \tag{4}
   \]

   and `(-lambda,1)` is the physical left separator of the complete
   augmented map `(J_0,q)`.

Thus `q(r)=0` by itself is **not** the annihilator branch.  The annihilator
appears only after testing the entire protected kernel.  Once the domain is
the exhaustive relative source complex, there is no fourth branch and no
further relative-cell census is needed.

Checker:
[`verify_oo_dark_R_physical_generator_annihilator.py`](../computations/verify_oo_dark_R_physical_generator_annihilator.py).

## Why the visible branch is the existing physical generator

On a protected-zero class the six selected literal matching rows in (3)
vanish.  Hence

\[
                           q=-\operatorname{ainc}.     \tag{5}
\]

Normalizing `q=1` therefore gives

\[
 (\operatorname{ainc},D,W,\operatorname{tgt},
       \operatorname{ores},\operatorname{Eq})
                         =(-1,0,0,0,0,0),             \tag{6}
\]

which is precisely the primitive protected-zero relative-anchor signature.
This is the physical version of the indeterminacy-or-generator theorem of
`0373033`.  The raw chart-marked functional in that theorem is not enough;
equation (5) is the required derived-to-physical identification.

If `q` kills the kernel, elementary row-space duality gives (4).  For every
source class `x`,

\[
 (-\lambda,1)(J_0x,q(x))=-\lambda J_0x+q(x)=0.       \tag{7}

So (7) annihilates every complete augmented correction column.  A formal
desired anchor with `J_0x=0,q(x)=1` pairs to one and is separated.  This is
the Fredholm annihilator, not merely a componentwise cokernel covector.

## The smallest guard: one dark class is not the whole kernel

Take

\[
                    J_0=(1\;0\;0),\qquad
                    r=(0,1,0).                        \tag{8}

Then `ker J_0` is two-dimensional.

* For `q=(0,1,0)`, `r` itself normalizes to the generator.
* For `q=(0,0,1)`, `q(r)=0`, but `(0,0,1)` is another visible kernel class.
  There is a generator and no separator.
* For `q=(1,0,0)`, `q` kills the whole kernel and equals `J_0`; the left
  separator is `(-1,1)`.

This is the smallest nontrivial protected-row guard for the mistaken
implication

```text
q(r)=0  =>  q factors through J0.
```

The checker exhausts 13,004 binary `(J_0,q,r)` packets through width four:

```text
r itself is the generator             4,724
r is dark, another kernel class wins  5,640
physical left separator               2,640.
```

## Why an arbitrary component charge cannot replace `q`

In (8), let

```text
component charge chi = (0,1,0)
physical anchor q    = (0,0,1).
```

Then `chi(r)=1` while `q(r)=0`.  Normalizing `r` by `chi` creates a
component-charge generator whose physical anchor value is zero.  It does
not have signature (6).

This guard has two direct physical counterparts.

* The Schur charge `ell` is defined on a critical interference component.
  It determines whether `g` is component-exact, but it is not physical
  anchor incidence on the relative correction complex.
* The primitive chart-odd marked value of `0373033` can detect a chart
  difference while its physical boundary and anchor incidence vanish.  It
  becomes usable only after a comparison proves that it equals (3) in the
  same physical grade.

Therefore “some component `q` sees the dark class” is insufficient.  The
functional must be the physical six-term/pentagon anchor readout on the
whole domain.

## Exact typing needed

The generator/annihilator conclusion requires all of the following.

1. `C_i`, `G`, `y`, and (1) live in one physical word, fine grade, repeated
   grade, and endpoint orientation.
2. `J_0` retains every protected physical row.  The component equation
   `My=g`, or `pi_M(r)=0`, does not imply (2).
3. `q` is defined on the same entire relative source domain and is
   identified with (3), not with a Schur charge, a chart tag, or an
   untyped terminal coordinate.
4. The domain is exhaustive for the claimed conclusion.  If `q` kills only
   the kernel of the currently listed columns, (4) is only a bounded
   separator and can be broken by a later relative generator.
5. For cyclic assembly, the five facewise readouts must share this physical
   typing.  Their sum kills the saturated rank-four `C5` edge lattice and
   pairs to five with the primitive aggregate; characteristic zero permits
   normalization by five.

The placement theorem `6824c9e` proves that the ambient Cartan prism has a
nonzero critical occurrence in its exact fine label.  It does not create
item 3 in an arbitrary component grade.  The dark-potential theorem
`a60ee53` likewise proves the complete-lift identity and its type-split
guard, but only (2)--(3) promote it to Fredholm.

## Frontier consequence

For the canonical face, the six-term covector already has the physical
interpretation (3).  Once a dark Cartan combination satisfies (2), its fate
is automatic: it is the generator, points to another kernel generator, or
participates in the complete physical annihilator (4).

For an arbitrary critical component, the remaining theorem is exactly the
augmented comparison which transports its terminal to (3) while preserving
all rows of `J_0`.  No argument using only the component charge can replace
that typing.

## Verification

Run

```text
python3 computations/verify_oo_dark_R_physical_generator_annihilator.py
python3 -O computations/verify_oo_dark_R_physical_generator_annihilator.py
python3 -I -S computations/verify_oo_dark_R_physical_generator_annihilator.py
```

The checker pins commits `a60ee53`, `0373033`, and `6824c9e`, together with
the physical first-flat six-term anchor and exhaustive relative-extension
alternative.  The frozen ledger SHA-256 is

```text
65ecec226f94bf8771af9d10ccabad41e95e6b43bcb1b12a4d5de4f462b3bf74
```
