# Exact frame descent on the PR200 bit word

## Result

The PR200 bit supplier has a new exact physical-frame overlay. Its paid coarse
saving increases from

    677773948354561/10^18 = 0.000677773948354561

to

    677840450131861/10^18 = 0.000677840450131861.

The exact coarse gain is `665017773/10^16`. Repricing through PR184's unchanged
selection and balanced assembly, followed by the PR185 depth-2 finite
ordinary-leaf construction used in PR199, gives

    κ = 1693453/2500000000 = 0.0006773812.

This exceeds PR199's computed `1693287/2500000000` by
`83/1250000000 = 0.0000000664`, and PR197's published claim
`135216063303877/200000000000000000` by
`260176696123/200000000000000000`. The complex profile remains the PR193/194
source-assisted v4 profile with saving `219037/312500000`; the bit side still
binds. Open PR204 currently reports the same exact
`1693287/2500000000`; this candidate exceeds it by the same `83/1250000000`.

## Frame construction

The deterministic search ranks single-operation endpoint lowerings by their
floating point moment-root estimate. A candidate replacement frame is the join
of the actual physical predecessor frames and the node's full value span. It is
admitted only when it is nondegenerate and contained in both successor frames
on both physical ports. Candidates that change terminal-sink writes are
excluded. The search finds 2,596 structural candidates and 112 positive
single-operation candidates. A deterministic greedy independent set on
consecutive operations in the full physical role chains selects all 112.
Scores choose the proposals only; the verifier certifies the frozen batch with
exact arithmetic.

The selected batch adds 266 total frame-dimension reductions. The complete
physical word has 41,288 operations and 17,148 physical chains. It has 7,394
operation frames different from the compiler frames, versus 7,282 in PR200.
The physical internal rank histogram changes by:

| Rank | Delta | Rank | Delta | Rank | Delta |
| ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | +94 | 2 | +116 | 3 | -66 |
| 4 | +24 | 5 | -32 | 7 | -36 |
| 9 | -18 | 10 | -6 | 11 | +10 |
| 12 | -24 | 13 | +2 | 14 | -18 |
| 16 | +48 | 18 | -46 | 19 | +46 |

This preserves the exact physical rank mass. The operation word, gauges,
compensated handoffs, terminal sinks and target-read schedule are unchanged.
The verifier reconstructs all role chains, checks frame geometry and nesting,
independently rebuilds each selected frame as the exact join of both actual
predecessor frames and the written node's value span, and checks that it lies
inside both actual successor caps. It then reruns the complete F2 and
defining-integer-decoder columns, including
source and dirty-register restoration. It replays terminal sink chronology and
recomputes the exact paid moment certificate. A separate exact prime witness
set covers every used frame, including the new frames.

## Exact composition

The PR200 source profile is repriced with PR184's unchanged rational moment
enclosures, `10^-16` bad-row allowance, `32 m^2` fallback, `10^-10` coarse
grid, least payable atom on the `10^-12` grid, and finite bridge. Applying the
depth-2 recurrence

    a_(j+1) = (1-C)C + C a_j

to the resulting ordinary leaf gives the exact effective bit saving and the
stated κ. The verifier recomputes the recurrence and exact assembly, then
checks all 47 strict inequalities and seven margins. The PR200 baseline and
descended candidate use the same complex profile, pricing code, and leaf
construction, so the difference comes from the physical bit histogram only.

## Dependencies and limits

This is conditional on PR200's analytic and compiler interfaces, exact finite
bit-word contracts, PR184's arithmetic/precision and finite-bridge interfaces,
and PR185's completed finite ordinary-leaf construction. PR199 supplies the
depth-2 pricing recurrence and its application to PR200. The endpoint-frame
descent method follows PR198; this package applies it to PR200's different
physical graph. PR200's original files and source manifest remain unchanged
and are pinned as the parent witness.

The candidate does not establish a global optimum over possible frame
assignments. The composed multiplication bound remains conditional; this
certificate does not remove the inherited all-size or compiler hypotheses.
