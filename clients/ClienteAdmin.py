import json
import os
import time
import datetime
from utils import Colores, input_int, request


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

    group_index = input_int(" > ") - 1

    group_id = response['groups'][group_index][0]

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

import json

def crear_formularios():
    name = input("Nombre del formulario > ")
    print("Ingrese preguntas. Cuando haya ingresado todas, escriba [S]. Para cancelar o eliminar la pregunta anterior, escriba [C].")

    preguntas = []
    while True:
        pregunta = input("Pregunta > ").strip()
        if pregunta.upper() == "S":
            # Finalizar la creación de preguntas
            break
        elif pregunta.upper() == "C":
           
            if preguntas:
                eliminada = preguntas.pop()
                print(f"Pregunta eliminada: '{eliminada}'")
            else:
                print("Cancelado")
                break
        else:
            preguntas.append(pregunta)
    
    
    data = {
        "comando" : "insert_form",
        "name": name,
        "preguntas": preguntas
    }

    response = request('127.0.0.1', 5000, 'GestionFormulariosService.py', json.dumps(data))

    
    print(f"Formulario '{name}' creado y guardado como {name.replace(' ', '_')}_formulario.json.")



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


## Auditorias

def get_auditoria(auditoria_id):
    data = {
        "comando": 'get_auditoria',
        'auditoria_id': auditoria_id
    }
        
    response = request('127.0.0.1', 5000, 'AuditoriaService.py', json.dumps(data))
    return json.loads(response)


def get_formulario(formulario_id):
    data = {
        "comando": 'get_form',
        'body': {
            'id_grupo_campos': formulario_id
        }
    }
        
    response = request('127.0.0.1', 5000, 'GestionFormulariosService.py', json.dumps(data))
    return json.loads(response)


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
            print(f"{i + 1:<5} | {auditoria['formulario']:<15} | {auditoria['fecha']:<20} | {auditoria['bus']:<7} | {auditoria['tipo']:<15} | {auditoria['auditor']:<20}")

        comando = input(Colores.OKCYAN + "Ver auditoria [ID] o .salir > " + Colores.ENDC)

        if comando == ".salir":
            return
        
        auditoria_id = auditorias['auditorias'][int(comando) - 1]['id']
        
        ver_auditoria(auditoria_id)


def ver_auditoria(auditoria_id):
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

    comando = input(Colores.OKCYAN + ".eliminar, .modificar o Enter > " + Colores.ENDC)

    if comando == ".eliminar":
        eliminar_auditoria(auditoria_id)

    if comando == ".modificar":
        eliminar_auditoria(auditoria_id)


def editar_auditoria(auditoria_id):
    datos = get_auditoria()
    preguntas = get_formulario(datos['id_grupo_campos'])
    
    response = {
        "comando": 'edit',
        "body": {
            "marca_temporal": datos['marca_temporal'],
            "fecha" : datos['fecha'],
            "id_grupo_campos" : datos['id_grupo_campos'],
            "id_bus" : datos['id_bus'],
            "id_tipo_auditoria" : datos['id_tipo_auditoria'],
            "id_auditor" : datos['id_auditor'],
            "respuestas" : []
        }
    }


def ver_resumen():
    data = {
        "comando": 'get_all_auditorias'
    }

    response = request('127.0.0.1', 5000, 'AuditoriaService.py', json.dumps(data))
    auditorias = json.loads(response)

    date_format = '%Y-%m-%d %H:%M:%S'
    auditorias_24h = [auditoria for auditoria in auditorias['auditorias'] if datetime.datetime.now() - datetime.datetime.strptime(auditoria[2], date_format) <= datetime.timedelta(hours=24)]

    print(Colores.HEADER + "Numero de auditorias: " + Colores.ENDC + str(len(auditorias)))

    print(Colores.HEADER + "Numero de auditorias en las ultimas 24 horas: "  + Colores.ENDC + str(len(auditorias_24h)))
    print(Colores.HEADER + "Buses auditados en las ultimas 24 horas: "  + Colores.ENDC)
    for auditoria in auditorias_24h:
        print(" - " + auditoria[4])

    input(Colores.OKCYAN + "Presione enter para continuar... > " + Colores.ENDC)


def generar_reporte():
    while True:
        data = {
            'comando': 'get_all_forms'
        }

        response = request('127.0.0.1', 5000, 'GestionFormulariosService.py', json.dumps(data))
        response = json.loads(response)

        forms = list(response['forms'].values())

        os.system('cls')
        print(Colores.HEADER + "Generar Reporte" + Colores.ENDC)
        for i, form in enumerate(forms):
            print(f"{i + 1}.- {form['nombre']}")

        comando = input(Colores.OKCYAN + "[ID] Formulario o .salir > " + Colores.ENDC) 

        if comando == ".salir":
            return
        
        try:
            form_index = int(comando) - 1
        except ValueError:
            continue

        if not 0 <= form_index < len(forms):
            continue

        data = {
            'comando': 'generar_reporte',
            'id_form': forms[form_index]
        }

        response = request('127.0.0.1', 5000, 'GenerateReportService.py', json.dumps(data))
        response = json.loads(response)

        if response['status'] == 'correct':
            print(Colores.OKGREEN + 'Reporte generado con exito!' + Colores.ENDC)
            time.sleep(3)

        if response['status'] == 'error':
            print(Colores.FAIL + response['error'] + Colores.ENDC)
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
        ("Generar Reporte", lambda x: generar_reporte()),
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