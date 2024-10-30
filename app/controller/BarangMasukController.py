from app import db, response
from flask import render_template, request, url_for, flash, redirect
from app.model.transaksimasuk import transaksimasuk
from app.model.barang import barang
from app.model.supplier import supplier
from datetime import datetime
import pytz

def index():
    try:
        # Query untuk mengambil data transaksi masuk dengan join ke tabel barang dan supplier
        transaksi_masuk = db.session.query(
            transaksimasuk.id_transaksi,
            barang.nama_barang,
            transaksimasuk.jumlah,
            transaksimasuk.tanggal_masuk,
            supplier.nama_supplier
        ).join(barang, transaksimasuk.id_barang == barang.id_barang) \
         .join(supplier, transaksimasuk.id_supplier == supplier.id_supplier).all()

        # Kirim data transaksi_masuk ke template
        return render_template("barang_masuk.html", transaksi_masuk=transaksi_masuk)
    except Exception as e:
        print(e)
        return response.badRequest([], "Gagal mengambil data barang masuk")

def formatarray(datas):
    array = []
    for i in datas:
        array.append(singleObject(i))
    return array

def singleObject(data):
    return {
        'id_transaksi': data.id_transaksi,
        'nama_barang': data.nama_barang,
        'jumlah': data.jumlah,
        'tanggal_masuk': data.tanggal_masuk,
        'nama_supplier': data.nama_supplier
    }

def detail(id_transaksi):
    try:
        TransaksiMasuk=transaksimasuk.query.filter_by(id_transaksi=id_transaksi).first()
        Barang = barang.query.filter((barang.id_barang == id_transaksi)).all()
        Supplier = supplier.query.filter((supplier.id_supplier == id_transaksi)).all()
        
        if not TransaksiMasuk:
            return response.badRequest([], "Tidak ada data transaksi")
        
        databarang=formatbarang(Barang)
        datasupplier=formatsupplier(Supplier)
        data=singleDetailBarang(TransaksiMasuk, databarang)
        datas=singleDetailSupplier(TransaksiMasuk, datasupplier)
        response.success(datas, "Success")
        return response.success(data, "Success")
    
    except Exception as e:
        print(e)
        
def singleDetailBarang(transaksimasuk, barang):
    data={
        'id_transaksi' : transaksimasuk.id_transaksi,
        'id_barang' : transaksimasuk.id_barang,
        'jumlah' : transaksimasuk.jumlah,
        'tanggal_masuk' : transaksimasuk.tanggal_masuk,
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

def singleDetailSupplier(transaksimasuk, supplier):
    data={
        'id_transaksi' : transaksimasuk.id_transaksi,
        'id_barang' : transaksimasuk.id_barang,
        'jumlah' : transaksimasuk.jumlah,
        'tanggal_masuk' : transaksimasuk.tanggal_masuk,
        'supplier' : supplier
    }
    
    return data

def singleSupplier(supplier):
    data={
        'id_supplier' : supplier.id_supplier,
        'nama_supplier' : supplier.nama_supplier,
        'alamat_supplier' : supplier.alamat_supplier,
        'telepon_supplier' : supplier.telepon_supplier
    }
    
    return data

def formatbarang(data):
    array=[]
    for i in data:
        array.append(singleBarang(i))
    return array

def formatsupplier(data):
    array=[]
    for i in data:
        array.append(singleSupplier(i))
    return array

def save():
    try:
        # Mengambil data dari request (tanpa tanggal_masuk)
        id_barang = request.form.get('id_barang')
        jumlah = request.form.get('jumlah')
        id_supplier = request.form.get('id_supplier')

        # Membuat instance transaksimasuk baru dengan tanggal otomatis
        jakarta_timezone = pytz.timezone('Asia/Jakarta')
        tanggal_masuk = datetime.now(jakarta_timezone) 
        
        transaksimasuks = transaksimasuk(
            id_barang=id_barang,
            jumlah=jumlah,
            tanggal_masuk=tanggal_masuk,  # Tanggal otomatis
            id_supplier=id_supplier
        )
        
        db.session.add(transaksimasuks)
        db.session.commit()
        flash('Transaksi baru berhasil ditambahkan', 'success')
        return redirect(url_for('barang_masuk'))
    except Exception as e:
        print(e)
        flash('Gagal menambahkan transaksi', 'danger')
        return redirect(url_for('barang_masuk'))
    
def tambah_transaksi():
    try:
        barang_list = barang.query.all()
        supplier_list = supplier.query.all()
        return render_template("tambah_transaksimasuk.html", barang=barang_list, suppliers=supplier_list)
    except Exception as e:
        print(e)
        return response.badRequest([], "Gagal memuat halaman tambah transaksi")

