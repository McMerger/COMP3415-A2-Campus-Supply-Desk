# Testing notes

Mailles Machiana / COMP3415 A2 / November 8, 2026

Windows, Python 3.12.10, unittest. Tests use temporary saves. The starting commit
is `82ed75e`. There are 49 passing test methods now, including the original four.
Some methods check several inputs with subtests.

## Runs saved in evidence/

- `01-starter-tests.txt`: the original 4 pass.
- `02-regressions-before.txt`: 27 tests, 6 failures.
- `03-refactor-before-fixes.txt`: the same 6 failures after moving shared code.
- `04-baseline-fixes.txt`: all 27 pass after the fixes.
- `05-cr01-before.txt`: 49 tests, 5 failures and 8 errors before express support.
- `06-cr01-after.txt` and `07-final-tests.txt`: all 49 pass.

The old failures are kept to show what the tests caught before the fixes.

## Main things checked - all pass

Pricing: a $50 student order gets $5 off. A 5005-cent test price gives a 501-cent
discount. Standard delivery costs $6 at $95 after discount and nothing at $100.
See `tests/test_pricing.py`.

Stock and orders: notebook lines of 11 + 10 are rejected with stock 20; 9 + 11
are accepted. Cancelling twice doesn't add stock twice. Bad requests don't change
saves or use IDs. Reopened orders keep their original prices. See
`tests/test_validation.py` and `tests/test_lifecycle.py`.

Express: the client examples total $22, $84 and $132. The fee stays $12, even
above the free-standard-delivery threshold. Reopening and cancelling keep the
original totals. See `tests/test_express.py`.

Interfaces: real commands and scripted menu input check output, defaults, help,
errors and confirmation. See `tests/test_interfaces.py`.

## One extra check

Seven wrong changes were tried in temporary copies. They covered the discount
boundary, duplicate stock, repeated cancellation, waived or discounted express,
rounding down, and removing express from command choices. All seven were caught.
Output: `evidence/08-targeted-mutations.json`.

```sh
python -m unittest discover -s tests -v
python scripts/verify.py
```
