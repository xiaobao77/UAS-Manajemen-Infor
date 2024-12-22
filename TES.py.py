import mysql.connector
from datetime import datetime
from tabulate import tabulate
from pyfiglet import figlet_format
from colorama import Fore, Style, init
import os
import time  # Tambahkan ini untuk efek loading

# Initialize colorama for Windows compatibility
init()

# Koneksi ke database MySQL
def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",  # Ganti dengan username MySQL Anda
        password="",  # Ganti dengan password MySQL Anda
        database="tes"
    )

def clear_screen():
    # Clear screen for different operating systems
    os.system('cls' if os.name == 'nt' else 'clear')

def loading_animation(duration):
    end_time = time.time() + duration
    spinner = ['◐', '◓', '◑', '◒']  # Karakter untuk spinner berbentuk lingkaran
    while time.time() < end_time:
        for symbol in spinner:
            print(Fore.CYAN + f"\r{symbol}  ", end='', flush=True)  # Ubah warna menjadi cyan
            time.sleep(0.2)  # Delay untuk efek loading
    print("\r" + " " * 20 + "\r", end='')  # Menghapus loading

def tampilkan_menu():
    clear_screen()
    # Display banner
    banner = figlet_format("Caffe Shop", font="slant")  # Menggunakan font yang lebih besar
    print(Fore.CYAN + banner + Style.RESET_ALL)
    
    loading_animation(3)  # Menampilkan loading selama 3 detik

    print(Fore.CYAN   + "┌──────────────────────────────┐")
    print(Fore.YELLOW + "│          Menu Utama          │")
    print(Fore.CYAN   + "├──────────────────────────────┤")
    print(Fore.MAGENTA+ "│ [1] Produk                   │")
    print(Fore.MAGENTA+ "│ [2] Pembelian                │")
    print(Fore.MAGENTA+ "│ [3] Cetak Struk              │")
    print(Fore.MAGENTA+ "│ [4] Keluar                   │")
    print(Fore.CYAN   + "└──────────────────────────────┘")
    print(Style.RESET_ALL)

# Fungsi untuk menampilkan menu utama
def main_menu():
    while True:
        tampilkan_menu()  # Menampilkan menu utama
        choice = input("Pilih menu (1-4): ")

        if choice == '1':
            produk_menu()
        elif choice == '2':
            pembelian_menu()
        elif choice == '3':
            cetak_struk_menu()  # Memanggil menu cetak struk
        elif choice == '4':
            print("Terima kasih!")
            break
        else:
            print("Pilihan tidak valid. Silakan coba lagi.")

# Fungsi untuk menu produk
def produk_menu():
    while True:
        print(Fore.CYAN    + "┌──────────────────────────────┐")
        print(Fore.YELLOW  + "│          Menu Produk         │")
        print(Fore.CYAN    + "├──────────────────────────────┤")
        print(Fore.MAGENTA + "│ [1] Insert Produk            │")
        print(Fore.MAGENTA + "│ [2] Update Produk            │")
        print(Fore.MAGENTA + "│ [3] Delete Produk            │")
        print(Fore.MAGENTA + "│ [4] Show Produk              │")
        print(Fore.MAGENTA + "│ [5] Keluar                   │")
        print(Fore.CYAN    + "└──────────────────────────────┘")
        choice = input("Pilih menu (1-5): ")

        if choice == '1':
            insert_produk()
        elif choice == '2':
            update_produk()
        elif choice == '3':
            delete_produk()
        elif choice == '4':
            show_produk()
        elif choice == '5':
            break
        else:
            print("Pilihan tidak valid. Silakan coba lagi.")

# Fungsi untuk menambahkan produk
def insert_produk():
    db = connect_db()
    cursor = db.cursor()
    id_produk = int(input("Masukkan ID Produk: "))
    nama_produk = input("Masukkan Nama Produk: ")
    jenis_produk = input("Masukkan Jenis Produk: ")
    harga = float(input("Masukkan Harga: "))
    stok = int(input(" Masukkan Stok : "))
    
    sql = "INSERT INTO produk (id_produk, nama_produk, jenis_produk, harga, stok) VALUES (%s, %s, %s, %s, %s)"
    cursor.execute(sql, (id_produk, nama_produk, jenis_produk, harga, stok))
    db.commit()
    print("Produk berhasil ditambahkan.")
    cursor.close()
    db.close()

