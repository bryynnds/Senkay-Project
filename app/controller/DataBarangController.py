from app.model.barang import barang
from app import response, app, db
from flask import request, redirect, url_for,render_template, jsonify, flash
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
        id_kategori = request.form.get('id_kategori')
        nama_barang = request.form.get('nama_barang')
        deskripsi = request.form.get('deskripsi')
        stok = int(request.form.get('stok'))
        harga = float(request.form.get('harga'))
        
        new_barang = barang(
            id_kategori=id_kategori,
            nama_barang=nama_barang,
            deskripsi=deskripsi,
            stok=stok,
            harga=harga
        )
        
        db.session.add(new_barang)
        db.session.commit()
        flash('Data barang berhasil ditambahkan', 'success')
        return redirect(url_for('data_barang'))
    except Exception as e:
        print(e)
        flash('Gagal menambahkan data barang', 'danger')
        return redirect(url_for('data_barang'))


def tambah_barang():
    kategoris = kategoribarang.query.all()
    return render_template("tambah_barang.html", kategoris=kategoris)

def edit_barang(id_barang):
    try:
        # Query untuk mencari barang berdasarkan id_barang
        Barang = barang.query.filter_by(id_barang=id_barang).first()
        kategoris = kategoribarang.query.all()  # ambil semua kategori untuk dropdown

        # Periksa apakah Barang ditemukan
        if not Barang:
            flash("Data barang tidak ditemukan", "danger")
            return redirect(url_for('data_barang'))
        
        return render_template("edit_barang.html", barang=Barang, kategoris=kategoris)
    except Exception as e:
        print("Error:", e)
        flash("Gagal mengambil data barang", "danger")
        return redirect(url_for('data_barang'))


def update_barang(id_barang):
    try:
        Barang = barang.query.filter_by(id_barang=id_barang).first()
        if not Barang:
            flash("Data barang tidak ditemukan", "danger")
            return redirect(url_for('data_barang'))

        # Update data barang dengan data dari form
        Barang.nama_barang = request.form.get('nama_barang')
        Barang.deskripsi = request.form.get('deskripsi')
        Barang.id_kategori = request.form.get('id_kategori')
        Barang.stok = int(request.form.get('stok'))
        Barang.harga = float(request.form.get('harga'))

        db.session.commit()
        flash("Data barang berhasil diperbarui", "success")
        return redirect(url_for('data_barang'))
    except Exception as e:
        print(e)
        flash("Gagal memperbarui data barang", "danger")
        return redirect(url_for('edit_barang', id_barang=id_barang))
    
def delete_barang(id_barang):
    try:
        Barang = barang.query.filter_by(id_barang=id_barang).first()
        
        if not Barang:
            flash("Data barang tidak ditemukan", "danger")
            return redirect(url_for('data_barang'))
        
        db.session.delete(Barang)
        db.session.commit()
        flash("Data barang berhasil dihapus", "success")
        return redirect(url_for('data_barang'))
    except Exception as e:
        print("Error:", e)
        flash("Gagal menghapus data barang", "danger")
        return redirect(url_for('data_barang'))




