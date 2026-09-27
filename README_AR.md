<div dir="rtl">

<p align="center">
  <img src="assets/project-logo.svg" alt="شعار Codebase Navigator AI" width="104" />
</p>

# Codebase Navigator AI — الدليل العربي

**Codebase Navigator AI** أداة محلية لاستكشاف المستودعات البرمجية من خلال سطر الأوامر وواجهة Python API صغيرة. تفهرس الملفات النصية المدعومة، وتستخرج رموز Python باستخدام AST، وتبحث بالنص أو Regex، وتعرض سياقًا مركزًا حول سطر محدد.

المشروع المفحوص لا يتم تشغيله أو استيراد وحداته أو رفع شفرته إلى خدمة خارجية.

## ملاحظة مهمة حول الاسم

اسم المشروع يتضمن **AI**، لكن الإصدار 1.0 الحالي يعتمد على تحليل محلي حتمي، ولا يحتوي على:

- نموذج لغوي LLM.
- Embeddings.
- Vector Database.
- خدمة استدلال سحابية.
- API Key.
- اتصال شبكة خفي.

أي أفكار دلالية مستقبلية موضحة بشكل منفصل في [ROADMAP.md](ROADMAP.md) وليست ميزات حالية.

## المتطلبات

- Python 3.10 أو أحدث.
- صلاحية قراءة المستودع المراد استكشافه.
- لا توجد اعتماديات تشغيل خارجية.

## التثبيت

</div>

```bash
git clone https://github.com/rad03i2/codebase-navigator-ai.git
cd codebase-navigator-ai
python -m pip install -e .
codebase-nav --version
```

<div dir="rtl">

## أوامر الاستكشاف

### ملخص المستودع

</div>

```bash
codebase-nav --root /path/to/project summary
```

<div dir="rtl">

يعرض جذر المشروع بعد حله، وعدد الملفات المفهرسة، وعدد رموز Python المكتشفة، وعدد الملفات التي تم تجاوزها.

### اكتشاف الرموز

</div>

```bash
codebase-nav --root . symbols service
codebase-nav --root . symbols handler --kind function
codebase-nav --root . symbols worker --kind async-function
```

<div dir="rtl">

تُستخدم مكتبة Python القياسية `ast` لاكتشاف:

- الأصناف `class`.
- الدوال `function`.
- الدوال غير المتزامنة `async-function`.

التوقيع المختصر يعرض أسماء المعاملات، لكنه ليس محلل أنواع أو إعادة بناء كاملة للتوقيع.

### البحث النصي

</div>

```bash
codebase-nav --root . search "timeout"
codebase-nav --root . search "class\\s+Service" --regex
codebase-nav --root . search "TODO" --glob "*.py"
```

<div dir="rtl">

البحث النصي العادي غير حساس لحالة الأحرف. يمكن تفعيل Regex واستخدام glob لتحديد الملفات المطلوبة.

### عرض السياق

</div>

```bash
codebase-nav --root . context src/app.py 42 --radius 5
```

<div dir="rtl">

يجب أن يبقى المسار داخل جذر المشروع وأن يكون الملف ضمن الفهرس الحالي. ترفض الأداة محاولة الخروج من الجذر.

### مخرجات JSON

</div>

```bash
codebase-nav --root . --json symbols parser
```

<div dir="rtl">

الخيار `--json` عام، لذلك يوضع قبل الأمر الفرعي.

## Python API

</div>

```python
from codebase_navigator import build_index, context, find_symbols, search_text

index = build_index(".")
print(index.summary())
print(find_symbols(index, "client"))
print(search_text(index, "timeout", glob="*.py"))
print(context(index, "src/app.py", 20, radius=2))
```

<div dir="rtl">

تصدّر الحزمة العامة الكيانات والدوال التالية:

- `Index`
- `Symbol`
- `Match`
- `build_index`
- `find_symbols`
- `search_text`
- `context`

## سلوك الفهرسة

تتجاهل الأداة افتراضيًا مجلدات شائعة مثل:

</div>

```text
.git
.venv
venv
node_modules
dist
build
__pycache__
.pytest_cache
```

<div dir="rtl">

وتدعم البحث النصي في الامتدادات التالية:

</div>

```text
.py .js .ts .tsx .jsx .java .go .rs .c .h .cpp .cs
.rb .php .md .toml .yaml .yml .json .txt
```

<div dir="rtl">

الإعدادات الافتراضية الحالية:

- حد أقصى قدره 20,000 ملف.
- حد حجم قدره 1,000,000 بايت لكل ملف.
- تجاهل الروابط الرمزية.
- تجاوز الملفات غير القابلة للقراءة أو غير الصالحة كـ UTF-8.
- استخراج الرموز الدلالية من Python فقط.

إذا تم تجاوز حد عدد الملفات، تتوقف عملية الفهرسة بخطأ واضح بدل المتابعة بصمت.

## الأمان والخصوصية

الأداة تتعامل مع الشفرة كبيانات للقراءة:

- لا تنفذ شفرة المستودع.
- لا تستورد وحداته.
- لا ترسل الشفرة إلى خدمة خارجية.
- لا تتبع symlinks.
- تتحقق من أن مسار السياق يبقى داخل جذر المشروع.

هذا يقلل المخاطر لكنه لا يجعل الأداة ماسح برمجيات خبيثة. عند التعامل مع مستودع غير موثوق استخدم إجراءات العزل المعتادة لنظام التشغيل. راجع [SECURITY.md](SECURITY.md).

## الاختبارات وCI

</div>

```bash
python -m compileall -q src tests
python -m unittest discover -s tests -v
codebase-nav --root . summary
```

<div dir="rtl">

يعمل CI على Ubuntu وWindows وmacOS باستخدام Python 3.10 و3.12 و3.13.

## حدود الإصدار الحالي

- استخراج الرموز الدلالي خاص بـ Python.
- اللغات الأخرى تدخل في البحث النصي فقط.
- يعاد بناء الفهرس في كل تشغيل CLI.
- ملفات Python غير الصالحة نحويًا لا تنتج رموز AST.
- لا يوجد Call Graph.
- لا يوجد Type Checker.
- لا يوجد محرك Embeddings.
- لا يوجد LLM Assistant.
- لا توجد واجهة رسومية.

راجع [ROADMAP.md](ROADMAP.md) للأفكار المستقبلية المنفصلة عن الإمكانات الحالية.

## الترخيص والمطور

المشروع مرخص وفق MIT.

**رضوان عبدالهادي**  
**Radwan Abd alhady Ahmed**  
GitHub: [@rad03i2](https://github.com/rad03i2)

</div>