# Fungsi untuk mengupdate produk
def update_produk():
    db = connect_db()
    cursor = db.cursor()
    id_produk = int(input("Masukkan ID Produk yang ingin diupdate: "))
    stok = int(input("Masukkan Stok baru: "))
    
    sql = "UPDATE produk SET stok = %s WHERE id_produk = %s"
    cursor.execute(sql, (stok, id_produk))
    db.commit()
    print("Produk berhasil diupdate.")
    cursor.close()
    db.close()

# Fungsi untuk menghapus produk
def delete_produk():
    db = connect_db()
    cursor = db.cursor()
    id_produk = int(input("Masukkan ID Produk yang ingin dihapus: "))
    
    sql = "DELETE FROM produk WHERE id_produk = %s"
    cursor.execute(sql, (id_produk,))
    db.commit()
    print("Produk berhasil dihapus.")
    cursor.close()
    db.close()

# Fungsi untuk menampilkan produk
def show_produk():
    db = connect_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM produk")
    results = cursor.fetchall()
    
    # Menyiapkan data untuk tabulate
    headers = ["ID", "Nama", "Jenis", "Harga", "Stok"]
    table = []
    
    for row in results:
        id_produk, nama_produk, jenis_produk, harga, stok = row
        
        # Menentukan warna untuk stok
        if stok == 1:
            stok_display = Fore.RED + str(stok) + Style.RESET_ALL  # Warna merah untuk stok 1
        elif 2 <= stok <= 5:
            stok_display = Fore.YELLOW + str(stok) + Style.RESET_ALL  # Warna kuning untuk stok 2-5
        else:
            stok_display = str(stok)  # Stok normal tanpa warna
        
        # Menambahkan baris ke dalam tabel
        table.append((id_produk, nama_produk, jenis_produk, harga, stok_display))
    
    # Menampilkan tabel menggunakan tabulate dengan garis samping yang lebih baik
    print("\nDaftar Produk:")
    print(tabulate(table, headers=headers, tablefmt="fancy_grid"))  # Menggunakan fancy_grid untuk tampilan yang lebih baik
    
    cursor.close()
    db.close()

# Fungsi untuk menu pembelian
def pembelian_menu():
    while True:
        print(Fore.CYAN    + "┌─────── Menu Pembelian ───────┐")
        print(Fore.CYAN    + "│                              │")
        print(Fore.MAGENTA + "│ [1] Pembelian                │")
        print(Fore.MAGENTA + "│ [2] Keluar                   │")
        print(Fore.CYAN    + "└──────────────────────────────┘")
        choice = input("Pilih menu (1-2): ")

        if choice == '1':
            proses_pembelian()
        elif choice == '2':
            break
        else:
            print("Pilihan tidak valid. Silakan coba lagi.")

# Fungsi untuk memproses pembelian
def proses_pembelian():
    db = connect_db()
    cursor = db.cursor()
    nama_pembeli = input("Masukkan Nama Pembeli: ")
    nama_produk = input("Masukkan Nama Produk: ")
    jumlah = int(input("Masukkan Jumlah Produk yang Dibeli: "))

    # Mendapatkan harga dan stok produk
    cursor.execute("SELECT harga, stok FROM produk WHERE nama_produk = %s", (nama_produk,))
    result = cursor.fetchone()
    
    if result:
        harga, stok = result  # Ambil harga dan stok dari hasil query
        if stok == 1:
            print("Pembelian tidak dapat dilakukan karena stok sisa 1.")
            # Menampilkan informasi dalam format tabel
            print(tabulate([[nama_produk, Fore.RED + str(stok) + Style.RESET_ALL]], headers=["Nama Produk", "Stok"], tablefmt="fancy_grid"))
        elif stok >= jumlah:  # Cek apakah stok cukup
            total_harga = harga * jumlah
            
            # Menyimpan data pembelian
            sql = "INSERT INTO pembelian (nama_pembeli, nama_produk, jumlah, total_harga) VALUES (%s, %s, %s, %s)"
            cursor.execute(sql,(nama_pembeli, nama_produk, jumlah, total_harga))
            db.commit()
            
            # Mengupdate stok produk
            new_stok = stok - jumlah
            sql_update = "UPDATE produk SET stok = %s WHERE nama_produk = %s"
            cursor.execute(sql_update, (new_stok, nama_produk))
            db.commit()
            
            print("Pembelian berhasil disimpan.")
            # Tampilkan detail pembelian setelah berhasil
            print("\nDetail Pembelian:")
            print(f"Nama Pembeli: {nama_pembeli}")
            print(f"Nama Produk: {nama_produk}")
            print(f"Jumlah: {jumlah}")
            print(f"Total Harga: {total_harga}")
        else:
            print("Stok tidak cukup untuk memenuhi pembelian.")
    else:
        print("Produk tidak ditemukan.")
    
    cursor.close()
    db.close()


