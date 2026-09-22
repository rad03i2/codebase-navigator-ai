# Codebase Navigator AI

Local-first codebase navigation for developers who need to understand an unfamiliar repository quickly — without uploading source code or executing the project.

> **English** · العربية أدناه

## Overview
Codebase Navigator AI indexes readable source/text files, extracts Python classes and functions with the standard-library AST, performs literal or regular-expression search, filters by path glob, and prints focused source context. Despite the project name, v1.0 deliberately uses deterministic local analysis rather than claiming an LLM integration that is not present.

## Why it exists
Large repositories are slow to explore with ad-hoc shell commands. This tool provides one cross-platform CLI and a small Python API for repeatable discovery while remaining dependency-free at runtime and safe for private codebases.

## Features
- Recursive local indexing with common vendor/build directories ignored.
- Python AST symbol discovery: classes, functions, async functions and compact signatures.
- Case-insensitive literal search or opt-in regex search across supported text files.
- Glob filtering such as `src/*.py` or `**/*.md`.
- Focused line context with project-root traversal protection.
- Human-readable and JSON output for scripts.
- Symlinks are not indexed; files over 1 MB are skipped by default.
- No network calls, telemetry, source execution, imports from the inspected project, or API keys.

## Preview
```text
$ codebase-nav --root . symbols Navigator
src/codebase_navigator/core.py:34  class Index

$ codebase-nav --root . search "build_index" --glob "*.py"
src/codebase_navigator/core.py:70  def build_index(...)
```
Output depends on the repository being inspected. For screenshots, capture the terminal output of these commands; the project has no GUI.

## Requirements & installation
Requires Python 3.10+.

```bash
git clone https://github.com/rad03i2/codebase-navigator-ai.git
cd codebase-navigator-ai
python -m pip install -e .
```

## Usage
```bash
codebase-nav --root /path/to/project summary
codebase-nav --root . symbols service
codebase-nav --root . symbols handler --kind function
codebase-nav --root . search "TODO"
codebase-nav --root . search "def\\s+load" --regex --glob "*.py"
codebase-nav --root . context src/app.py 42 --radius 5
codebase-nav --root . --json symbols parser
codebase-nav --version
```

Global options (`--root`, `--json`) go before the subcommand.

### Python API
```python
from codebase_navigator import build_index, find_symbols, search_text, context

index = build_index(".")
print(index.summary())
print(find_symbols(index, "client"))
print(search_text(index, "timeout", glob="*.py"))
print(context(index, "src/app.py", 20, radius=2))
```

## Configuration
No configuration file or environment variables are required. The API exposes `max_files`, `max_bytes`, and `ignores` for callers that need different indexing limits. CLI v1.0 intentionally keeps safe defaults fixed.

## Project structure
```text
src/codebase_navigator/
  __init__.py       public API
  core.py           indexing, AST symbols, search, context
  cli.py            command-line interface
tests/test_core.py  functional unit tests
.github/workflows/ci.yml
SECURITY.md
CONTRIBUTING.md
```

## Testing
```bash
python -m compileall -q src tests
python -m unittest discover -s tests -v
codebase-nav --root . summary
```
CI runs these checks on Ubuntu, Windows and macOS with Python 3.10, 3.12 and 3.13.

## Security & privacy
Inspection is read-only. The tool does not execute inspected source, import inspected modules, follow symlinks, or send source to a service. Context lookup resolves paths and rejects paths outside the indexed root. See `SECURITY.md` for the security model and reporting guidance.

## Limitations
Python is currently the only language with semantic symbol extraction; other supported text/source types participate in text search only. This is not a call graph, type checker, malware scanner, semantic embedding engine, or LLM assistant. AST parsing of syntactically invalid Python files yields no symbols for that file. Very large files are skipped, and indexing is rebuilt for each CLI invocation rather than persisted.

## Optional roadmap
Persistent indexes, additional language parsers, ignore-file support, and an optional pluggable local semantic-search backend are reasonable future additions. They are not claimed as current features.

## Contributing
See `CONTRIBUTING.md`. Keep changes focused, tested, local-first, and free of hidden network behavior.

## License
MIT License — see `LICENSE`.

## Author
**Radwan Abdulhadi Ahmed**  
**رضوان عبدالهادي أحمد**  
GitHub: **@rad03i2**

---

# العربية

