#Gestión de biblioteca | Pablo P.H.
'''
Este programa gestiona una biblioteca permitiendo añadir, buscar, eliminar libros y registrar usuarios.
Los usuarios pueden pedir prestados y devolver libros, con un historial completo de préstamos.
Los datos se guardan en archivos JSON y se utilizan tablas hash para una gestión eficiente.
'''
import json
from datetime import datetime

#Clase para manejar la tabla hash
class HashTable:
    def __init__(self, size):
        self.size = size
        self.table = [[] for _ in range(size)]  #Inicializa la tabla con listas vacías

    #Función hash para mapear claves a índices de la tabla
    def _hash_function(self, key):
        return key % self.size


#Clase libro
class Book:
    def __init__(self, title, location, section, borrowed=False):
        self.title = title  # Título del libro
        self.location = location  # Ubicación física del libro
        self.section = section  # Sección donde se encuentra
        self.borrowed = borrowed  # Estado de préstamo (True si está prestado)
        self.borrowed_by = None  # Nombre del usuario que lo ha prestado
        self.borrow_date = None  # Fecha en la que se prestó el libro


#Clase usuario
class User:
    def __init__(self, user_id, name):
        self.user_id = user_id  # ID único del usuario
        self.name = name  #Nombre del usuario
        self.borrowed_books = []  #Lista de libros actualmente prestados por el usuario

    #Método para agregar un libro a la lista de libros prestados
    def borrow_book(self, book):
        self.borrowed_books.append(book)

    #Método para devolver un libro
    def return_book(self, book):
        self.borrowed_books.remove(book)


#Funciones para manejar los libros
def insert_book(hash_table, book):
    if search_book(hash_table, book.title):
        print(f"El libro '{book.title}' ya existe en la biblioteca.")
        return

    index = hash_table._hash_function(hash(book.title))
    bucket = hash_table.table[index]
    bucket.append(book)


def search_book(hash_table, title):
    index = hash_table._hash_function(hash(title))
    bucket = hash_table.table[index]

    for book in bucket:
        if book.title == title:
            return book

    return None


def remove_book(hash_table, title):
    index = hash_table._hash_function(hash(title))
    bucket = hash_table.table[index]

    for i, book in enumerate(bucket):
        if book.title == title:
            if not book.borrowed:
                del bucket[i]
                return book
            else:
                print(f"El libro '{title}' está prestado y no se puede eliminar.")
                return None

    print(f"El libro '{title}' no existe en la biblioteca.")
    return None


def list_books(hash_table):
    all_books = []
    for bucket in hash_table.table:
        for book in bucket:
            all_books.append(book)

    return all_books


def list_borrowed_books(hash_table):
    borrowed_books = []
    for bucket in hash_table.table:
        for book in bucket:
            if book.borrowed:
                borrowed_books.append(book)

    return borrowed_books


def list_available_books(hash_table):
    available_books = []
    for bucket in hash_table.table:
        for book in bucket:
            if not book.borrowed:
                available_books.append(book)
    return available_books


def borrow_book(hash_table, user_table, title, user_id, loan_history):
    #Busca el libro y el usuario en sus respectivas tablas
    book = search_book(hash_table, title)
    user = search_user(user_table, user_id)

    if not user:
        print(f"Usuario con ID '{user_id}' no encontrado. Regístralo antes de prestar libros.")
        return None

    if not book:  #Verifica si el libro no existe
        print(f"El libro '{title}' no se encuentra en la biblioteca.")
        return None

    if book and not book.borrowed:
        book.borrowed = True
        book.borrowed_by = user.name
        book.borrow_date = datetime.now()
        user.borrow_book(book)
        loan_history.add_loan(user, book, book.borrow_date)
        print(f"✅ Libro '{title}' prestado correctamente a {user.name}.")
        return book

    elif book:
        print(f"El libro '{title}' ya está prestado.")
    else:
        print(f"El libro '{title}' no está disponible.")

    return None


def return_book(book_table, user_table, book_title, user_id, loan_history):
    #Verifica si el usuario existe
    user = search_user(user_table, user_id)

    if not user:
        print(f"Usuario con ID '{user_id}' no encontrado.")
        return None

    #Verifica si el libro existe
    book = search_book(book_table, book_title)

    if not book:
        print(f"El libro '{book_title}' no existe en la biblioteca.")
        return None

    #Verifica si el libro está prestado y pertenece al usuario
    if book and book.borrowed and book.borrowed_by == user.name:
        book.borrowed = False
        book.borrowed_by = None
        book.borrow_date = None
        user.return_book(book)
        loan_history.add_return(book, user, datetime.now())
        print(f"\033[94mLibro '{book_title}' devuelto correctamente por {user.name}.\033[0m")
        return book

    elif book.borrowed and book.borrowed_by != user.name:
        print(f"El libro '{book_title}' está prestado por otro usuario, no por {user.name}.")
    else:
        print(f"El libro '{book_title}' no estaba prestado.")

    return None

