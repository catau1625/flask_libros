from config.mysqlconnection import connectToMySQL
from models import usuario

class Libro:
    def __init__(self,data):
        self.id = data['id']
        self.titulo = data['titulo']
        self.pag_num = data['pag_num']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.usuarios = []
        
    @classmethod
    def guardar(cls,data):
        query = "INSERT INTO libros (titulo,pag_num,created_at,updated_at) VALUES (%(titulo)s,%(pag_num)s,NOW(),NOW());"
        return connectToMySQL('esquema_libros').query_db(query,data)
    
    @classmethod
    def eliminar(cls,data):
        query = "DELETE FROM libros WHERE libros.id = %(id)s;"
        return connectToMySQL('esquema_libros').query_db(query,data)
    
    @classmethod
    def show_books(cls):
        query = "SELECT * FROM libros;"
        results = connectToMySQL('esquema_libros').query_db(query)
        libros = []
        for data in results:
            libros.append(data)
        return libros
    
    @classmethod
    def get_one_book(cls,data):
        query = "SELECT * FROM libros WHERE libros.id = %(id)s;"
        book_from_db = connectToMySQL('esquema_libros').query_db(query,data)
        return cls(book_from_db[0])
    
    @classmethod
    def book_fans(cls,data):
        query = "SELECT * FROM libros LEFT JOIN favoritos ON libros.id = favoritos.libro_id LEFT JOIN usuarios ON favoritos.usuario_id = usuarios.id WHERE libros.id = %(id)s;"
        results = connectToMySQL('esquema_libros').query_db(query,data)
        fans = []
        for data in results:
            fans_data = {
                "id": data['usuarios.id'],
                "first_name": data['first_name'],
                "last_name": data['last_name'],
                "created_at": data['usuarios.created_at'],
                "updated_at": data['usuarios.updated_at']
            }
            fans.append(usuario.Usuario(fans_data))
        return fans
    
    @classmethod
    def no_fans_of_this_book(cls,data):
        query = "SELECT * FROM usuarios WHERE usuarios.id NOT IN (SELECT usuarios.id FROM usuarios JOIN favoritos ON usuarios.id = favoritos.usuario_id WHERE favoritos.libro_id = %(id)s);"
        results = connectToMySQL('esquema_libros').query_db(query,data)
        no_fans_of = []
        for data in results:
            no_fans_data = {
                "id": data['id'],
                "first_name": data['first_name'],
                "last_name": data['last_name'],
                "created_at": data['created_at'],
                "updated_at": data['updated_at']
            }
            no_fans_of.append(usuario.Usuario(no_fans_data))
        return no_fans_of