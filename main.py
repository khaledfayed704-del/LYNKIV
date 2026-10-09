# -*- coding: utf-8 -*-
#  LYNIKV TOOL Qr — محمّل الحزمة المشفّرة (مولّد آلياً · لا تُعدّله)
#  الطبع والحقوق: Lynox & Kivix
import gzip
import hashlib
import hmac
import importlib.util
import io
import json
import os
import sys
import tarfile

sys.dont_write_bytecode = True

_HERE = os.path.dirname(os.path.abspath(__file__))
_LOADER = os.path.abspath(__file__)


def _xor(a, b):
    return bytes(x ^ y for x, y in zip(a, b))


_KEY = _xor(bytes([113,167,198,210,154,234,79,106,218,75,29,254,52,247,57,53,115,201,161,173,143,182,100,6,98,3,202,103,212,160,112,224]), bytes([138,11,142,220,28,244,49,172,199,161,236,172,196,163,149,33,145,124,233,71,210,206,238,65,176,163,175,196,173,91,225,232]))
_DAT = _xor(bytes([197,85,87,95,180,201,53,29,105,10,134]), bytes([154,57,46,49,221,162,67,51,13,107,242])).decode("latin-1")
_MAGIC = _xor(bytes([249,136,104,226,187,184,120,134]), bytes([181,198,62,169,254,246,59,183]))
_OWNER = _xor(bytes([116,21,65,161,230,51,179,154,59,127,249,185,168]), bytes([56,108,47,206,158,19,149,186,112,22,143,208,208])).decode("utf-8")

_MEM = {}


def _key(path):
    return os.path.normcase(os.path.realpath(os.fspath(path)))


def _load_mem(tar, manifest):
    for rel, sha in manifest.get("mem", {}).items():
        member = tar.extractfile(rel)
        if member is None:
            _fail("الحزمة ناقصة: {}".format(rel))
        blob = member.read()
        if hashlib.sha256(blob).hexdigest() != sha:
            _fail("تعذّر التحقق من: {}".format(rel))
        _MEM[_key(os.path.join(_HERE, *rel.split("/")))] = blob


def _install_fs_guard():
    import builtins
    import pathlib

    real_text = pathlib.Path.read_text
    real_bytes = pathlib.Path.read_bytes
    real_is_file = pathlib.Path.is_file
    real_exists = pathlib.Path.exists
    real_open = builtins.open

    def _hit(path):
        return _MEM.get(_key(path))

    def read_text(self, *args, **kwargs):
        blob = _hit(self)
        if blob is None:
            return real_text(self, *args, **kwargs)
        encoding = kwargs.get("encoding") or (args[0] if args else None) or "utf-8"
        errors = kwargs.get("errors") or (args[1] if len(args) > 1 else None) or "strict"
        return blob.decode(encoding, errors)

    def read_bytes(self):
        blob = _hit(self)
        return blob if blob is not None else real_bytes(self)

    def is_file(self):
        return True if _hit(self) is not None else real_is_file(self)

    def exists(self):
        return True if _hit(self) is not None else real_exists(self)

    def opener(file, mode="r", *args, **kwargs):
        blob = None
        if isinstance(file, (str, bytes, os.PathLike)):
            blob = _hit(file)
        if blob is None:
            return real_open(file, mode, *args, **kwargs)
        if "b" in mode:
            return io.BytesIO(blob)
        encoding = kwargs.get("encoding") or (args[0] if args else None) or "utf-8"
        errors = kwargs.get("errors") or (args[1] if len(args) > 1 else None) or "strict"
        return io.StringIO(blob.decode(encoding, errors))

    pathlib.Path.read_text = read_text
    pathlib.Path.read_bytes = read_bytes
    pathlib.Path.is_file = is_file
    pathlib.Path.exists = exists
    builtins.open = opener


def _fail(msg, code=1):
    text = "[LYNIKV] " + str(msg) + "\n"
    try:
        sys.stderr.write(text)
    except Exception:
        try:
            sys.stderr.buffer.write(text.encode("utf-8", "replace"))
        except Exception:
            pass
    raise SystemExit(code)


