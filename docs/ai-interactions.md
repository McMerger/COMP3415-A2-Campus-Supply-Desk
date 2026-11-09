# AI-use record - final review

Mailles Machiana / COMP3415 A2 / November 8, 2026

This is a relevant interaction excerpt from the current assignment chat, not a
complete transcript. The three recommendations were made during final review,
after the initial implementation. They are recorded here now, not backdated.
The assistant also helped with tests, code and writing after Checkpoint A.

## Request

User: "execute and be done with it"

Context: revise the existing work against the newly supplied original handout.

## Actual assistant recommendation excerpt

"For the Task 6 record, I'm evaluating three suggestions now: add an exact-$50
express-order round-trip test; replace catalog scans with dictionary lookup;
and replace the discount formula with round(subtotal * 0.1). The record will
show these as final-review suggestions, not as older interactions."

The excerpt above normalizes Markdown backticks and dollar-sign formatting.
The source is the visible assistant commentary in this chat immediately before
the final-review code and test changes.

## Decisions and what happened

1. ACCEPT the combined $50 express round-trip test. Added
   `tests/test_express.py::ExpressTests.test_exact_discount_threshold_round_trip`
   in commit c5f1bb5. Expected amounts: 5000 subtotal, 500 discount, 1200 fee,
   5700 total. The test also checks saved snapshots, stock and ORD-0002 after
   cancelling. Final log 07 shows 50 tests passing.
2. MODIFY dictionary lookup. Retain the existing split: `_change_stock` indexes
   trusted IDs; `_build_quote` scans the five products to validate raw input.
   Validation tests reject list/dict IDs with ValueError without changing saved
   data. This final-review recommendation confirms the existing approach rather
   than inventing a new earlier implementation decision.
3. REJECT floating-point round. The comparison was actually run: round(5005 * 0.1)
   gives 500, but integer half-up gives 501. Output is in log 12. Production keeps
   integer arithmetic; the fixture test expects 501 and passes.

## Evidence to inspect

- Report section 6 gives the technical reasoning for all three choices.
- `evidence/07-final-tests.txt`: final suite, including the new case.
- `evidence/08-targeted-mutations.json`: seven caught wrong changes.
- `evidence/12-rounding-comparison.txt`: the rejected alternative's result.
- `supplydesk/service.py`: final validation, stock lookup and discount formula.

Public record: https://github.com/McMerger/COMP3415-A2-Campus-Supply-Desk/blob/main/docs/ai-interactions.md
