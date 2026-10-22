# Fork PR14 CI repair and historical source roles

The initial registered-package run 39712725535 at f4657a0ad4c11a56646c8c6c422f09335b0c73ba ran 318 onboarding tests and failed four current-status/navigation assertions. The separate exact transport run 39712725621 passed. No scientific failure is inferred from the planning failure.

## Navigation repair

The two documentation files reuse the exact corrections from zxv's PR4436 head 56003680aee2871773de408e5f01cc5dd46b144c. They identify selected conditional kappa 0.0023, its actual reproduction command and source/review/validation paths, and label earlier sections as historical. Credit zxv and the existing documentation authors. The tests and selected record are unchanged.

## Historical replay boundary

PR3563's historical-1042-link finding binds the old selected #1094 record and its previous_record pointer to #1042. Applying that frozen assertion directly to #4359 is incorrect. Its original verifier, test, RESULT.json, source hashes and base commit are retained unchanged. The added historical_replay.py authenticates the original manifest from ancestor f4657a0, retrieves the three exact original blobs from base 20ecf289, and executes the unchanged verifier and test in a temporary snapshot. It also checks that the live #1042 checkpoint has not changed. No working source file is overwritten. Git replacement objects are disabled and both blob IDs and SHA256 are checked.

The two evolving documents in that package's SOURCES.json are now historical provenance, not required to equal working-tree bytes. All original VERIFY.json invalidation paths remain present. The registered command explicitly reports historical-snapshot scope. The original direct verify.py command still requires its original inputs; use the registered command on a later frontier.

The locale package has a different contract. Its unchanged verifier deliberately tests the current status document and current test module, including both negative codec controls and the complete onboarding suite. Its old document hash is historical provenance; the current path remains a declared replay input. This preserves live regression coverage without freezing the document's entire contents.

No hash is rewritten to a newer value, no failure is suppressed, and neither shared workflow nor package runner is weakened. Six new adapter tests cover exact retrieval, live-edit isolation, wrong hashes/blob IDs, missing history, Git replacements, unsafe paths and the immutable original-manifest guard. They pass locally on Python 3.13.5 in normal and optimised modes. Full Python 3.12 execution is assessed on the actual subsequent hosted run, not presumed from this note.

## Scope and credit

This is a fork-local workflow repair, not a new research result, supplier admission or frontier update. It preserves James Reed's PR3563 historical finding, the locale-package author and existing checker attribution, and zxv's documentation repair. Prepared for Chris / Clear1nsight with substantial OpenAI assistance, Apache-2.0.

## Open next questions

Confirm the exact-head hosted plan, both affected historical/locale replays and the transport package after publication. A scientific follow-up must separately bind the declared physical-pair list to every event and helper boundary in PR4470's chronological word. CI success alone does not establish that completeness.
