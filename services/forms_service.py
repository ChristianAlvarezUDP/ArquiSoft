import sys
import socket
import threading
import sqlite3
import json

def service_worker(service_name, host, port):
    print(f"{service_name} starting on {host}:{port}")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((host, port))
        server_socket.listen()
        while True:
            client_socket, _ = server_socket.accept()
            data = client_socket.recv(1024).decode('utf-8')
            print(f"{service_name} received: {data}")
            
            data = json.loads(data)

            if data["comando"] == "agregar":
                insert_form(data["nombre"], data["preguntas"])

            response = ""

            client_socket.sendall(response.encode('utf-8'))
            client_socket.close()


def insert_form(nombre, preguntas):
    """
    Insert the question into the SQLite database (arqui.db).
    The questions will be inserted into the 'campo_auditoria.titulo' table.
    """
    try:
        conn = sqlite3.connect('sqlite/arqui.db')
        cursor = conn.cursor()

        cursor.execute("INSERT INTO grupo_campos (nombre) VALUES (?)", (nombre,))
        group_id = cursor.lastrowid

        for pregunta in preguntas:
            cursor.execute("INSERT INTO campo_auditoria (titulo, id_grupo) VALUES (?, ?)", (pregunta, group_id))
        
        conn.commit()
        conn.close()
        print(f"Form inserted: {nombre}")
    except sqlite3.Error as e:
        print(f"Error inserting question into database: {e}")


def get_form(nombre, preguntas):
    """
    Insert the question into the SQLite database (arqui.db).
    The questions will be inserted into the 'campo_auditoria.titulo' table.
    """
    try:
        conn = sqlite3.connect('sqlite/arqui.db')
        cursor = conn.cursor()

        cursor.execute("INSERT INTO grupo_campos (nombre) VALUES (?)", (nombre,))
        group_id = cursor.lastrowid

        for pregunta in preguntas:
            cursor.execute("INSERT INTO campo_auditoria (titulo, id_grupo) VALUES (?, ?)", (pregunta, group_id))
        
        conn.commit()
        conn.close()
        print(f"Form inserted: {nombre}")
    except sqlite3.Error as e:
        print(f"Error inserting question into database: {e}")


if __name__ == '__main__':
    threading.Thread(target=service_worker, args=(sys.argv[0].split('/')[-1], '127.0.0.1', int(sys.argv[1]))).start()
