from app.model.supplier import supplier
from app import db
from flask import request, render_template, jsonify, redirect, url_for, flash

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
        flash('Data supplier berhasil ditambahkan', 'success')
        return redirect(url_for('supplier'))
    except Exception as e:
        print(e)
        flash('Gagal menambahkan data supplier', 'danger')
        return redirect(url_for('supplier'))
    
def hapus_supplier(id_supplier):
    try:
        supplier_data = supplier.query.get(id_supplier)
        if supplier_data:
            db.session.delete(supplier_data)
            db.session.commit()
            flash('Data supplier berhasil dihapus', 'success')
            return redirect(url_for('supplier'))
        else:
            flash('Data supplier tidak ditemukan', 'warning')
            return redirect(url_for('supplier'))
    except Exception as e:
        print(e)
        flash('Gagal menghapus data supplier', 'danger')
        return redirect(url_for('supplier'))
    
def edit_supplier(id_supplier):
    supplier_data = supplier.query.get(id_supplier)
    if supplier_data:
        return render_template("edit_supplier.html", supplier=supplier_data)
    else:
        return jsonify({'error': 'Data tidak ditemukan'}), 404

# Fungsi untuk menyimpan perubahan
def update_supplier(id_supplier):
    try:
        supplier_data = supplier.query.get(id_supplier)
        if supplier_data:
            supplier_data.nama_supplier = request.form['nama_supplier']
            supplier_data.alamat_supplier = request.form['alamat_supplier']
            supplier_data.telepon_supplier = request.form['telepon_supplier']
            
            db.session.commit()
            flash('Data supplier berhasil diperbarui', 'success')
            return redirect(url_for('supplier'))
        else:
            flash('Data supplier tidak ditemukan', 'warning')
            return redirect(url_for('supplier'))
    except Exception as e:
        print(e)
        flash('Gagal memperbarui data supplier', 'danger')
        return redirect(url_for('supplier'))

