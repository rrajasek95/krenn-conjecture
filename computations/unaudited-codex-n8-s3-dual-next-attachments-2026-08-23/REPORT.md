# Minimal S3 dual: raw lift and first attachment

The localized three-row dual lifts to a common support factor
`A_25[0,0] A_67[0,0]`, but its three coefficient extractions come from
separately multiplied raw source terms.  It is not a single raw Bianchi or
carrier identity.

Every genuinely new total-degree-six column incident to the dual was found
by inverse deletion.  There are 14, and every one is a singleton on the y3
layer with pairing `+/-1`.  The lex-first is

```text
code       135 (word 00012000)
multiplier 1557 = A_03[1,0] A_14[2,0]
output     1557a7
pairing    +1
raw row    00155787a7f3
```

It has no cap-response spoke pair, so it is neither a triangle blocker nor a
rank-drop condition.  It kills the cubic dual before a carrier HPL lift.

For the canonical cap `67` and triangle `012`, the K00 response packet is
`3072a7 + 3969a7`.  These are two separate degree-six singleton columns.
Replacing `K00` by the direct blocker `<K,A_67>` adds 16 off-support cap
terms, but they first appear as 16 further, independent degree-seven
singleton columns.  No single next attachment supplies the direct-blocker
combination.

Replay with `audit_s3_dual_next_attachments.py --check`; hostile mutation is
rejected by `--mutate`.
