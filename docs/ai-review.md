# AI decision notes

Mailles Machiana / COMP3415 A2

AI assistance was used after Checkpoint A. These three suggestions were evaluated
during final review. The actual interaction excerpt and evidence are in
`docs/ai-interactions.md`, supplied as the AI-use record.

## ACCEPT - test the $50 express order from start to finish

Added a test that quotes and places two bags for a student using express, then
reopens, cancels twice and places another order. Expected amounts are
5000/500/1200/5700 cents. Stock is restored once and the next ID is ORD-0002.
Commit c5f1bb5 adds the case. It passes; the full suite now has 50 tests.

## MODIFY - use dictionary lookup everywhere

Keep indexing for validated stock updates, but keep the small scan for raw
product IDs. Otherwise list/dict IDs can cause TypeError instead of ValueError.
The existing validation tests check those inputs without saved changes. This
review retains that split; it isn't presented as a new change to earlier code.

## REJECT - calculate discounts with round(subtotal * 0.1)

At 5005 cents the proposed expression gives 500, while the required half-up
result is 501. The actual comparison is saved in evidence/12-rounding-comparison.txt.
The integer formula stays, the 501-cent fixture passes and the downward-rounding
mutation is caught. The rejected formula wasn't put into production.

These are three different decisions. The report explains the code and tests
behind them; the AI-use record provides the interaction rather than just a list
of unsupported claims about what was suggested.
