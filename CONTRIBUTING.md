# Contributing

Contributions are welcome when they keep the project local-first, deterministic, and easy to audit.

1. Fork the repository and create a focused branch.
2. Use Python 3.10+ and install with `python -m pip install -e .`.
3. Run `python -m compileall -q src tests` and `python -m unittest discover -s tests -v`.
4. Add tests for behavior changes and keep public APIs documented.
5. Open a focused pull request describing the problem, approach, and validation performed.

Please avoid unrelated generated files, credentials, telemetry, hidden network calls, or dependencies that are not justified by functionality.

## المؤلف
Radwan Abdulhadi Ahmed — رضوان عبدالهادي أحمد — GitHub: @rad03i2
