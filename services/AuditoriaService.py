import sys
import socket
import threading
import sqlite3
import json

def service_worker(service_name, host, port):
    print(f"{service_name} iniciando en {host}:{port}")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((host, port))
        server_socket.listen()
        while True:
            client_socket, _ = server_socket.accept()
            data = client_socket.recv(1024).decode('utf-8')
            print(f"{service_name} received: {data}")

            data = json.loads(data)

            print(data)

            response = ""
            if data['comando'] == 'retrieve':
                conn = sqlite3.connect("sqlite/arqui.db")
                cursor = conn.cursor()
                
                cursor.execute(f'''
                    SELECT * FROM auditoria
                    ''')
                result = cursor.fetchall()
                print(f"Obtenido: {result}")
                response = json.dumps(result)
            
            if data['comando'] == 'add':
                conn = sqlite3.connect("sqlite/arqui.db")
                cursor = conn.cursor()
                cursor.execute(f'''
                    INSERT INTO auditoria VALUES (
                        {data['body']['id']}, {data['body']['marca_temporal']}, {data['body']['fecha']}, {data['body']['id_grupo_campos']}, {data['body']['id_bus']}, {data['body']['id_tipo_auditoria']}, {data['body']['id_auditor']}
                    )           
                    ''')
                result = conn.commit()
                print(f"Obtenido: {result}")
                response = json.dumps("Added one row")

            if data['comando'] == 'register':
                conn = sqlite3.connect("sqlite/arqui.db")
                cursor = conn.cursor()
                cursor.execute(f'''
                    INSERT INTO auditoria VALUES (
                        {data['body']['id']}, {data['body']['marca_temporal']}, {data['body']['fecha']}, {data['body']['id_grupo_campos']}, {data['body']['id_bus']}, {data['body']['id_tipo_auditoria']}, {data['body']['id_auditor']}
                    )           
                    ''')
                result = conn.commit()
                print(f"Obtenido: {result}")
                response = json.dumps("Added one row")
            if data['comando'] == 'login':
                result = login(data['data']['user'], data['data']['password'])

                if result:
                    response_data = {
                        'status': 'correct'
                    }
                
                else:
                    response_data = {
                        'status': 'error',
                        'mesage': 'Credenciales invalidas'
                    }

                response = json.dumps(response_data)

            else:
                response_data = {
                    'status': 'error',
                    'mesage': 'Comando incorrecto'
                }

                response = json.dumps(response_data)

            client_socket.sendall(response.encode('utf-8'))
            client_socket.close()


def login(username, password):
    conn = sqlite3.connect("sqlite/arqui.db")
    cursor = conn.cursor()

    cursor.execute(f'''
        SELECT * FROM usuario
        WHERE username = '{username}'
        AND password = '{password}';
        '''
    )

    result = cursor.fetchall()
    return len(result) > 0


if __name__ == '__main__':
    threading.Thread(target=service_worker, args=(sys.argv[0].split('/')[-1], '127.0.0.1', int(sys.argv[1]))).start()