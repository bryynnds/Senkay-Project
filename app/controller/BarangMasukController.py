from app import db, response
from flask import make_response, render_template, request, url_for, flash, redirect
from app.model.transaksimasuk import transaksimasuk
from app.model.barang import barang
from app.model.supplier import supplier
from datetime import datetime
import pytz
from weasyprint import HTML
import io

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
        # Mengambil data dari request
        id_barang = request.form.get('id_barang')
        jumlah = int(request.form.get('jumlah'))  # Pastikan jumlah adalah integer
        id_supplier = request.form.get('id_supplier')

        # Membuat instance transaksimasuk baru dengan tanggal otomatis
        jakarta_timezone = pytz.timezone('Asia/Jakarta')
        tanggal_masuk = datetime.now(jakarta_timezone)
        
        transaksimasuks = transaksimasuk(
            id_barang=id_barang,
            jumlah=jumlah,
            tanggal_masuk=tanggal_masuk,
            id_supplier=id_supplier
        )

        # Menambahkan transaksi ke database
        db.session.add(transaksimasuks)

        # Memperbarui stok di tabel barang
        barang_item = barang.query.filter_by(id_barang=id_barang).first()
        if barang_item:
            barang_item.stok += jumlah  # Tambah stok sesuai jumlah transaksi masuk
            db.session.commit()  # Commit perubahan stok

        flash('Transaksi baru berhasil ditambahkan dan stok diperbarui', 'success')
        return redirect(url_for('barang_masuk'))
    except Exception as e:
        print(e)
        db.session.rollback()  # Rollback jika ada error
        flash('Gagal menambahkan transaksi atau memperbarui stok', 'danger')
        return redirect(url_for('barang_masuk'))
    
def tambah_transaksi():
    try:
        barang_list = barang.query.all()
        supplier_list = supplier.query.all()
        return render_template("tambah_transaksimasuk.html", barang=barang_list, suppliers=supplier_list)
    except Exception as e:
        print(e)
        return response.badRequest([], "Gagal memuat halaman tambah transaksi")
    
def delete_transaksi(id_transaksi):
    try:
        Transaksi = transaksimasuk.query.filter_by(id_transaksi=id_transaksi).first()   
        
        if not Transaksi:
            flash("Transaksi tidak ditemukan", "danger")
            return redirect(url_for('barang_masuk'))
        
        db.session.delete(Transaksi)
        db.session.commit()
        flash("Transaksi berhasil dihapus", "success")
        return redirect(url_for('barang_masuk'))
    except Exception as e:
        print("Error:", e)
        flash("Gagal menghapus Transaksi", "danger")
        return redirect(url_for('barang_masuk'))
    
def cetak_transaksi_masuk():
    try:
        # Mengambil data transaksi masuk dengan join tabel barang dan supplier
        transaksi_masuk = db.session.query(
            transaksimasuk.id_transaksi,
            barang.nama_barang,
            transaksimasuk.jumlah,
            transaksimasuk.tanggal_masuk,
            supplier.nama_supplier
        ).join(barang, transaksimasuk.id_barang == barang.id_barang) \
         .join(supplier, transaksimasuk.id_supplier == supplier.id_supplier).all()

        # Render template menjadi HTML string
        html = render_template("cetak_barang_masuk.html", transaksi_masuk=transaksi_masuk)

        # Konversi HTML menjadi PDF
        pdf_file = HTML(string=html).write_pdf()

        # Mengirim PDF sebagai respons
        response = make_response(pdf_file)
        response.headers['Content-Type'] = 'application/pdf'
        response.headers['Content-Disposition'] = 'attachment; filename=transaksi_masuk.pdf'

        return response
    except Exception as e:
        print(e)
        flash("Gagal mencetak transaksi masuk", "danger")
        return redirect(url_for('barang_masuk'))

def index_karyawan():
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
        return render_template("/karyawan/barang_masuk_karyawan.html", transaksi_masuk=transaksi_masuk)
    except Exception as e:
        print(e)
        return response.badRequest([], "Gagal mengambil data barang masuk")
