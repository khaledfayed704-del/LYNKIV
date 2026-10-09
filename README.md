<div align="center">

# LYNIKV TOOL Qr

**وكيل ذكاء اصطناعي عربي للتحكم في المتصفح + حلال QuREO التلقائي**

لوحة تحكم ويب neo-brutalist · 22 أداة · 7 مزوّدات ذكاء اصطناعي · دعم كامل للعربية (RTL)

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Playwright](https://img.shields.io/badge/Playwright-1.44+-2EAD33?logo=playwright&logoColor=white)](https://playwright.dev/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

</div>

---

## نبذة

`LYNIKV TOOL Qr` أداة سطح مكتب تعمل بواجهة سطر أوامر وواجهة رسومية، ووحدة تحكم ويب محلية.
تعطيها أمراً بالعربية، فتتصرف في متصفح حقيقي عبر Playwright حتى تنجز المطلوب، ثم ترجع بجواب نهائي.

بالإضافة إلى ذلك، تحتوي الأداة على **حلال QuREO** يكمّل محاضرات وأسئلة الكورسات المفعّلة في حسابك
تلقائياً، مع إمكانية الحل **بدون ذكاء اصطناعي** إطلاقاً.

**التطوير:** [Lynox](https://lynkiv.duckdns.org/) · **Kivix**

---

## المميزات

| الميزة | الوصف |
|---|---|
| **أوامر عربية** | اكتب طلبك بالعربية naturally، والوكيل يترجمه إلى خطوات على المتصفح |
| **لوحة تحكم ويب** | واجهة كاملة على `127.0.0.1:8770` لإدارة كل الإعدادات والأدوات |
| **22 أداة** | تنقل، قراءة، نقر، تعبئة، تبويبات، لقطات، وأدوات QuREO |
| **7 مزوّدات** | Groq · OpenAI · OpenRouter · Together · DeepSeek · Anthropic · Gemini |
| **اختيار الموديل** | قائمة موديلات محدّثة لكل مزوّد + اختبار الاتصال من اللوحة |
| **حفظ مشفّر** | مفتاح API يُخزَّن مشفّراً في `config.json` ولا يظهر أبداً في الواجهة |
| **جلسة QuREO محفوظة** | تسجيل دخول واحد، وتبقى الجلسة محفوظة في ملف تعريف المتصفح |
| **نسخة exe** | بناء Windows موقّع من مجلد واحد عبر PyInstaller |
| **استجابة كاملة** | الواجهة تعمل من 320px حتى الشاشات العريضة |
| **سمة داكنة/فاتحة** | تبديل فوري مع حفظ الاختيار |

---

## المتطلبات

- **Windows** 10/11 (أو Linux/macOS للتشغيل من المصدر)
- **Python** 3.10 أو أحدث *(تم التطوير والاختبار على 3.14.8)*
- **Chrome** أو Chromium — يثبّته Playwright تلقائياً بأمر واحد
- اتصال إنترنت للوصول إلى مزوّد الذكاء الاصطناعي

---

## التثبيت

```bash
git clone https://github.com/<your-username>/LYNIKV-TOOL-Qr.git
cd LYNIKV-TOOL-Qr

python -m venv .venv
.venv\Scripts\activate          # على ويندوز
# source .venv/bin/activate     # على لينكس/ماك

pip install -r requirements.txt
python -m playwright install chrome
```

> على ويندوز يمكن ببساطة تشغيل `run.bat` — يكتشف نقص التبعيات ويثبتها تلقائياً.

---

## التشغيل

### واجهة رسومية (GUI)

```bat
run_gui.bat
```

### سطر الأوامر

```bat
run.bat
```

أو مباشرة:

```bash
python main.py --panel-only          # لوحة التحكم فقط
python main.py -c "افتح example.com واكتب عنوانه"
python main.py --qureo               # تشغيل حل QuREO مباشرة
```

### إيقاف الأداة

```bat
stop.bat
```

يغلق الأداة وجميع عمليات المتصفح وينظّف الملفات المؤقتة.

---

## خيارات سطر الأوامر

| الخيار | الوظيفة |
|---|---|
| `-c`, `--command` | تنفيذ أمر واحد ثم الخروج |
| `--qureo` | تشغيل مسار حل QuREO مباشرة |
| `--headless` | تشغيل المتصفح بدون نافذة مرئية |
| `--panel-only` | فتح لوحة التحكم فقط بدون وكيل |
| `--no-panel` | تعطيل لوحة التحكم |
| `--no-color` | إخراج بدون ألوان الطرفية |
| `--steps N` | الحد الأقصى لخطوات الوكيل |
| `--show-results` | عرض النتائج الخام أثناء التنفيذ |

---

## لوحة التحكم

تُفتح تلقائياً عند التشغيل على <http://127.0.0.1:8770/>

عشرة تبويبات: **QuREO · التشغيل · الذكاء الاصطناعي · المفتاح والأمان · المتصفح · الواجهة · خريطة الأدوات · السجل المباشر · المطورون · عن الأداة**

### واجهة برمجية (API)

كل النداءات تمر عبر نقطة واحدة على `127.0.0.1` فقط — لا يوجد أي اتصال خارجي من اللوحة.

**طلبات GET**

| المسار | الوصف |
|---|---|
| `/` · `/index.html` | صفحة اللوحة |
| `/api/state` | الحالة الكاملة: الإعدادات، المزوّد، هل المتصفح يعمل، هل مشغول |
| `/api/logs?after=N` | السجلات بعد الرقم التسلسلي `N` |
| `/api/tools` | خريطة الأدوات الـ22 مع الملفات وأرقام الأسطر |
| `/assets/<file>` | الشعار والأصول |

**طلبات POST**

| المسار | الجسم | الوظيفة |
|---|---|---|
| `/api/settings` | `{"settings":{...}}` | حفظ الإعدادات المسموح بها فقط |
| `/api/key` | `{"key":"..."}` | حفظ مفتاح API مشفّراً |
| `/api/test` | `{}` | اختبار الاتصال بالمزوّد |
| `/api/models` | `{}` | جلب قائمة الموديلات |
| `/api/browser` | `{"action": "start أو stop أو restart أو info"}` | التحكم في المتصفح |
| `/api/run` | `{"command":"..."}` | تنفيذ أمر عربي |
| `/api/qureo/solve` | `{"course","student_id","password","delay","use_ai"}` | بدء جولة حل |
| `/api/reset` | `{}` | استعادة الإعدادات الافتراضية |
| `/api/clear-logs` | `{}` | مسح السجل |
| `/api/shutdown` | `{}` | إغلاق الأداة |

> الإعدادات تُرشَّح بقائمة بيضاء (`ALLOWED` في `core/panel.py`) — أي مسار غير معروف يُرفض.

---

## الأدوات المتاحة (22)

| المجموعة | الأدوات |
|---|---|
| **التنقل** | `open_url` · `web_search` |
| **القراءة** | `page_snapshot` · `extract_text` · `current_page_info` |
| **التفاعل** | `click` · `fill` · `press_key` · `history` |
| **التبويبات** | `list_tabs` · `new_tab` · `switch_tab` · `close_tab` |
| **التحكم** | `wait` · `screenshot` |
| **QuREO** | `qureo_status` · `qureo_chapters` · `qureo_login` · `qureo_solve_chapter` · `qureo_solve_course` |
| **إنهاء** | `finish` |

تبويب **خريطة الأدوات** يعرض لكل أداة ملفها المنفّذ ورقم السطر والدوال التي تستدعيها.

---

## الإعدادات

كل الإعدادات في `config.json` (يُنشأ تلقائياً). القيم الافتراضية:

```json
{
  "ai": {
    "provider": "groq",
    "model": "",
    "base_url": "",
    "api_key": "",
    "temperature": 0.1,
    "max_steps": 14,
    "max_tokens": 4000,
    "timeout": 120,
    "extra_instructions": ""
  },
  "browser": {
    "headless": false,
    "channel": "chrome",
    "user_data_dir": "browser_profile",
    "locale": "ar-EG",
    "viewport_width": 1360,
    "viewport_height": 850,
    "timeout_ms": 30000,
    "slow_mo": 0,
    "search_engine": "duckduckgo",
    "downloads_path": "media",
    "max_snapshot_items": 60
  },
  "ui": {
    "color": true,
    "show_steps": true,
    "show_raw_results": false,
    "show_banner": true,
    "banner_text": ""
  },
  "panel": {
    "enabled": true,
    "open_on_start": true,
    "host": "127.0.0.1",
    "port": 8770
  },
  "qureo": {
    "course": "python_short_ar",
    "section_id": 106,
    "course_url": "https://me-tp.qureo.education/course/python_short_ar",
    "delay_seconds": 3,
    "use_ai": true,
    "max_attempts": 5
  }
}
```

**المزوّدون المدعومون:** Groq · OpenAI · OpenRouter · Together AI · DeepSeek · Anthropic · Google Gemini

---

## QuREO

مسار حل كامل من البوابة إلى إكمال الفصول:

1. **البوابة** — `https://me-portal.qureo.education` (تسجيل دخول)
2. **تفعيل الجلسة** — الضغط على `div.course-card` لفتح جلسة موقع التعلّم
3. **موقع التعلّم** — `https://me-tp.qureo.education/api/study`
4. **الحل** — مراجعة المحاضرات ثم أسئلة الاختبار، مع إعادة محاولة حتى 5 محاولات لكل سؤال

**وضع بدون ذكاء اصطناعي:** فعّل «بدون ذكاء اصطناعي» في تبويب QuREO — тогда الإجابات تُحلّ
بمنطق القاعدة فقط بدون أي استدعاء لنموذج خارجي.

> **ملاحظة:** الأداة تعمل بحسابك أنت فقط. لا تُخزَّن أي بيانات دخول في الكود أو Git.
> تأكد أن استخدامك يلتزم بشروط منصة QuREO وسياستها التدريبية.

---

## بناء نسخة exe

```bat
build_exe.bat
```

الناتج: `dist\LYNIKV TOOL Qr\LYNIKV TOOL Qr.exe`

- انشر المجلد `dist\LYNIKV TOOL Qr` **بالكامل** إلى أي جهاز — لا تنسخ الـ exe وحده
- الإعداد في `LYNIKV.spec`
- السكربت ASCII-only لتفادي أخطاء cmd في ترميزات Windows

**اختبار سريع بعد البناء:**

```bat
"dist\LYNIKV TOOL Qr\LYNIKV TOOL Qr.exe" --selftest
```

يكتب النتيجة في `logs\qt_selftest.txt` ويتحقق من: عنوان الـ backend · `/api/state` · تحميل الصفحة · عنوان المستند.

---

## بنية المشروع

```
.
├── main.py              # نقطة الدخول: الوكيل، الخيط، مجدول المهام
├── qt_app.py            # غلاف PySide6 + QWebEngineView + وضع selftest
├── core/
│   ├── browser.py       # Playwright: الجلسة، المتصفح، الاستعادة التلقائية
│   ├── panel.py         # خادم اللوحة + واجهة API
│   ├── panel.html       # واجهة اللوحة (HTML/CSS/JS متصلة)
│   ├── ai_provider.py   # Groq, OpenAI, OpenRouter, Together, DeepSeek, Anthropic, Gemini
│   ├── qureo.py         # عميل QuREO: بوابة، SSO، API، حل الفصول
│   ├── tools.py         # تعريف 22 أداة + منفّذها
│   ├── planner.py       # موجّه الوكيل وتعليماته
│   ├── config.py        # إدارة الإعدادات + مفتاح مشفّر
│   ├── crypto.py        # تشفير المفتاح (Fernet)
│   ├── logbus.py        # سجل دائري برقوم تسلسلية
│   ├── ui.py            # مخرجات الطرفية
│   └── inspect_map.py   # خريطة الأدوات للوحة
├── assets/              # الشعار والأيقونة
├── run.bat / run_gui.bat / stop.bat
├── build_exe.bat
└── LYNIKV.spec
```

---

## الأمان

- **مفتاح API** يُخزَّن مشفّراً في `config.json`، والمفتاح نفسه في `.secret_key`
- **لا يوجد أي مفتاح أو كلمة مرور في الكود**، ولا في هذا المستودع
- **اللوحة تستمع على `127.0.0.1` فقط** — غير متاحة من الشبكة
- الملفات الحساسة مستثناة في `.gitignore`:
  `config.json` · `.secret_key` · `browser_profile/` · `logs/` · `media/` · `dist/` · `build/` · الأرشيفات
- **إن نشرت مفتاحاً بالخطأ:** أزله فوراً من تاريخ Git، وصدار مفتاحاً جديداً من لوحة المزوّد — فحذف الملف وحده لا يكفي

---

## استكشاف الأخطاء

**المتصفح لا يفتح / `Target page, context or browser has been closed`**
الأداة تكشف موت جلسة Playwright وتعيد تشغيلها تلقائياً. اضغط «تشغيل المتصفح» مرة أخرى.
تأكد من عدم وجود نافذة أخرى تستخدم `browser_profile` — الملف يُقفل من أول عملية فقط.

**`Tool call validation failed` (خطأ 400 من Groq)**
بعض الموديلات المنفتحة تُصدر أسماء أدوات مشوّهة. جرّب موديلاً مستقراً مثل `llama-3.3-70b-versatile` من تبويب **الذكاء الاصطناعي**.

**لوحة التحكم تفتح ثم تُغلق**
منفذ `8770` مشغول. غيّر `panel.port` من تبويب **الواجهة**، ثم أعد تشغيل الأداة (المنفذ لا يُطبَّق إلا بعد إعادة التشغيل).

**فشل تسجيل دخول QuREO**
جرّب أولاً **بدون ذكاء اصطناعي** وبجلسة محفوظة. إن فشل، افحص `logs/login_fail.txt` والتقطة `logs/login_fail.png`.

**توقّف المتصفح فجأة بعد إغلاقه يدوياً**
اضغط على زر المتصفح مرة أخرى — الاستعادة التلقائية تعيد تشغيله. تأكد أن لا نافذة أخرى تستخدم مجلد `browser_profile`؛ القفل يسمح بعملية واحدة فقط.

---

## المساهمة

مستحسن: افتح issue أولاً لوصف المشكلة أو الميزة قبل أي تعديل كبير.

---

## الترخيص

MIT — انظر [LICENSE](LICENSE).

---

## English summary

**LYNIKV TOOL Qr** is an Arabic-first AI browser agent. Give it a command in Arabic and it drives a
real Chrome instance via Playwright until the task is done, then returns a final answer.

- **22 browser tools** across navigation, reading, interaction, tabs, control and QuREO
- **7 AI providers**: Groq, OpenAI, OpenRouter, Together, DeepSeek, Anthropic, Gemini
- **Local web panel** on `127.0.0.1:8770` with a tool map that shows the source file and line of every tool
- **QuREO auto-solver** for activated courses, with an **AI-free mode**
- **Encrypted key storage**, a whitelist-filtered settings API, and a Windows `.exe` build

```bash
pip install -r requirements.txt
python -m playwright install chrome
python main.py --panel-only
```

The QuREO solver runs **under your own account only**. Make sure your usage complies with the
platform's terms of service.

---

<div align="center">

**LYNIKV TOOL Qr** — developed by [Lynox](https://lynkiv.duckdns.org/) & Kivix

</div>