# Toolkit release status

Target: v0.2.0 (source update; no tag or hosted deployment implied)
Status: Verified (local toolkit checks only)
Date: 2026-10-10

This describes the toolkit, not a user's tracked application.

## v0.2.0 — Local reader tools

Implemented: explicit-baseline page catalog comparison, manual personal review marks, changed-read-page warning, search/status filters, 20-page pagination, local JSON export, English/Turkish labels, and explicit catalog/unsupported-data/storage-unavailable behavior. Same reusable hook/JS/CSS is kept independent of any specific application's parser, model, datasets or evidence schema.

Source contract: unique/stable project identity in configuration; public rendered-body/title/notes and declared artifact hashes; optional author introductions/change notes, not inferred semantic diffs. Marks are browser state, not application progress or agent instructions. No source edits, telemetry, provider keys, accounts, import, multi-device sync, or automatic AI messaging.

The first-use project CURRENT_STATE and work log remain blank. Toolkit verification and publication are recorded here, not invented as application accomplishments. Current validation is documented in [the new verification record](verification/2026-10-10.md).

Windows / Python 3.12.14 / Node 26.4.0: 29 Python tests and 12 pure JavaScript logic tests passed; fresh local setup, content checks and strict build passed. The final reader-title regression distinguishes actual page headings from repeated navigation labels such as Overview. Selected English/Turkish desktop/mobile reader and failure-case browser observations are recorded with limitations in [result-0.2.json](verification/result-0.2.json). These are toolkit checks, not tests of your application. Source push is not a hosting deployment or a release tag.

## v0.1.0 — Initial record (2026-10-05)

Implemented scope: generic Markdown portal, provider-neutral onboarding, optional private style preferences, local setup/build/serve, shared state metadata, content checking, and normal/negative unit tests.

Verification on Windows with Python 3.12.14: local setup completed, 19 unit tests passed, content checks passed, and the strict MkDocs build passed. A live loopback preview was reviewed in the browser: main sections, search, and the fictional Mermaid example worked. No browser warning/error logs were observed during the review.

See [the dated verification record](verification/2026-10-05.md) for methods and limits. GitHub publication is a separate Git operation; this file does not assert a tag or a hosted deployment.

Windows is the initial local target. macOS/Linux must not be advertised as tested until run there. No separate LLM installation/adaptation session has been tested; instructions are best-effort contracts, not certified provider integrations.
