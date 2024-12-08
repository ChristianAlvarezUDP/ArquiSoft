import socket
import json
import os
import time
import datetime


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

    input(Colores.OKCYAN + "Presione enter para continuar... > " + Colores.ENDC)


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


def eliminar_auditoria(auditoria_id):
    print("Esta seguro de que desea eliminar?")
    comando = input('[S] o [N]')

    if comando.lower() == 'n':
        return
    
    data = {
        "comando": 'delete_auditoria',
        "auditoria_id": auditoria_id 
    }

    response = request('127.0.0.1', 5000, 'AuditoriaService.py', json.dumps(data))


def ver_auditorias():
    while True:
        data = {
            "comando": 'get_all_auditorias'
        }

        os.system('cls')
        print(Colores.HEADER + "Num   | " + "%-15s" % "Formulario" + " | " + "%-20s" % "Fecha" + " | " + "%-7s" % "Bus" + " | " + "%-15s" % "Tipo Auditoria" + " | " + "%-20s" % "Auditor" + Colores.ENDC)
        response = request('127.0.0.1', 5000, 'AuditoriaService.py', json.dumps(data))
        auditorias = json.loads(response)

        
        for i, auditoria in enumerate(auditorias['auditorias']):
            print(f"{i + 1:<5} | {auditoria[3]:<15} | {auditoria[2]:<20} | {auditoria[4]:<7} | {auditoria[5]:<15} | {auditoria[6]:<20}")

        comando = input(Colores.OKCYAN + "Ver auditoria [ID] o .salir > " + Colores.ENDC)

        if comando == ".salir":
            return
        
        auditoria_id = auditorias['auditorias'][int(comando) - 1][0]
        
        data = {
            "comando": 'get_auditoria',
            'auditoria_id': auditoria_id
        }
        
        response = request('127.0.0.1', 5000, 'AuditoriaService.py', json.dumps(data))
        response = json.loads(response)
        
        os.system('cls')
        print(Colores.HEADER + "Auditoria" + Colores.ENDC)

        print(f"""{"%-20s" % 'Marca Temporal'}: {response['auditoria']['auditoria'][1]}
{"%-20s" % 'Fecha'}: {response['auditoria']['auditoria'][2]}
{"%-20s" % 'Bus'}: {response['auditoria']['auditoria'][4]}
{"%-20s" % 'Tipo Auditoria'}: {response['auditoria']['auditoria'][5]}
{"%-20s" % 'Auditor'}: {response['auditoria']['auditoria'][6]}
""")
        
        print(Colores.HEADER + response['auditoria']['auditoria'][3] + Colores.ENDC)
        
        for respuesta in response['auditoria']['respuestas']:
            print(f"{respuesta[0]:<20}: {respuesta[1]:<40}")

        comando = input(Colores.OKCYAN + ".eliminar o Enter > " + Colores.ENDC)

        if comando == ".eliminar":
            eliminar_auditoria(auditoria_id)


def ver_resumen():
    data = {
        "comando": 'get_all_auditorias'
    }

    response = request('127.0.0.1', 5000, 'AuditoriaService.py', json.dumps(data))
    auditorias = json.loads(response)

    date_format = '%Y-%m-%d %H:%M:%S'
    auditorias_24h = [auditoria for auditoria in auditorias['auditorias'] if datetime.datetime.now() - datetime.datetime.strptime(auditoria[2], date_format) <= datetime.timedelta(hours=24)]

    print(Colores.HEADER + "Numero de auditorias: "  + Colores.ENDC + str(len(auditorias)))

    print(Colores.HEADER + "Numero de auditorias en las ultimas 24 horas: "  + Colores.ENDC + str(len(auditorias_24h)))
    print(Colores.HEADER + "Buses auditados en las ultimas 24 horas: "  + Colores.ENDC)
    for auditoria in auditorias_24h:
        print(" - " + auditoria[4])


    input(Colores.OKCYAN + "Presione enter para continuar... > " + Colores.ENDC)


def logout():
    return "break"

if __name__ == '__main__':
    locked_in = False

    comandos = [
        ("Listar usuarios", lambda x: listar_usuarios()),
        ("Agregar usuario", lambda x: agregar_usuario()),
        ("Agregar grupo", lambda x: agregar_grupo()),
        ("Crear formularios", lambda x: crear_formularios()),
        ("Listar auditorias", lambda x: ver_auditorias()),
        ("Ver resumen", lambda x: ver_resumen()),
        ("Logout", lambda x: logout()),
    ]

    while True:
        os.system('cls')
        print(Colores.HEADER + "Login como Administrador" + Colores.ENDC)

        username = input("Usuario > ")
        password = input("Contraseña > ")

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