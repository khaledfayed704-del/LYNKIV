#!/usr/bin/env bash
# ============================================================================
#  LYNIKV TOOL Qr — مشغّل لينكس / أندرويد (Termux)
# ----------------------------------------------------------------------------
#  الحد الأدنى للتشغيل:  python + requests
#
#  ملاحظة مهمة عن أندرويد:
#     لا توجد نسخ Playwright لمنصّة أندرويد، لذا كل ما يحتاج متصفحًاليفتّل
#     عند استدعائه برسالة واضحة (بدلاً من انهيار كامل التطبيق). والباقي يعمل:
#       * لوحة التحكم الكاملة  http://127.0.0.1:8770
#       * الذكاء الاصطناعي  (groq / openai / anthropic / google / ...)
#       * الأدوات الـ22 (ملفات، نصوص، ويب، نظام، ...)
#       * التكامل مع LYNIKV / LynikV
#
#  الاستخدام:
#       ./run.sh              لوحة التحكم على http://127.0.0.1:8770
#       ./run.sh --cli        الطرفية الكاملة (الوكيل يعمل داخل Terminal)
#       ./run.sh --install    تثبيت المتطلبات فقط
#       ./run.sh --status     حالة الخادم
#       ./run.sh --stop       إيقاف الخادم
#       ./run.sh -- --headless        تمرير خيارات لـ main.py
# ============================================================================

set -u

APP_DIR="$(cd "$(dirname "$0")" && pwd)"
HOST="127.0.0.1"
PORT="8770"
URL="http://${HOST}:${PORT}/"
LOG_DIR="${APP_DIR}/logs"
LOG_FILE="${LOG_DIR}/run.sh.log"
PYTHON=""
RUN_MODE="panel"      # panel = اللوحة · cli = الطرفية الكاملة

c_ok=""; c_bad=""; c_dim=""; c_hi=""; c_off=""
if [ -t 1 ]; then
  c_ok=$'\033[32m'; c_bad=$'\033[31m'; c_dim=$'\033[2m'
  c_hi=$'\033[1;32m'; c_off=$'\033[0m'
fi

say() { printf '%s\n' "$*"; }
ok()  { printf '%s✓%s %s\n' "$c_ok" "$c_off" "$*"; }
bad() { printf '%s✗%s %s\n' "$c_bad" "$c_off" "$*"; }
dim() { printf '%s%s%s\n' "$c_dim" "$*" "$c_off"; }

# هل نحن داخل Termux؟
is_termux() {
  case "${PREFIX:-}${TERMUX_VERSION:-}" in
    *com.termux*) return 0 ;;
  esac
  [ -d "/data/data/com.termux" ] && return 0
  return 1
}

find_python() {
  for c in python3 python; do
    if command -v "$c" >/dev/null 2>&1; then PYTHON="$c"; return 0; fi
  done
  return 1
}

server_up() {
  "$PYTHON" - "$HOST" "$PORT" <<'PY' 2>/dev/null
import socket, sys
s = socket.socket(); s.settimeout(2)
try:
    s.connect((sys.argv[1], int(sys.argv[2]))); sys.exit(0)
except Exception:
    sys.exit(1)
finally:
    s.close()
PY
}

do_install() {
  say "── تثبيت المتطلبات ──────────────────────────────────"
  if ! find_python; then
    if is_termux; then
      dim "لم يُعثر على python — جارٍ التثبيت عبر pkg…"
      pkg update -y >/dev/null 2>&1 || true
      pkg install -y python >/dev/null 2>&1 || {
        bad "تعذّر تثبيت python عبر pkg"; return 1; }
      hash -r 2>/dev/null || true
      find_python || { bad "python ما زال غير متاح"; return 1; }
    else
      bad "python غير مثبّت. على ديبيان/أوبونتو: sudo apt install python3 python3-pip"
      return 1
    fi
  fi
  ok "python: $($PYTHON -V 2>&1)"

  if "$PYTHON" -c "import requests" >/dev/null 2>&1; then
    ok "requests: مثبّت"
  else
    dim "تثبيت requests…"
    "$PYTHON" -m pip install --user requests >/dev/null 2>&1 \
      || "$PYTHON" -m pip install requests >/dev/null 2>&1 \
      || { bad "تعذّر تثبيت requests"; return 1; }
    if "$PYTHON" -c "import requests" >/dev/null 2>&1; then ok "requests: تم التثبيت"
    else bad "requests لم يُستورد بعد"; return 1; fi
  fi

  # اختياري: psutil لفحص المعرّفات — ليس شرطاً للتشغيل
  if "$PYTHON" -c "import psutil" >/dev/null 2>&1; then
    dim "psutil: مثبّت (اختياري)"
  else
    dim "psutil: غير مثبّت (اختياري — pip install psutil)"
  fi

  # Playwright: لا يُطلب على أندرويد إطلاقاً
  if is_termux; then
    dim "Playwright: مُتخطّى (غير متاح على أندرويد — الوظائف المتاحة تعمل بلاه)"
  else
    if "$PYTHON" -c "import playwright" >/dev/null 2>&1; then
      ok "Playwright: مثبّت"
    else
      dim "Playwright غير مثبّت (اختياري): pip install playwright && playwright install chrome"
    fi
  fi
  say
  ok "اكتمل التثبيت. شغّل: ./run.sh"
  return 0
}

