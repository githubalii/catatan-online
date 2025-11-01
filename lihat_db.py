import sqlite3
from tabulate import tabulate

def lihat_isi_database(db_path="notes.db"):
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Ambil daftar tabel
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()

        if not tables:
            print("❌ Tidak ada tabel ditemukan di database.")
            return

        print("\n📋 Daftar tabel dalam database:")
        for t in tables:
            print(f" - {t[0]}")

        # Jika ada tabel note, tampilkan isinya
        print("\n📄 Isi tabel 'note':")
        try:
            cursor.execute("SELECT * FROM note;")
            rows = cursor.fetchall()
            columns = [desc[0] for desc in cursor.description]

            if rows:
                print(tabulate(rows, headers=columns, tablefmt="grid"))
            else:
                print("(Belum ada data dalam tabel note.)")
        except sqlite3.OperationalError:
            print("⚠️ Tabel 'note' tidak ditemukan dalam database.")

        conn.close()
    except Exception as e:
        print(f"❌ Terjadi kesalahan: {e}")

if __name__ == "__main__":
    lihat_isi_database()
