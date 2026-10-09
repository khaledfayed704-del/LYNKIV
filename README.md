<div align="center">

# LYNIKV TOOL Qr

**وكيل ذكاء اصطناعي عربي للتحكم في المتصفح + حلال QuREO التلقائي**

نسخة محمية (Encrypted Build) · 22 أداة · 7 مزوّدات ذكاء اصطناعي · دعم كامل للعربية (RTL)

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Protected](https://img.shields.io/badge/Build-Encrypted-success)]()
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

</div>

---

## نبذة

`LYNIKV TOOL Qr` وكيل ذكاء اصطناعي عربي يتحكم في متصفح حقيقي عبر Playwright لتنفيذ أوامرك،
بالإضافة إلى **حلال QuREO** التلقائي لمحاضرات وأسئلة الكورسات المفعّلة في حسابك (مع وضع **بدون
ذكاء اصطناعي** بالكامل).

هذه نسخة **بناء محمي (encrypted build)**: الكود المصدري الحقيقي غير موجود كملفات `.py` منفصلة،
بل مجمّع ومشفّر داخل ملف واحد يقرأه محمّل (`main.py`) وقت التشغيل فقط.

**التطوير:** [Lynox](https://lynkiv.duckdns.org/) · **Kivix**

---

## الملفات الفعلية في هذه الحزمة

```
.
├── main.py              # المحمّل (loader) — يفك تشفير _lynikv.dat وقت التشغيل فقط، لا يُعدَّل
├── _lynikv.dat            # الحزمة المشفّرة: كل كود الأداة (22 أداة + اللوحة + QuREO...) + أصول + HTML
├── config.json             # إعدادات التشغيل (يُنشأ/يُحدَّث تلقائياً، مفتاح الـ API فاضي افتراضياً)
├── run.sh                   # مشغّل لينكس/أندرويد (Termux)
├── requirements.txt          # playwright>=1.44 · requests>=2.31
├── FIRST_RUN.txt               # دليل تشغيل سريع على Termux بالعربي
├── README.md
└── LICENSE
```

> لا يوجد مجلد `core/` ولا `assets/` ظاهر على القرص — كل شيء (الكود، `panel.html`،
> `banner.txt`، `logo.png`) مضغوط جوه `_lynikv.dat` ويُقدَّم من الذاكرة مباشرة وقت التشغيل.

---

## آلية الحماية (Encrypted Build)

- **تشفير الحزمة**: `_lynikv.dat` مشفّر بخوارزمية مبنية على HMAC-SHA256 (stream cipher)، ومضغوط بـ gzip فوق أرشيف tar.
- **تحقق التكامل**: كل حزمة موقّعة بـ HMAC على المحتوى كامل (salt + nonce + tag) — أي تعديل ولو بايت واحد يفشّل التحقق ويرفض التشغيل.
- **حماية المحمّل نفسه**: `main.py` بيتحقق من `sha256` الخاص به مقابل القيمة المسجّلة وقت البناء — لو اتعدّل، الأداة ترفض تشتغل.
- **ملفات في الذاكرة فقط**: `panel.html`، `banner.txt`، و`assets/logo.png` بيتقدموا من الذاكرة مباشرة عبر حارس (guard) على `open`/`pathlib.Path` — مفيش نسخة مفكوكة منهم على القرص أبداً.
- **ربط بالمالك**: الحزمة فيها حقل `owner` موقّع لازم يطابق قيمة مبنية في المحمّل.

### أوامر التحقق المدمجة

```bash
python main.py --protect-verify     # يعرض توقيع الحزمة، المالك، تاريخ البناء، عدد الملفات
python main.py --protect-selftest   # يشغّل اختبار ذاتي كامل (استيراد، خريطة الأدوات، الذاكرة)
```

مثال ناتج `--protect-verify`:
```
[✓] التوقيع رقمي على الحزمة سليم — لم يُمسّ المحتوى
    الأداة     : LYNIKV TOOL Qr
    المالك     : Lynox & Kivix
    ملفات الشيفرة: 13 · ملفات في الذاكرة: 4
```

---

## المتطلبات

- **Python** 3.10 أو أحدث
- **Linux / Termux (أندرويد)** — هذه الحزمة مبنية لهذه البيئة
- `requests` (أساسي) و`playwright` (اختياري — أدوات المتصفح فقط، غير متاح على أندرويد)
- اتصال إنترنت للوصول إلى مزوّد الذكاء الاصطناعي

---

## التثبيت والتشغيل

```bash
git clone https://github.com/khaledfayed704-del/LYNKIV.git
cd LYNKIV

chmod +x run.sh
./run.sh --install     # يثبّت python + requests تلقائياً
./run.sh                 # يشغّل اللوحة على http://127.0.0.1:8770
```

أوامر `run.sh` الأخرى:

```bash
./run.sh --cli          # الطرفية الكاملة (الوكيل داخل Terminal)
./run.sh --status        # حالة الخادم
./run.sh --stop           # إيقاف الخادم
./run.sh -- --headless     # تمرير خيارات لـ main.py (مثل تشغيل المتصفح بلا نافذة)
```

أو مباشرة عبر بايثون:

```bash
python main.py --panel-only          # لوحة التحكم فقط
python main.py -c "افتح example.com واكتب عنوانه"
python main.py --qureo               # تشغيل حل QuREO مباشرة
```

> **على Termux/أندرويد:** Playwright غير متاح، فأدوات المتصفح (فتح صفحات، نقر، تعبئة)
> غير مفعّلة، لكن اللوحة كاملة وحلّ QuREO يعمل عبر HTTP مباشرة (`qureo.transport: auto`).
> التفاصيل في `FIRST_RUN.txt`.

---

## الإعدادات (config.json)

يُنشأ تلقائياً عند أول تشغيل بهذه القيم الافتراضية:

```json
{
  "ai": {
    "provider": "groq", "model": "", "base_url": "", "api_key": "",
    "temperature": 0.1, "max_steps": 14, "max_tokens": 4000,
    "timeout": 120, "extra_instructions": ""
  },
  "browser": {
    "headless": false, "channel": "chrome", "user_data_dir": "browser_profile",
    "locale": "ar-EG", "viewport_width": 1360, "viewport_height": 850,
    "timeout_ms": 30000, "slow_mo": 0, "search_engine": "duckduckgo",
    "downloads_path": "media", "max_snapshot_items": 60
  },
  "ui": { "color": false, "show_steps": true, "show_raw_results": false, "show_banner": true, "banner_text": "" },
  "panel": { "enabled": true, "open_on_start": true, "host": "127.0.0.1", "port": 8770 },
  "qureo": {
    "course": "python_short_ar", "section_id": 0,
    "course_url": "https://me-tp.qureo.education/course/python_short_ar",
    "delay_seconds": 0.0, "use_ai": false, "max_attempts": 5, "transport": "auto"
  }
}
```

**المزوّدون المدعومون:** Groq · OpenAI · OpenRouter · Together AI · DeepSeek · Anthropic · Google Gemini

> مفتاح الـ API يُخزَّن مشفّراً داخل `config.json` ولا يظهر أبداً في الواجهة. لا تنشر
> `config.json` بعد ما تحطّ فيه مفتاح حقيقي — انشر النسخة الافتراضية (الفاضية) فقط.

---

## لوحة التحكم

تُفتح تلقائياً على <http://127.0.0.1:8770/> — عشرة تبويبات: **QuREO · التشغيل · الذكاء
الاصطناعي · المفتاح والأمان · المتصفح · الواجهة · خريطة الأدوات · السجل المباشر ·
المطورون · عن الأداة**.

كل نداءات الـ API تمر عبر `127.0.0.1` فقط — لا يوجد اتصال خارجي من اللوحة، والإعدادات
مُرشَّحة بقائمة بيضاء (أي مسار غير معروف يُرفض).

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

---

## QuREO

1. **البوابة** — `https://me-portal.qureo.education` (تسجيل دخول)
2. **تفعيل الجلسة** — فتح جلسة موقع التعلّم
3. **موقع التعلّم** — `https://me-tp.qureo.education/api/study`
4. **الحل** — مراجعة المحاضرات ثم الأسئلة، حتى 5 محاولات لكل سؤال

**وضع بدون ذكاء اصطناعي:** فعّل «بدون ذكاء اصطناعي» في تبويب QuREO لحل بمنطق القاعدة فقط.

> الأداة تعمل بحسابك أنت فقط. تأكد أن استخدامك يلتزم بشروط منصة QuREO وسياستها التدريبية.

---

## الأمان

- الكود الحقيقي غير قابل للقراءة أو التعديل المباشر — مشفّر جوه `_lynikv.dat`.
- أي تلاعب في `main.py` أو `_lynikv.dat` يفشّل تحقق التكامل ويوقف التشغيل فوراً.
- **اللوحة تستمع على `127.0.0.1` فقط** — غير متاحة من الشبكة.
- لا تُخزَّن أي بيانات دخول أو مفاتيح API في الكود نفسه.

---

## استكشاف الأخطاء

**`الحزمة المشفّرة مفقودة أو غير صالحة`**
تأكد أن `_lynikv.dat` في نفس مجلد `main.py` ولم يُعدَّل أو يُنقَل بشكل جزئي.

**`ملف المحمّل عُدّل عن نسخة البناء الأصلية`**
لا تُعدّل `main.py` يدوياً إطلاقاً — أي تغيير فيه، حتى مسافة، يُفشل التحقق.

**لوحة التحكم تفتح ثم تُغلق**
منفذ `8770` مشغول. غيّر `panel.port` في `config.json`، ثم أعد تشغيل الأداة.

**فشل تسجيل دخول QuREO**
جرّب أولاً **بدون ذكاء اصطناعي** وبجلسة محفوظة. التفاصيل في `FIRST_RUN.txt`.

---

## الترخيص

MIT — انظر [LICENSE](LICENSE).

---

<div align="center">

**LYNIKV TOOL Qr** — developed by [Lynox](https://lynkiv.duckdns.org/) & Kivix

</div>
