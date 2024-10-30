from app.model.barang import barang
from app import response, app, db
from flask import request, redirect, url_for,render_template, flash
from app.model.transaksikeluar import transaksikeluar
import pytz
from datetime import datetime

def index():
    try:
        # Query join barangkeluar dan barang untuk mendapatkan nama_barang
        transaksi_keluar = db.session.query(
            transaksikeluar.id_transaksi,
            barang.nama_barang,
            transaksikeluar.jumlah,
            transaksikeluar.tanggal_keluar
        ).join(barang, transaksikeluar.id_barang == barang.id_barang).all()

        # Kirim data transaksi_keluar ke template
        return render_template("barang_keluar.html", transaksi_keluar=transaksi_keluar)
    except Exception as e:
        print(e)
        return response.badRequest([], "Gagal mengambil data barang keluar")
        
def formatarray(datas):
    array = []
    
    for i in datas:
        array.append(singleObject(i))    
        
    return array 

def singleObject(data):
    data = {
        'id_transaksi' : data.id_transaksi,
        'id_barang' : data.id_barang,
        'jumlah' : data.jumlah,
        'tanggal_keluar' : data.tanggal_keluar
    }
    
    return data

def detail(id_transaksi):
    try:
        TransaksiKeluar=transaksikeluar.query.filter_by(id_transaksi=id_transaksi).first()
        Barang = barang.query.filter((barang.id_barang == id_transaksi)).all()
        
        if not TransaksiKeluar:
            return response.badRequest([], "Tidak ada data dosen")
        
        databarang=formatbarang(Barang)
        data=singleDetailBarang(TransaksiKeluar, databarang)
        return response.success(data, "Success")
    
    except Exception as e:
        print(e)
        
def singleDetailBarang(transaksikeluar, barang):
    data={
        'id_transaksi' : transaksikeluar.id_transaksi,
        'id_barang' : transaksikeluar.id_barang,
        'jumlah' : transaksikeluar.jumlah,
        'tanggal_keluar' : transaksikeluar.tanggal_keluar,
        'barang' : barang
    }
    
    return data

def singleBarang(barang):
    data={
        'id_barang' : barang.id_barang,
        'id_kategori' : barang.id_kategori,
        'nama_barang' : barang.nama_barang,
        'deskripsi' : barang.deskripsi,
        'kategori' : barang.kategori,
        'stok' : barang.stok,
        'harga' : barang.harga,
        'tanggal_ditambahkan' : barang.tanggal_ditambahkan
    }
    
    return data

def formatbarang(data):
    array=[]
    for i in data:
        array.append(singleBarang(i))
    return array
    
def save():
    try:
        # Mengambil data dari request
        id_barang = request.form.get('id_barang')
        jumlah = int(request.form.get('jumlah'))  # Pastikan jumlah adalah integer

        # Tentukan zona waktu Jakarta
        jakarta_timezone = pytz.timezone('Asia/Jakarta')
        tanggal_keluar = datetime.now(jakarta_timezone)

        # Membuat instance transaksi keluar baru dengan tanggal otomatis
        transaksikeluars = transaksikeluar(
            id_barang=id_barang,
            jumlah=jumlah,
            tanggal_keluar=tanggal_keluar
        )

        # Menambahkan transaksi ke database
        db.session.add(transaksikeluars)

        # Memperbarui stok di tabel barang
        barang_item = barang.query.filter_by(id_barang=id_barang).first()
        if barang_item:
            if barang_item.stok >= jumlah:  # Pastikan stok cukup untuk dikurangi
                barang_item.stok -= jumlah  # Kurangi stok sesuai jumlah transaksi keluar
                db.session.commit()  # Commit perubahan stok
                flash('Transaksi keluar berhasil ditambahkan dan stok diperbarui', 'success')
            else:
                flash('Stok tidak mencukupi untuk transaksi keluar', 'danger')
                db.session.rollback()  # Batalkan transaksi jika stok tidak mencukupi
                return redirect(url_for('tambah_transaksikeluar'))
        
        return redirect(url_for('barang_keluar'))
    except Exception as e:
        print(e)
        db.session.rollback()  # Rollback jika ada error
        flash('Gagal menambahkan transaksi atau memperbarui stok', 'danger')
        return redirect(url_for('barang_keluar'))

    
def tambah_transaksikeluar():
    try:
        barang_list = barang.query.all()
        return render_template("tambah_transaksikeluar.html", barang=barang_list)
    except Exception as e:
        print(e)
        return response.badRequest([], "Gagal memuat halaman tambah transaksi")
        
def delete_transaksikeluar(id_transaksi):
    try:
        Transaksi = transaksikeluar.query.filter_by(id_transaksi=id_transaksi).first()
        
        if not Transaksi:
            flash("Transaksi tidak ditemukan", "danger")
            return redirect(url_for('barang_keluar'))
        
        db.session.delete(Transaksi)
        db.session.commit()
        flash("Transaksi berhasil dihapus", "success")
        return redirect(url_for('barang_keluar'))
    except Exception as e:
        print("Error:", e)
        flash("Gagal menghapus Transaksi", "danger")
        return redirect(url_for('barang_keluar'))