## نظرة عامة
**Codebase Navigator AI** أداة محلية مكتوبة ببايثون لاستكشاف المشاريع البرمجية بسرعة دون رفع الشفرة إلى خدمة خارجية أو تشغيل المشروع المفحوص. تفهرس الملفات النصية، وتستخرج الأصناف والدوال من ملفات Python باستخدام AST، وتبحث بالنص أو بالتعبيرات النمطية، وتعرض سياق الأسطر المطلوب. الاسم يتضمن AI، لكن الإصدار 1.0 لا يدّعي وجود نموذج لغوي؛ التحليل الحالي محلي وحتمي وقابل للفهم.

## لماذا هذا المشروع؟
استكشاف مستودع غير مألوف عبر أوامر متفرقة قد يكون بطيئًا. توحّد الأداة عمليات الجرد والبحث واكتشاف الرموز وعرض السياق في CLI واحد يعمل على الأنظمة الرئيسية، مع Python API صغيرة وبدون اعتماديات تشغيل خارجية.

## الميزات
- فهرسة متكررة للمشروع مع تجاهل مجلدات مثل `.git` و`node_modules` و`.venv` و`dist` و`build`.
- اكتشاف classes وfunctions وasync functions في Python مع التوقيع المختصر.
- بحث نصي غير حساس لحالة الأحرف أو Regex اختياري.
- تصفية الملفات باستخدام glob.
- عرض سياق الأسطر مع منع الخروج من جذر المشروع.
- مخرجات بشرية أو JSON للأتمتة.
- عدم تتبع الروابط الرمزية وتجاوز الملفات الأكبر من 1MB افتراضيًا.
- لا شبكة، لا telemetry، لا مفاتيح API، ولا تنفيذ لشفرة المشروع المفحوص.

## التثبيت والمتطلبات
يتطلب Python 3.10 أو أحدث.

```bash
git clone https://github.com/rad03i2/codebase-navigator-ai.git
cd codebase-navigator-ai
python -m pip install -e .
```

## الاستخدام
```bash
codebase-nav --root . summary
codebase-nav --root . symbols client
codebase-nav --root . search "TODO"
codebase-nav --root . search "class\\s+Service" --regex --glob "*.py"
codebase-nav --root . context src/app.py 20 --radius 3
codebase-nav --root . --json symbols parser
```
يجب وضع الخيارات العامة مثل `--root` و`--json` قبل الأمر الفرعي.

## Python API
يمكن استيراد `build_index` و`find_symbols` و`search_text` و`context` مباشرة من حزمة `codebase_navigator` لاستخدامها داخل أدوات أخرى.

## الإعداد
لا تحتاج الأداة إلى ملف إعداد أو متغيرات بيئة. تتيح الـAPI تغيير حدود عدد الملفات وحجم الملف وقائمة المجلدات المتجاهلة. يستخدم CLI إعدادات آمنة ثابتة في الإصدار الحالي.

## بنية المشروع
الكود الأساسي في `src/codebase_navigator/`، والاختبارات في `tests/`، وسير CI في `.github/workflows/ci.yml`. توجد سياسات مستقلة للأمان والمساهمة.

## الاختبارات
```bash
python -m compileall -q src tests
python -m unittest discover -s tests -v
codebase-nav --root . summary
```
يشغّل CI الفحوص على Ubuntu وWindows وmacOS مع عدة إصدارات من Python.

## الأمان والخصوصية
العمل قراءة فقط. لا تستورد الأداة وحدات المشروع المفحوص ولا تنفذها ولا ترسل المصدر خارجيًا ولا تتبع symlinks. كما تتحقق عملية عرض السياق من بقاء المسار داخل جذر المشروع. راجع `SECURITY.md` للتفاصيل.

## القيود
استخراج الرموز الدلالي متاح حاليًا لبايثون فقط؛ بقية الأنواع المدعومة تدخل في البحث النصي. الأداة ليست call graph أو type checker أو ماسح برمجيات خبيثة أو محرك embeddings أو مساعد LLM. الملفات ذات Python غير الصالح نحويًا لا تنتج رموزًا، والملفات الكبيرة تُتجاوز، والفهرس يعاد بناؤه في كل تشغيل CLI.

## التطوير الاختياري
يمكن مستقبلًا إضافة فهرس دائم، محللات لغات أخرى، دعم ملفات التجاهل، ومحرك بحث دلالي محلي اختياري. هذه أفكار مستقبلية وليست ميزات حالية.

## المساهمة
راجع `CONTRIBUTING.md`. يجب أن تكون التغييرات محددة ومختبرة وتحافظ على مبدأ العمل المحلي وعدم وجود اتصالات مخفية.

## الترخيص
MIT — راجع `LICENSE`.

## المؤلف
**Radwan Abdulhadi Ahmed**  
**رضوان عبدالهادي أحمد**  
GitHub: **@rad03i2**
