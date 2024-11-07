from app import db
from datetime import datetime
from app.model import kategoribarang

class barang(db.Model):
    id_barang = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    # Ubah ondelete menjadi 'SET NULL' dan pastikan nullable=True
    id_kategori = db.Column(db.BigInteger, db.ForeignKey('kategoribarang.id_kategori', ondelete='SET NULL'), nullable=True)
    nama_barang = db.Column(db.String(250), nullable=False)
    deskripsi = db.Column(db.Text, nullable=True)
    stok = db.Column(db.Integer, nullable=False)
    harga = db.Column(db.Float, nullable=False)
    tanggal_ditambahkan = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return '<barang {}>'.format(self.nama_barang)
