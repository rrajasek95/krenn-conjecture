# N=8 P5 generic-L strict-order-seven point

## Result

The first apparent generic-$L$ P5 pure survivor is killed by the next mixed
compatibility at the deterministic exact point.  Retaining the third free
$z_{46}$ bend $r$, strict order seven has only the Q30 and Q33 compatibility
rows.  They are consistent and determine

$$
r=\frac{6630040}{13}.
$$

At this lifted jet both H1 degree nine and H0 degree ten vanish exactly.
Thus this point has no pure witness through the newly checked order.  This is
a point-local finite-order result, not yet generic-$L$ ideal membership or an
all-orders P5 theorem.

The exact checker is
`computations/verify_n8_p5_generic_L_strict7_point.py`.  Its frozen ledger has
SHA-256
`466ebdf963f95fe70bd9c2b6493257b7bde3be2fa99cefa6ee00198b3b74a81e`.

## Streamed mixed tail

The checker constructs the identity-safe third ambient-normal graph and
streams the 39 mixed equations one at a time.  After specializing the 45
base P5 parameters while retaining $r$, every degree-nine tail has at most
two univariate terms.  Releasing the ambient caches after each row keeps the
calculation below the earlier global-basis memory frontier.

The old strict-order-five and strict-order-six compatibility remainders both
recompute to zero.  Strict order seven leaves

$$
\begin{aligned}
Q30&=-3463864398000+6791850r,\\
Q33&= 831327455520-1630044r.
\end{aligned}
$$

Their roots agree at $r=6630040/13$, proving that this exact generic-$L$
point lifts one mixed order farther.

## Pure coefficients

With the same symbolic third bend installed, the pure coefficients are

$$
H1^{(9)}=0,
\qquad
H0^{(10)}=17180767414080-33687576r.
$$

The checker verifies the stronger pre-solution identities

$$
H0^{(10)}=-\frac{124}{25}Q30
          =\frac{62}{3}Q33.
$$

Consequently the unique mixed-compatible value of $r$ forces the apparent
H0 survivor to zero.  The nonzero 52-term normal form found before strict
order seven was therefore a compatibility candidate, not a survivor on this
longer jet.

## Frontier

The next decisive calculation is the symbolic localized version of the same
identity on the dense $L$ component: adjoin a symbolic third bend, form the
strict-order-seven Q30/Q33 relations, and reduce the full H0 degree-ten form.
If H0 belongs to that ideal generically, pure membership advances another
order on every checked P5 lane.  If the proportionality is special to this
point, another open sublocus may still retain a survivor.  Only after this
generic decision is it useful to build the fourth normal graph for the next
H1/H0 pure coefficients.
