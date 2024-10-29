# DashboardController.py
from app.model.barang import barang
from app import db
from flask import render_template, jsonify
from app.model.transaksimasuk import transaksimasuk
from app.model.transaksikeluar import transaksikeluar
from app.model.supplier import supplier
from app.model.kategoribarang import kategoribarang

def index():
    try:
        total_barang = db.session.query(barang).count()
        total_barang_masuk = db.session.query(transaksimasuk).count()
        total_barang_keluar = db.session.query(transaksikeluar).count()
        total_supplier = db.session.query(supplier).count()
        total_kategori = db.session.query(kategoribarang).count()
        
        # Query barang dengan stok di bawah 50
        barang_minimum = db.session.query(barang).filter(barang.stok < 50).all()

        # Pass data to the template
        return render_template(
            "dashboard.html",
            total_barang=total_barang,
            total_barang_masuk=total_barang_masuk,
            total_barang_keluar=total_barang_keluar,
            total_supplier=total_supplier,
            total_kategori=total_kategori,
            barang_minimum=barang_minimum
        )
    except Exception as e:
        print(e)
        return {"error": str(e), "message": "Gagal mengambil data"}, 500
