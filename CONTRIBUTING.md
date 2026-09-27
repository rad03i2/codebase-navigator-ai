# Contributing to Codebase Navigator AI

Contributions are welcome when they preserve the project's core principles:

- local-first analysis;
- deterministic behavior unless a future optional mode clearly states otherwise;
- no hidden network activity;
- no execution of inspected repositories;
- clear distinction between current capabilities and roadmap ideas.

## Development setup

```bash
git clone https://github.com/rad03i2/codebase-navigator-ai.git
cd codebase-navigator-ai
python -m pip install -e .
```

## Required validation

Run the same core checks used by CI:

```bash
python -m compileall -q src tests
python -m unittest discover -s tests -v
codebase-nav --root . summary
```

## Behavior changes

When changing behavior:

1. add or update tests;
2. document user-facing CLI/API changes;
3. keep public API expectations clear;
4. update `CHANGELOG.md`;
5. update both language guides when the change affects users.

## Trust-boundary changes

Changes to any of the following deserve explicit security review:

- repository traversal;
- symlink behavior;
- path resolution;
- ignore semantics;
- file-size/file-count limits;
- text decoding;
- AST parsing;
- any future network or model integration.

Do not introduce source execution, implicit imports from inspected projects, telemetry, credentials, or network access without an explicit design change that is documented and testable.

## Pull requests

Keep pull requests focused. Explain:

- the problem;
- the implementation approach;
- how it was validated;
- whether repository privacy or trust boundaries changed.

Do not commit secrets, private repositories, generated indexes containing sensitive paths, real API keys, or large unrelated fixtures.

---

<div dir="rtl">

## المساهمة

يجب أن تحافظ المساهمات على مبدأ أن المشروع أداة استكشاف محلية وآمنة، وألا تضيف اتصالات شبكة أو تنفيذًا لشفرة المستودع بشكل مخفي.

قبل إرسال Pull Request شغّل اختبارات المشروع الحالية، وأضف اختبارات مناسبة لأي تغيير في السلوك، وحدّث التوثيق عند تغيير CLI أو Python API.

</div>

Maintainer: **Radwan Abd alhady Ahmed — رضوان عبدالهادي — [@rad03i2](https://github.com/rad03i2)**
