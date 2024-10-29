from app.model.barang import barang
from app import response, app, db
from flask import request, redirect, url_for,render_template, jsonify
from app.model.kategoribarang import kategoribarang

def index():
    try:
        Barang = db.session.query(barang, kategoribarang.nama_kategori)\
                           .join(kategoribarang, barang.id_kategori == kategoribarang.id_kategori).all()
        data = formatarray(Barang)
        return render_template("data_barang.html", barang=data)
    except Exception as e:
        print(e)
        return jsonify({'error': str(e), 'message': "Gagal mengambil data"}), 500

def formatarray(datas):
    array = []
    for i in datas:
        array.append({
            'id_barang': i.barang.id_barang,
            'nama_barang': i.barang.nama_barang,
            'deskripsi': i.barang.deskripsi,
            'kategori': i.nama_kategori,  # dari tabel kategoribarang
            'stok': i.barang.stok,
            'harga': i.barang.harga,
            'tanggal_ditambahkan': i.barang.tanggal_ditambahkan
        })
    return array

def singleObject(data):
    data = {
        'id_barang' : data.id_barang,
        'id_kategori' : data.id_kategori,
        'nama_barang' : data.nama_barang,
        'deskripsi' : data.deskripsi,
        'kategori' : data.kategori,
        'stok' : data.stok,
        'harga' : data.harga,
        'tanggal_ditambahkan' : data.tanggal_ditambahkan
    }
    
    return data

def detail(id_barang):
    try:
        Barang=barang.query.filter_by(id_barang=id_barang).first()
        Kategori = kategoribarang.query.filter((kategoribarang.id_kategori == id_barang)).all()
        
        if not Barang:
            return response.badRequest([], "Tidak ada data barang")
        
        datakategori=formatkategori(Kategori)
        data=singleDetailKategori(Barang, datakategori)
        return response.success(data, "Success")
    
    except Exception as e:
        print(e)
        
def singleDetailKategori(barang, kategori):
    data={
        'id_barang' : barang.id_barang,
        'id_kategori' : barang.id_kategori,
        'nama_barang' : barang.nama_barang,
        'deskripsi' : barang.deskripsi,
        'kategori' : barang.kategori,
        'stok' : barang.stok,
        'harga' : barang.harga,
        'tanggal_ditambahkan' : barang.tanggal_ditambahkan,
        'kategori': kategori
    }
    
    return data

def singleKategori(kategori):
    data={
        'id_kategori' : kategori.id_kategori,
        'nama_kategori' : kategori.nama_kategori,
    }
    
    return data

def formatkategori(data):
    array=[]
    for i in data:
        array.append(singleKategori(i))
    return array
    
def save():
    try:
        id_barang=request.form.get('id_barang')
        id_kategori=request.form.get('id_kategori')
        nama_barang=request.form.get('nama_barang')
        deskripsi=request.form.get('deskripsi')
        kategori=request.form.get('kategori')
        stok=request.form.get('stok')
        harga=request.form.get('harga')
        tanggal_ditambahkan=request.form.get('tanggal_ditambahkan')
        
        barangs=barang(id_barang=id_barang, id_kategori=id_kategori, nama_barang=nama_barang, deskripsi=deskripsi,
                       kategori=kategori, stok=stok, harga=harga, tanggal_ditambahkan=tanggal_ditambahkan)
        db.session.add(barangs)
        db.session.commit()
        return response.success(',','Data Berhasil Ditambah')
    except Exception as e:
        print(e)
        
