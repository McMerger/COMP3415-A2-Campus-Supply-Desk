# Notes on AI recommendations

Mailles Machiana | COMP3415 Assignment 2

AI assistance: Codex supported the tests, implementation and writing after
Checkpoint A. The shared-builder suggestion came up during implementation;
the other options below were considered when preparing this evaluation.

## Share the quote and order calculations - accepted

The starter repeats the same rules in two methods. `_build_quote` now handles
both, so a pricing change only needs to be made once. It uses the state already
loaded by the caller. The refactor kept the same six failing assertions before
the bug fixes, and tests compare quote and order results afterward.

## Use dictionary lookup everywhere - partly accepted

A dictionary is useful for adjusting stock using validated product IDs. Using it
directly on incoming IDs could raise TypeError for a list or dictionary instead
of the required ValueError. The small catalog scan was kept for validation.
Explicit type validation could make indexing safe too; this was a simplicity
choice, not a measured performance improvement.

## Use floating-point round() for the discount - rejected

`round(subtotal * 0.1)` does not express half-up rounding. The integer formula
was kept. A 5,005-cent test fixture needs a discount of 501 cents, so it catches
the difference. The bundled prices do not reach that half-cent case on their own.

## Reuse standard delivery's threshold for express - rejected

CR-01 says the $12 express fee is never waived. A separate express branch avoids
accidentally applying free standard delivery to it. High-value orders and student
orders are tested to make sure the fee is neither waived nor discounted.

## Add a database or delivery classes - rejected

Three delivery choices do not need a new hierarchy, and the assignment already
uses JSON storage. Keeping those parts small makes the actual changes easier to
check. Duplicate item lines also stay separate in the result; their quantities
are combined only when checking stock.

The recommendations were checked against the specification and test results.
The 49 passing tests and seven caught wrong changes support these decisions,
but they are not proof that the application has no remaining bugs.
