@echo off
title TDA Dili Kurulum Sihirbazi
color 0a
cls

echo ==========================================
echo   TDA DILI OTOMATIK KURULUM BASLIYOR...
echo ==========================================
echo.

:: 1. Adim: Eski islemleri sonlandir (Dosyalar serbest kalsin)
taskkill /f /im python.exe >nul 2>&1

:: 2. Adim: C surucusunde TDA klasoru olustur
if not exist "C:\TDA" mkdir "C:\TDA"

:: 3. Adim: Python Yorumlayicisini (Motoru) Olustur
echo Python dosyasini olusturuyorum...
(
echo import sys
echo import os
echo.
echo def komut_calistir(satir, hafiza^):
echo     satir = satir.strip(^)
echo     if not satir or satir.startswith("#"^): return
echo     if " olsun " in satir:
echo         try:
echo             p = satir.split(" olsun "^)
echo             degisken, deger = p[0].strip(^), p[1].strip(^)
echo             if deger.startswith('"'^) and deger.endswith('"'^): hafiza[degisken] = deger.strip('"'^)
echo             else: hafiza[degisken] = eval(deger, {}, hafiza^)
echo         except: print("Hata: Atama yapilamadi."^)
echo     elif satir.startswith("yaz "^):
echo         ifade = satir[4:].strip(^)
echo         if ifade.startswith('"'^) and ifade.endswith('"'^): print(ifade.strip('"'^)^)
echo         elif ifade in hafiza: print(hafiza[ifade]^)
echo         else:
echo             try: print(eval(ifade, {}, hafiza^)^)
echo             except: print("Hata: Tanimli degil -> " + ifade^)
echo     elif satir.startswith("eger "^):
echo         try:
echo             kalan = satir[5:]
echo             kosul, islem = kalan.split(" ise "^)
echo             if eval(kosul, {}, hafiza^): komut_calistir(islem, hafiza^)
echo         except: print("Hata: Mantik hatasi."^)
echo     elif satir == "cikis": sys.exit(^)
echo     elif satir == "temizle": os.system('cls'^)
echo.
echo def canli_mod(^):
echo     hafiza = {}
echo     print("=== TDA Dili v1.0 (Cikis icin 'cikis') ==="^)
echo     while True:
echo         try:
echo             g = input("TDA > "^)
echo             komut_calistir(g, hafiza^)
echo         except: break
echo.
echo if __name__ == "__main__":
echo     if len(sys.argv^) ^> 1:
echo         try:
echo             with open(sys.argv[1], 'r'^) as f:
echo                 for s in f: komut_calistir(s, {}^)
echo         except: print("Dosya bulunamadi."^)
echo     else: canli_mod(^)
) > "C:\TDA\main.py"

:: 4. Adim: Calistiriciyi (BAT) Olustur
echo Baslatma dosyasini olusturuyorum...
(
echo @echo off
echo python "C:\TDA\main.py" %%*
) > "C:\TDA\tda.bat"

:: 5. Adim: PATH Ayari (Windows'a TDA'yi ogret)
echo Windows Ortam Degiskenleri ayarlaniyor...
setx PATH "%PATH%;C:\TDA" >nul

echo.
echo ==========================================
echo   KURULUM TAMAMLANDI!
echo ==========================================
echo.
echo Lutfen acik olan BUTUN siyah ekranlari kapatin.
echo Ardindan yeni bir CMD acip sadece 'tda' yazin.
echo.
pause