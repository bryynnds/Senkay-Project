from app.model import pengguna
from app import response, app, db
from flask import request

def index():
    try:
        Pengguna = pengguna.query.all()
        data = formatarray(Pengguna)
        return response.success(data, "success")
    except Exception as e:
        print(e)
        
def formatarray(datas):
    array = []
    for i in datas:
        array.append(singleObject(i))
    return array

def singleObject(data):
    data = {
    'idpengguna' : data.idpengguna,
    'nama_pengguna' : data.nama_pengguna,
    'username' : data.username,
    'password' : data.password,
    'created_at' : data.created_at,
    'updated_at' : data.updated_at
    }
    return data