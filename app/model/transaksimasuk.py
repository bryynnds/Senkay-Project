from app import db
from datetime import datetime
from app.model import barang
from app.model import supplier
from app.model import pengguna

class transaksimasuk(db.Model):
    id_transaksi = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    id_barang = db.Column(db.BigInteger, db.ForeignKey('barang.id_barang', ondelete='CASCADE'), nullable=False)
    jumlah = db.Column(db.Integer, nullable=False)
    tanggal_masuk = db.Column(db.DateTime, default=datetime.utcnow)
    id_supplier = db.Column(db.BigInteger, db.ForeignKey('supplier.id_supplier', ondelete='CASCADE'), nullable=False) 
    
    def __repr__(self):
        return '<transaksimasuk {}>'.format(self.name)