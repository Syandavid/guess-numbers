# Guess Numbers Maintenance Guide

## Project boundary

This repository is a dependency-light static PWA. `index.html` contains the
game UI and browser logic, while `manifest.webmanifest` and `sw.js` provide
installability and offline fallback. There is no build step or application
server.

Firebase is used for anonymous authentication and Firestore-backed features:
claimed names, daily records, global challenge state and multiplayer rooms.
Firebase project configuration is public client configuration; service account
credentials must never be committed.

## Change workflow

Keep `main` deployable. Use short-lived branches such as:

- `feat/daily-streak`
- `fix/room-reconnect`
- `docs/firebase-rules`

Before committing, run:

```bash
python scripts/validate_project.py
```

For UI changes, serve the repository over HTTP so the service worker can run:

```bash
python -m http.server 8080
```

Check local practice, daily mode, challenge mode, account switching, room
join/create, offline startup and the mobile layout. For phone testing, use the
computer's current LAN IP rather than a previously recorded address.

## Firebase changes

The source of truth for Firestore access is `firestore.rules`; indexes are in
`firestore.indexes.json`. Review every rule change for:

1. authentication requirements;
2. ownership or membership checks;
3. allowed field names and value ranges;
4. whether a read exposes more data than the screen needs;
5. whether a delete or update can affect another player's record.

Deploy rules and indexes separately from client code when possible:

```bash
firebase use guessnums-9f588
firebase deploy --only firestore:rules,firestore:indexes
```

Firestore data is not backed up by Git. If daily records or names matter, set
up a separate Firebase export/backup process.

## Multiplayer security boundary

The room number must be delivered to a participant's browser during the flash
phase, so a determined participant can inspect it with browser developer tools.
The current design is suitable for a casual memory game, not a trusted
competition or anti-cheat system. The rules still protect authentication,
membership and write shapes; they do not hide data that the client must render.

## Release and rollback

Record user-visible changes in `CHANGELOG.md` and use tags such as `v0.1.0` for
stable milestones. If a release breaks the PWA, revert the client commit and
keep the last known-good Firestore rules until replacement rules are tested.
Do not delete Firestore data as part of a client rollback.

## External assets

The sound files are runtime assets and are cached on first use by the service
worker. Sounds are loaded on demand after the audio context is armed, so avoid
preloading unused media during service-worker installation or on the first
tap. When adding or renaming an asset, update both the file references and
`sw.js` when appropriate, then run the integrity check.
Recheck the license and redistribution terms of vendored or remote assets
before public distribution.

Room and challenge synchronization currently uses guarded, visible-tab polling
as a REST fallback. If the project grows beyond casual use, migrate these
flows to Firestore realtime listeners and keep server-side validation for all
score and answer writes.
