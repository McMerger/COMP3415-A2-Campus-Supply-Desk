# CR-01 planning and review record

This record recovers actual pre-implementation commentary from the assignment
chat. It was assembled during the final handout review and is not a backdated
Part A worksheet.

## Preserved note before express implementation

"CR-01 is available now: it adds express delivery at a fixed $12 fee through the
service, commands, and menu. I'll include tests for its pricing, persistence,
cancellation, and discoverability."

The next recorded paragraph said that the baseline tests confirmed the three
suspected defects, with six failing assertions recorded before code changes.

The interfaces named above correspond to service.py, cli.py and menu.py. Those
paths are explained in this recovery record; the original note named interfaces
rather than spelling out a separate list of file paths.

## Checkable sequence

- c3e234b: Add tests for express delivery and the menu, November 8, 2026,
  21:19:09 America/Toronto (recorded commit author time).
- e6abcca: Add express delivery, November 8, 2026, 21:20:20 America/Toronto.

The commits' file snapshots and times can be inspected. Their messages were
reworded later while preserving the source trees, authors and times. Test log 05
shows express failures before support; log 06 shows the completed feature passing.

## What changed

The service validator/pricing, command choices and menu prompt changed as
predicted. test_express.py and test_interfaces.py cover the requested paths.
README and functional-spec updates were also needed; they weren't separately
listed in the original chat note. The shared pricing helper made the fee a single
rule for both quote and place. The money-name refactor was added afterward.