def _decrypt(raw):
    if len(raw) < 72 or raw[:8] != _MAGIC:
        _fail("الحزمة المشفّرة مفقودة أو غير صالحة.")
    salt, nonce, tag, ct = raw[8:24], raw[24:40], raw[40:72], raw[72:]
    ek = hmac.new(_KEY, b"LNVK|enc|" + salt, hashlib.sha256).digest()
    mk = hmac.new(_KEY, b"LNVK|mac|" + salt, hashlib.sha256).digest()
    expect = hmac.new(mk, raw[:40] + ct, hashlib.sha256).digest()
    if not hmac.compare_digest(tag, expect):
        _fail("فشل التحقق من سلامة الحزمة — عُدّل الملف أو تلف.")
    out = bytearray(len(ct))
    ctr = 0
    i = 0
    while i < len(ct):
        block = hmac.new(ek, nonce + ctr.to_bytes(4, "big"), hashlib.sha256).digest()
        for j, byte in enumerate(ct[i:i + 32]):
            out[i + j] = byte ^ block[j]
        i += 32
        ctr += 1
    try:
        return gzip.decompress(bytes(out))
    except Exception:
        _fail("تعذّر فك ضغط الحزمة.")


class _Loader:
    def __init__(self, name, src, path, pkg):
        self.name = name
        self.src = src
        self.path = path
        self.pkg = pkg

    def create_module(self, spec):
        return None

    def exec_module(self, module):
        module.__file__ = self.path
        if self.pkg:
            module.__path__ = []
        code = compile(self.src, self.path, "exec", dont_inherit=True)
        exec(code, module.__dict__)

    def is_package(self, name):
        return self.pkg

    def get_source(self, name):
        return self.src.decode("utf-8")

    def get_code(self, name):
        return compile(self.src, self.path, "exec", dont_inherit=True)

    def get_filename(self, name):
        return self.path


class _Finder:
    def __init__(self, mods):
        self.mods = mods

    def find_spec(self, fullname, path=None, target=None):
        entry = self.mods.get(fullname)
        if entry is None:
            return None
        src, filename, pkg = entry
        spec = importlib.util.spec_from_loader(
            fullname, _Loader(fullname, src, filename, pkg),
            origin=filename, is_package=pkg)
        if pkg:
            spec.submodule_search_locations = []
        return spec


def _sync_data(tar, manifest):
    for rel, sha in manifest.get("data", {}).items():
        dest = os.path.join(_HERE, *rel.split("/"))
        fresh = False
        try:
            with open(dest, "rb") as fh:
                fresh = hashlib.sha256(fh.read()).hexdigest() == sha
        except OSError:
            pass
        if fresh:
            continue
        member = tar.extractfile(rel)
        if member is None:
            _fail("الحزمة ناقصة: {}".format(rel))
        blob = member.read()
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        with open(dest, "wb") as fh:
            fh.write(blob)


def _install(tar, manifest):
    mods = {}
    for rel in manifest["code"]:
        member = tar.extractfile(rel)
        if member is None:
            _fail("الحزمة ناقصة: {}".format(rel))
        src = member.read()
        pkg = rel == "__init__.py" or rel.endswith("/__init__.py")
        name = rel[:-3].replace("/", ".")
        if pkg:
            name = name[:-len(".__init__")] or name
        mods[name] = (src, os.path.join(_HERE, *rel.split("/")), pkg)
    sys.meta_path.insert(0, _Finder(mods))
    return mods


