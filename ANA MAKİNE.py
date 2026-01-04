import sys
import os
import math
import random
import time
import datetime
import webbrowser
import winsound
import platform
import socket
import string
import urllib.request
import hashlib
import base64
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext, font, ttk, colorchooser

# Windows Konsolunu UTF-8 Yap
os.system('chcp 65001 >nul')

GUI_UYGULAMA = None 

# --- EXE ICIN DOSYA YOLU BULUCU ---
def resource_path(relative_path):
    """ PyInstaller ile paketlenince gecici klasoru, normalde şu anki klasoru bulur """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# --- MAGAZA LINKLERI ---
REAL_MAGAZA = {
    "NOTEPAD++": "https://github.com/notepad-plus-plus/notepad-plus-plus/releases/download/v8.5.4/npp.8.5.4.Installer.x64.exe",
    "7-ZIP": "https://www.7-zip.org/a/7z2301-x64.exe",
    "PYTHON_LOGO": "https://www.python.org/static/community_logos/python-logo-master-v3-TM.png"
}

# --- YARDIMCI MOTOR FONKSIYONLARI ---
def tda_gercek_indir(url, dosya_adi):
    if GUI_UYGULAMA: GUI_UYGULAMA.yazdir(f">> İNDİRİLİYOR: {url}...")
    try:
        opener = urllib.request.build_opener()
        opener.addheaders = [('User-agent', 'Mozilla/5.0')]
        urllib.request.install_opener(opener)
        urllib.request.urlretrieve(url, dosya_adi)
        if GUI_UYGULAMA: GUI_UYGULAMA.yazdir(f">> BAŞARILI: {dosya_adi} indi!")
        return "Basarili"
    except Exception as e:
        if GUI_UYGULAMA: GUI_UYGULAMA.yazdir(f"HATA: {e}")
        return "Hata"

def tda_sistem_baslat(dosya_adi):
    if os.path.exists(dosya_adi):
        try: os.startfile(dosya_adi); return "Acildi"
        except OSError as e:
            if e.winerror == 1223: return "Iptal"
            return "Hata"
    return "Dosya Yok"

# --- 50+ OZELLIK KUTUPHANESI ---
TDA_EVREN = {
    # 1. KRYPTO / SIFRELEME
    'md5': lambda x: hashlib.md5(str(x).encode()).hexdigest(),
    'sha256': lambda x: hashlib.sha256(str(x).encode()).hexdigest(),
    'b64_kodla': lambda x: base64.b64encode(str(x).encode()).decode(),
    'b64_coz': lambda x: base64.b64decode(str(x).encode()).decode(),

    # 2. DOSYA ISLEMLERI
    'kopyala': lambda k, h: shutil.copy(k, h),
    'tasi': lambda k, h: shutil.move(k, h),
    'yeniden_adlandir': lambda e, y: os.rename(e, y),
    'uzanti_al': lambda x: os.path.splitext(x)[1],
    'klasor_sil': lambda x: shutil.rmtree(x, ignore_errors=True),
    'dosya_oku': lambda x: open(x, 'r', encoding='utf-8').read() if os.path.exists(x) else "Yok",
    
    # 3. MATEMATIK
    'faktoriyel': math.factorial, 'ebob': math.gcd, 'ekok': math.lcm,
    'log': math.log10, 'derece': math.degrees, 'radyan': math.radians, 'mod': lambda x,y: x%y,
    'topla': sum, 'cikar': lambda x,y: x-y, 'carp': lambda x,y: x*y, 'bol': lambda x,y: x/y,
    'kare': lambda x: x*x, 'kup': lambda x: x*x*x, 'kok': math.sqrt, 'mutlak': abs, 'yuvarla': round, 'pi': math.pi, 'rastgele': random.randint,

    # 4. SISTEM / EKRAN
    'ekran_en': lambda: GUI_UYGULAMA.root.winfo_screenwidth(),
    'ekran_boy': lambda: GUI_UYGULAMA.root.winfo_screenheight(),
    'mouse_x': lambda: GUI_UYGULAMA.root.winfo_pointerx(),
    'mouse_y': lambda: GUI_UYGULAMA.root.winfo_pointery(),
    
    # 5. METIN ANALIZ
    'sayi_mi': lambda x: str(x).isdigit(), 'harf_mi': lambda x: str(x).isalpha(),
    'kac_tane': lambda x, y: str(x).count(y), 'parcala': lambda x, y: str(x).split(y),
    'ascii_kod': ord, 'karakter': chr,
    'buyuk': lambda x: str(x).upper(), 'kucuk': lambda x: str(x).lower(), 'ters': lambda x: str(x)[::-1], 'kirp': lambda x: str(x).strip(),
    'uzunluk': len, 'birlestir': lambda x,y: str(x)+str(y), 'degistir': lambda x,y,z: str(x).replace(y,z), 'bul': lambda x,y: str(x).find(y),

    # DIGERLERI
    'web_indir': tda_gercek_indir, 'sistem_ac': tda_sistem_baslat,
    'bilgisayar': platform.node, 'kullanici': os.getlogin, 'isletim_sis': platform.system, 'islemci': platform.processor,
    'dizin': os.getcwd, 'dosyalar': lambda: str(os.listdir(os.getcwd())),
    'simdi': lambda: datetime.datetime.now().strftime("%d.%m.%Y %H:%M"),
    'dosya_varmi': os.path.exists, 'dosya_sil': lambda x: os.remove(x) if os.path.exists(x) else "Yok",
    'klasor_ac': lambda x: os.mkdir(x), 'boyut': lambda x: os.path.getsize(x) if os.path.exists(x) else 0,
    'google': lambda: webbrowser.open("www.google.com"), 'site_ac': lambda x: webbrowser.open(x), 'ip_adresim': lambda: socket.gethostbyname(socket.gethostname()),
    'renk_sec': lambda: colorchooser.askcolor()[1], 'uyari': lambda x: messagebox.showwarning("TDA", str(x)),
    'bekle': time.sleep, 'tip': lambda x: type(x).__name__
}