# Fungsi untuk menu cetak struk
def cetak_struk_menu():
    while True:
        print(Fore.YELLOW  + "┌────── Menu Cetak Struk ──────┐")
        print(Fore.MAGENTA + "│                              │")
        print(Fore.MAGENTA + "│ [1] Tampilkan Pembelian      │")
        print(Fore.MAGENTA + "│ [2] Cetak Struk              │")
        print(Fore.MAGENTA + "│ [3] Keluar                   │")
        print(Fore.YELLOW  + "└──────────────────────────────┘")
        choice = input("Pilih menu (1-3): ")

        if choice == '1':
            tampilkan_pembelian()
        elif choice == '2':
            cetak_struk()  # Memanggil fungsi cetak struk yang telah dimodifikasi
        elif choice == '3':
            break
        else:
            print("Pilihan tidak valid. Silakan coba lagi.")

# Fungsi untuk menampilkan pembelian
def tampilkan_pembelian():
    db = connect_db()
    cursor = db.cursor()
    nama_pembeli = input("Masukkan Nama Pembeli: ")
    
    loading_animation(3)  # Menambahkan efek loading sebelum menampilkan pembelian
    
    cursor.execute("SELECT * FROM pembelian WHERE nama_pembeli = %s", (nama_pembeli,))
    results = cursor.fetchall()
    
    # Menyiapkan data untuk tabulate
    headers = ["ID", "Nama Pembeli", "Nama Produk", "Jumlah", "Total Harga", "Tanggal"]
    table = []
    
    for row in results:
        table.append(row)  # Menambahkan setiap baris ke dalam tabel
    
    # Menampilkan tabel menggunakan tabulate dengan garis samping
    print("\nData Pembelian:")
    print(tabulate(table, headers=headers, tablefmt="fancy_grid"))  # Menggunakan fancy_grid untuk tampilan yang lebih baik
    
    cursor.close()
    db.close()

# Fungsi untuk mencetak struk
def cetak_struk():
    db = connect_db()
    cursor = db.cursor()
    nama_pembeli = input("Masukkan Nama Pembeli untuk mencetak struk: ")
    
    loading_animation(3)  # Menambahkan efek loading sebelum menampilkan struk
    
    cursor.execute("SELECT * FROM pembelian WHERE nama_pembeli = %s", (nama_pembeli,))
    results = cursor.fetchall()
    
    if results:
        # Informasi toko
        nama_toko = "Caffe Shop"
        alamat_toko = "Jl. Utama Rukoh"
        alamat_toko2 = "Darussalam, Banda Aceh"
        no_telp = "085758497957"
        
        sekarang = datetime.now()
        tanggal_waktu = sekarang.strftime("%Y-%m-%d %H:%M:%S")

        print("=" * 50)  # Garis pembatas atas
        print(f"{nama_toko:^50}")  # Nama toko di tengah
        print(f"{alamat_toko:^50}")  # Alamat toko di tengah
        print(f"{alamat_toko2:^50}")  # Alamat toko kedua di tengah
        print(f"{no_telp:^50}")  # Nomor telepon di tengah
        print("=" * 50)  # Garis pemisah
        print(f"Tanggal: {tanggal_waktu}")
        print("-" * 50)

        print(f"{'Nama Barang':<30}{'Qty':^5}{'Harga':>10}")  # Header tabel
        print("-" * 50)

        total_harga = 0
        for row in results:
            nama_produk = row[2]  # Nama produk
            qty = row[3]          # Jumlah
            harga = row[4]        # Total harga
            total_harga += harga
            print(f"{nama_produk:<30}{qty:^5}{harga:>10,.0f}")

        print("-" * 50)
        print(f"{'Total':<30}{'':^5}{total_harga:>10,.0f}")
        print("=" * 50)
        print("Terima Kasih Telah Berbelanja di Caffe Shop :)!")
        print("=" * 50)  # Garis pembatas bawah
    else:
        print("Tidak ada data pembelian untuk nama pembeli ini.")
    
    cursor.close()
    db.close()

# Menjalankan program
if __name__ == "__main__":
    main_menu()