from app import db
from datetime import datetime
from app.model import barang
from app.model import pengguna

class transaksikeluar(db.Model):
    id_transaksi = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    id_barang = db.Column(db.BigInteger, db.ForeignKey('barang.id_barang', ondelete='SET NULL'), nullable=True)
    jumlah = db.Column(db.Integer, nullable=False)
    tanggal_keluar = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return '<transaksikeluar {}>'.format(self.id_transaksi)
