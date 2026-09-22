# Security Policy

## Supported version
Security fixes target the latest release on `main`.

## Reporting
Please report suspected vulnerabilities privately through GitHub's security reporting features when available. Do not publish secrets or exploit details in a public issue.

## Security model
Codebase Navigator AI is local-first and read-only. It does not execute, import, compile, or upload the project being inspected. Symbol extraction uses Python's `ast` parser. Symlinks are not indexed, common generated/vendor directories are ignored, and context lookup rejects paths outside the indexed root.

The tool is not a malware scanner and untrusted repositories should still be handled using normal operating-system isolation practices.
