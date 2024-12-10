import sys
import socket
import threading
import sqlite3
import json

def dict_factory(cursor, row):
    fields = [column[0] for column in cursor.description]
    return {key: value for key, value in zip(fields, row)}

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
            response = ""

            if data["comando"] == "agregar":
                insert_form(data["nombre"], data["preguntas"])

            if data["comando"] == "get_all_forms":
                form_data = get_all_forms()
                response = {
                    "status": "correct",
                    "forms": form_data
                }

                response = json.dumps(response)
                
            if data["comando"] == "get_all_forms_group":
                form_data = get_all_forms_group()

                response = {
                    "status": "correct",
                    "body": form_data
                }

                response = json.dumps(response)
            
            if data["comando"] == "get_form":
                form = get_form(data["body"]['id_grupo_campos'])

                response = {
                    "status": "correct",
                    "body": form
                }
                response = json.dumps(response)
            if data["comando"] == "insert_form":
                insert_form(data[name], data[preguntas])
                   
            client_socket.sendall(response.encode('utf-8'))
            client_socket.close()

def insert_form(nombre, preguntas):
    try:
        conn = sqlite3.connect('sqlite/arqui.db')
        cursor = conn.cursor()

        cursor.execute("INSERT INTO grupo_campos (nombre) VALUES (?)", (nombre))
        group_id = cursor.lastrowid

        for pregunta in preguntas:
            cursor.execute("INSERT INTO campo_auditoria (titulo, id_grupo) VALUES (?, ?)", (pregunta, group_id))
        
        conn.commit()
        conn.close()
        print(f"Form inserted: {nombre}")
    except sqlite3.Error as e:
        print(f"Error inserting question into database: {e}")

def get_all_forms_group():
    try:
        conn = sqlite3.connect('sqlite/arqui.db')
        conn.row_factory = dict_factory 
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM grupo_campos")
        forms = cursor.fetchall()

        conn.close()

        return forms
    except sqlite3.Error as e:
        print(f"Error getting form: {e}")
        return forms

def get_all_forms():
    try:
        conn = sqlite3.connect('sqlite/arqui.db')
        conn.row_factory = dict_factory 
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM grupo_campos")
        forms = cursor.fetchall()

        form_data = {}

        for form in forms:
            cursor.execute("SELECT * FROM campo_auditoria WHERE id_grupo = (?)", (form[0],))
            questions = [{"id": question[0], "titulo": question[2]} for question in cursor.fetchall()]

            form_data[form[0]] = {"id": form[0], "nombre": form[1], "preguntas": questions}

        conn.close()

        return form_data
    except sqlite3.Error as e:
        print(f"Error getting form: {e}")
        return {}

def get_form(form_id):
    try:
        conn = sqlite3.connect('sqlite/arqui.db')
        conn.row_factory = dict_factory 
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM grupo_campos WHERE id = (?)", (form_id,))
        form = cursor.fetchone()

        cursor.execute("SELECT * FROM campo_auditoria WHERE id_grupo = (?)", (form_id,))

        preguntas = cursor.fetchall()

        conn.close()
        return {'formulario': form, 'preguntas': preguntas}
    except sqlite3.Error as e:
        print(f"Error getting form: {e}")


if __name__ == '__main__':
    threading.Thread(target=service_worker, args=(sys.argv[0].split('/')[-1], '127.0.0.1', int(sys.argv[1]))).start()
