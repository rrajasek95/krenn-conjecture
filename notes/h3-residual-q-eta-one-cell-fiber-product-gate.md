# The eta primitive and residual correction form one fiber-product target, not a coefficient product

## Verdict

The additive eta primitive

\[
                         c_v=t-u_v                    \tag{1}
\]

cannot be multiplied into the residual correction

\[
 -\delta=(-1,1,1,-1)                                \tag{2}
\]

to produce a source-valid cell in the fixed repeated grade.  It can only be
the normalized terminal value of a new **relative** cell.  At the augmented
row level, one such cell can carry (2) and (1) simultaneously, so the two
obstructions do not force two generators.  Its existence is one exact
fiber-product image-membership theorem.

There is one further physical condition.  The eta primitive is exact only
on the marked clean eta slice.  The next target stabilizer fixes (t,u_v) but
moves the corrected endpoint by (q_{pq}^{22}).  A full physical cell must
therefore carry the additional terminal response

\[
                         -q_{pq}^{22}                 \tag{3}
\]

facewise.  Neither (1) nor the ordinary-residue signature (2) supplies (3).

## Why ordinary multiplication fails

Use the full eight-site grading with

\[
 \deg t=e_p+e_q,\qquad \deg u_v=e_x+e_v.             \tag{4}
\]

Let (g) be the fixed degree of the resolved residual packet.  Then

\[
 (\deg t+g)-(\deg u_v+g)=\deg t-\deg u_v\ne0.       \tag{5}
\]

Thus a common residual tail or a common `P3+K2` multiplier cannot make

\[
                         (t-u_v)(-\delta)             \tag{6}
\]

homogeneous.  This is independent of the chosen (g); it cancels from (5).

The minimal complementary homogenization does not give a higher cell.  It
is the coefficientwise identity

\[
 u_v\bigl(t(-\delta)\bigr)
       -t\bigl(u_v(-\delta)\bigr)=0.                 \tag{7}
\]

Both terms in (7) are the same labelled monomial (tu_v(-\delta)).  A
nonzero construction must retain distinct endpoint/rootless source labels,
which is precisely relative or mapping-cone data.

There is also a simpler boundary mismatch: even if (6) were written
formally, its residue is (-(t-u_v)\delta), not the required (-\delta).
Dividing by (t-u_v) would introduce a new localization, fail where the
primitive vanishes, and undo the proposed terminal factor.  It is not a
global construction.

## The extra stabilizer condition

For the five marked stabilizers,

\[
 \eta_z(c_v)=1+\delta_{vz}u_z/t,
 \qquad d\Omega_v(\eta_z)=-1-\delta_{vz}u_z/t.       \tag{8}
\]

So (Omega_v+c_v) is eta-invariant facewise.  This is the useful content of
the additive primitive.

Now apply the further target stabilizer

\[
              \sigma_{p,2}=1,\qquad \sigma_{x,2}=-1.
\]

It fixes (t) and every (u_v), hence fixes (c_v), while

\[
 \Omega_v+c_v=q_{pq}^{22}-q_{xv}^{0m_v}
\]

has sigma derivative (+q_{pq}^{22}).  The cyclic aggregate failure is

\[
                         5q_{pq}^{22}.                \tag{9}
\]

Consequently the physical terminal lift of (1) needs (3).  The residual
condition (2) lives in the ordinary-residue rows and does not determine a
sigma-terminal response.  The direct sum of the two presently specified
interfaces is therefore still incomplete.

## Exact one-cell criterion

Fix a face (v), the source word `1211222`, and the labelled repeated
`P3+K2` comparison grade.  Let (B) be the common augmented base consisting
of

```text
endpoint-odd main boundary D,
physical W,
target,
anchor incidence.
```

Let (F_v^{res}) be the resolved four-corner residue presentation and let
(F_v^{term}) be the terminal presentation retaining all (eta_z) values and
the (sigma) value.  Form the fiber product over their common base:

\[
 F_v=F_v^{res}\times_B F_v^{term}.                   \tag{10}
\]

The desired element (f_v\in F_v) has the three projections

\[
\begin{aligned}
 D(f_v)&=0,\\
 \operatorname{ores}(f_v)&=-\delta,\\
 d r_v(\eta_z)&=1+\delta_{vz}u_z/t,\\
 d r_v(\sigma)&=-q_{pq}^{22},\\
 (W,\operatorname{tgt},\operatorname{ainc})(f_v)&=(0,0,0).
\end{aligned}                                        \tag{11}
\]

These outputs are formally compatible:

* the endpoint-odd residue projection of (-\delta) is
  (-e_{00}+e_{11}), whose tail incidence sum is zero;
* the eta values integrate to (t-u_v);
* the sigma value in (11) cancels the remaining (+q_{pq}^{22}); and
* both sides land at zero in (B).

Thus one formal column has every required row, and adjoining it to the
standard graph raises rank by one.  No rank or readout argument currently
forces separate residual and eta generators.

Let

\[
 \Psi_v:C_{g,v}^{\rm phys,rel}\longrightarrow F_v   \tag{12}
\]

be the complete source-labelled relative/Spencer map in this word and
grade.  The sharp construction theorem is exactly

\[
                         f_v\in\operatorname{im}\Psi_v.               \tag{13}
\]

The standard transport graph does not prove (13): it obeys (R=D), whereas
(11) has (D=0) and nonzero residue.  The coefficient-ring eta construction
does not prove it either, by (5), (7), and (9).  A new relative source cell
could prove (13), but no committed inventory constructs it.

## Frontier consequence

The sharpest justified theorem is therefore:

* actual construction: **not obtained**;
* literal additive/multiplicative combination: **excluded by multigrading,
  residue normalization, and the extra stabilizer**;
* remaining positive interface: **one relative-cell fiber-product
  criterion**, equation (13).

This improves the attack target.  Search for one source-labelled
relative/Spencer cell with the complete three-projection signature (11),
not for a scalar multiple of a standard bar or for two unrelated correction
cells.

Verification:

```text
python3 computations/verify_h3_residual_q_eta_one_cell_fiber_product_gate.py
python3 -O computations/verify_h3_residual_q_eta_one_cell_fiber_product_gate.py
python3 -I -S computations/verify_h3_residual_q_eta_one_cell_fiber_product_gate.py
```

Frozen ledger SHA-256:

```text
cb1dace33e0557afc263026ecac86927d2013706cc3735e0f2a658957bf295f7
```
