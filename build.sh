#!/data/data/com.termux/files/usr/bin/bash
echo "=== Base64 Tool APK Builder ==="
echo ""

# Check dependencies
echo "[*] Checking dependencies..."

if ! command -v pip &>/dev/null; then
    echo "[X] pip bulunamadi!"
    exit 1
fi

# Install buildozer & kivy
echo "[*] Installing buildozer and kivy..."
pip install --no-cache-dir kivy buildozer cython 2>&1

if [ $? -ne 0 ]; then
    echo "[X] Paket kurulumu basarisiz! Internet baglantinizi kontrol edin."
    exit 1
fi

echo "[*] Kivy basariyla kuruldu."

# Check if running in Termux
if [ -d "/data/data/com.termux" ]; then
    echo "[*] Termux ortami algilandi."
    echo "[!] NOT: APK build etmek icin Android SDK/NDK gerekli."
    echo "[!] Buildozer otomatik olarak SDK/NDK indirecektir."
    echo "[!] Bu islem uzun surebilir (1-2 saat) ve ~3GB yer kaplar."
    echo ""
    read -p "Build islemini baslatmak istiyor musunuz? (e/h): " answer
    if [ "$answer" != "e" ]; then
        echo "[*] Iptal edildi."
        exit 0
    fi
fi

# Build
echo "[*] APK build basliyor..."
cd "$(dirname "$0")"
buildozer android debug

if [ $? -eq 0 ]; then
    echo "[+] APK basariyla olusturuldu!"
    echo "[+] Konum: bin/"
    ls -lh bin/*.apk 2>/dev/null
else
    echo "[X] APK build basarisiz!"
    echo "[*] Hata detaylari icin buildozer.spec dosyasini kontrol edin."
fi
