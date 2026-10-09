# Claim, construction and scope

## Claim

Under the retained interfaces, T(n) = O(n (log n)^(1−κ)) with

    κ = 1693453/2500000000 = 0.0006773812.

The complex saving is `b = 219037/312500000 = 0.0007009184`, on PR184's 10^-10 selection grid. The bit profile is PR200's complete fixed-coordinate/face-diagonal supplier with 112 additional endpoint-frame lowerings. Its exact paid coarse saving is `677840450131861/10^18`, up from PR200's `677773948354561/10^18`. PR184's unchanged pricing selects `C = 1694601/2500000000` and initial effective saving `a_0 = 1354814557990498681/2000000000000000000000`. The finite depth-2 leaf wrapper uses `a_(j+1) = (1-C)C + C a_j`, giving `a_1 = 3389200532065424457055321281/5000000000000000000000000000000` and `a_2 = 8473004997512436600350350404498103881/12500000000000000000000000000000000000000`. Exact checks establish `a_0 < a_1 < a_2 < C < 1-a_2`. The result exceeds PR199's computed `1693287/2500000000` by `83/1250000000`, and PR197's `135216063303877/200000000000000000` by `260176696123/200000000000000000`.

## What changes

PR184 (icekylinx) built a source-parity local word and a source-assisted frame flow on the PR168 snapshot `fd25adb7fbaa12ee761d02c733c54d1d2a7687ee`. This package keeps PR184's local configuration, arc transport, frame inheritance, flow, exact lift, contract checks, finite bridge, bit supplier and assembly. It changes two inputs. First, it replaces the three frozen query modules with PR168 v4's selected modules, the same modules that `scripts/paired_cube_producer.py` uses:

- `tmod_TE_TD_TB3_1_1_4_full_6.0617964e-4.json` (triple module),
- `pmod_J0_full_6.0666810e-4.json` (pair module),
- `qmod_climb3u_best.json` (all-but-one module).

It also changes the donor/recipient pairs. PR184 pairs each live gauge (recipient) with an earlier donor role by a plain maximum bipartite matching, and its flow then erases some donors with original-source X controls at cube parity frames. The pairs in `data/physical-pairs.json` come from `source_aligned_local_v4.py --avoid-parity-erasure`. This option takes a minimum-weight full matching of the recipients that avoids pairs the purification could erase. With these pairs the flow erases no donor and reuses no kernel. It finds far fewer dependent outgoing values (8,116 instead of 10,364), so it needs 1,412 fewer dirty births: R = 9,412 and W = 12,052. Any legal pairing is allowed. `paired_cube_physical.physical()` checks the legality of the frozen pairs, and PR184's exact lift and contract checks run on the resulting flow.

The old word that supplies the inherited frames is PR168 v4's own complex word: the producer cache and `references/paired-cube/physical/frames.json`. PR184's code transports the old matching arcs and the old preferred operation frames to the new local word, clips each frame to its exact future cap, and closes the frames forward. It then matches donors to recipients and checks the physical layer with the original `paired_cube_physical.physical()`.

## Bit supplier and finite wrapper

PR200 (Chafik Boukhalfa, with substantial Anthropic Claude and OpenAI Codex assistance) supplies a fixed-coordinate/face-diagonal PR168 v4 bit word with 7,282 descended operation frames, 1,760 compensated handoffs and 34 terminal sinks. Its complete graph, physical frames, word, terminal proof, exact frame prime witnesses, moment certificate and verifier are vendored under `research/paired-cube-diagonal-bit-168/` from exact head `a1175449f34d39ff933d9d8ab23ced1f32b290ec`. The unchanged upstream certificate gives R = 17,114, W = 20,634, rank mass = 1,483,712, deficit = 1,936 and largest child = 60. Its own verifier regenerates the source word, physical layer, terminal substitutions, every formal column, exact paid moment and all 47 strict inequalities/seven margins. The original PR200 source manifest is preserved byte-for-byte; the active manifest documents and pins the source-hash overlay required by this branch's stack.

