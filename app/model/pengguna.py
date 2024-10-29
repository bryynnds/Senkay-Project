from app import db
from datetime import datetime

class pengguna(db.Model):
    idpengguna=db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    nama_pengguna=db.Column(db.String(250), nullable=False)
    username=db.Column(db.String(250), nullable=False)
    password=db.Column(db.String(250), nullable=False)
    created_at=db.Column(db.DateTime, default=datetime.utcnow)
    updated_at=db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return '<pengguna {}>'.format(self.name)