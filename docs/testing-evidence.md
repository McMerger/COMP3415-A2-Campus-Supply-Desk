# Testing record

Mailles Machiana | COMP3415 Assignment 2 | November 8, 2026

Tests ran on Windows with Python 3.12.10 and unittest, using temporary save files.
The final suite has 49 passing methods, including the original four. Some methods
use subtests for several inputs. The starting commit is `82ed75e`.

## Before and after

These logs are under `evidence/`. Earlier failures show what the tests caught
before the corresponding code was fixed or added.

| Run | Result | Log filename |
| --- | --- | --- |
| Starter | 4 pass | 01-starter-tests.txt |
| Added baseline tests | 27 tests, 6 failures | 02-regressions-before.txt |
| Shared-code refactor | Same 6 failures | 03-refactor-before-fixes.txt |
| Three fixes | 27 pass | 04-baseline-fixes.txt |
| Express tests before support | 49 tests, 5 failures and 8 errors | 05-cr01-before.txt |
| Express implemented | 49 pass | 06-cr01-after.txt |
| Final verification | 49 pass | 07-final-tests.txt |

## Main checks - all pass

- Pricing: a $50 student order gets $5 off. A 5,005-cent test subtotal rounds
  the discount to 501 cents. Standard delivery costs $6 at $95 after discount
  and is free at $100. See `tests/test_pricing.py`.
- Validation: duplicate notebook lines of 11 + 10 are rejected when stock is 20.
  Bad quantities, empty requests and an invalid later item leave saves and IDs
  unchanged. See `tests/test_validation.py`.
- Orders: duplicate lines of 9 + 11 are accepted. Cancelling restores stock once,
  even after reopening. History keeps original prices. Placement rechecks stock
  after a quote. See `tests/test_lifecycle.py`.
- Express: two notebooks total $22; two hoodies for a student total $84; three
  hoodies for a regular customer total $132. The fee stays $12, and reopening
  or cancelling preserves the original totals. See `tests/test_express.py`.
- Interfaces: real command processes and scripted menu input check defaults,
  help, output, errors and confirmation. See `tests/test_interfaces.py`.

## Extra check and rerunning

Seven wrong changes were introduced in temporary copies: excluding the $50
boundary, checking duplicates separately, restoring stock twice, waiving or
discounting express, rounding down and removing express from command choices.
All seven were caught; output is in `evidence/08-targeted-mutations.json`.

```sh
python -m unittest discover -s tests -v
python scripts/verify.py
```
