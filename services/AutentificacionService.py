import sys
import socket
import threading
import json
import sqlite3

bus_ip = '127.0.0.1'
bus_port = 5000




def service_worker(service_name, host, port):
    print(f"{service_name} iniciando en {host}:{port}")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((host, port))
        server_socket.listen()
        while True:
            client_socket, _ = server_socket.accept()
            data = client_socket.recv(1024).decode('utf-8')

            data = json.loads(data)
            response = handle_command(data)

            print(f"{service_name} received: {data}")
            client_socket.sendall(json.dumps(response).encode('utf-8'))
            client_socket.close()


def handle_command(data):
    if data['comando'] == 'login':
        success = login(data["username"], data["password"], data["permisos"].lower())

        if success:
            return {
                'status': 'correct',
                'idUsuario': success
            }
        else:
            return {
                'status': 'error',
                'message': 'Credenciales incorrectas'
            }
    
    elif data['comando'] == 'get_users':
        users = get_users()

        return {
            'status': 'correct',
            'usuarios': users
        }
    elif data['comando'] == 'get_groups':
        groups = get_groups()

        return {
            'status': 'correct',
            'groups': groups
        }
    elif data['comando'] == 'add_user':
        success = add_user(data['username'], data['password'], data['group_id'])

        return {
            'status': 'correct'
        }
    elif data['comando'] == 'add_group':
        success = add_group(data['nombre'])

        return {
            'status': 'correct'
            
        }
    else:
        return {
            'status': 'error',
            'message': 'Comando incorrecto'
        }


def login(username, password, permisos):
    conn = sqlite3.connect("sqlite/arqui.db")
    cursor = conn.cursor()

    cursor.execute(f'''
        SELECT id_grupo FROM usuario AS u
        JOIN grupo_usuario AS gu ON u.id_grupo = gu.id
        WHERE username = (?)
        AND password = (?)
        AND LOWER(gu.nombre) = (?)
        ''', (username, password, permisos))

    result = cursor.fetchall()
    return result


def get_users():
    conn = sqlite3.connect("sqlite/arqui.db")
    cursor = conn.cursor()

    cursor.execute(f'''
        SELECT * FROM usuario AS u
        JOIN grupo_usuario AS gu ON u.id_grupo = gu.id;
        ''')
    
    result = cursor.fetchall()
    conn.close()

    return result

def get_groups():
    conn = sqlite3.connect("sqlite/arqui.db")
    cursor = conn.cursor()

    cursor.execute(f'''
        SELECT * FROM grupo_usuario;
        ''')
    
    result = cursor.fetchall()
    conn.close()

    return result

def add_user(username, password, group_id):
    try:
        conn = sqlite3.connect("sqlite/arqui.db")
        cursor = conn.cursor()

        cursor.execute(f'''
            INSERT INTO usuario (username, password, id_grupo) VALUES (?, ?, ?)
            ''', (username, password, group_id))
        
        conn.commit()
        conn.close()

        return True
    except:
        return False


def add_group(name):
    try:
        conn = sqlite3.connect("sqlite/arqui.db")
        cursor = conn.cursor()

        cursor.execute(f'''
            INSERT INTO grupo_usuario (nombre) VALUES (?)
            ''', (name,))
        
        conn.commit()
        conn.close()

        return True
    except:
        return False
    

if __name__ == '__main__':
    bus_ip = sys.argv[2]
    bus_port = int(sys.argv[3])

    threading.Thread(target=service_worker, args=(sys.argv[0].split('/')[-1], '127.0.0.1', int(sys.argv[1]))).start()
