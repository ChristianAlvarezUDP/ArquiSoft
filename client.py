import socket
import json

def request(bus_ip, bus_port, service_name, message):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((bus_ip, bus_port))
        request = f"{service_name}:{message}"
        client_socket.sendall(request.encode('utf-8'))
        response = client_socket.recv(1024)
        print(f"Response: {response.decode('utf-8')}")

        return response.decode('utf-8')


def login(username, password):
    data = {
        "comando": 'login',
        "data": {
            "user": username,
            "password": password
        }
    }

    response = request('127.0.0.1', 5000, 'auth_service.py', json.dumps(data))

    response = json.loads(response)

    if 'status' not in response:
        return False

    return response['status'] == "correct"


def listar_auditorias():
    data = {
    }

    request('127.0.0.1', 5000, 'auth_service.py', json.dumps(data))
    return "hola"


def logout():
    return "break"

def agregar_formulario():
    data = {
    }

    request('127.0.0.1', 5000, 'createForm_service.py', json.dumps(data))

if __name__ == '__main__':
    locked_in = True

    comandos = {
        "listar auditorias": lambda x: listar_auditorias(),
        "logout": lambda x: logout(),
        "agregar formulario": lambda x: agregar_formulario()
    }

    while locked_in:
        for comando in comandos.keys():
            print(comando)

        comando = input("Comando > ").lower()

        if comando not in comandos:
            continue

        x = comandos[comando](1)

        if x == "break":
            break

