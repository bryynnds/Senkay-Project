from app import db
from datetime import datetime

class supplier(db.Model):
    id_supplier = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    nama_supplier = db.Column(db.String(250), nullable=False)
    alamat_supplier = db.Column(db.Text, nullable=True)
    telepon_supplier = db.Column(db.String(20), nullable=True)
    
    def __repr__(self):
        return '<supplier {}>'.format(self.name)