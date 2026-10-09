# Source-assisted complex word on PR168 v4 modules

This package applies the [PR184](https://github.com/CrocSwap/integer-mult-bounds/pull/184) source-parity local word and source-assisted frame flow to the PR168 v4 query modules. PR184 used the older PR168 snapshot `fd25adb7fbaa12ee761d02c733c54d1d2a7687ee`. The newer modules and a new choice of donor/recipient pairs give a stronger complex supplier. The bit supplier starts from [PR200](https://github.com/CrocSwap/integer-mult-bounds/pull/200), whose complete construction is vendored under `research/paired-cube-diagonal-bit-168/` from head `a1175449f34d39ff933d9d8ab23ced1f32b290ec`; [the follow-up package](../paired-cube-diagonal-bit-168-followup/) lowers 112 additional operation frames on that word while preserving its terminal sinks. We price the descended exact profile with PR184's unchanged assembly and pass it through the depth-2 finite ordinary-leaf wrapper from [PR185](https://github.com/CrocSwap/integer-mult-bounds/pull/185), following the recurrence first applied to PR189 in [PR199](https://github.com/CrocSwap/integer-mult-bounds/pull/199). The earlier 102-operation PR189 frame descent remains separately certified in the branch and is not substituted for the PR200 descent.

## Complex supplier

| Quantity | PR184 (fd25adb7 modules) | PR191 (v4 modules) | PR193 and this version (v4 modules, new pairs) |
| --- | ---: | ---: | ---: |
| Physical auxiliaries `R` | 11,056 | 10,824 | 9,412 |
| Persistent roles `W` | 13,696 | 13,464 | 12,052 |
| Source-controlled erasures | 1,410 | 1,412 | 0 |
| Zero-fresh kernel reuses | 706 | 707 | 0 |
| Complex saving | 6.570752e-4 | 6.630702e-4 | 7.009184e-4 |

PR193 changed the donor/recipient pairs. PR184 matches donors to recipients with a plain maximum matching. Here `source_aligned_local_v4.py --avoid-parity-erasure` picks a full matching that avoids pairs which PR184's parity purification would erase. The flow then needs 1,412 fewer dirty births.

## Bit supplier and κ

The complex saving is 219037/312500000 = 0.0007009184, so the bit-side constraints bind. PR200's exact coarse bit witness is `677773948354561/10^18`; the new physical descent raises it to `677840450131861/10^18`. PR184's unchanged pricing grid selects `C = 1694601/2500000000` and initial effective saving `a_0 = 1354814557990498681/2000000000000000000000`. The depth-2 recurrence `a_(j+1) = (1-C)C + C a_j` gives `a_1 = 3389200532065424457055321281/5000000000000000000000000000000` and `a_2 = 8473004997512436600350350404498103881/12500000000000000000000000000000000000000`; exact checks establish `a_0 < a_1 < a_2 < C < 1-a_2`. The unchanged 47-constraint assembly then yields the final κ below.

| Version | Bit supplier | Binding side | κ |
| --- | --- | --- | ---: |
| PR191 | PR184 | complex | 6.626307e-4 |
| PR193 | PR184 | bit | 6.647872e-4 |
| PR194 baseline | PR189 | bit | 6.674324e-4 |
| PR199 legacy | PR194's PR189 bit + finite leaf bootstrap | bit | 6.678525e-4 |
| PR197 | packed PR187 bit residuals | bit | 6.76080316519385e-4 |
| PR200 standalone | stronger bit supplier, its own complex word binds | complex | 6.65046903615388e-4 |
| PR199 composition | PR194 complex + PR200 bit + depth-2 bootstrap | bit-side assembly constraints | 6.773148e-4 |
| PR204 composition | same exact suppliers and depth-2 bootstrap, no frame descent | bit-side assembly constraints | 6.773148e-4 |
| this follow-up | PR194 complex + PR200 bit after 112 frame lowerings + depth-2 bootstrap | bit-side assembly constraints | **6.773812e-4** |

The exact result is κ = 1693453/2500000000 = 0.0006773812. It exceeds open PR199 and PR204, each reporting `1693287/2500000000`, by `83/1250000000`, and PR197's `135216063303877/200000000000000000` by `260176696123/200000000000000000`. Those comparison PRs had no checks reported at the time this branch was prepared. This remains a candidate until this branch's complete CI and final live leaderboard review finish; it is not an unconditional theorem or a claim of global optimality. Exact recurrence values, all 47 strict constraints and all seven positive margins are recorded in `certificate.json`.

Run from the repository root with Python assertions enabled:

```sh
python3 -m pip install -r research/source-assisted/requirements-round13.txt
make verify-source-assisted-v4
```

The target checks package source hashes, regenerates PR189 and PR200's unchanged parent certificates, replays the 112-operation PR200 frame-descent witness and its prime exclusions, rebuilds the PR168 v4 complex cache and source-parity word, runs PR184's unchanged frame-flow and exact-lift checkers, verifies the contract, recomputes the exact assembly and compares it with `certificate.json`. The source manifests pin the vendored PR200 construction, descent inputs and finite leaf wrapper inputs. Scratch files go to `.work/` inside this package, and the verifier deletes them at the end.

See [PROOF.md](PROOF.md) for the claim, the changes, and the scope.
