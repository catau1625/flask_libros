from config.mysqlconnection import connectToMySQL
from models import libro

class Usuario:
    def __init__(self,data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.libros = []
        
    @classmethod
    def guardar(cls,data):
        query = "INSERT INTO usuarios (first_name,last_name,created_at,updated_at) VALUES (%(first_name)s,%(last_name)s,NOW(),NOW());"
        return connectToMySQL('esquema_libros').query_db(query,data)
    
    @classmethod
    def eliminar(cls,data):
        query = "DELETE FROM usuarios WHERE usuarios.id = %(id)s;"
        return connectToMySQL('esquema_libros').query_db(query,data)
    
    @classmethod
    def show_users(cls):
        query = "SELECT * FROM usuarios;"
        results = connectToMySQL('esquema_libros').query_db(query)
        usuarios = []
        for data in results:
            usuarios.append(data)
        return usuarios
    
    @classmethod
    def get_one_user(cls,data):
        query = "SELECT * FROM usuarios WHERE usuarios.id = %(id)s;"
        results = connectToMySQL('esquema_libros').query_db(query,data)
        user_data = results[0]
        return (user_data)
    
    @classmethod
    def fav_books(cls,data):
        query = "SELECT * FROM usuarios LEFT JOIN favoritos ON usuarios.id = favoritos.usuario_id LEFT JOIN libros ON favoritos.libro_id = libros.id WHERE usuarios.id = %(id)s;"
        results = connectToMySQL('esquema_libros').query_db(query,data)
        books = []
        for data in results:
            if data['libros.id'] == None:
                break
            data_books = {
                "id": data['libros.id'],
                "titulo": data['titulo'],
                "pag_num": data['pag_num'],
                "created_at": data['created_at'],
                "updated_at": data['updated_at']
            }
            books.append(libro.Libro(data_books))
        return books
    
    @classmethod
    def agregar_libro_favorito(cls,data):
        query = "INSERT INTO favoritos (usuario_id,libro_id) VALUES (%(usuario_id)s,%(libro_id)s);"
        return connectToMySQL('esquema_libros').query_db(query,data)
    
    @classmethod
    def libros_no_favoritos(cls,data):
        query = "SELECT * FROM libros WHERE libros.id NOT IN (SELECT libros.id FROM libros JOIN favoritos ON libros.id = favoritos.libro_id WHERE favoritos.usuario_id = %(id)s);"
        usuario = []
        results = connectToMySQL('esquema_libros').query_db(query,data)
        for data in results:
            if data['id'] == None:
                break
            data_books = {
                "id": data['id'],
                "titulo": data['titulo'],
                "pag_num": data['pag_num'],
                "created_at": data['created_at'],
                "updated_at": data['updated_at']
            }
            usuario.append(libro.Libro(data_books))
        return usuario