The earlier PR189 endpoint-frame descent freezes 102 nonadjacent operation-frame lowerings from 2,534 eligible candidates. Its full physical ordering, frame geometry, terminal-write preservation and exact cost receipt remain separately recorded in `research/paired-cube-twin-local-168/bit/frame-descent.json`; it is a separate supplier and does not feed the final κ. The new PR200 descent is recorded in `research/paired-cube-diagonal-bit-168-followup/frame-descent.json`: the search selects 112 of 2,596 structurally feasible operations, across the full physical order including compensated handoffs. It preserves all 34 terminal sinks and contributes the exact physical histogram delta and rank-mass-neutral frame overlay.

`assemble.py` reprices the descended PR200 profile with PR184's `select()`, including the 10^-16 bad-row allowance, `32 m^2` fallback per edge, 10^-10 coarse grid and least payable atom on the 10^-12 grid. The selected `C = 1694601/2500000000` is below the exact `677840450131861/10^18` witness. Starting from PR184's ordinary-leaf price `a_0`, the PR185 finite acyclic wrapper is applied twice using the recurrence first applied to PR189 by PR199. The verifier checks the recurrence and closed form, positive atom toll, positive row-borrowing toll, and `a_0 < a_1 < a_2 < C < 1-a_2`. The physical wrapper is inherited from PR185. PR184's finite bridge still has `m ≤ 72`, `W < 10^7` and the uniform bit interface; the unchanged assembly checks all 47 strict constraints and seven positive margins.

## Checks

`verify.py` runs these steps:

1. The PR168 v4 producer regenerates the signed DAG, the carrier matching and the gauges, and checks them against `certificates/paired-cube-complex-input.json`.
2. `source_aligned_local_v4.py` builds the source-parity local word (all G channels `s`, all A channels `fd`, F = 2), with the frozen physical pairs in `data/physical-pairs.json`. `paired_cube_physical.physical()` checks every value span, alias, chain and target order.
3. PR184's `complex_frame_flow.py` prices the equal-frame flow with source-donor purification enabled and the frozen kernel reuse pairs in `data/kernel-pairs.json` (an empty list for these pairs).
4. PR184's `exact_complex_flow_lift.py` builds exact rational local lifts and inverse gate programs. It verifies the monotone flow and the zero-fresh kernel reuse DAG.
5. `contract_v4.py` runs PR184's contract validation unchanged: all fresh columns equal the identity over the integers, source controls sit at paid parity frames, original V injections precede all controls, controls precede K, centers finish in phase 1, target cap reads occur in phase 2, and target chains nest. It recounts the complete child histogram.
6. PR200's own verifier regenerates its unchanged parent bit certificate. The follow-up verifier checks the 112 frame assignments, full physical chains, unchanged terminal sinks, every F2 and integer column, exact paid moment and prime witnesses. `assemble.py` checks the complex half of PR184's construction receipts, reprices the descended bit profile with PR184's rational enclosures, applies the PR185 depth-2 finite wrapper and PR184 finite bridge, and checks all 47 strict constraints and seven margins. The PR189 descent verifier remains an independent regression check.

The exact candidate exceeds open PR199 and PR204, each of which reports `0.0006773148`, and PR197's reported `0.000676080316519385`. At the time this branch was prepared, those PRs had no checks reported. It remains Draft until complete CI, source checks and a post-CI leaderboard review finish; no validated public record is claimed before those gates.

## Scope

The validation scope retains PR184's conditional assumptions and arithmetic interfaces. The exact lift and contract checks establish the local maps and flow ledger; a globally renumbered scalar transcript of the complex word and a full Clifford/router replay are not included. The bit word and analytic/compiler interfaces are inherited from PR200; this package adds and verifies a finite exact physical-frame overlay. The finite ordinary-leaf wrapper and nested restoration argument are inherited from PR185, with the PR199 recurrence. This is a conditional finite witness, not an unconditional multiplication theorem or a global optimum.