# --- KOMUT ISLEYICI ---
def komut_calistir(satir, hafiza):
    satir = satir.strip()
    if not satir or satir.startswith("#"): return

    if satir.startswith("web_indir "):
        try:
            p = satir[10:].split(" ", 1)
            tda_gercek_indir(p[0].strip('"'), p[1].strip('"'))
        except: pass
        return

    if satir.startswith("sistem_ac "):
        tda_sistem_baslat(satir[10:].strip().strip('"'))
        return

    if satir == "temizle": 
        if GUI_UYGULAMA: GUI_UYGULAMA.ekrani_temizle()
        return
    
    if satir == "cikis": sys.exit()

    if satir.startswith("yaz "):
        ifade = satir[4:].strip()
        baglam = hafiza.copy()
        baglam.update(TDA_EVREN)
        try: 
            sonuc = eval(ifade, {}, baglam)
            if GUI_UYGULAMA: GUI_UYGULAMA.yazdir(sonuc)
        except: 
            if GUI_UYGULAMA: GUI_UYGULAMA.yazdir(ifade.strip('"'))
        return

    if " sor " in satir:
        try:
            p = satir.split(" sor ")
            degisken, soru = p[0].strip(), p[1].strip().strip('"')
            if GUI_UYGULAMA: 
                # BURADA ARTIK POPUP YOK, GUI_UYGULAMA.veri_al KULLANILIYOR
                cevap = GUI_UYGULAMA.veri_al(soru)
                if cevap.isdigit(): hafiza[degisken] = int(cevap)
                else: hafiza[degisken] = cevap
                GUI_UYGULAMA.ram_guncelle(hafiza)
        except: pass
        return

    if " olsun " in satir:
        try:
            p = satir.split(" olsun ")
            var, val = p[0].strip(), p[1].strip()
            baglam = hafiza.copy()
            baglam.update(TDA_EVREN)
            try: hafiza[var] = eval(val, {}, baglam)
            except: 
                try: 
                    baglam_str = {k: str(v) for k, v in baglam.items()}
                    hafiza[var] = eval(val, {}, baglam_str)
                except: hafiza[var] = val.strip('"')
            if GUI_UYGULAMA: GUI_UYGULAMA.ram_guncelle(hafiza)
        except: pass
        return

    if satir.startswith("eger "):
        try:
            k, i = satir[5:].split(" ise ")
            baglam = hafiza.copy()
            baglam.update(TDA_EVREN)
            if eval(k, {}, baglam): komut_calistir(i, hafiza)
        except: pass
        return

    if satir.startswith("tekrarla "):
        try:
            kalan = satir[9:] 
            adet, komut = kalan.split(" kez: ")
            for i in range(int(eval(adet, {}, hafiza))): komut_calistir(komut, hafiza)
        except: pass
        return

