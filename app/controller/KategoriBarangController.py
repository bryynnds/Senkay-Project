from app.model.kategoribarang import kategoribarang
from app import db
from flask import request, render_template, jsonify, redirect, url_for

def index():
    try:
        Kategori = kategoribarang.query.all()  # Mengambil semua data kategori dari tabel
        data = formatarray(Kategori)           # Format data
        return render_template("kategori.html", values=data)  # Menampilkan data ke template
    except Exception as e:
        print(e)
        return jsonify({'error': str(e), 'message': "Gagal mengambil data"}), 500

def formatarray(datas):
    array = []
    for i in datas:
        array.append(singleObject(i))    
    return array 

def singleObject(data):
    return {
        'id_kategori' : data.id_kategori,
        'nama_kategori' : data.nama_kategori,
    }

def save():
    try:
        id_kategori = request.form.get('id_kategori')
        nama_kategori = request.form.get('nama_kategori')
        
        Kategori = kategoribarang(id_kategori=id_kategori, nama_kategori=nama_kategori)
        db.session.add(Kategori)
        db.session.commit()
        return redirect(url_for('kategori', success=True))
    except Exception as e:
        print(e)
        return jsonify({'error': str(e), 'message': "Gagal menyimpan data"}), 500
    
def hapus_kategori(id_kategori):
    try:
        Kategori = kategoribarang.query.get(id_kategori)
        if not Kategori:
            return jsonify({'error': True, 'message': "Kategori tidak ditemukan"}), 404
        db.session.delete(Kategori)
        db.session.commit()
        return redirect(url_for('kategori', success="Kategori berhasil dihapus!"))
    except Exception as e:
        print(e)
        return jsonify({'error': str(e), 'message': "Gagal menghapus data"}), 500

# Fungsi untuk menampilkan form edit kategori
def edit_kategori(id_kategori):
    kategori_data = kategoribarang.query.get(id_kategori)
    if kategori_data:
        return render_template("edit_kategori.html", kategori=kategori_data)
    else:
        return jsonify({'error': 'Data tidak ditemukan'}), 404

# Fungsi untuk menyimpan perubahan
def update_kategori(id_kategori):
    try:
        kategori_data = kategoribarang.query.get(id_kategori)
        if kategori_data:
            kategori_data.nama_kategori = request.form['nama_kategori']
            
            db.session.commit()
            return redirect(url_for('kategori'))
        else:
            return jsonify({'error': 'Data tidak ditemukan'}), 404
    except Exception as e:
        print(e)
        return jsonify({'error': str(e), 'message': 'Gagal memperbarui data'}), 500
