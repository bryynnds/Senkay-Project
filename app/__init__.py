from flask import Flask
from config import config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config.from_object(config)
db= SQLAlchemy(app)
migrate=Migrate(app, db)

from app import routes
from app.model import pengguna
from app.model import kategoribarang
from app.model import barang
from app.model import supplier
from app.model import transaksimasuk
from app.model import transaksikeluar

app.secret_key = 'esa130219231'