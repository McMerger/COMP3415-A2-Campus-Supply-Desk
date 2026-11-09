# Testing evidence record

Environment: Windows, Python 3.12.10, standard-library unittest. The source
application requires Python 3.10+. Python 3.10 itself was not tested. Runs use
temporary save files and do not touch personal application data. Baseline:
`82ed75e0714e50c086a13ee491f51b349814d8a4` from the instructor repository.

## Recorded development stages

| Stage | Observed result | Evidence |
| --- | --- | --- |
| Original starter suite | 4 tests pass | evidence/01-starter-tests.txt |
| Added baseline requirements tests | 27 tests, 6 failing assertions | evidence/02-regressions-before.txt |
| Shared logic refactor, before bug fixes | 27 tests, same 6 failing assertions | evidence/03-refactor-before-fixes.txt |
| Corrected baseline behavior | 27 tests pass | evidence/04-baseline-fixes.txt |
| CR-01 and adapter tests before express support | 49 tests, 5 failures and 8 errors | evidence/05-cr01-before.txt |
| Express support added | 49 tests pass | evidence/06-cr01-after.txt |
| Final reproducible run | 49 tests pass | evidence/07-final-tests.txt |
| Targeted regression sensitivity | 7 of 7 mutations detected | evidence/08-targeted-mutations.json |

unittest counts methods; subtests exercise additional input partitions. The
six baseline failures occur in four test methods, with separate quote/place
subtests. CR-01 pre-implementation failures/errors are expected red tests,
not failures in the final result. Early logs preserve their actual commands'
raw output; they are not reconstructed from the corrected application.

## Expected and observed cases

| Requirement/case | Expected and final observed result | Test location |
| --- | --- | --- |
| Student subtotal exactly 5,000 cents | 500-cent discount in quote and place | test_pricing.py |
| Student subtotal 4,750 cents | No student discount | test_pricing.py |
| 5,005-cent synthetic subtotal | Discount rounds half-up to 501 cents | test_pricing.py |
| Standard delivery at 9,500 / 10,000 / 12,000 | Fees 600 / 0 / 0 cents | test_pricing.py |
| Student merchandise 10,000 before discount | Fee still 600 after 1,000 discount | test_pricing.py |
| Duplicate notebook quantities 11 + 10 | ValueError, no saved mutation | test_validation.py |
| Duplicate notebook quantities 9 + 11 | Two lines retained; stock 0; cancel restores 20 | test_lifecycle.py |
| Second cancellation of two mugs | Stock remains 8; save bytes unchanged | test_lifecycle.py |
| Invalid quantity bool/string/fraction/range | ValueError, saved bytes and numbering unchanged | test_validation.py |
| Invalid later line | No partial order or stock change | test_validation.py |
| Quote then competing placement in same session | Placement rechecks now-insufficient stock | test_lifecycle.py |
| Existing malformed/unreadable save | Error, no silent reset | test_lifecycle.py |
| Historical prices after catalog fixture change | Original order snapshot preserved | test_lifecycle.py |
| Regular express, two notebooks | Delivery 1,200; total 2,200 cents | test_express.py |
| Student express, two hoodies | Discount 800; total 8,400 cents | test_express.py |
| Regular express, three hoodies | Delivery 1,200; total 13,200 cents | test_express.py |
| Student express above free-standard threshold | Express fee remains 1,200 cents | test_express.py |
| Express order reopen/cancel/repeat cancel | Original totals and fulfillment retained | test_express.py |
| Real CLI quote/place/show/history/cancel | JSON output, correct state and exit codes | test_interfaces.py |
| Both command help screens | Express choice discoverable | test_interfaces.py |
| Menu typed quantities and defaults | Integers parsed; regular/pickup preserved | test_interfaces.py |
| Menu declined placement/cancellation | No saved mutation | test_interfaces.py |
| Menu confirmed express placement | $84.00 displayed; express persisted | test_interfaces.py |
| Menu bad input, EOF, Ctrl+C | Retry or clean exit, as specified | test_interfaces.py |

All test locations above are under `tests/`. Tests use fixed independently
calculated expected amounts rather than calling production pricing code to
construct their expected values. Only fixture setup for unreachable catalog
price/stock boundaries and simulated file permission failure uses mocks.
Menu tests patch input; command tests spawn real Python processes.

## Reproduce locally

```sh
python -m unittest discover -s tests -v
python scripts/verify.py
git diff --check
```

`verify.py` reruns the complete suite, then copies application/test files to
temporary directories and changes one defect at a time. It does not mutate
the working source. Outputs 07-09 are overwritten on rerun. Metadata includes
UTC recording time, Python version, exact command and SHA-256 hashes for all
Python source and test files.

## Targeted mutations

1. Exclude the exact student-discount threshold.
2. Check duplicate stock per line instead of combined quantities.
3. Restore stock again on repeated cancellation.
4. Waive express delivery at the standard free-delivery threshold.
5. Discount the express fee for students.
6. Round a half-cent discount downward.
7. Remove express from command parser choices.

All seven are detected by assertion failures in isolated suites. This is a
hand-selected regression check, not an exhaustive mutation-testing score or
a statement-coverage measurement. No coverage percentage is claimed.

## Verification limits

No physical keyboard usability study was performed. Menu evidence is scripted;
EOF and Ctrl+C are simulated exceptions. File permission errors are simulated
to remain reliable across Windows permission configurations. Save crashes,
multiple writers, arbitrary manual edits and schema migration are outside
scope. The full assignment handout is unavailable, so exact evidence-format
and grading requirements still need comparison. Nothing has been submitted
to D2L or pushed to GitHub.
