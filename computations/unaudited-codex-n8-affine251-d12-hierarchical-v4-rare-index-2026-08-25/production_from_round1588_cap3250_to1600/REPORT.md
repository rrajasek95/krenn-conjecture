# Round1588 to round1600 production plan

The accepted round1588 cap3.25m candidate is continued through six exact two-round stages, split into two three-stage resource blocks. The v4.1 source, binary, and watchdog are unchanged; the run remains cold/rare, hierarchical, nonincremental, 16-worker, with native120/wrapper150/RSS36 and no portfolio.

Preflight passes. The 309,357-column headroom exceeds the 189,000 conservative six-stage projection derived from the maximum observed 25,200-column two-round growth and a 1.25 multiplier. Free space is 105,062,712 KiB, above the frozen 58,720,256 KiB floor. Both guards are recomputed before every stage; any failure stops without launching the next stage.

Production must stop at round1600 and remain held for an independent six-edge descendant scan and final all-column replay.

Production reached round1600 exactly. Six atomic stages cover rounds1589–1600 without gaps or overlaps. The endpoint exposes 3,089,153 columns with dual support6,162. Block A used352.461833 watchdog seconds and Block B353.115636 seconds; peak live RSS was24,879,776 KiB. Every launch passed the conservative cap and 56 GiB disk floors. The producer is sealed and held for independent audit.
