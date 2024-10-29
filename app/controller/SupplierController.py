from app.model.supplier import supplier
from app import db
from flask import request, render_template, jsonify, redirect, url_for

def index():
    try:
        Supplier = supplier.query.all()  # Mengambil semua data Supplier dari tabel
        data = formatarray(Supplier)           # Format data
        return render_template("supplier.html", values=data)  # Menampilkan data ke template
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
        'id_supplier' : data.id_supplier,
        'nama_supplier' : data.nama_supplier,
        'alamat_supplier' : data.alamat_supplier,
        'telepon_supplier' : data.telepon_supplier
    }

def save():
    try:
        id_supplier = request.form.get('id_supplier')
        nama_supplier = request.form.get('nama_supplier')
        alamat_supplier = request.form.get('alamat_supplier')
        telepon_supplier = request.form.get('telepon_supplier')
        
        Supplier = supplier(id_supplier=id_supplier, nama_supplier=nama_supplier, alamat_supplier=alamat_supplier, telepon_supplier=telepon_supplier)
        db.session.add(Supplier)
        db.session.commit()
        return redirect(url_for('supplier', success=True))
    except Exception as e:
        print(e)
        return jsonify({'error': str(e), 'message': "Gagal menyimpan data"}), 500
