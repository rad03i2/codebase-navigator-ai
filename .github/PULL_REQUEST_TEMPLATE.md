## Summary

Describe the repository-navigation problem this change addresses.

## Validation

- [ ] `python -m compileall -q src tests`
- [ ] `python -m unittest discover -s tests -v`
- [ ] `codebase-nav --root . summary`
- [ ] User-facing documentation updated if behavior changed
- [ ] No secrets or private repository content included

## Trust-boundary review

Check any statement that applies:

- [ ] This change does not execute inspected source.
- [ ] This change does not import inspected project modules.
- [ ] This change does not add hidden network activity or telemetry.
- [ ] Path traversal / symlink behavior is unchanged or explicitly documented and tested.
- [ ] Any AI/model behavior is clearly identified as implemented or not implemented.

## Notes

Include platform-specific behavior, limitations, or follow-up work if relevant.