do_status() {
  if ! find_python; then bad "python غير متاح"; return 1; fi
  if server_up; then ok "الخادم يعمل: ${URL}"; else bad "الخادم متوقف"; return 1; fi
}

do_stop() {
  if ! find_python; then bad "python غير متاح"; return 1; fi
  if ! server_up; then dim "الخادم متوقف أصلاً"; return 0; fi
  "$PYTHON" - "$HOST" "$PORT" <<'PY'
import json, sys, urllib.request
host, port = sys.argv[1], sys.argv[2]
req = urllib.request.Request(
    "http://%s:%s/api/shutdown" % (host, port),
    data=b"{}", headers={"Content-Type": "application/json"})
try:
    urllib.request.urlopen(req, timeout=8).read()
    print("✓ أُرسل أمر الإيقاف")
except Exception as exc:
    print("✗ فشل الإيقاف: %s" % exc); sys.exit(1)
PY
  return $?
}

do_run() {
  say
  printf '%s' "$c_hi"
  printf '╔══════════════════════════════════════════════════════════╗\n'
  printf '║   LYNIKV TOOL Qr  —  مشغّل لينكس / أندرويد             ║\n'
  printf '╚══════════════════════════════════════════════════════════╝\n'
  printf '%s' "$c_off"
  say

  if ! find_python; then
    bad "python غير مثبّت. نفّذ:  ./run.sh --install"
    return 1
  fi

  if ! "$PYTHON" -c "import requests" >/dev/null 2>&1; then
    bad "requests غير مثبّت. نفّذ:  ./run.sh --install"
    return 1
  fi

  if server_up; then
    ok "الخادم يعمل مسبقاً: ${URL}"
    open_hint
    return 0
  fi

  mkdir -p "$LOG_DIR"

  # uname -s يعيد Linux على Termux؛ المنصّة الحقيقية في uname -o
  _os="$(uname -o 2>/dev/null || uname -s 2>/dev/null || echo unknown)"
  say "المنصّة : ${_os}"
  if is_termux; then dim "النمط  : Termux — الوظائف التي تحتاج متصفحًاليفتّل برسالة واضحة"; fi
  say "الرابط  : ${URL}"
  dim   "السجل  : ${LOG_FILE}"
  say
  dim   "اضغط Ctrl+C للإيقاف."
  say

  # تمرير أي خيارات إضافية إلى main.py (مثال: ./run.sh -- --headless)
  EXTRA=""
  if [ "${1:-}" = "--" ]; then shift; EXTRA="$*"; fi

  set +e
  # panel = اللوحة فقط (افتراضي) · cli = الطرفية الكاملة داخل Termux
  _mode_flag="--panel-only"
  [ "${RUN_MODE:-panel}" = "cli" ] && _mode_flag=""
  # shellcheck disable=SC2086
  "$PYTHON" "$APP_DIR/main.py" $_mode_flag --no-color $EXTRA 2>&1 | tee -a "$LOG_FILE"
  # $? هنا حالة tee وليست حالة python — نلتقط حالة الطرف الأول من الأنبوب
  rc=${PIPESTATUS[0]:-0}

  say
  if [ "$rc" -eq 0 ]; then ok "انتهى التشغيل."
  else bad "خرج بشفرة $rc — راجع ${LOG_FILE}"; fi
  return "$rc"
}

open_hint() {
  if is_termux && command -v termux-open-url >/dev/null 2>&1; then
    printf '%s' "$c_hi"
    printf 'افتح الرابط الآن في متصفح الهاتف؟ [y/N] '
    printf '%s' "$c_off"
    read -r ans || ans="n"
    case "$ans" in
      [yY]|[yY][eE][sE]|[ن][ع][م]) termux-open-url "$URL" 2>/dev/null && return ;;
    esac
  fi
  dim "افتح الرابط في متصفحك: ${URL}"
}

# ── نقطة الدخول ─────────────────────────────────────────────
MODE="${1:-}"

case "$MODE" in
  --install|-i)  do_install ;;
  --status|-s)   do_status ;;
  --stop)        do_stop ;;
  --cli)         RUN_MODE="cli"; do_run ;;
  --help|-h)
    sed -n '2,22p' "$0" | sed 's/^# \{0,1\}//'
    ;;
  "")            do_run ;;
  --)            do_run "$@" ;;
  *)
    bad "خيار غير معروف: $MODE"; dim "جرّب: --install | --status | --stop | --cli | --help"; exit 2 ;;
esac
