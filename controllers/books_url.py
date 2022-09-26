from crypt import methods
from models.libro import Libro
from __init__ import app
from flask import render_template,request,redirect
from models.usuario import Usuario

@app.route('/')
def home():
    libros = Libro.show_books()
    return render_template('home.html',libros=libros)

@app.route('/libro/crear')
def crear_libro():
    return render_template('crear_libro.html')

@app.route('/libro/agregar/procesar',methods=['POST'])
def libro_agregar_procesar():
    data = {
        "titulo": request.form['titulo'],
        "pag_num": request.form['pag_num']
    }
    Libro.guardar(data)
    return redirect('/')

@app.route('/libro/show/<int:libro_id>')
def show_book(libro_id):
    data = {
        "id": libro_id
    }
    libro = Libro.get_one_book(data)
    fav_users = Libro.book_fans(data)
    not_fans = Libro.no_fans_of_this_book(data)
    return render_template('show_books.html',libro=libro,fav_users=fav_users,not_fans=not_fans)

@app.route('/agregar/fav/libro',methods=['POST'])
def agregar_fav_libro():
    data = {
        "usuario_id": request.form['user_id'],
        "libro_id": request.form['libro_id']
    }
    Usuario.agregar_libro_favorito(data)
    return redirect('/')

@app.route('/agregar/fan',methods=['POST'])
def agregar_fan():
    data = {
        "usuario_id": request.form['usuario_id'],
        "libro_id": request.form['libro_id']
    }
    Usuario.agregar_libro_favorito(data)
    return redirect('/')