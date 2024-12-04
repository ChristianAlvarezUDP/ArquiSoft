import socket
import json

def client_request(bus_host, bus_port, service_name, message):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((bus_host, bus_port))
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

    response = client_request('127.0.0.1', 5000, 'login', json.dumps(data))

    response = json.loads(response)

    if 'status' not in response:
        return False

    return response['status'] == "correct"


def listar_auditorias():
    client_request('127.0.0.1', 5000, 'login', json.dumps(data))
    return "hola"


def logout():
    return "break"


if __name__ == '__main__':
    locked_in = True

    comandos = {
        "listar auditorias": lambda x: listar_auditorias(),
        "logout": lambda x: logout()
    }

    while True:
        print("Realizar login")
        username = input("Usuario > ")
        password = input("Contraseña > ")

        if login(username, password):
            locked_in = True
            break
        else:
            print("Credenciales incorrectas")
 
    while locked_in:
        for comando in comandos.keys():
            print(comando)

        comando = input("Comando > ").lower()

        if comando not in comandos:
            continue

        x = comandos[comando](1)

        if x == "break":
            break