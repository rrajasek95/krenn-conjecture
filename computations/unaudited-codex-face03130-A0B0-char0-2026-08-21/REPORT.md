# Face `0:31:30`, closed pivot `A=B=0`

Status: **exact source interface frozen; the sole characteristic-zero gate
timed out, so the branch remains open.**

The normalized chart uses `b0=b1=b2=d1=1`.  The exact input contains `A`,
`B`, all sixteen literal rows `6..21`, and one fully expanded Rabinowitsch
row for exactly the original selected-base, both-live `a*d`, and remaining
`c`-numerator factors.  The sixteen source rows have rank sixteen over `Q`.
Neither `A` nor `H` is localized.

The canonical eight-thread exact-Q run reached its 600-second cap after
`600.224684s`.  It produced a zero-byte output, no unit sentinel, and no
positive-dimensional envelope.  Therefore `H` was not added: the instruction
to add it applied only after a verified positive-dimensional result.

Three replay modes give logical digest
`517e3411aea1c2b85e0b3665467857cd9b2e95697ca46f4c34ac0ea0d1a2cffb`;
the mutation digest is `2cbf250375bc389aa3143427775b58a54938377386d4e8fede0dccee988a8249`.
The exact input SHA is `135adba15d9da51cf0dac8797a063284f846403e6cb42266ce39a29dae71e257`.

This is a process blocker, not an algebraic result.  It says nothing about
the `A!=0,R25=0` branch, and it does not establish dimension, nonemptiness,
or emptiness of `A=B=0`.
