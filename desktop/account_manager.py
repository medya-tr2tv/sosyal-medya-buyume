# -*- coding: utf-8 -*-
"""Sosyal Hesap Yöneticisi: kişisel tarayıcı profilleri ve MANUEL işlem kaydı.

Windows + Python 3.10 veya üzeri. Üçüncü taraf Python paketi gerekmez.
Program şifre, SMS kodu veya çerez toplamaz. Hesaplar tarayıcıların
ayrı user-data-dir profillerinde oturum açabilir. Etkileşimler elle işaretlenir.
Ölçülen süre SADECE başlat/durdur zamanlayıcısıdır; doğrulanmış video izleme değildir.
"""
from __future__ import annotations

import json
import os
import shutil
import subprocess
import time
import uuid
from datetime import datetime
from pathlib import Path
from tkinter import Tk, BooleanVar, StringVar, messagebox, ttk
from urllib.parse import urlparse
import tkinter as tk

APP_DIR = Path(os.environ.get("LOCALAPPDATA") or str(Path.home())) / "SosyalHesapYonetimi"
INDEX = APP_DIR / "veriler.json"
PROFILES = APP_DIR / "tarayici_profilleri"
PLATFORMS = {
    "YouTube": ("youtube.com", "youtu.be"),
    "Instagram": ("instagram.com",),
    "TikTok": ("tiktok.com",),
    "Facebook": ("facebook.com", "fb.watch"),
}
HOMES = {
    "YouTube": "https://www.youtube.com/",
    "Instagram": "https://www.instagram.com/",
    "TikTok": "https://www.tiktok.com/",
    "Facebook": "https://www.facebook.com/",
}


def platform_of(value: str) -> str | None:
    try:
        parsed = urlparse(value.strip())
        if parsed.scheme not in ("http", "https") or not parsed.hostname:
            return None
        host = parsed.hostname.lower()
        for name, domains in PLATFORMS.items():
            if any(host == d or host.endswith("." + d) for d in domains):
                return name
    except ValueError:
        pass
    return None


def browser_executables() -> dict[str, str | None]:
    roots = [
        Path(os.environ.get("PROGRAMFILES", "C:/Program Files")),
        Path(os.environ.get("PROGRAMFILES(X86)", "C:/Program Files (x86)")),
        Path(os.environ.get("LOCALAPPDATA", str(Path.home()))),
    ]
    result = {}
    for label, parts, filename in (
        ("Microsoft Edge", ("Microsoft", "Edge", "Application", "msedge.exe"), "msedge.exe"),
        ("Google Chrome", ("Google", "Chrome", "Application", "chrome.exe"), "chrome.exe"),
    ):
        found = shutil.which(filename)
        paths = ([Path(found)] if found else []) + [root.joinpath(*parts) for root in roots]
        result[label] = next((str(p) for p in paths if p.is_file()), None)
    return result


def load_data() -> dict:
    try:
        data = json.loads(INDEX.read_text(encoding="utf-8"))
        if not isinstance(data, dict):
            raise ValueError("Not object")
        accounts = data.get("accounts", [])
        records = data.get("records", [])
        if not isinstance(accounts, list) or not isinstance(records, list):
            raise ValueError("Not arrays")
        clean_accounts = []
        for a in accounts:
            if not isinstance(a, dict):
                continue
            ident = a.get("id")
            name = a.get("name")
            platform = a.get("platform")
            if (isinstance(ident, str) and len(ident) == 32
                    and all(c in "0123456789abcdef" for c in ident)
                    and isinstance(name, str) and platform in PLATFORMS):
                clean_accounts.append({
                    "id": ident, "name": name[:120], "platform": platform,
                    "email": str(a.get("email", ""))[:200],
                    "profile_url": str(a.get("profile_url", ""))[:1600],
                })
        clean_records = []
        for r in records:
            if not isinstance(r, dict):
                continue
            if (isinstance(r.get("account_id"), str) and isinstance(r.get("url"), str)
                    and platform_of(r["url"]) and isinstance(r.get("seconds", 0), (int, float))):
                clean_records.append({
                    "account_id": r["account_id"], "url": r["url"][:2000],
                    "seconds": max(0, int(r.get("seconds", 0))),
                    "liked": bool(r.get("liked", False)),
                    "commented": bool(r.get("commented", False)),
                    "followed": bool(r.get("followed", False)),
                    "updated": str(r.get("updated", ""))[:40],
                })
        return {"accounts": clean_accounts, "records": clean_records}
    except (OSError, ValueError, TypeError, OverflowError):
        return {"accounts": [], "records": []}


