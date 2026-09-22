---
title: General Information
---

## Coding Style

When writing, refactoring, or modifying files:

1. Follow the existing coding style of the project.
2. Keep changes focused and avoid unrelated refactoring.
3. Keep code simple, readable, and maintainable.
4. Remove unused code, imports, variables, and dependencies.
5. Reuse existing functionality where appropriate.
6. Keep platform-specific or operational changes documented when they affect users.

## Go

TunGuard is written in Go.

Format Go code before submitting changes:

```sh
gofmt -w .
```

Run the test suite:

```sh
go test ./...
```

Build the project:

```sh
go build ./...
```

Changes should be formatted, compile successfully, and pass the relevant tests before submission.

## Documentation

Documentation should be clear, concise, and practical.

When adding or changing documentation:

- Follow the existing Markdown structure.
- Keep commands and examples accurate.
- Do not document features that are not available yet.
- Keep configuration examples consistent with the actual application.
- Prefer copy-and-run commands where possible.
- Keep related information on the appropriate documentation page.
- Avoid unnecessary marketing language.

## Commit Messages

Use a short prefix followed by a clear description:

```text
update: description
fix: description
add: description
remove: description
docs: description
refactor: description
test: description
build: description
```

Examples:

```text
update: improve router provisioning
fix: correct peer address validation
add: p2p connection support
remove: deprecated API endpoint
docs: update router provisioning guide
refactor: simplify peer registration
test: add peer registration tests
build: update release workflow
```

Keep commit messages:

- Short and descriptive.
- Written in lowercase after the prefix.
- Focused on what changed.
- Free from unnecessary details.

Avoid vague messages:

```text
update: changes
fix: stuff
update: final
changes: many things
```

## Changelog

All user-facing changes must be documented in the project's `CHANGELOG.md`.

TunGuard follows [Keep a Changelog](https://keepachangelog.com/) and [Semantic Versioning](https://semver.org/).

Changes are grouped under:

```markdown
Added

Changed

Fixed
```

Use `Added` for new functionality:

```markdown
Added

P2P peer discovery and relay support.
```

Use `Changed` for changes to existing functionality:

```markdown
Changed

Router provisioning now supports custom WireGuard MTU values.
```

Use `Fixed` for bug fixes:

```markdown
Fixed

Router provisioning no longer fails when the server address contains a hostname.
```

Keep entries focused on the user-visible change.

Do not add changelog entries for changes that have no user-visible impact, such as:

- Internal formatting
- Local development changes
- Temporary debugging
- Internal refactoring with no behavior change

### Changelog Format

Follow the existing versioned structure:

```markdown
[2.2.2] - YYYY-MM-DD
Added
New functionality.

Changed
Changes to existing functionality.

Fixed
Bug fixes.

[2.2.1] - YYYY-MM-DD
Fixed
Previous changes remain here.
```

Do not modify or reorder existing released entries.

When preparing a new release, add the new version at the top of the changelog.

## Pull Requests

Before opening a pull request:

1. Review the complete diff.
2. Format Go code with `gofmt`.
3. Run `go test ./...`.
4. Run `go build ./...`.
5. Update `CHANGELOG.md` when the change is user-facing.
6. Check documentation examples and commands.
7. Make sure commit messages follow the required format.

Keep pull requests focused on one change or a closely related set of changes.
