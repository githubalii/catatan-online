@echo off
REM ====================================================
REM  Otomatis Push ke GitHub
REM  Dibuat untuk project FastAPI - githubalii
REM ====================================================

:: Pastikan script dijalankan di folder proyek kamu
cd /d "%~dp0"

:: Periksa apakah folder sudah repo Git
if not exist ".git" (
    echo ❌ Folder ini belum diinisialisasi sebagai repo Git.
    echo Jalankan perintah berikut dulu:
    echo     git init
    echo     git remote add origin https://github.com/githubalii/catatan-online.git
    pause
    exit /b
)

:: Tambahkan semua perubahan
git add .

:: Buat pesan commit otomatis dengan tanggal
for /f "tokens=2-4 delims=/ " %%a in ('date /t') do (
    set today=%%a-%%b-%%c
)
git commit -m "Auto commit on %today%"

:: Push ke GitHub
git push -u origin main

echo.
echo ✅ Semua perubahan berhasil di-push ke GitHub!
pause
