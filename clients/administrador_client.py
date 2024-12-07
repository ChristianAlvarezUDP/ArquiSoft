import socket
import json

def request(bus_ip, bus_port, service_name, message):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((bus_ip, bus_port))
        request = f"{service_name}:{message}"
        client_socket.sendall(request.encode('utf-8'))
        response = client_socket.recv(1024)

        return response.decode('utf-8')
    

def listar_usuarios():
    


def logout():
    return "break"

if __name__ == '__main__':
    locked_in = True

    comandos = {
        "listar usuarios": lambda x: listar_usuarios(),
        "agregar usuario": lambda x: agregar_usuario(),
        "crear reporte": lambda x: crear_reporte(),
        "logout": lambda x: logout(),
    }

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