def save_data(data: dict) -> None:
    APP_DIR.mkdir(parents=True, exist_ok=True)
    temp = INDEX.with_suffix(".tmp")
    temp.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    temp.replace(INDEX)


def as_minutes(seconds: int) -> str:
    minutes, secs = divmod(max(0, int(seconds)), 60)
    return f"{minutes} dk {secs:02d} sn"


class Manager:
    def __init__(self, root: Tk):
        self.root = root
        self.root.title("Sosyal Hesap Yönetimi - Windows")
        self.root.geometry("1100x760")
        self.root.minsize(850, 600)

        self.data = load_data()
        self.browsers = browser_executables()
        available = [name for name, path in self.browsers.items() if path]
        self.browser = StringVar(value=available[0] if available else "Microsoft Edge")
        self.platform = StringVar(value="Instagram")
        self.account_name = StringVar()
        self.account_email = StringVar()
        self.profile_url = StringVar()
        self.permission = BooleanVar(value=False)
        self.link = StringVar()
        self.watch_message = StringVar(value="Süre ölçer kapalı.")
        self.status = StringVar(value="Hazır. Giriş yalnızca platformun kendi sayfasında yapılır.")
        self.timer_context = None
        self.timer_start = None

        self.build_ui()
        self.render_accounts()
        self.render_records()
        self.root.protocol("WM_DELETE_WINDOW", self.close)
        self.tick()

    def build_ui(self):
        outer = ttk.Frame(self.root, padding=15)
        outer.pack(fill="both", expand=True)
        ttk.Label(outer, text="Çoklu Hesap ve Bağlantı Yöneticisi",
                  font=("Segoe UI", 17, "bold")).pack(anchor="w")
        ttk.Label(outer, text=(
            "YouTube / Instagram / TikTok / Facebook • Her hesap için ayrı Chrome/Edge profili. "
            "Platform girişini tarayıcıda yaparsın; program şifre veya SMS kodu toplamaz."
        ), wraplength=1000).pack(anchor="w", pady=(3, 12))

        row = ttk.Frame(outer)
        row.pack(fill="x", pady=(0, 12))
        ttk.Label(row, text="Tarayıcı").pack(side="left", padx=(0, 8))
        ttk.Combobox(row, textvariable=self.browser, state="readonly",
                     values=list(self.browsers.keys()), width=22).pack(side="left")
        ttk.Label(row, text="Giriş doğrulaması gerekiyorsa platform yeniden isteyebilir.",
                  foreground="#596c85").pack(side="left", padx=14)

        paned = ttk.Panedwindow(outer, orient="horizontal")
        paned.pack(fill="both", expand=True)
        left = ttk.Frame(paned, padding=(6, 4))
        right = ttk.Frame(paned, padding=(12, 4))
        paned.add(left, weight=2)
        paned.add(right, weight=3)

        ttk.Label(left, text="1. Hesap ekle", font=("Segoe UI", 12, "bold")).pack(anchor="w")
        self.field(left, "Platform", ttk.Combobox(left, state="readonly",
                  values=list(PLATFORMS.keys()), textvariable=self.platform))
        self.field(left, "Hesap adı (etiket)", ttk.Entry(left, textvariable=self.account_name))
        self.field(left, "E-posta / kullanıcı adı (isteğe bağlı, şifre değil)",
                   ttk.Entry(left, textvariable=self.account_email))
        self.field(left, "Profil bağlantısı (isteğe bağlı)",
                   ttk.Entry(left, textvariable=self.profile_url))
        ttk.Checkbutton(left, text="Hesap benim veya hesap sahibinin açık izni var.",
                        variable=self.permission).pack(anchor="w", pady=12)
        ttk.Button(left, text="Hesabı ekle", command=self.add_account).pack(fill="x")
        ttk.Separator(left).pack(fill="x", pady=12)
        ttk.Label(left, text="Oturumu hatırla / tek tıkla aç",
                  font=("Segoe UI", 11, "bold")).pack(anchor="w", pady=(0, 4))
        ttk.Label(left, text=(
            "İlk girişte platformdaki hesap doğrulamasını tamamla. "
            "Sonrasında 'Tarayıcı profilini aç' aynı hesaba ayrılmış profili kullanır. "
            "Tarayıcının kendi parola yöneticisi şifreyi hatırlayabilir. "
            "Bu program platformun SMS veya güvenlik kontrolünü kapatamaz."
        ), wraplength=340).pack(anchor="w")

        ttk.Label(right, text="2. Hesap seç ve işlem aç",
                  font=("Segoe UI", 12, "bold")).pack(anchor="w")
        frame = ttk.Frame(right)
        frame.pack(fill="both", expand=True, pady=(8, 6))
        self.accounts_table = ttk.Treeview(
            frame, columns=("platform", "account"), show="headings",
            height=9, selectmode="browse"
        )
        self.accounts_table.heading("platform", text="Platform")
        self.accounts_table.heading("account", text="Kayıtlı hesap")
        self.accounts_table.column("platform", width=120, stretch=False)
        self.accounts_table.column("account", width=240)
        self.accounts_table.pack(side="left", fill="both", expand=True)
        scroll = ttk.Scrollbar(frame, command=self.accounts_table.yview)
        scroll.pack(side="right", fill="y")
        self.accounts_table.configure(yscrollcommand=scroll.set)
        self.accounts_table.bind("<<TreeviewSelect>>", lambda e: self.render_records())

        buttons = ttk.Frame(right)
        buttons.pack(fill="x", pady=5)
        ttk.Button(buttons, text="Tarayıcı profilini aç",
                   command=self.open_home).pack(side="left", padx=(0, 7))
        ttk.Button(buttons, text="Hesap kaydını kaldır",
                   command=self.remove_account).pack(side="left")
        self.field(right, "Gönderi/video bağlantısı (aynı hesabın platformundan)",
                   ttk.Entry(right, textvariable=self.link))

        actions = ttk.Frame(right)
        actions.pack(fill="x", pady=(7, 8))
        ttk.Button(actions, text="Gönderiyi seçili hesapta aç",
                   command=self.open_link).pack(side="left", padx=(0, 8))
        ttk.Button(actions, text="Süre ölçümünü başlat",
                   command=self.start_timer).pack(side="left", padx=(0, 8))
        ttk.Button(actions, text="Durdur ve kaydet",
                   command=self.stop_timer).pack(side="left")

        ttk.Label(right, textvariable=self.watch_message, foreground="#395b8b").pack(anchor="w")
        ttk.Label(right, text=(
            "Süre ölçer yalnızca senin başlat/durdur aralığını kaydeder. "
            "Videonun gerçekten oynatıldığını veya platformda izlenme sayıldığını doğrulamaz."
        ), wraplength=620).pack(anchor="w", pady=(3, 10))

        ttk.Label(right, text="3. Bu hesap + bağlantı için elle kaydedilen işlemler",
                  font=("Segoe UI", 11, "bold")).pack(anchor="w", pady=(4, 6))
        manual_buttons = ttk.Frame(right)
        manual_buttons.pack(fill="x")
        ttk.Button(manual_buttons, text="Beğendim / Geri al",
                   command=lambda: self.toggle("liked")).pack(side="left", padx=(0, 6))
        ttk.Button(manual_buttons, text="Yorum yaptım / Geri al",
                   command=lambda: self.toggle("commented")).pack(side="left", padx=(0, 6))
        ttk.Button(manual_buttons, text="Takip ettim / Geri al",
                   command=lambda: self.toggle("followed")).pack(side="left")

        lower = ttk.LabelFrame(outer, text="Hesap bazında sayaç — seçili bağlantı", padding=8)
        lower.pack(fill="both", expand=True, pady=(12, 0))
        self.records_table = ttk.Treeview(
            lower, columns=("name", "platform", "seconds", "like", "comment", "follow"),
            show="headings", height=6
        )
        for key, label, width in [
            ("name", "Hesap", 240), ("platform", "Platform", 100),
            ("seconds", "Ölçülen süre", 150), ("like", "Beğeni işareti", 120),
            ("comment", "Yorum işareti", 120), ("follow", "Takip işareti", 120),
        ]:
            self.records_table.heading(key, text=label)
            self.records_table.column(key, width=width)
        self.records_table.pack(fill="both", expand=True)
        ttk.Label(outer, text=(
            "Bu sayaçlar kullanıcının manuel işaretleri ve zamanlayıcı kayıtlarıdır; "
            "YouTube/TikTok/Instagram/Facebook'tan doğrulanmış etkileşim istatistiği değildir."
        ), foreground="#5b6575").pack(anchor="w", pady=(6, 2))
        ttk.Label(outer, textvariable=self.status).pack(anchor="w")

    @staticmethod
    def field(parent, label, control):
        ttk.Label(parent, text=label).pack(anchor="w", pady=(9, 3))
        control.pack(fill="x")

    def add_account(self):
        name = self.account_name.get().strip()
        url = self.profile_url.get().strip()
        platform = self.platform.get()
        if not name or not self.permission.get():
            messagebox.showwarning("Eksik bilgi", "Hesap adı ve hesap sahibinin izin onayı gerekiyor.")
            return
        if url and platform_of(url) != platform:
            messagebox.showwarning("Bağlantı", "Profil bağlantısı seçilen platforma ait olmalı.")
            return
        account = {
            "id": uuid.uuid4().hex, "name": name[:120], "platform": platform,
            "email": self.account_email.get().strip()[:200], "profile_url": url[:1600],
        }
        self.data["accounts"].append(account)
        save_data(self.data)
        self.account_name.set("")
        self.account_email.set("")
        self.profile_url.set("")
        self.permission.set(False)
        self.render_accounts()
        self.accounts_table.selection_set(account["id"])
        self.accounts_table.focus(account["id"])
        self.status.set("Hesap eklendi. Giriş yapmak için 'Tarayıcı profilini aç' düğmesini kullan.")

    def selection(self):
        rows = self.accounts_table.selection()
        if not rows:
            messagebox.showinfo("Hesap seç", "Önce listeden bir hesap seç.")
            return None
        return next((a for a in self.data["accounts"] if a["id"] == rows[0]), None)

    def remove_account(self):
        account = self.selection()
        if not account:
            return
        if not messagebox.askyesno(
            "Kayıt kaldır",
            "Bu hesap listeden kaldırılsın mı?\nTarayıcı profili ve oturum verileri güvenlik nedeniyle "
            "diskten otomatik silinmez."
        ):
            return
        self.data["accounts"] = [a for a in self.data["accounts"] if a["id"] != account["id"]]
        save_data(self.data)
        self.render_accounts()
        self.render_records()
        self.status.set("Hesap kaydı kaldırıldı; disk üzerindeki tarayıcı profili korunuyor.")

    def open_browser(self, account, url):
        path = self.browsers.get(self.browser.get())
        if not path:
            messagebox.showerror("Tarayıcı yok", "Chrome veya Edge kurulu olmalı.")
            return
        directory = PROFILES / account["id"]
        directory.mkdir(parents=True, exist_ok=True)
        try:
            subprocess.Popen(
                [path, "--user-data-dir=" + str(directory), "--no-first-run", url],
                shell=False, close_fds=True
            )
            self.status.set(
                account["name"] + " için ayrı tarayıcı profili açıldı. "
                "Platform tekrar güvenlik doğrulaması isteyebilir."
            )
        except OSError as exc:
            messagebox.showerror("Açma hatası", str(exc))

    def open_home(self):
        account = self.selection()
        if account:
            self.open_browser(account, account["profile_url"] or HOMES[account["platform"]])

    def target(self):
        account = self.selection()
        if not account:
            return None
        url = self.link.get().strip()
        if platform_of(url) != account["platform"]:
            messagebox.showwarning(
                "Platform uyuşmuyor",
                "Gönderi bağlantısı, seçili hesabın platformuyla aynı olmalı."
            )
            return None
        return account, url

    def open_link(self):
        info = self.target()
        if info:
            self.open_browser(*info)

    def record(self, account_id, url, create=False):
        item = next(
            (r for r in self.data["records"]
             if r["account_id"] == account_id and r["url"] == url),
            None
        )
        if not item and create:
            item = {
                "account_id": account_id, "url": url, "seconds": 0,
                "liked": False, "commented": False, "followed": False, "updated": ""
            }
            self.data["records"].append(item)
        return item

    def toggle(self, key):
        info = self.target()
        if not info:
            return
        account, url = info
        item = self.record(account["id"], url, True)
        item[key] = not item[key]
        item["updated"] = datetime.now().isoformat(timespec="seconds")
        save_data(self.data)
        self.render_records()
        self.status.set("İşaret kaydedildi. Platformdaki işlemin gerçekleştiği otomatik doğrulanmadı.")

    def start_timer(self):
        if self.timer_context is not None:
            messagebox.showinfo("Zamanlayıcı çalışıyor", "Önce mevcut süre ölçümünü durdur.")
            return
        info = self.target()
        if not info:
            return
        account, url = info
        self.timer_context = (account["id"], url)
        self.timer_start = time.monotonic()
        self.status.set("Elle süre ölçümü başladı. Video oynatma durumuna erişim yok.")

    def stop_timer(self):
        if self.timer_context is None:
            messagebox.showinfo("Zamanlayıcı", "Önce süre ölçümünü başlat.")
            return
        elapsed = max(0, round(time.monotonic() - self.timer_start))
        account_id, url = self.timer_context
        item = self.record(account_id, url, True)
        item["seconds"] += elapsed
        item["updated"] = datetime.now().isoformat(timespec="seconds")
        self.timer_context = None
        self.timer_start = None
        save_data(self.data)
        self.watch_message.set("Kaydedildi: " + as_minutes(elapsed) + " (manuel ölçüm).")
        self.render_records()
        self.status.set("Ölçüm kaydedildi. Bu süre, doğrulanmış video izlenmesi değildir.")

    def tick(self):
        if self.timer_context is not None:
            elapsed = max(0, round(time.monotonic() - self.timer_start))
            self.watch_message.set("Süre ölçer: " + as_minutes(elapsed) + " — gerçek izleme doğrulanmıyor.")
        self.root.after(1000, self.tick)

    def render_accounts(self):
        for iid in self.accounts_table.get_children():
            self.accounts_table.delete(iid)
        for account in self.data["accounts"]:
            self.accounts_table.insert(
                "", "end", iid=account["id"],
                values=(account["platform"], account["name"])
            )

    def render_records(self):
        for iid in self.records_table.get_children():
            self.records_table.delete(iid)
        target_url = self.link.get().strip()
        for a in self.data["accounts"]:
            item = self.record(a["id"], target_url) if platform_of(target_url) else None
            self.records_table.insert(
                "", "end", values=(
                    a["name"], a["platform"],
                    as_minutes(item["seconds"]) if item else "—",
                    "İşaretli" if item and item["liked"] else "—",
                    "İşaretli" if item and item["commented"] else "—",
                    "İşaretli" if item and item["followed"] else "—",
                )
            )

    def close(self):
        if self.timer_context is not None:
            if not messagebox.askyesno(
                "Süre ölçer çalışıyor",
                "Süre ölçümü devam ediyor. Kaydedip uygulamadan çıkılsın mı?"
            ):
                return
            self.stop_timer()
        self.root.destroy()


if __name__ == "__main__":
    root = Tk()
    app = Manager(root)
    app.link.trace_add("write", lambda *_: app.render_records())
    root.mainloop()
