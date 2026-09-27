# Security Policy

Codebase Navigator AI reads source repositories, so its security model is centered on keeping inspected code as **data**, not executable input.

## Supported code

Security fixes target the current `main` branch and latest published project version.

## Reporting

Use an appropriate private GitHub security-reporting channel when available.

Do not publish in a public issue:

- secrets;
- private repository contents;
- sensitive source paths;
- exploit details;
- credentials;
- proprietary code samples.

A minimal synthetic reproduction is preferred.

## Current trust boundary

The implementation currently:

- reads supported text/source files from a selected root;
- does not intentionally execute inspected source;
- does not import inspected project modules;
- uses Python's standard-library AST for Python symbol extraction;
- skips symlinks;
- ignores common generated/vendor path components;
- rejects context paths that resolve outside the project root;
- has no declared runtime third-party dependency;
- has no network client, telemetry flow, API-key handling, LLM call, embedding backend, or source upload.

## Important limits

These properties do **not** make the tool a malware scanner or sandbox.

Potentially hostile repositories can still contain:

- extremely large directory structures;
- unusual filesystem entries;
- sensitive information;
- files designed to stress parsers or other tools used around the repository.

The current implementation applies file-count and file-size limits, but users should still use normal operating-system isolation for untrusted code.

## Path handling

Targeted context lookup resolves the requested path and verifies that it remains under the indexed root. It also requires the file to be present in the current index.

Symlinks are excluded during index discovery.

## Data sensitivity

Human-readable and JSON outputs can reveal:

- source paths;
- symbol names;
- matching source lines.

Treat captured terminal output and generated JSON as sensitive when the inspected repository is private.

## Future AI / network features

No LLM or semantic model is part of v1.0.

If a future feature introduces a model, remote service, credential, or network transfer, it should document:

- exactly what data leaves the machine;
- how users opt in;
- how credentials are stored;
- whether a local-only alternative exists.

Maintainer: **Radwan Abd alhady Ahmed (@rad03i2)**
