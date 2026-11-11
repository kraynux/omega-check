<!-- Copyright (c) 2026 kraynux - kraynux@proton.me - رخصة MIT (انظر ملف LICENSE) -->
<div align="center">
  <img src="https://raw.githubusercontent.com/kraynux/kraynux/refs/heads/main/docs/assets/omega-check.png" alt="Omega-Check" width="512">
</div>

#  OMEGA-CHECK

**ماسح المنافذ والخدمات وأدوار الشبكة (هدف واحد)**

> طوّره [kraynux](https://github.com/kraynux) من أجل [Omega-Server](https://kraynux.snake-mackarel.ts.net)   

الصفحة الرسمية: [OMEGA-CHECK](https://kraynux.snake-mackarel.ts.net/omega-check/) &nbsp; معاينة: [Screenshots](https://kraynux.snake-mackarel.ts.net/omega-check/screenshots/)  

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](../../../LICENSE)
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Platform](https://img.shields.io/badge/Platform-Linux-informational.svg)](https://www.linux.org/)
[![Interface](https://img.shields.io/badge/Interface-TUI%20%2B%20Rich-cyan.svg)](https://github.com/Textualize/rich)

🌐 الواجهة والتقارير المُصدَّرة متاحة بـ **17 لغة** — انظر [لغات الواجهة](#لغات-الواجهة).  
**اللغات:**  
<img src="https://flagcdn.com/w20/fr.png" alt="Français" style="height:14px;"> [Français](../../../README.md) · <img src="https://flagcdn.com/w20/gb.png" alt="English" style="height:14px;"> [English](../en/README.md) · <img src="https://flagcdn.com/w20/es.png" alt="Español" style="height:14px;"> [Español](../es/README.md) · <img src="https://flagcdn.com/w20/br.png" alt="Português (Brasil)" style="height:14px;"> [Português (Brasil)](../pt-BR/README.md) · <img src="https://flagcdn.com/w20/it.png" alt="Italiano" style="height:14px;"> [Italiano](../it/README.md) · <img src="https://flagcdn.com/w20/de.png" alt="Deutsch" style="height:14px;"> [Deutsch](../de/README.md) · <img src="https://flagcdn.com/w20/nl.png" alt="Nederlands" style="height:14px;"> [Nederlands](../nl/README.md) · <img src="https://flagcdn.com/w20/pl.png" alt="Polski" style="height:14px;"> [Polski](../pl/README.md) · <img src="https://flagcdn.com/w20/ru.png" alt="Русский" style="height:14px;"> [Русский](../ru/README.md) · <img src="https://flagcdn.com/w20/cn.png" alt="中文" style="height:14px;"> [中文](../zh-CN/README.md) · <img src="https://flagcdn.com/w20/vn.png" alt="Tiếng Việt" style="height:14px;"> [Tiếng Việt](../vi/README.md) · <img src="https://flagcdn.com/w20/th.png" alt="ไทย" style="height:14px;"> [ไทย](../th/README.md) · <img src="https://flagcdn.com/w20/id.png" alt="Bahasa Indonesia" style="height:14px;"> [Bahasa Indonesia](../id/README.md) · <img src="https://flagcdn.com/w20/jp.png" alt="日本語" style="height:14px;"> [日本語](../ja/README.md) · <img src="https://flagcdn.com/w20/kr.png" alt="한국어" style="height:14px;"> [한국어](../ko/README.md) · <img src="https://flagcdn.com/w20/in.png" alt="हिन्दी" style="height:14px;"> [हिन्दी](../hi/README.md) · <img src="https://flagcdn.com/w20/ae.png" alt="العربية" style="height:14px;"> [العربية](README.md)

---

**Omega-check** أداة TUI + CLI تفحص منافذ هدف شبكي واحد، وتتعرّف على الخدمة التي تعمل على كل منفذ مفتوح (البروتوكول، والبرنامج، والإصدار، والمصادقة، وWAF، وTLS)، وتستنتج دورها المحتمل، دون أن تنفّذ أي هجوم نشط أبدًا. هي إحدى أدوات مجموعة `omega-`، مبنية وفق Clean Architecture — انظر `docs/ARCHITECTURE.md` لكل التفاصيل التقنية.

<p align="center">
  <img src="https://raw.githubusercontent.com/kraynux/kraynux/refs/heads/main/docs/translation/ar/omega-check/A.png" width="24%" />
  <img src="https://raw.githubusercontent.com/kraynux/kraynux/refs/heads/main/docs/translation/ar/omega-check/B.png" width="24%" />
  <img src="https://raw.githubusercontent.com/kraynux/kraynux/refs/heads/main/docs/translation/ar/omega-check/C.png" width="24%" />
  <img src="https://raw.githubusercontent.com/kraynux/kraynux/refs/heads/main/docs/translation/ar/omega-check/D.png" width="24%" />
</p>

## 1. الرؤية والنطاق

Omega-check ماسح منافذ موجّه لإدارة الأنظمة: التحقق بسرعة مما يستمع على جهاز ما (جهازك، أو الشبكة المحلية، أو هدف خارجي مأذون به)، وبماذا، ومدى الثقة التي يمكن منحها لكل معلومة.

### ما يفعله Omega-check

- يفحص قائمة منافذ (ملف تعريف النظام، أو ملف تعريف شخصي، أو إدخال حر) على هدف واحد.
- يتعرّف على الخدمة العاملة على كل منفذ مفتوح: البروتوكول (HTTP/HTTPS/SSH/TLS/VNC/عام)، والبرنامج وإصداره عندما يكونان مكشوفين، وضرورة المصادقة.
- يستنتج دورًا محتملًا (خادم ويب، وصول إلى الصدفة، وصول رسومي، قاعدة بيانات) من البروتوكول الذي جرى التفاوض عليه فعلًا، وليس من مجرد افتراض مبني على رقم المنفذ.
- يكتشف تواقيع WAF المعروفة (Cloudflare وSucuri وAkamai وImperva Incapsula) عندما تكون مُعلنة في الترويسات.
- يعرض النتيجة في TUI (Textual) أو في CLI قابل للبرمجة النصية، ومن خلال ثلاثة أنواع من التصدير: JSON، ونص، وHTML (5 سمات).
- يمنح كل معلومة مجمّعة مستوى ثقة صريحًا — انظر [§7](#7-سياسة-الثقة).
- يحتفظ بسجل دائم للفحوص، قابل لإعادة التشغيل والمقارنة عبر الزمن.
- يتيح تثبيت الأهداف وإنشاء ملفات تعريف منافذ شخصية، قابلة لإعادة الاستخدام من فحص إلى آخر.

### ما لا يفعله Omega-check

- فحص الثغرات النشط: لا SQLi ولا XSS ولا RCE.
- فحص CVE.
- التعرّف على نظام التشغيل (يتضمن نموذج البيانات الحقل، لكن لا توجد حاليًا أي قاعدة استدلالية تملؤه).
- تقنيات الفحص منخفضة المستوى على طريقة nmap (فحص SYN، والحزم الخام) — اتصال TCP على مستوى التطبيق فقط.
- أداة للتخمين بالقوة الغاشمة أو للتشويش (fuzzing).
- الفحص المتوازي لعدة أهداف.
- لوحة تحكم ويب.

## 2. التثبيت

### المتطلبات

- Python 3.10+
- اتصال بالإنترنت، من أجل الاعتماديات

### التثبيت

```bash
[ -d omega-check ] && echo "ℹ️ مُستخرَج هنا مسبقًا، تم تخطي الخطوة." || tar -xzf omega-check.tar.gz
cd omega-check/
chmod +x install.sh
./install.sh
```

`install.sh`:

1. ينشئ البيئة الافتراضية `.venv` إن لم تكن موجودة.
2. يثبّت الاعتماديات (`pip install -e .`؛ ويبقى `pyproject.toml` المرجع الوحيد).
3. يجعل `omega-check.sh` و`install.sh` قابلين للتنفيذ.
4. يضيف الاسم المستعار `check` إلى `~/.bashrc` و`~/.zshrc` (من دون تكرار إن كان موجودًا).

### الاعتماديات

مُعرَّفة في `pyproject.toml` (لم يعد هناك `requirements.txt`):
- `omega-lib`: المكتبة المشتركة للمجموعة (`ConfidenceLevel`، والسمات، واكتشاف الطرفية)
- `textual`: واجهة TUI، والسمات، والتكيّف التلقائي مع الطرفية
- `httpx`: مسبار HTTP/HTTPS
- `cryptography`: قراءة شهادة TLS المتفاوض عليها
- `jinja2`: قوالب تصدير HTML
- اعتماديات التطوير (`pip install -e ".[dev]"`): `pytest` و`pytest-asyncio` و`pytest-cov` و`pytest-httpserver` و`trustme` و`ruff` و`mypy` و`import-linter`

## 3. الاستخدام

### الوضع التفاعلي (TUI)

يُنصح به للاستخدام اليومي — يُشغَّل من دون وسائط:

```bash
./omega-check.sh
```
إن أنشأت الاسم المستعار، فاكتب `check` فقط في الطرفية:
```bash
check
```

المسار: شاشة البداية (تُغلق بضغطة مفتاح أو نقرة) ← القائمة الرئيسية (فحص / الأهداف / ملفات التعريف / السجل / الإعدادات / مساعدة) ← إدخال الهدف (مع منتقٍ للأهداف المثبّتة) واختيار ملف التعريف (تحذير مع `complet`، وحقل ثانٍ لملف تعريف شخصي أو لإدخال حر للمنافذ مع `CUSTOM`) ← الفحص (مؤشر تقدّم غير محدد وسجل مباشر لعمليات الشبكة) ← تفاصيل الفحص (المنافذ/الخدمات/الأدوار، والتصدير) ← السجل/المقارنة/إعادة التشغيل والإعدادات من القائمة الرئيسية. التكيّف مع الطرفية (الألوان، والحجم، وتبسيط البنية) تلقائي.

#### اختصارات لوحة المفاتيح

| المفتاح | الإجراء |
|---|---|
| `↑` / `↓` | التنقل بين عناصر الشاشة |
| `Tab` / `Shift+Tab` | التنقل بين حقول النموذج |
| `Esc` | العودة إلى الشاشة السابقة (تأكيد الخروج في الشاشة الرئيسية) |
| `t` | السمة التالية (تُطبَّق فورًا دون تأكيد) |
| `r` | تحديث اكتشاف الطرفية |
| `a` | عرض المساعدة |
| `q` | الخروج (مع تأكيد) |

### لغات الواجهة

الواجهة متاحة بـ 17 لغة: الفرنسية، والإنجليزية، والإسبانية، والبرتغالية (البرازيل)، والإيطالية، والألمانية، والهولندية، والبولندية، والروسية، والصينية المبسّطة، والفيتنامية، والتايلاندية، والإندونيسية، واليابانية، والكورية، والهندية، والعربية. يتم الاختيار من الإعدادات («Langue / Language») ويسري بعد إعادة تشغيل الواجهة؛ ويفرض المتغير `OMEGA_CHECK_LANG` (مثلًا `OMEGA_CHECK_LANG=ar ./omega-check.sh`) لغة طوال جلسة واحدة. عند التشغيل من omega-suite، يأخذ omega-check لغة المجموعة. على وحدة التحكم النصية في Linux ‏(TTY)، تُعرض اللغات ذات الكتابة غير اللاتينية بالإنجليزية طوال الجلسة. يبقى سطر الأوامر بالفرنسية.

### التواصل والدعم

تتيح المساعدة (المفتاح `a`) شاشة **التواصل والدعم**: *ادفع ثمن قهوة* (صفحة PayPal الخاصة بالمطوّر)، و*التواصل مع الدعم* (عنوان البريد الإلكتروني ونموذج التواصل في الموقع، معروضان بوضوح)، و*تسجيلي كمستخدم (مجهول الهوية)* و*التحقق من التحديثات*. التسجيل اختياري، ومعطّل افتراضيًا، ويُرسل مرة واحدة فقط: يُستخدم فقط لإحصاء المستخدمين، وإن رغبت، قارتهم أو بلدهم (قوائم مغلقة، دون أي نص حر). يُرسل مفتاحًا مولَّدًا عشوائيًا واسم البرنامج (`omega-check`) وإصداره؛ ولا يُرسل أبدًا اسمًا أو اسم جهاز أو إعدادًا أو هدفًا أو نتيجة. لا يُحفظ عنوان IP في التسجيلات، لكنه، كأي زيارة، يمر عبر فحوص الأمان وسجل الخادم المستقبِل. يمكن السحب في أي وقت من الشاشة نفسها (*إلغاء تسجيلي*). يقرأ التحقق من التحديثات قائمة الإصدارات المنشورة على الموقع فقط، ولا يحدث أبدًا دون نقرة.

### وضع البرمجة النصية (CLI)

أي أمر فرعي يفعّل وضع CLI:

```bash
# فحص هدف بملف تعريف منافذ
./omega-check.sh scan 192.168.1.10 --profile minimal

# السجل (قابل للتصفية حسب الهدف)
./omega-check.sh history --target 192.168.1.10 --limit 20

# تفاصيل فحص (نص أو JSON أو HTML) — اختيار من 5 سمات للتصدير
./omega-check.sh show <scan_id> --format html --theme omega-base --output report.html

# مقارنة فحصين (تغيّرات حالة المنافذ)
./omega-check.sh compare <scan_id_a> <scan_id_b>

# ملفات تعريف المنافذ الشخصية
./omega-check.sh profile list
./omega-check.sh profile create lab --ports 22,80,443 --description "ملفي الشخصي"
./omega-check.sh profile edit lab --ports 22,80,443,8080
./omega-check.sh profile pin lab
./omega-check.sh profile unpin lab
./omega-check.sh profile delete lab
```

### صيغ الهدف المقبولة

```text
192.168.1.10                IPv4
example.org                 اسم المضيف
http://example.org          عنوان HTTP  (يُزال المخطط قبل التحليل)
https://example.org:8443    عنوان HTTPS مع منفذ  (يُزال المخطط والمنفذ)
```

يُزال المخطط والمنفذ، إن وُجدا، قبل تحليل DNS ‏(`domain/targets/validation.py::normalize_target_input`) — لصق عنوان URL كامل يعمل، ولا يُحتفظ إلا بالمضيف.

## 4. ملفات تعريف الفحص

| ملف التعريف | الوصف | مثبّت |
|---|---|---|
| `minimal` | فحص فائق السرعة: SSH + HTTP + HTTPS (‏22، 80، 443) | نعم |
| `classic` | خدمات الإنترنت/الشبكة المحلية الشائعة (37 منفذًا) | نعم |
| `web` | خدمات الويب والمنافذ البديلة | لا |
| `db` | قواعد البيانات وخدمات البيانات | لا |
| `remote` | الوصول عن بُعد — الصدفة، وسطح المكتب، وRustDesk | لا |
| `mail` | خدمات البريد | لا |
| `dns` | خدمات DNS | لا |
| `iot` | أجهزة إنترنت الأشياء، والكاميرات، والموجّهات، والمنزل الذكي | لا |
| `dev` | بيئات التطوير/المختبر | لا |
| `docker` | Docker وSwarm والخدمات الشائعة في الحاويات | لا |
| `complet` | **يُنشأ فوريًا**: اتحاد مرتّب وخالٍ من التكرار لكل ملفات التعريف أعلاه | لا |
| `CUSTOM` | ملف تعريف شخصي أُنشئ في شاشة **ملفات التعريف**، و/أو إدخال حر (`80` / `22,443,8080` / `1000-2000`) — يُجمع الاثنان معًا دون تكرار | لا |

التفاصيل الكاملة، وقواعد التحقق، وإدارة ملفات التعريف الشخصية: `docs/PROFILES.md`.

## 5. البنية المعمارية

بُني Omega-check وفق **Clean Architecture** ‏(domain / application / infrastructure / interfaces / ports / core / app / plugins / shared)، بما يتّسق مع قالب مجموعة `omega-` (انظر `omega-scan`/`omega-stress`)، ويتحقق منها `import-linter` عند كل تعديل. التفاصيل الكاملة في **`docs/ARCHITECTURE.md`**.

نظرة عامة قصيرة جدًا:

```text
src/omega_check/
├── domain/          منطق أعمال خالص (الفحوص، والأهداف، والخدمات، وملفات التعريف، والتقارير...)
├── application/     حالات الاستخدام (commands/queries)
├── ports/           العقود التي يتوقعها التطبيق (المسابير، والمستودعات، والمُصدِّرات...)
├── infrastructure/  تنفيذات فعلية (socket/httpx/cryptography، SQLite؛ Textual ليس هنا)
├── interfaces/      tui/ ‏(Textual) وcli/ (قابل للبرمجة النصية)، بتكافؤ وظيفي صارم
├── app/             التجميع (DependencyContainer، bootstrap، دورة الحياة)
├── core/, shared/   مفردات مشتركة، وأدوات مساعدة خارج منطق الأعمال
└── plugins/         البنية جاهزة، فارغة (لا يوجد محور توسعة مؤكد)
```

قواعد التصميم:
- `domain/services/policies.py`: يصنّف القرائن المجمّعة مسبقًا، ولا يتصل بالشبكة أبدًا.
- `infrastructure/network/`: يتصل بالشبكة (المقابس، و`httpx`، و`cryptography`)، ولا يُصدر أحكامًا أبدًا.
- `interfaces/`: تعرض فقط، ولا تحتوي أي منطق أعمال.
- `infrastructure/exporters/`: تقرأ نتيجة الفحص، ولا تعيد حساب أي شيء.

## 6. التعرّف على الخدمات والأدوار

### البروتوكولات المكتشفة

| البروتوكول | المسبار | التفاصيل المجمّعة |
|---|---|---|
| HTTP / HTTPS | `httpx` | لافتة `Server`، وترويسات المصادقة |
| TLS | `cryptography` (الشهادة المتفاوض عليها، بما فيها `CERT_NONE`) | الإصدار، والتشفير، وصاحب الشهادة/مُصدِرها |
| SSH | لافتة خام | البرنامج والإصدار (مثل `OpenSSH 10.4`) |
| VNC (RFB) | رموز الأمان التي يعلنها الخادم | أنواع المصادقة المدعومة |
| عام | لافتة خام على منفذ مفتوح غير معروف | استخراج حذر، دون قواعد استدلالية متشددة |

### الأدوار المستنتجة

تُستنتج من البروتوكول **المتفاوض عليه فعلًا**، ولا تُستنتج أبدًا من افتراض مبني على رقم المنفذ:

| الدور | الشرط | الثقة |
|---|---|---|
| `خادم ويب` | تأكيد بروتوكول HTTP/HTTPS | `INFERRED` |
| `وصول إلى الصدفة` | تأكيد بروتوكول SSH | `CORROBORATED` |
| `وصول رسومي` | تأكيد بروتوكول VNC | `CORROBORATED` |
| `قاعدة بيانات` | المنفذ ضمن نطاق ملف تعريف النظام `db` | `INFERRED` |

### تواقيع WAF المعروفة

تُكتشف عبر ترويسة تصريحية (`server`، `x-sdk`) — وجودها **مُعلن من الهدف**، ولا يُتحقق منه بشكل مستقل أبدًا: Cloudflare وSucuri وAkamai وImperva Incapsula وAWS ELB (مُدرج للعلم، وليس جدار حماية تطبيقات بالمعنى الدقيق).

## 7. سياسة الثقة

يحمل كل حقل مجمّع أحد المستويات التالية:

| المستوى | المعنى |
|---|---|
| `VERIFIED` | حقيقة بروتوكولية مُلاحظة مباشرة، لا يستطيع الهدف تزويرها (مثل منفذ مغلق أكّده TCP RST، أو إصدار TLS متفاوض عليه فعلًا). |
| `DECLARED` | قيمة أعلنها الهدف بنفسه في حقل يتحكم فيه بالكامل (مثل لافتة `Server`) — معقولة لكنها قابلة للتزوير كما يشاء. |
| `CORROBORATED` | قيمة `DECLARED` أكّدتها قرينة مستقلة (مثل دور SSH، لأن البروتوكول جرى التفاوض عليه فعلًا). |
| `INFERRED` | مستنتجة من نمط/قاعدة استدلالية، دون تصريح صريح من الهدف. |
| `UNKNOWN` | لا توجد قرينة صالحة، أو أخفاها الهدف عمدًا. |

## 8. الحماية من القيم المزوّرة

لا يثق Omega-check بأي بيانات أعلنها الهدف بنفسه دون الإشارة إلى ذلك صراحة. تبقى لافتة `Server` أو ترويسة `X-Powered-By` بحالة `DECLARED`، ولا تصبح `VERIFIED` أبدًا مهما بدت معقولة — فالهدف نفسه هو من يقدّمها ويستطيع تزويرها كما يشاء. وحده التأكيد عبر قناة مستقلة (مثل بروتوكول SSH المتفاوض عليه فعلًا لدور «الوصول إلى الصدفة») يرفع المعلومة إلى `CORROBORATED`. هذا التمييز، الذي تحمله `omega-lib` ‏(`ConfidenceLevel`)، بنيوي: لا يمكن لأي تصدير أو عرض أن يخفيه.

## 9. التوافق مع الطرفيات

تكتشف واجهة TUI ‏(Textual) قدرات الطرفية تلقائيًا (المحاكي، والحجم) وتكيّف ورقة أنماطها البنيوية وفقًا لذلك (`complete`/`standard`/`reduced`/`mono`)، دون أي خيار يدوي. يبقى وضع CLI نصًا بسيطًا دائمًا، مستقلًا عن الطرفية. وهي سياسة تتشاركها مجموعة `omega-` كلها (`omega-lib`، `terminal/policies.py`).

### الملف الشخصي حسب المحاكي المكتشَف

| المحاكي | الملف الشخصي الأولي |
|---|---|
| Ghostty, Alacritty, WezTerm, Kitty | `complete` |
| Konsole, GNOME Terminal, Terminator, Xfce4 Terminal | `standard` |
| xterm، urxvt، SSH حديث | `reduced` |
| TTY في Linux، SSH قديم | `mono` |
| محاكٍ غير معروف | `reduced` (البديل الافتراضي) |

### الملف الشخصي حسب حجم الطرفية

| الحجم الأدنى (أعمدة × أسطر) | سقف الملف الشخصي |
|---|---|
| 120 × 32 | `complete` |
| 100 × 28 | `standard` |
| 80 × 24 | `reduced` |
| أقل من ذلك | `mono` |

الملف الشخصي النهائي هو **الأكثر تقييدًا بين الاثنين** (المحاكي والحجم) — فطرفية Ghostty بملء الشاشة إذا صُغّرت إلى 70 عمودًا تنزل إلى `mono`، حتى لو كان محاكيها يسمح بـ `complete`. ويمكن تحديثه مباشرة بالمفتاح `r`.

## 10. التصدير

تُكتب التقارير النصية وتقارير HTML باللغة المختارة في الإعدادات («لغة التصدير»، وهي افتراضيًا لغة الواجهة)؛ ويبقى JSON بيانات لا تُترجم. تُنشأ التقارير افتراضيًا في `var/exports/` (مسار تشغيل مرتبط بمجلد المشروع، و`$OMEGA_CHECK_VAR_DIR` لتغييره)، أو في المسار المحدد (`--output` في CLI، ومربع حوار في TUI). اسم ملف واضح ومؤرّخ: `scan-{ملف-التعريف}-{التاريخ}.ext`، و`scan-custom-{التاريخ}.ext` لملف تعريف شخصي، و`scan-{التاريخ}.ext` لإدخال حر دون ملف تعريف.

### JSON، المرجع

البنية الكاملة للفحص (`Scan` + `Host`)، قابلة للتسلسل إلى JSON بصرامة، بما في ذلك مستويات الثقة.

### النص، تقرير مقروء موجز

مقروء خارج الطرفية، دون رموز ANSI.

### HTML، تقرير ويب مستقل

خمس سمات للاختيار (`--theme` في CLI، ومنتقٍ في TUI؛ ويتبع افتراضيًا سمة الواجهة النشطة عند وجود مقابل لها). تخطيط خاص: حاوية، وشبكة معلومات، ومربعات إحصاءات حسب حالة المنفذ، وشارات ملوّنة — من العائلة البصرية نفسها لـ `omega-scan`/`omega-stress`.

## 11. السجل والمقارنة

يُحفظ كل فحص (SQLite، `var/db/omega-check.db`): سجل قابل للتصفح حسب الهدف، وتفاصيل تشغيل سابق، ومقارنة بين فحصين (حالة المنافذ)، وإعادة تشغيل فحص على الهدف نفسه دون إعادة إدخاله.

## 12. الاختبارات

```bash
source .venv/bin/activate
lint-imports        # يتحقق من Dependency Rule
pytest -q           # 191 اختبارًا
ruff check src tests
mypy -p omega_check
```

البنية: `tests/unit/` (النطاق والتطبيق، دون إدخال/إخراج حقيقي)، و`tests/integration/` (SQLite/ملفات حقيقية، وخادم HTTP وهمي `pytest-httpserver`، وTLS عبر `trustme`).

## 13. خارج النطاق

- فحص CVE
- الكشف النشط عن SQLi وXSS وRCE
- التعرّف على نظام التشغيل
- تقنيات الفحص منخفضة المستوى على طريقة nmap (فحص SYN، والحزم الخام)
- الزحف على المواقع
- التشويش (fuzzing)
- القوة الغاشمة
- الفحص المتزامن لعدة أهداف
- لوحة تحكم ويب

---

> Omega-check — افحص، وتعرّف، وصنّف، وأبلغ.
> ماسح منافذ بثقة صريحة، لا تخمين متنكّر في هيئة حقيقة.