#Funciones para manejar los usuarios
def insert_user(user_table, user):
    if not isinstance(user.user_id, int) or user.user_id <= 0:
        print("El ID de usuario debe ser un número entero positivo.")
        return

    if search_user(user_table, user.user_id):
        print(f"⚠️ El usuario con ID '{user.user_id}' ya existe.")
        return  # No insertamos el usuario si ya existe

    if search_user(user_table, user.user_id):
        print(f"El usuario con ID '{user.user_id}' ya existe.")
        return

    index = user_table._hash_function(user.user_id)
    bucket = user_table.table[index]
    bucket.append(user)
    print(f"✅ Usuario '{user.name}' añadido correctamente con ID {user.user_id}.")



def search_user(user_table, user_id):
    index = user_table._hash_function(user_id)
    bucket = user_table.table[index]

    for user in bucket:
        if user.user_id == user_id:
            return user

    return None


def list_users(user_table):
    all_users = []
    for bucket in user_table.table:
        for user in bucket:
            all_users.append(user)

    return all_users


#Clase para manejar el historial de préstamos
class LoanHistory:
    def __init__(self):
        self.history = []

    def add_loan(self, user, book, borrow_date):
        loan_entry = {
            'user_id': user.user_id,
            'user_name': user.name,
            'book_title': book.title,
            'borrow_date': borrow_date.isoformat()
        }
        self.history.append(loan_entry)

    def add_return(self, book, user, return_date):
        return_entry = {
            'user_id': user.user_id,
            'user_name': user.name,
            'book_title': book.title,
            'return_date': return_date.isoformat()
        }
        self.history.append(return_entry)

    def save_history_to_json(self, filename='loan_history.json'):
        with open(filename, 'w') as file:
            json.dump(self.history, file, indent=4)

    def load_history_from_json(self, filename='loan_history.json'):
        try:
            with open(filename, 'r') as file:
                self.history = json.load(file)
        except FileNotFoundError:
            print("No se encontró el archivo de historial de préstamos.")

    def display_history(self):
        if not self.history:
            print("\nNo hay registros en el historial de préstamos.")
            return

        print("\n 📚 Historial de préstamos:")
        for entry in self.history:
            if 'borrow_date' in entry:
                print(
                    f"- Libro: '{entry['book_title']}', Prestado a: {entry['user_name']} (ID: {entry['user_id']}), Fecha: {entry['borrow_date']}")
            if 'return_date' in entry:
                print(
                    f"- Libro: '{entry['book_title']}' devuelto por: {entry['user_name']} (ID: {entry['user_id']}), Fecha: {entry['return_date']}")

#Funciones para guardar y cargar libros
def save_books_to_json(book_table, filename='books.json'):
    books_data = []
    for bucket in book_table.table:
        for book in bucket:
            book_info = {
                'title': book.title,
                'location': book.location,
                'section': book.section,
                'borrowed': book.borrowed,
                'borrowed_by': book.borrowed_by,
                'borrow_date': book.borrow_date.isoformat() if book.borrow_date else None
            }
            books_data.append(book_info)

    with open(filename, 'w') as file:
        json.dump(books_data, file, indent=4)


def load_books_from_json(book_table, filename='books.json'):
    try:
        with open(filename, 'r') as file:
            books_data = json.load(file)

        for book_info in books_data:
            book = Book(book_info['title'], book_info['location'], book_info['section'], book_info['borrowed'])
            if book_info['borrowed']:
                book.borrowed_by = book_info['borrowed_by']
                book.borrow_date = datetime.fromisoformat(book_info['borrow_date'])
            insert_book(book_table, book)

    except FileNotFoundError:
        print("No se encontró el archivo JSON. Se creará uno nuevo.")


#Funciones para gestionar los usuarios en el json

def save_users_to_json(user_table, filename='users.json'):
    users_data = []
    for bucket in user_table.table:
        for user in bucket:
            user_info = {
                'user_id': user.user_id,
                'name': user.name,
                'borrowed_books': [book.title for book in user.borrowed_books]  # Guarda títulos de libros prestados
            }
            users_data.append(user_info)

    with open(filename, 'w') as file:
        json.dump(users_data, file, indent=4)


def load_users_from_json(user_table, filename='users.json'):
    try:
        with open(filename, 'r') as file:
            users_data = json.load(file)

        for user_info in users_data:
            user = User(user_info['user_id'], user_info['name'])
            # No es necesario añadir libros prestados aquí, ya que se manejarán al cargar los libros
            insert_user(user_table, user)

    except FileNotFoundError:
        print("No se encontró el archivo JSON de usuarios. Se creará uno nuevo.")


#Programa principal
book_table = HashTable(101)
user_table = HashTable(101)
loan_history = LoanHistory()

#Carga los datos desde archivos JSON al inicio
load_books_from_json(book_table)
load_users_from_json(user_table)  #Cargar usuarios al inicio
loan_history.load_history_from_json()

