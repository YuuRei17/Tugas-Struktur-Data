import os
os.system("cls")

import csv
from datetime import datetime
from collections import defaultdict


DATA_FILE = 'masukan_nama_file.csv'


def init_csv():
    try:
        if not os.path.exists(DATA_FILE):
            with open(DATA_FILE, mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(['id', 'tanggal', 'jenis', 'kategori', 'jumlah', 'keterangan'])
    except PermissionError:
        print("Tidak bisa membuat atau menulis ke data.csv. Tutup dulu file jika sedang dibuka.")
        exit()


def baca_data():
    data = []
    if not os.path.exists(DATA_FILE):
        return data
    with open(DATA_FILE, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['id'].strip() == '':
                continue  
            row['jumlah'] = int(row['jumlah'])  
            data.append(row)
    return data


def tulis_data(data):
    with open(DATA_FILE, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=['id', 'tanggal', 'jenis', 'kategori', 'jumlah', 'keterangan'])
        writer.writeheader()
        for row in data:
            writer.writerow(row)


def tambah_transaksi():
    data = baca_data()
    id_baru = str(len(data) + 1)
    tanggal = input("Tanggal (Format: YYYY-MM-DD, Contoh: 2025-08-12): ")
    jenis = input("Jenis (pemasukan/pengeluaran): ").lower()
    kategori = input("Kategori: ")
    jumlah = int(input("Jumlah: "))
    keterangan = input("Keterangan: ")

    data.append({
        'id': id_baru,
        'tanggal': tanggal,
        'jenis': jenis,
        'kategori': kategori,
        'jumlah': jumlah,
        'keterangan': keterangan
    })
    tulis_data(data)
    print("✅ Transaksi berhasil ditambahkan.")


def tampilkan_transaksi():
    data = baca_data()
    print("\n--- Daftar Transaksi ---")
    for d in data:
        print(f"{d['id']}. {d['tanggal']} | {d['jenis']} | {d['kategori']} | Rp{d['jumlah']} | {d['keterangan']}")


def update_transaksi():
    data = baca_data()
    tampilkan_transaksi()
    id_update = input("Masukkan ID yang ingin diupdate: ")
    for d in data:
        if d['id'] == id_update:
            d['tanggal'] = input(f"Tanggal baru ({d['tanggal']}): ") or d['tanggal']
            d['jenis'] = input(f"Jenis baru ({d['jenis']}): ") or d['jenis']
            d['kategori'] = input(f"Kategori baru ({d['kategori']}): ") or d['kategori']
            jumlah_input = input(f"Jumlah baru ({d['jumlah']}): ")
            d['jumlah'] = int(jumlah_input) if jumlah_input else d['jumlah']
            d['keterangan'] = input(f"Keterangan baru ({d['keterangan']}): ") or d['keterangan']
            tulis_data(data)
            print("Transaksi berhasil diupdate.")
            return
    print("ID tidak ditemukan.")


def hapus_transaksi():
    data = baca_data()
    tampilkan_transaksi()
    id_hapus = input("Masukkan ID yang ingin dihapus: ")
    data_baru = [d for d in data if d['id'] != id_hapus]
    if len(data_baru) != len(data):
        tulis_data(data_baru)
        print("Transaksi berhasil dihapus.")
    else:
        print("ID tidak ditemukan.")

def laporan_kategori():
    data = baca_data()
    map_kategori = defaultdict(int)
    for d in data:
        if d['jenis'] == 'pengeluaran':
            map_kategori[d['kategori']] += d['jumlah']
    print("\n--- Laporan Pengeluaran per Kategori ---")
    for kategori, total in map_kategori.items():
        print(f"{kategori}: Rp{total}")


def laporan_waktu():
    data = baca_data()
    bulan = input("Masukkan bulan (01-12) atau tekan Enter untuk semua: ")
    tahun = input("Masukkan tahun (YYYY) atau tekan Enter untuk semua: ")
    total_masuk = total_keluar = 0

    for d in data:
        try:
            tanggal = datetime.strptime(d['tanggal'], "%Y-%m-%d")
        except ValueError:
            continue  

        if (bulan and tanggal.strftime('%m') != bulan) or (tahun and tanggal.strftime('%Y') != tahun):
            continue
        if d['jenis'] == 'pemasukan':
            total_masuk += d['jumlah']
        elif d['jenis'] == 'pengeluaran':
            total_keluar += d['jumlah']
    
    print("\n--- Laporan Keuangan ---")
    print(f"Total Pemasukan   : Rp{total_masuk}")
    print(f"Total Pengeluaran : Rp{total_keluar}")
    print(f"Saldo Akhir       : Rp{total_masuk - total_keluar}")

def menu():
    init_csv()
    while True:
        print("\nAplikasi Manajemen Keuangan Pribadi")
        print("1. Tambah Transaksi")
        print("2. Tampilkan Transaksi")
        print("3. Update Transaksi")
        print("4. Hapus Transaksi")
        print("5. Laporan per Kategori")
        print("6. Laporan Bulanan/Tahunan")
        print("0. Keluar")
        pilihan = int(input("Pilih menu: "))

        if pilihan == 1:
            tambah_transaksi()
        elif pilihan == 2:
            tampilkan_transaksi()
        elif pilihan == 3:
            update_transaksi()
        elif pilihan == 4:
            hapus_transaksi()
        elif pilihan == 5:
            laporan_kategori()
        elif pilihan == 6:
            laporan_waktu()
        elif pilihan == 0:
            print("Terima kasih telah menggunakan aplikasi.")
            break
        else:
            print(" Pilihan tidak valid. Coba lagi.")

# Jalankan aplikasi
if __name__ == "__main__":
    menu()