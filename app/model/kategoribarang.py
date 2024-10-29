from app import db
from datetime import datetime

class kategoribarang(db.Model):
    id_kategori = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    nama_kategori = db.Column(db.String(250), nullable=False)
    
    def __repr__(self):
        return '<kategoribarang {}>'.format(self.name)