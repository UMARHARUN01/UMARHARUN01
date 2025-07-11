import csv
from collections import deque
from datetime import datetime

produk = []
antrian = deque()
transaksi = []

def load_produk():
    try:
        with open("produk.csv", newline='') as f:
            for row in csv.DictReader(f):
                produk.append(row)
    except FileNotFoundError:
        pass

def simpan_produk():
    with open("produk.csv", 'w', newline='') as f:
        kolom = ['id', 'nama', 'stok', 'harga', 'deskripsi']
        writer = csv.DictWriter(f, fieldnames=kolom)
        writer.writeheader()
        for p in produk:
            writer.writerow(p)

def tampil_produk():
    for p in produk:
        print(p)

def tambah_produk():
    data = {
        'id': input("ID: "),
        'nama': input("Nama: "),
        'stok': input("Stok: "),
        'harga': input("Harga: "),
        'deskripsi' : input("Deskripsi barang: ")
    }
    produk.append(data)
    simpan_produk()
    print("Produk ditambah.")

def ubah_produk():
    id_edit = input("ID produk yang diubah: ")
    for p in produk:
        if p['id'] == id_edit:
            p['nama'] = input("Nama baru: ")
            p['stok'] = input("Stok baru: ")
            p['harga'] = input("Harga baru: ")
            p['deskripsi'] = input("Deskripsi: ")
            simpan_produk()
            print("Produk diperbarui.")
            return
    print("Produk tidak ditemukan.")

def hapus_produk():
    id_hapus = input("ID produk yang dihapus: ")
    for p in produk:
        if p['id'] == id_hapus:
            produk.remove(p)
            simpan_produk()
            print("Produk dihapus.")
            return
    print("Tidak ditemukan.")

def tambah_transaksi():
    idp = input("ID Produk: ")
    jenis = input("Jual/Beli: ").lower()
    jumlah = int(input("Jumlah: "))
    for p in produk:
        if p['id'] == idp:
            antrian.append({
                'jenis': jenis,
                'id': idp,
                'jumlah': jumlah,
                'tanggal': datetime.now().strftime('%Y-%m-%d')
            })
            print("Transaksi masuk antrian.")
            return
    print("Produk tidak ditemukan.")

def proses_transaksi():
    while antrian:
        tr = antrian.popleft()
        for p in produk:
            if p['id'] == tr['id']:
                stok = int(p['stok'])
                jml = tr['jumlah']
                if tr['jenis'] == 'jual':
                    if stok >= jml:
                        p['stok'] = str(stok - jml)
                        print("Jual berhasil.")
                    else:
                        print("Stok kurang.")
                        continue
                else:
                    p['stok'] = str(stok + jml)
                    print("Beli berhasil.")
                transaksi.append(tr)
    simpan_produk()
    simpan_transaksi()

def simpan_transaksi():
    with open("transaksi.csv", 'w', newline='') as f:
        kolom = ['jenis', 'id', 'jumlah', 'tanggal']
        writer = csv.DictWriter(f, fieldnames=kolom)
        writer.writeheader()
        for t in transaksi:
            writer.writerow(t)

def laporan():
    tipe = input("Laporan (harian/mingguan/bulanan): ").lower()
    hari_ini = datetime.now()
    for t in transaksi:
        tgl = datetime.strptime(t['tanggal'], '%Y-%m-%d')
        if tipe == 'harian' and tgl.date() == hari_ini.date():
            print(t)
        elif tipe == 'mingguan' and tgl.isocalendar()[1] == hari_ini.isocalendar()[1]:
            print(t)
        elif tipe == 'bulanan' and tgl.month == hari_ini.month:
            print(t)

def menu():
    load_produk()
    while True:
        print("=== MENU UTAMA ===")
        print("1. Tampil Produk")
        print("2. Tambah Produk")
        print("3. Update Produk")
        print("4. Hapus Produk")
        print("5. Transaksi")
        print("6. Laporan")
        print("7. Keluar")
        pilih = input("Pilih: ")
        if pilih == '1': tampil_produk()
        elif pilih == '2': tambah_produk()
        elif pilih == '3': ubah_produk()
        elif pilih == '4': hapus_produk()
        elif pilih == '5':
            tambah_transaksi()
            proses_transaksi()
        elif pilih == '6': laporan()
        elif pilih == '7': break
        else: print("Pilihan salah.")

if __name__ == '__main__':
    menu()
