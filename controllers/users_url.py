from models.usuario import Usuario
from __init__ import app
from flask import Flask,render_template,request,redirect

@app.route('/usuarios')
def usuarios():
    usuarios = Usuario.show_users()
    return render_template('usuarios.html',usuarios=usuarios)

@app.route('/usuario/show/<int:user_id>')
def show_user(user_id):
    data = {
        "id": user_id
    }
    usuario = Usuario.get_one_user(data)
    fav_books = Usuario.fav_books(data)
    libros_restantes = Usuario.libros_no_favoritos(data)
    return render_template('show_user.html',usuario=usuario,fav_books=fav_books,libros_restantes = libros_restantes)

@app.route('/usuario/crear')
def crear_user():
    return render_template('add_user.html')

@app.route('/usuario/agregar/procesar',methods=['POST'])
def usuario_agregar():
    data = {
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name']
    }
    Usuario.guardar(data)
    return redirect('/usuarios')

@app.route('/usuario/agregar_favorito', methods = ['POST'])
def agregar_libro_fav():
    usuario_id = request.form['usuario_id']
    libro_id = request.form['libro_id']
    data = {
        "usuario_id": usuario_id,
        "libro_id": libro_id
    }
    Usuario.agregar_libro_favorito(data)
    return redirect('/usuarios')

