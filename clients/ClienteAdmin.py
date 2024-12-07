import socket
import json

def request(bus_ip, bus_port, service_name, message):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((bus_ip, bus_port))
        request = f"{service_name}:{message}"
        client_socket.sendall(request.encode('utf-8'))
        response = client_socket.recv(1024)

        return response.decode('utf-8')
    

def login(username, password):
    data = {
        "comando": "login",
        "username": username,
        "password": password,
        "permisos": "administrador"
    }

    response = request('127.0.0.1', 5000, 'AutentificacionService.py', json.dumps(data))
    return json.loads(response)


def listar_usuarios():
    data = {
        "comando": 'get',
    }

    response = request('127.0.0.1', 5000, 'AutentificacionService.py', json.dumps(data))


def logout():
    return "break"

if __name__ == '__main__':
    locked_in = False

    comandos = {
        "listar usuarios": lambda x: listar_usuarios(),
        "agregar usuario": lambda x: agregar_usuario(),
        "crear reporte": lambda x: crear_reporte(),
        "logout": lambda x: logout(),
    }

    while True:
        print("Login")

        username = input("Usuario > ")
        password = input("Password > ")

        response = login(username, password)

        if response['status'] == 'correct':
            locked_in = True
            break
        else:
            print(response['message'])

    while locked_in:
        print("Seleccione comando:")

        for comando in comandos.keys():
            print(comando)

        comando = input("Comando > ").lower()

        if comando not in comandos:
            continue

        x = comandos[comando](1)

        if x == "break":
            break