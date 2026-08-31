# Changelog

## [Unreleased]

- Document the Firebase data boundary and casual-game anti-cheat limitation.
- Add offline integrity checks and a repeatable maintenance workflow.
- Reduce room/challenge polling cost and pause synchronization in hidden or offline tabs.
- Prevent replayed local rounds from adding duplicate scores and include room rounds in local records.
- Load sound effects on demand, remove the unused MQTT asset, and improve mobile accessibility labels.
- Add basic Firestore shape, range, ownership, and score-consistency checks.
- Change challenge configuration updates to ask for confirmation after two consecutive correct answers, with one-tap saving.
- Persist challenge qualification records, verify configuration writes by reading them back, and offer retry on failure.
- Move challenge qualification records to the valid `challengeBeats/{uid}` collection path.

## [0.1.0] - 2026-08-30

- Initial public PWA with practice, daily, challenge and multiplayer room modes.
- Make challenge-mode round feedback shorter and distinct from the configuration-saved confirmation sound.
- Bypass Service Worker caching for Firebase reads so saved challenge settings are verified against live data.
