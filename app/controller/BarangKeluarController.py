from app.model.barang import barang
from app import response, app, db
from flask import request, redirect, url_for,render_template
from app.model.transaksikeluar import transaksikeluar

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
        id_transaksi=request.form.get('id_transaksi')
        id_barang=request.form.get('id_barang')
        jumlah=request.form.get('jumlah')
        tanggal_keluar=request.form.get('tanggal_keluar')
        
        transaksikeluars=transaksikeluar(id_transaksi=id_transaksi, id_barang=id_barang, jumlah=jumlah, tanggal_keluar=tanggal_keluar)
        db.session.add(transaksikeluars)
        db.session.commit()
        return response.success(',','Data Berhasil Ditambah')
    except Exception as e:
        print(e)
        