def _selftest(manifest, tar):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
    failed = []
    try:
        import main  # noqa: F401
    except Exception as exc:
        failed.append("import main -> {!r}".format(exc))
    try:
        from core.inspect_map import build_map
        result = build_map()
        if not result.get("tools"):
            failed.append("build_map فارغ")
        else:
            good = sum(1 for row in result["tools"]
                       if row["handler"]["symbol"] != "(غير موجود)" and row["handler"]["line"] > 0)
            print("[✓] خريطة الأدوات: {} أداة · {} بمواضع مصدرية صحيحة".format(
                result["count"], good))
            if result.get("missing"):
                print("[!] أدوات غير موجودة في المنفّذ: {}".format(", ".join(result["missing"])))
    except Exception as exc:
        failed.append("build_map -> {!r}".format(exc))
    for rel, sha in manifest.get("mem", {}).items():
        blob = _MEM.get(_key(os.path.join(_HERE, *rel.split("/"))))
        if blob is None or hashlib.sha256(blob).hexdigest() != sha:
            failed.append("ملف غير محمّل في الذاكرة: {}".format(rel))
    try:
        import core.panel
        sha = manifest.get("mem", {}).get("core/panel.html")
        got = hashlib.sha256(core.panel.PANEL_HTML.encode("utf-8")).hexdigest()
        if not sha or got != sha:
            failed.append("صفحة اللوحة لا تطابق الحزمة المشفّرة")
        else:
            print("[✓] صفحة HTML تُقدَّم من الذاكرة ({:,} حرف) — لا وجود لها على القرص".format(
                len(core.panel.PANEL_HTML)))
    except Exception as exc:
        failed.append("core.panel -> {!r}".format(exc))
    try:
        sha = manifest.get("mem", {}).get("core/banner.txt")
        with open(os.path.join(_HERE, "core", "banner.txt"), "r", encoding="utf-8") as fh:
            text = fh.read()
        if not sha or hashlib.sha256(text.encode("utf-8")).hexdigest() != sha:
            failed.append("banner.txt لا يطابق الحزمة")
        else:
            print("[✓] banner.txt يُقرأ من الذاكرة (اختبار open محمي)")
    except Exception as exc:
        failed.append("banner -> {!r}".format(exc))
    try:
        import pathlib
        sha = manifest.get("mem", {}).get("assets/logo.png")
        logo = pathlib.Path(_HERE) / "assets" / "logo.png"
        if not sha or not logo.is_file() or hashlib.sha256(logo.read_bytes()).hexdigest() != sha:
            failed.append("assets/logo.png لا يطابق الحزمة")
        else:
            print("[✓] الأصول تُقدَّم من الذاكرة (is_file + read_bytes محميان)")
    except Exception as exc:
        failed.append("assets -> {!r}".format(exc))
    bad_data = []
    for rel, sha in manifest.get("data", {}).items():
        try:
            with open(os.path.join(_HERE, *rel.split("/")), "rb") as fh:
                if hashlib.sha256(fh.read()).hexdigest() != sha:
                    bad_data.append(rel)
        except OSError:
            bad_data.append(rel)
    if bad_data:
        failed.append("ملفات بيانات معطوبة: {}".format(", ".join(bad_data)))
    if failed:
        for line in failed:
            print("[✗] " + line)
        return 1
    print("[✓] الاختبار الذاتي نجح — الحزمة المشفّرة تعمل بالكامل")
    return 0


def _verify(manifest):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
    print("[✓] التوقيع رقمي على الحزمة سليم — لم يُمسّ المحتوى")
    print("    الأداة     : {}".format(manifest.get("tool", "")))
    print("    المالك     : {}".format(manifest.get("owner", "")))
    print("    الحقوق     : {}".format(manifest.get("copyright", "")))
    print("    تاريخ البناء: {}".format(manifest.get("built", "")))
    print("    ملفات الشيفرة: {} · ملفات في الذاكرة (بلا وجود على القرص): {}".format(
        len(manifest.get("code", [])), len(manifest.get("mem", {}))))
    return 0


def _run():
    path = os.path.join(_HERE, _DAT)
    try:
        with open(path, "rb") as fh:
            raw = fh.read()
    except OSError:
        _fail("لم يُعثر على الحزمة المشفّرة ({}) بجانب المحمّل.".format(_DAT))
    blob = _decrypt(raw)
    try:
        with tarfile.open(fileobj=io.BytesIO(blob), mode="r:") as tar:
            handle = tar.extractfile("__manifest__.json")
            if handle is None:
                _fail("الحزمة بلا ملف manifest.")
            manifest = json.loads(handle.read().decode("utf-8"))
            if manifest.get("owner") != _OWNER:
                _fail("بيانات مالك الحزمة غير مطابقة للنسخة الأصلية.")
            try:
                with open(_LOADER, "rb") as fh:
                    digest = hashlib.sha256(fh.read()).hexdigest()
            except OSError:
                digest = ""
            if digest != manifest.get("loader_sha256"):
                _fail("ملف المحمّل عُدّل عن نسخة البناء الأصلية.")
            _load_mem(tar, manifest)
            _sync_data(tar, manifest)
            _install(tar, manifest)
            _install_fs_guard()
            argv = sys.argv[1:]
            if argv and argv[0] == "--protect-verify":
                return _verify(manifest)
            if argv and argv[0] == "--protect-selftest":
                return _selftest(manifest, tar)
    except SystemExit:
        raise
    except Exception as exc:
        _fail("تعذّر فتح الحزمة: {!r}".format(exc))
    import main as _app
    return _app.main()


if __name__ == "__main__":
    sys.exit(_run())
