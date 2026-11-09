# AI recommendations and critical evaluation

This is an AI-assisted decision record prepared during implementation. It is
not a verbatim full chat transcript, an independent student critique, or a
replacement for the already-submitted Checkpoint A. The student should review
these decisions and add their own assessment before submitting the report.

The task supplied to Codex was to proceed with tests, refactoring, CR-01 and
local deliverables after Checkpoint A, keeping everything local before push
approval. Evidence includes inspected starter code, FUNCTIONAL_SPEC.md,
the supplied CR-01, and recorded before/after runs.

## R1 - Share request validation and pricing

Recommendation: extract a single quote builder used by both quote and place.
Decision: accepted. The two starter methods repeated nearly the same request
validation, line construction and money rules. `_build_quote` receives the
loaded state; placement validates that same state before reducing inventory.
Calling public `quote()` from placement instead would load the file again and
obscure which snapshot is being changed. Separate quote/order agreement and
recheck-after-quote tests check the result. The structural refactor was
committed separately and retained all six pre-existing failing assertions.

## R2 - Use dictionary lookup everywhere

Recommendation: replace all catalog scans with an index for faster lookup.
Decision: accepted only for internal stock changes; rejected for unvalidated
external product IDs. A list/dict supplied as a product ID must produce
ValueError as an invalid request, but a direct dictionary lookup can raise
TypeError for an unhashable key. The public validation path retains its small
catalog scan. Invalid list/dict product IDs are exercised in the validation
test. `_change_stock` indexes only validated snapshot lines. No performance
benefit is claimed for this five-product application.

## R3 - Simplify discounts with floating-point round()

Recommendation: compute `round(subtotal * 0.1)`.
Decision: rejected. The specification requires integer cents and half-up
rounding. Python rounding uses ties to even, and binary floats are unnecessary.
The existing integer formula is retained. A 5,005-cent synthetic merchandise
fixture requires a 501-cent discount; rounding down is caught by a targeted
mutation. This fixture is necessary because bundled prices cannot yield a
half-cent discount. This alternative was evaluated, not committed or run as
an implementation.

## R4 - Treat express as a larger standard delivery fee

Recommendation: reuse standard delivery's threshold and change only its fee.
Decision: rejected. CR-01 explicitly prohibits waiving express fees. A distinct
express branch always sets 1,200 cents after calculating the merchandise
discount. Tests cover high-value regular and student orders, merchandise
below the student threshold, and the exact discount threshold. Mutations that
waive or discount express fees are detected.

## R5 - Introduce delivery strategy classes or a database

Recommendation: generalize fulfillment into classes and replace JSON storage.
Decision: rejected for this scope. Three fixed fulfillment values do not
justify a strategy hierarchy, and database migration would change the starter
application beyond the requested improvement. The small conditional and schema
version 1 remain. Crash recovery and concurrent writers are expressly outside
the functional spec. This option was considered, not implemented.

## R6 - Combine duplicate lines in returned orders

Recommendation: merge duplicate product lines to simplify stock handling.
Decision: adapted. Combined quantities are tracked for stock validation while
the original ordered lines remain separate. The spec permits separate lines;
retaining them reduces observable output changes. A duplicate request exactly
at stock capacity is placed, preserved as two lines and restored by cancelling.

## Limits of this evaluation

Record provenance: R1 describes the shared-builder recommendation made during
implementation. R2-R6 document design alternatives evaluated by the AI while
preparing this decision record; they are not attributed to an earlier model
response or an unavailable prompt transcript. The options and their critiques
must not be presented as independent human recommendations or human review.

Passing tests and seven detected hand-selected mutations support specific
claims; they do not prove exhaustive correctness. The report and critique were
generated with AI assistance and have not yet been independently reviewed by
the student. No original Checkpoint A text was available for comparison.
