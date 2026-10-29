# Interactive intake validation review

Review date: 2026-10-29. Base: `fcf31684ac0c3efbae2eca15d86b0145ce7c8d7c`.
Scope: `Engine/IntakeGear.py` and isolated regression tests. No production
records, services, databases, merges, or deployments were used.

Run from the repository root:

```sh
python3 -m unittest discover -s tests -p 'test_intake_validation.py' -v
python3 -m py_compile Engine/IntakeGear.py tests/test_intake_validation.py
```

## Behavior and compatibility decisions for human review

- Each identifier starts with an ASCII letter/digit, followed by ASCII
  letters/digits, underscores, or hyphens. Surrounding whitespace is stripped;
  the acronym is uppercased only after ASCII validation. Company/partner IDs
  retain their case, leading zeros, and full string precision. Safe short IDs
  remain accepted; this is syntax validation, not a HubSpot existence check.
- Keep the existing `ACRONYM-company.partner.json` layout and JSON fields.
  Reject unsafe identifiers rather than sanitizing them into possible aliases.
  No existing records are renamed or migrated. The entire filename is limited
  to 255 ASCII bytes; filesystems with smaller limits may reject creation.
- Score input is 1–3 ASCII decimal digits, with optional surrounding whitespace,
  and must represent 0–100 inclusive. Signs, Unicode digits, underscores,
  decimals, and longer spellings are rejected and reprompted. This deliberately
  narrows the old `int()` input syntax. EOF/interruption exits before writes.
- Existing files, directories, symlinks (including dangling links), and hardlinks
  are refused. Intake no longer silently overwrites records; a separate reviewed
  update workflow would be needed for that use case.
- Relative roots and `~` expansion remain supported. Root paths containing
  symlink components are refused. Resolve authorized symlink-based configurations
  to their actual directory before adoption. POSIX descriptor-relative opens,
  directory flags, and no-follow support are required; unsupported platforms
  fail before creating the root. New directories/files request modes 0700/0600;
  existing permissions are not changed.

The generated filename receives a resolved-parent containment check. Root
traversal and creation then use directory descriptors and no-follow opens for
each component. Final creation is descriptor-relative, exclusive, and no-follow,
so a destination inserted after validation cannot redirect or overwrite a file.
All interactive identifier/score validation and record serialization precede
filesystem creation. `save_node` is a narrow persistence helper: it checks the
system ID and serialization, while `run_intake` validates the interactive fields.

## Executed validation

- Default-branch scoring dependency plus intake patch: **19 tests passed**.
- Temporary composition with PR #6 head
  `a43abdd3b62c93a235db1b7e4687f0bd08a12130`: **19 intake tests passed** and
  **7 existing Watchdog snapshot checks passed**. This was a temporary source
  overlay, not a merge or a modification of PR #6.
- Python compilation and `git diff --check` passed.
- Canon validator: 0 errors, 0 warnings on the implementation and test file.

Tests exercise the actual ScoringGear for valid intake, synthetic identifiers,
score endpoints, malformed values, interrupted input, maximum filenames,
existing-record preservation, link rejection, missing configuration, unsupported
platforms, and controlled root/destination insertion races. All filesystem effects
are within temporary test trees. Rejected interactive identifier cases compare
the entire tree before/after; outside sentinels remain unchanged in link/race tests.

## Downstream findings and limits

- ScoringGear still reopens the saved filename. A hostile writer with access to
  the node directory could replace it between persistence and scoring. This patch
  does not claim immutable snapshot scoring or full filesystem-race protection.
- Successful intake still writes a node before scoring. Main's Watchdog can react
  with synthesis, execution, and Git effects; PR #6 addresses that separate path
  and remains unmerged. No live observer was started for intake tests.
- ExecutionGear derives workspace paths from `display_name` with incomplete
  sanitization; NexusGear constructs paths independently, and SynthesisGear also
  builds an output filename. They were inspected but are not hardened by this
  intake-only patch. Free-text display names are retained for compatibility and
  must not be considered safe filesystem names by other callers.
- Writes are exclusive, but not atomic JSON publication: I/O failure can leave a
  partial new file, and an observer may see the file before writing finishes.
  No durability/fsync guarantee, rollback, daemon test, or live HubSpot check is
  established. Trusted root ownership/permissions remain necessary; hostile
  directory renaming/mount changes are outside the tested race model.

Human review must accept the identifier/score syntax, no-overwrite behavior,
POSIX requirement, and no-symlink root policy before adoption. Review does not
assert that the broader execution chain is ready for production.
