import sys
import socket
import threading
import json
import sqlite3

bus_ip = '127.0.0.1'
bus_port = 5000

TablaDePrivilegios = {
    "Admin": "2af264b99ff1d93e9477482ed9037db8",
    "Digitador": "3d17a2504f185d7cae5a0044a6040d18",
    "Auditor": "83088ecc77b52a62602337d2c37b4772"
}

TablaPrivilegiosJerarquia = {    
    "Admin": 3,
    "Digitador": 2,
    "Auditor": 1
}

def check_privileges(roleHash):
    role = next((r for r, h in TablaDePrivilegios.items() if h == roleHash), None)
    
    if role is None:
        return "Invalid role hash"
    
    return TablaPrivilegiosJerarquia.get(role, "Role not found")

def login(username, password):
    try:
        conn = sqlite3.connect("sqlite/arqui.db")
        cursor = conn.cursor()

        cursor.execute('''
            SELECT role FROM usuario
            WHERE username = ? AND password = ?;
        ''', (username, password))

        result = cursor.fetchone()

        if result:
            role = result[0]
            return TablaDePrivilegios.get(role, "Role not found")
        else:
            return "Invalid username or password"
    except sqlite3.Error as e:
        return f"Database error: {e}"
    finally:
        conn.close()



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
            client_socket.sendall(response.encode('utf-8'))
            client_socket.close()


def handle_command(data):
    if data['comando'] == 'login':
        success = login(data["username"], data["password"], data["permisos"])

        if success:
            return {
                'status': 'correct'
            }
        else:
            return {
                'status': 'error',
                'message': 'Credenciales incorrectas'
            }
    
    elif data['comando'] == 'get':
        return get_users()
    else:
        return {
            'status': 'error',
            'message': 'Comando incorrecto'
        }


def login(username, password, permisos):
    conn = sqlite3.connect("sqlite/arqui.db")
    cursor = conn.cursor()

    cursor.execute(f'''
        SELECT * FROM usuario AS u
        JOIN grupo_usuario AS gu ON u.id_grupo = gu.id
        WHERE username = '{username}'
        AND password = '{password}'
        AND gu.nombre = {permisos};
        ''')

    result = cursor.fetchall()
    return len(result) > 0


def get_users():
    conn = sqlite3.connect("sqlite/arqui.db")
    cursor = conn.cursor()

    cursor.execute(f'''
        SELECT * FROM usuario;
        ''')
    
    result = cursor.fetchall()

    return result


if __name__ == '__main__':
    bus_ip = sys.argv[2]
    bus_port = int(sys.argv[3])

    threading.Thread(target=service_worker, args=(sys.argv[0].split('/')[-1], '127.0.0.1', int(sys.argv[1]))).start()
