from app import app, db
from flask import render_template, request, redirect, url_for, flash
from app.model.barang import barang
from app.model.kategoribarang import kategoribarang
from app.model.transaksimasuk import transaksimasuk
from app.model.transaksikeluar import transaksikeluar
from app.controller import KategoriBarangController
from app.controller import SupplierController
from app.controller import DataBarangController
from app.controller import BarangKeluarController
from app.controller import BarangMasukController
from app.controller import DashboardController

# Dashboard
@app.route('/', methods=['GET', 'POST'])
def dashboard():
    return DashboardController.index()

@app.route('/data_barang', methods=['GET', 'POST'])
def data_barang():
    if request.method == 'GET':
        return DataBarangController.index()
    else:
        return DataBarangController.save()


@app.route('/supplier', methods=['GET', 'POST'])
def supplier():
    if request.method == 'GET':
        return SupplierController.index()
    else:
        return SupplierController.save()

@app.route('/kategori', methods=['GET', 'POST'])
def kategori():
    if request.method == 'GET':
        return KategoriBarangController.index()
    else:
        return KategoriBarangController.save()

@app.route('/data_barang/add', methods=['GET', 'POST'])
def add_barang():
    if request.method == 'POST':
        new_barang = barang(
            id_kategori=request.form['id_kategori'],
            nama_barang=request.form['nama_barang'],
            deskripsi=request.form['deskripsi'],
            kategori=request.form['kategori'],
            stok=request.form['stok'],
            harga=request.form['harga']
        )
        db.session.add(new_barang)
        db.session.commit()
        flash('Barang berhasil ditambahkan!')
        return redirect(url_for('data_barang'))
    return render_template('add_barang.html')

@app.route('/data_barang/edit/<int:id>', methods=['GET', 'POST'])
def edit_barang(id):
    barang_edit = barang.query.get_or_404(id)
    if request.method == 'POST':
        barang_edit.nama_barang = request.form['nama_barang']
        barang_edit.deskripsi = request.form['deskripsi']
        barang_edit.kategori = request.form['kategori']
        barang_edit.stok = request.form['stok']
        barang_edit.harga = request.form['harga']
        db.session.commit()
        flash('Barang berhasil diperbarui!')
        return redirect(url_for('data_barang'))
    return render_template('edit_barang.html', barang=barang_edit)

@app.route('/data_barang/delete/<int:id>')
def delete_barang(id):
    barang_delete = barang.query.get_or_404(id)
    db.session.delete(barang_delete)
    db.session.commit()
    flash('Barang berhasil dihapus!')
    return redirect(url_for('data_barang'))

# Barang Masuk
# Barang Masuk
@app.route('/barang_masuk', methods=['GET', 'POST'])
def barang_masuk():
    if request.method == 'GET':
        return BarangMasukController.index()
    else:
        return BarangMasukController.save()


@app.route('/barang_masuk/add', methods=['GET', 'POST'])
def add_barang_masuk():
    if request.method == 'POST':
        new_transaksi_masuk = transaksimasuk(
            id_barang=request.form['id_barang'],
            jumlah=request.form['jumlah'],
            id_supplier=request.form['id_supplier'],
            id_pengguna=request.form['id_pengguna']
        )
        db.session.add(new_transaksi_masuk)
        db.session.commit()
        flash('Barang Masuk berhasil ditambahkan!')
        return redirect(url_for('barang_masuk'))
    return render_template('add_barang_masuk.html')

@app.route('/barang_masuk/delete/<int:id>')
def delete_barang_masuk(id):
    transaksi_masuk_delete = transaksimasuk.query.get_or_404(id)
    db.session.delete(transaksi_masuk_delete)
    db.session.commit()
    flash('Barang Masuk berhasil dihapus!')
    return redirect(url_for('barang_masuk'))

# Barang Keluar
@app.route('/barang_keluar')
def barang_keluar():
    return BarangKeluarController.index()

@app.route('/barang_keluar/add', methods=['GET', 'POST'])
def add_barang_keluar():
    if request.method == 'POST':
        new_transaksi_keluar = transaksikeluar(
            id_barang=request.form['id_barang'],
            jumlah=request.form['jumlah'],
            id_pengguna=request.form['id_pengguna']
        )
        db.session.add(new_transaksi_keluar)
        db.session.commit()
        flash('Barang Keluar berhasil ditambahkan!')
        return redirect(url_for('barang_keluar'))
    return render_template('add_barang_keluar.html')

@app.route('/barang_keluar/delete/<int:id>')
def delete_barang_keluar(id):
    transaksi_keluar_delete = transaksikeluar.query.get_or_404(id)
    db.session.delete(transaksi_keluar_delete)
    db.session.commit()
    flash('Barang Keluar berhasil dihapus!')
    return redirect(url_for('barang_keluar'))

@app.route('/laporan_barangmasuk')
def laporan_barangmasuk():
    laporan_masuk = transaksimasuk.query.all()
    return render_template('laporan_barangmasuk.html', laporan_masuk=laporan_masuk)

@app.route('/laporan_barangkeluar')
def laporan_barangkeluar():
    laporan_keluar = transaksikeluar.query.all()
    return render_template('laporan_barangkeluar.html', laporan_keluar=laporan_keluar)

