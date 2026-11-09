# Notes on the AI suggestions

Mailles Machiana / COMP3415 A2

AI assistance was used for tests, implementation and writing after Checkpoint A. The shared-builder suggestion came up during implementation;
the other options were considered when writing this evaluation.

## Sharing the calculations - useful

Quote and place had almost the same code. `_build_quote` removes that repetition
and uses the state already loaded by the caller. The refactor kept the same
failures before the bugs were fixed. Tests also compare quote and order prices.

## Dictionary lookup - useful in some places

It works for stock changes with validated IDs. Raw IDs are different: a list or
dictionary can cause TypeError, when the service should raise ValueError.
Keeping the small validation scan was fine for five products. This wasn't a
measured speed improvement.

## round() for the discount - doesn't fit the rule

Python rounds ties to even. The spec wants half cents rounded up, so the integer
formula stayed. A 5005-cent fixture needs a 501-cent discount and checks that case.

## Reusing free delivery for express - wrong result

CR-01 says express always costs $12. Reusing standard delivery's threshold would
waive it on bigger orders. A separate branch keeps the rule clear. Tests check
that the fee isn't waived or discounted.

## Bigger changes - not needed here

A database and delivery classes would add work without solving another required
problem. JSON and a short conditional were enough. Duplicate lines stay separate;
only the stock check adds their quantities together.

The 49 passing tests and seven caught wrong changes support these decisions.
They don't mean there can't be another bug.
