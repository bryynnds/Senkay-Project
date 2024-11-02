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
from weasyprint import HTML
import io
from flask import make_response
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from io import BytesIO

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
    
@app.route('/tambah_barang', methods=['GET'])
def tambah_barang():
    return DataBarangController.tambah_barang()

@app.route('/save_barang', methods=['POST'])
def save_barang():
    return DataBarangController.save()

@app.route('/edit_barang/<int:id_barang>', methods=['GET'])
def edit_barang_route(id_barang):
    return DataBarangController.edit_barang(id_barang)

@app.route('/update_barang/<int:id_barang>', methods=['POST'])
def update_barang_route(id_barang):
    return DataBarangController.update_barang(id_barang)

@app.route('/delete_barang/<int:id_barang>', methods=['GET'])
def delete_barang_route(id_barang):
    return DataBarangController.delete_barang(id_barang)


@app.route('/supplier', methods=['GET', 'POST'])
def supplier():
    if request.method == 'GET':
        return SupplierController.index()
    else:
        return SupplierController.save()
    
@app.route('/tambah_supplier')
def tambah_supplier():
    return render_template('tambah_supplier.html')

@app.route('/simpan_supplier', methods=['POST'])
def simpan_supplier():
    return SupplierController.save()

@app.route('/hapus_supplier/<id_supplier>', methods=['GET'])
def hapus_supplier(id_supplier):
    return SupplierController.hapus_supplier(id_supplier)

@app.route('/edit_supplier/<id_supplier>', methods=['GET'])
def edit_supplier_route(id_supplier):
    return SupplierController.edit_supplier(id_supplier)

@app.route('/update_supplier/<id_supplier>', methods=['POST'])
def update_supplier_route(id_supplier):
    return SupplierController.update_supplier(id_supplier)

@app.route('/kategori', methods=['GET', 'POST'])
def kategori():
    if request.method == 'GET':
        return KategoriBarangController.index()
    else:
        return KategoriBarangController.save()
    
@app.route('/tambah_kategori')
def tambah_kategori():
    return render_template('tambah_kategori.html')

@app.route('/simpan_kategori', methods=['POST'])
def simpan_kategori():
    return KategoriBarangController.save()

@app.route('/hapus_kategori/<id_kategori>', methods=['GET'])
def hapus_kategori(id_kategori):
    return KategoriBarangController.hapus_kategori(id_kategori)

@app.route('/edit_kategori/<id_kategori>', methods=['GET'])
def edit_kategori_route(id_kategori):
    return KategoriBarangController.edit_kategori(id_kategori)

@app.route('/update_kategori/<id_kategori>', methods=['POST'])
def update_kategori_route(id_kategori):
    return KategoriBarangController.update_kategori(id_kategori)


@app.route('/barang_masuk', methods=['GET', 'POST'])
def barang_masuk():
    if request.method == 'GET':
        return BarangMasukController.index()
    else:
        return BarangMasukController.save()

@app.route('/tambah_transaksimasuk', methods=['GET'])
def tambah_transaksimasuk():
    return BarangMasukController.tambah_transaksi()

@app.route('/save_transaksimasuk', methods=['POST'])
def save_transaksimasuk():
    return BarangMasukController.save()

@app.route('/delete_transaksi/<id_transaksi>', methods=['GET'])
def delete_transaksi(id_transaksi):
    return BarangMasukController.delete_transaksi(id_transaksi)

# Barang Keluar
@app.route('/barang_keluar', methods=['GET', 'POST'])
def barang_keluar():
    if request.method == 'GET':
        return BarangKeluarController.index()
    else:
        return BarangKeluarController.save()

@app.route('/tambah_transaksikeluar', methods=['GET'])
def tambah_transaksikeluar():
    return BarangKeluarController.tambah_transaksikeluar()

@app.route('/save_transaksikeluar', methods=['POST'])
def save_transaksikeluar():
    return BarangKeluarController.save()

@app.route('/delete_transaksikeluar/<id_transaksi>', methods=['GET'])
def delete_transaksikeluar(id_transaksi):
    return BarangKeluarController.delete_transaksikeluar(id_transaksi)

@app.route('/cetak_barang_masuk', methods=['GET'])
def cetak_barang_masuk():
    return BarangMasukController.cetak_transaksi_masuk()

@app.route('/cetak_barang_keluar', methods=['GET'])
def cetak_barang_keluar():
    return BarangKeluarController.cetak_transaksi_keluar()