# --- TDA STUDIO V1.0 ARAYUZU ---
class TDA_System:
    def __init__(self, root):
        self.root = root
        self.root.title("TDA Studio V1.0")
        self.root.geometry("1400x900")
        
        # --- ICON AYARI (HATA VERIRSE GEC) ---
        try:
            icon_path = resource_path("tda_icon.ico")
            self.root.iconbitmap(icon_path)
        except:
            pass

        self.tema_renkleri = {"bg": "#1e1e1e", "fg": "#e0e0e0", "editor": "#1e1e1e", "komut": "#569CD6"}
        self.root.configure(bg=self.tema_renkleri["bg"])
        self.font_family = "Consolas"
        self.font_size = 12

        style = ttk.Style()
        style.theme_use('clam')
        style.configure("Treeview", background="#1e1e1e", foreground="#ddd", fieldbackground="#1e1e1e", font=("Consolas", 10))
        style.configure("Treeview.Heading", background="#333", foreground="white", font=("Arial", 9, "bold"))

        # --- MENU ---
        menu_bar = tk.Menu(root)
        root.config(menu=menu_bar)
        
        dosya_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Dosya", menu=dosya_menu)
        dosya_menu.add_command(label="Aç (Yükle)", command=self.dosya_ac)
        dosya_menu.add_command(label="Kaydet", command=self.kaydet)
        dosya_menu.add_separator()
        dosya_menu.add_command(label="Çıkış", command=root.quit)

        menu_bar.add_command(label="Hakkında", command=self.hakkinda_goster)

        # --- ANA PANELLER (Sürüklenebilir) ---
        self.main_pane = tk.PanedWindow(root, orient=tk.HORIZONTAL, bg="#121212", sashwidth=8, sashrelief=tk.RAISED)
        self.main_pane.pack(fill=tk.BOTH, expand=True)

        # SOL PANEL (EDITOR)
        self.left_frame = tk.Frame(self.main_pane, bg="#121212")
        self.main_pane.add(self.left_frame, minsize=400, width=800)

        toolbar = tk.Frame(self.left_frame, bg="#2d2d2d", height=40)
        toolbar.pack(fill=tk.X)
        self.btn(toolbar, "▶ ÇALIŞTIR", "#2E7D32", self.calistir)
        self.btn(toolbar, "🧹 TEMİZLE", "#6A1B9A", self.ekrani_temizle)
        self.btn(toolbar, "🛒 MAĞAZA", "#D81B60", self.magaza_ac)
        self.btn(toolbar, "📖 REHBER", "#FF9800", self.rehber_ac)

        self.editor = scrolledtext.ScrolledText(self.left_frame, bg=self.tema_renkleri["editor"], fg=self.tema_renkleri["fg"], 
                                                font=(self.font_family, self.font_size), insertbackground="white", undo=True)
        self.editor.pack(fill=tk.BOTH, expand=True)
        
        self.status_bar = tk.Label(self.left_frame, text="TDA V1.0 Hazır | Tda_45", bg="#222", fg="#888", anchor=tk.W)
        self.status_bar.pack(fill=tk.X)

        # SAG PANEL
        self.right_pane = tk.PanedWindow(orient=tk.VERTICAL, bg="#121212", sashwidth=8, sashrelief=tk.RAISED)
        self.main_pane.add(self.right_pane, minsize=300)

        self.top_right_pane = tk.PanedWindow(orient=tk.HORIZONTAL, bg="#121212", sashwidth=6, sashrelief=tk.RAISED)
        self.right_pane.add(self.top_right_pane, height=400)

        ram_box = tk.Frame(self.top_right_pane, bg="#1f1f1f")
        self.top_right_pane.add(ram_box, minsize=150)
        tk.Label(ram_box, text=" 💾 RAM", bg="#1f1f1f", fg="#03A9F4", font=("Arial", 9, "bold")).pack(anchor=tk.W)
        self.ram_tablo = ttk.Treeview(ram_box, columns=('ad', 'deger'), show='headings')
        self.ram_tablo.heading('ad', text='Değişken'); self.ram_tablo.column('ad', width=80)
        self.ram_tablo.heading('deger', text='Değer'); self.ram_tablo.column('deger', width=100)
        self.ram_tablo.pack(fill=tk.BOTH, expand=True)

        cmd_box = tk.Frame(self.top_right_pane, bg="#1f1f1f")
        self.top_right_pane.add(cmd_box, minsize=150)
        tk.Label(cmd_box, text=" 📚 KOMUTLAR", bg="#1f1f1f", fg="#FFC107", font=("Arial", 9, "bold")).pack(anchor=tk.W)
        self.komut_listesi = ttk.Treeview(cmd_box, columns=('komut'), show='headings')
        self.komut_listesi.heading('komut', text='Komut Listesi (Çift Tıkla)')
        self.komut_listesi.pack(fill=tk.BOTH, expand=True)
        for k in sorted(TDA_EVREN.keys()): self.komut_listesi.insert('', tk.END, values=(k + "()",))
        self.komut_listesi.bind("<Double-1>", self.komut_ekle)

        term_box = tk.Frame(self.right_pane, bg="black")
        self.right_pane.add(term_box, minsize=200)
        tk.Label(term_box, text=" 📟 KONSOL ÇIKTISI", bg="black", fg="#888", font=("Arial", 8)).pack(anchor=tk.W)
        
        self.term = scrolledtext.ScrolledText(term_box, bg="black", fg="#00FF00", font=("Consolas", 11), state=tk.DISABLED)
        self.term.pack(fill=tk.BOTH, expand=True)
        
        # --- INPUT ALANI (ALT TARAFTA) ---
        input_frame = tk.Frame(term_box, bg="#333")
        input_frame.pack(fill=tk.X)
        tk.Label(input_frame, text="VERİ GİRİŞİ >", bg="#333", fg="white", font=("Arial", 10, "bold")).pack(side=tk.LEFT, padx=5)
        self.giris = tk.Entry(input_frame, bg="#222", fg="white", font=("Consolas", 12), insertbackground="white")
        self.giris.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.giris.bind("<Return>", self.input_gonder)
        self.giris.config(state=tk.DISABLED)
        self.input_var = tk.StringVar()

        kod = """# TDA Studio V1.0
yaz "Sistem Baslatildi..."
ad sor "Ismin nedir?"
yaz "Merhaba " + ad
"""
        self.editor.insert(tk.END, kod)
        self.renklendir_tetikle()

        self.root.bind('<F5>', lambda e: self.calistir())
        self.root.bind('<Control-s>', lambda e: self.kaydet())
        self.editor.bind('<KeyRelease>', self.renklendir_tetikle)

    def btn(self, p, t, c, cmd):
        tk.Button(p, text=t, bg=c, fg="white", relief="flat", padx=8, command=cmd).pack(side=tk.LEFT, padx=2, pady=5)

    def hakkinda_goster(self):
        mesaj = "Yapımcı: Tda_45\nSürüm: V1.0\n\nSorun Ve Destek Hattı:\ntdacompanytr@gmail.com\n\nİyi Kodlamalar..."
        messagebox.showinfo("Hakkında - TDA V1.0", mesaj)

    def rehber_ac(self):
        win = tk.Toplevel(self.root)
        win.title("TDA V1.0 Komut Rehberi")
        win.geometry("700x600")
        win.configure(bg="#222")
        t = scrolledtext.ScrolledText(win, bg="#1e1e1e", fg="white", font=("Consolas", 11))
        t.pack(fill=tk.BOTH, expand=True)
        text = "========================================\n"
        text += "   TDA V1.0 KOMUT LİSTESİ VE REHBERİ\n"
        text += "========================================\n\n"
        text += "[TEMEL KOMUTLAR]\n"
        text += "yaz \"Mesaj\"       -> Ekrana yazar.\n"
        text += "sor \"Soru\"        -> Aşağıdaki kutudan veri alır (POPUP YOK).\n"
        text += "olsun             -> Değişken atama (x olsun 5).\n\n"
        text += "[İNTERNET & DOSYA]\n"
        text += "web_indir(url, ad)-> İnternetten dosya indirir.\n"
        text += "sistem_ac(ad)     -> Dosyayı açar.\n"
        text += "kopyala(a, b)     -> Dosya kopyalar.\n\n"
        text += "[TÜM FONKSİYONLAR LİSTESİ]\n"
        komutlar = sorted(TDA_EVREN.keys())
        for k in komutlar: text += f"- {k}()\n"
        t.insert(tk.END, text)
        t.config(state=tk.DISABLED)

    def renklendir_tetikle(self, event=None):
        self.editor.tag_remove("k", "1.0", tk.END)
        self.editor.tag_remove("s", "1.0", tk.END)
        self.editor.tag_remove("f", "1.0", tk.END)
        keywords = ["yaz ", "olsun ", "sor ", "eger ", "tekrarla ", "web_indir ", "sistem_ac ", "dahil_et ", "indir "]
        for w in keywords: self.boya(w, "k", "#569CD6")
        for f in TDA_EVREN.keys(): self.boya(f, "f", "#FFD700")
        s = "1.0"
        while True:
            s = self.editor.search('"', s, stopindex=tk.END)
            if not s: break
            e = self.editor.search('"', f"{s}+1c", stopindex=tk.END)
            if not e: break
            self.editor.tag_add("s", s, f"{e}+1c")
            self.editor.tag_config("s", foreground="#CE9178")
            s = f"{e}+1c"

    def boya(self, w, t, color):
        self.editor.tag_config(t, foreground=color)
        s = "1.0"
        while True:
            s = self.editor.search(w, s, stopindex=tk.END)
            if not s: break
            e = f"{s}+{len(w)}c"
            self.editor.tag_add(t, s, e)
            s = e

    def magaza_ac(self):
        store = tk.Toplevel(self.root)
        store.title("TDA REAL STORE")
        store.geometry("600x450")
        store.configure(bg="#222")
        tk.Label(store, text="☁️ TDA STORE", bg="#222", fg="#D81B60", font=("Arial", 16, "bold")).pack(pady=10)
        liste = tk.Listbox(store, bg="#333", fg="white", font=("Consolas", 11))
        liste.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        for k in REAL_MAGAZA.keys(): liste.insert(tk.END, k)
        def indir():
            sel = liste.get(tk.ANCHOR)
            if sel:
                url = REAL_MAGAZA[sel]
                ext = url.split(".")[-1]
                self.editor.insert(tk.END, f'\nweb_indir "{url}" "{sel.lower()}.{ext}"\nsistem_ac "{sel.lower()}.{ext}"\n')
                store.destroy()
        tk.Button(store, text="İNDİR", command=indir, bg="#4CAF50", fg="white").pack(pady=10)

    def komut_ekle(self, event):
        item = self.komut_listesi.selection()[0]
        val = self.komut_listesi.item(item, "values")[0]
        self.editor.insert(tk.INSERT, val)

    def ram_guncelle(self, h):
        for i in self.ram_tablo.get_children(): self.ram_tablo.delete(i)
        for k, v in h.items(): self.ram_tablo.insert('', tk.END, values=(k, str(v)))

    def calistir(self):
        self.ekrani_temizle()
        k = self.editor.get("1.0", tk.END).strip()
        self.yazdir("--- RUNNING ---")
        h = {}
        self.ram_guncelle(h)
        for s in k.split("\n"):
            komut_calistir(s, h)
            self.root.update()
        self.yazdir("--- STOPPED ---")

    # --- INPUT MEKANIZMASI (ALT TARAFTA) ---
    def veri_al(self, s):
        self.yazdir(s)
        self.yazdir(">> (Aşağıya yaz ve Enter'a bas)")
        
        # Kutuyu aktif et ve odaklan
        self.giris.config(state=tk.NORMAL, bg="#444")
        self.giris.delete(0, tk.END)
        self.giris.focus_set()
        
        # Kullanicinin Enter'a basmasini bekle
        self.input_var.set("WAIT")
        self.root.wait_variable(self.input_var)
        
        # Veriyi al
        v = self.giris.get()
        self.yazdir(f"> {v}")
        
        # Kutuyu temizle ve kapat
        self.giris.delete(0, tk.END)
        self.giris.config(state=tk.DISABLED, bg="#222")
        return v
    
    def input_gonder(self, e): 
        if str(self.giris['state'])=='normal': self.input_var.set("O")

    def yazdir(self, m):
        self.term.config(state=tk.NORMAL); self.term.insert(tk.END, str(m)+"\n"); self.term.see(tk.END); self.term.config(state=tk.DISABLED)
    def ekrani_temizle(self):
        self.term.config(state=tk.NORMAL); self.term.delete('1.0', tk.END); self.term.config(state=tk.DISABLED)
    
    def kaydet(self):
        f = filedialog.asksaveasfilename(defaultextension=".tda", filetypes=[("TDA Dosyası", "*.tda"), ("Tüm Dosyalar", "*.*")])
        if f: 
            with open(f, "w", encoding="utf-8") as file: file.write(self.editor.get("1.0", tk.END))
            messagebox.showinfo("Başarılı", "Proje Kaydedildi!")
    def dosya_ac(self):
        f = filedialog.askopenfilename(defaultextension=".tda", filetypes=[("TDA Dosyası", "*.tda"), ("Tüm Dosyalar", "*.*")])
        if f:
            with open(f, "r", encoding="utf-8") as file:
                self.editor.delete('1.0', tk.END); self.editor.insert(tk.END, file.read()); self.renklendir_tetikle()

if __name__ == "__main__":
    root = tk.Tk()
    GUI_UYGULAMA = TDA_System(root)
    root.mainloop()