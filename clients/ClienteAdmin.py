import socket
import json
import os
import time


class Colores:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


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
        "comando": 'get_users',
    }

    response = request('127.0.0.1', 5000, 'AutentificacionService.py', json.dumps(data))
    response = json.loads(response)

    print(Colores.BOLD + Colores.HEADER + "Usuarios" + Colores.ENDC)
    print(Colores.HEADER + "Nombre - Grupo" + Colores.ENDC)

    for usuario in response["usuarios"]:
        print(f"{usuario[0]} - {usuario[4]}")

    input("Presione enter para continuar... > ")


def agregar_usuario():
    username = input("Usuario > ")
    password = input("Contraseña > ")

    response = request('127.0.0.1', 5000, 'AutentificacionService.py', json.dumps({'comando': 'get_groups'}))
    response = json.loads(response)

    print(Colores.HEADER + "Seleccione un grupo:" + Colores.ENDC)

    for i, group in enumerate(response['groups']):
        print(f"{i + 1}.- {group[1]}")

    # TODO: arreglar INT input
    group_selected = int(input(" > ")) - 1

    group_id = response['groups'][group_selected][0]

    data = {
        "comando": 'add_user',
        'username': username,
        'password': password,
        'group_id': group_id
    }

    response = request('127.0.0.1', 5000, 'AutentificacionService.py', json.dumps(data))
    response = json.loads(response)

    print(Colores.OKGREEN + 'Usuario agregado con exito!' + Colores.ENDC)
    time.sleep(3)
    
def agregar_grupo():
    name = input("Nombre > ")
    data = {
        "comando": 'add_group',
        'nombre': name
    }

    response = request('127.0.0.1', 5000, 'AutentificacionService.py', json.dumps(data))
    response = json.loads(response)

    print(Colores.OKGREEN + 'Grupo agregado con exito!' + Colores.ENDC)
    time.sleep(3)


def logout():
    return "break"

if __name__ == '__main__':
    locked_in = False

    comandos = [
        ("listar usuarios", lambda x: listar_usuarios()),
        ("agregar usuario", lambda x: agregar_usuario()),
        ("agregar grupo", lambda x: agregar_grupo()),
        #("crear reporte", lambda x: crear_reporte()),
        ("logout", lambda x: logout()),
    ]

    while True:
        os.system('cls')
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
        os.system('cls')
        print(Colores.HEADER + "Seleccione comando:" + Colores.ENDC)

        for i, comando in enumerate(comandos):
            print(f"{i + 1}.- {comando[0]}")

        try:
            comando = int(input(Colores.OKGREEN + "Comando > " + Colores.ENDC)) - 1
        except KeyboardInterrupt:
            quit()
        except:
            continue

        if comando > len(comandos):
            continue
        
        os.system('cls')
        x = comandos[comando][1](1)

        if x == "break":
            break