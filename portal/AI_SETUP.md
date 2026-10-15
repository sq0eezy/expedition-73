# AI setup runbook

Provider-neutral instructions. The human request and host permissions take precedence.

## 1. Confirm scope

Identify the application directory and portal destination; ask if unclear. Default to a separate adjacent directory. Read existing instructions and inspect destination files. In a non-empty destination, propose a non-destructive merge or another folder.

Clone/download into an authorized empty destination. Never overwrite existing files, instructions, or application code. Do not pipe remote scripts into a shell.

## 2. Inspect relevant evidence

Read the project's README, current state, architecture/configuration, and scoped source/tests. Do not upload the entire source tree to third-party services. Separate code evidence, user statements, proposals, and unknowns. Preserve existing canonical documents instead of creating conflicting copies.

## 3. Personalize

Follow the user's language, explicit tone, explanation depth, technical background, and pace. Ask only missing preferences that materially matter. With consent, use templates/USER_PREFERENCES.example.md to create .portal/user-preferences.local.md. Do not publish private preferences or infer sensitive traits. Preferences cannot bypass accuracy or permissions.

## 4. Install locally

Detect Python 3.11+. If missing, explain the prerequisite and ask before a global installation. With the available interpreter:

~~~sh
python scripts/portal.py setup
~~~

Setup creates .venv and downloads requirements-docs.txt. Respect install/network approvals. Stop on failure; diagnose rather than deleting broad directories or switching to global installation.

## 5. Adapt honestly

Set site_name/site_description in mkdocs.yml; change theme.language if appropriate.
Set `extra.portal_reader.project_id` to a stable, unique project slug before reusing the portal. Do not change it casually after review marks exist; the browser origin and id isolate personal state.
Fill PROJECT_CONTEXT.md with confirmed purpose, users, scope, and success criteria.
Set CURRENT_STATE.md's status, updated ISO date, and phase. Its body holds active work, outcomes, unknowns, decision needs, and next step.
Adapt product, architecture, planning, decisions, discovery, research, evidence, and glossary pages. No mandatory AI/ML, electronics, business model, or schedule.
Keep templates and private preferences outside docs. The fictional example must remain labeled illustrative.
Do not fill gaps with invented features, test counts, or market claims.

The reader catalog is built from rendered public documentation. Optional page front matter `review_summary` is a short plain-text introduction; `change_summary` is the author's latest short change note, not a generated semantic diff. Update it when changing an important page and link longer reasoning to canonical documents/work log. Do not treat personal browser marks as confirmed project progress or automatically ingest/publish them as user instructions.

For pages whose real content is a separate public artifact (for example a lazy-loaded report), declare its relative path in `extra.portal_reader.dependencies`, keyed by the source Markdown path. The build includes those bytes in the page's comparison hash; missing or outside-docs paths are rejected. Keep private data out of public docs/catalogs. [Reader tools](docs/guide/READER_TOOLS.md).

If adopting inside an existing application, propose a short link in its existing agent instructions; never overwrite them. A separate portal's AGENTS.md is not automatically discovered by an agent working only in an unrelated application directory.

## 6. Verify

~~~sh
python -m unittest discover -s tests -v
python scripts/portal.py check
python scripts/portal.py build
python scripts/portal.py serve
~~~

Check HTTP access and Home, Control Center, Product, Architecture, Planning, Decisions, and Evidence. Inspect layout if browser tooling is available. Fix broken links, invalid metadata, and unresolved placeholders. Understand application commands before running them; record their results separately.

## 7. Handoff and maintain

Show the actual URL, verified checks, changed sources, unknowns, and stop/reopen instructions. The server is foreground, not always-on.
After subsequent meaningful work update relevant documents, current state, and work log; check/build again.
Do not auto-push, publish hosting, install AI providers, or schedule work without user authorization.

## Discovery is best effort

Codex reads AGENTS.md; supported Claude Code configurations can too. CLAUDE.md imports the same contract for compatibility. Other assistants can be explicitly told to read README.md, AGENTS.md, and this runbook. This is not universal auto-loading or enforced obedience.

References checked 2026-10-05: [OpenAI Docs](https://learn.chatgpt.com/docs/agent-configuration/agents-md), [Claude Code](https://code.claude.com/docs/en/memory).