while True:
    opcion_menu = input(
        '''\n-- 📚 Menú 📚 --
1. Gestión de Libros:
   1.1 - Añadir libro
   1.2 - Buscar libro
   1.3 - Eliminar libro
   1.4 - Ver libros disponibles

2. Gestión de Préstamos:
   2.1 - Prestar libro
   2.2 - Devolver libro
   2.3 - Ver libros prestados
   2.4 - Ver historial de préstamos

3. Gestión de Usuarios:
   3.1 - Añadir usuario
   3.2 - Listar usuarios

4. Salir
Selecciona una opción: '''
    ).strip()

    print("-" * 50)

    if opcion_menu == '1.1':
        title = input("Introduce el título del libro: ").strip()
        location = input("Introduce la localización del libro: ").strip()
        section = input("Introduce la sección del libro: ").strip()
        if not title or not location or not section:
            print("⚠️ Todos los campos deben ser completados.")
            continue
        book = Book(title, location, section, borrowed=False)
        insert_book(book_table, book)
        save_books_to_json(book_table)
        print(f"✅ Libro '{title}' añadido correctamente.")

        input("\nPresiona Enter para continuar...")  # Pausa


    elif opcion_menu == '1.2':
        title = input("Introduce el título del libro que quieres buscar: ").strip()
        book = search_book(book_table, title)
        if book:
            print(f"✅ Libro encontrado: {book.title}, Sección: {book.section}, Localización: {book.location}")
        else:
            print("⚠️ El libro no se encontró.")

        input("\nPresiona Enter para continuar...")

    elif opcion_menu == '1.3':
        title = input("Introduce el título del libro que quieres eliminar: ").strip()
        removed_book = remove_book(book_table, title)
        if removed_book:
            print(f"✅ Libro '{removed_book.title}' eliminado exitosamente.")
        save_books_to_json(book_table)

        input("\nPresiona Enter para continuar...")

    elif opcion_menu == '1.4':
        available_books = list_available_books(book_table)
        if available_books:
            print("\nLibros disponibles:")
            for book in available_books:
                print(f" - Título: {book.title}, Sección: {book.section}, Ubicación: {book.location}")
        else:
            print("No hay libros disponibles en este momento.")

        input("\nPresiona Enter para continuar...")

    elif opcion_menu == '2.1':
        while True:  #Validar que el ID sea un número válido
            try:
                user_id = int(input("Introduce el ID del usuario: ").strip())
                break
            except ValueError:
                print("⚠️ Por favor, introduce un número válido para el ID del usuario.")
        book_title = input("Introduce el título del libro que quieres prestar: ").strip()
        book = borrow_book(book_table, user_table, book_title, user_id, loan_history)
        if book: #Solo guarda cambios si el prestamo ha sido exitoso
            save_books_to_json(book_table)
            loan_history.save_history_to_json()

        input("\nPresiona Enter para continuar...")

    elif opcion_menu == '2.2':
        book_title = input("Introduce el título del libro a devolver: ").strip()

        while True:
            try:
                user_id = int(input("Introduce el ID del usuario: "))
                break
            except ValueError:
                print("⚠️ Por favor, introduce un número válido para el ID del usuario.")

        return_book(book_table, user_table, book_title, user_id, loan_history)

        input("\nPresiona Enter para continuar...")


    elif opcion_menu == '2.3':
        borrowed_books = list_borrowed_books(book_table)
        if borrowed_books:
            print("\n📚 Lista de libros prestados:")
            for book in borrowed_books:
                print(f" - Título: {book.title}, Prestado a: {book.borrowed_by}, Fecha: {book.borrow_date}")
        else:
            print("No hay libros prestados actualmente.")

        input("\nPresiona Enter para continuar...")

    elif opcion_menu == '2.4':
        loan_history.display_history()

        input("\nPresiona Enter para continuar...")

    elif opcion_menu == '3.1':
        while True:
            try:
                user_id = int(input("Introduce el ID del usuario: "))
                break
            except ValueError:
                print("Por favor, introduce un número válido para el ID del usuario.")

        name = input("Introduce el nombre del usuario: ").strip()
        if not name:
            print("El nombre no puede estar vacío.")
            continue

        user = User(user_id, name)
        insert_user(user_table, user)
        save_users_to_json(user_table)

        input("\nPresiona Enter para continuar...")


    elif opcion_menu == '3.2':
        users = list_users(user_table)
        if users:
            print("\nLista de usuarios registrados:")
            for user in users:
                print(f" - ID: {user.user_id}, Nombre: {user.name}")
        else:
            print("No hay usuarios registrados.")

        input("\nPresiona Enter para continuar...")

    elif opcion_menu == '4':
        print("Saliendo del programa...")
        break
    else:
        print("⚠️Introduce una opción válida")

    #Separador
    print("-" * 50)
