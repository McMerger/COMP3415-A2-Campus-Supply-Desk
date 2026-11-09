# Testing notes

Mailles Machiana / COMP3415 A2 / November 8, 2026

Windows, Python 3.12.10, unittest. Tests use temporary saves. The original starter
is 82ed75e. There are now 50 passing test methods, including the original four.
Report section 2 explains the four required testing categories.

## Runs in evidence/

- 01: original 4 pass.
- 02: 27 tests, 6 failing assertions before refactoring.
- 03: the same 6 failures after sharing the code and naming constants.
- 04: all 27 pass after correcting the three defects.
- 05: 49 tests, 5 failures and 8 errors before express support.
- 06: all 49 pass after express support.
- 07: final 50 pass, including the new $50 express round-trip case.
- 10/11: reruns of the same 49 tests before/after the money-name refactor; both pass.
- 12: actual rejected rounding comparison, 500 versus required 501 cents.

The full filenames identify each stage. Early failures are retained, not replaced
with newly passing output. Logs 10/11 were made during final review by running
the prior service snapshot and renamed version, not claimed as older executions.

## Required categories and observed results

Normal: regular pickup of two notebooks totals 1000 cents, before and after.
Boundary: exactly $50 gets a 500-cent student discount; starter returned zero,
final code returns 500. Delivery at 9500/10000 after discount costs 600/0.
Invalid: bad types, empty requests and stock of 20 against 11+10 duplicate items
raise ValueError without saving or consuming IDs. The duplicate case failed in
the starter and passes now.
Preservation: quotes don't save/reserve; order prices, stock and IDs survive
reopening and cancellation. Final lifecycle tests pass.

## Further checks

Express examples total $22, $84 and $132. Menu and real command-process tests
cover help, defaults, errors and confirmation. Seven deliberate wrong changes
are caught; see 08-targeted-mutations.json. File 09 records source/test hashes.
No coverage percentage is claimed; menu interruptions/permissions are simulated.

```sh
python -m unittest discover -s tests -v
python scripts/verify.py
```
