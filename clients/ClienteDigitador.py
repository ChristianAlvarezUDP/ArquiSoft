import json
import os
import datetime
import time
from utils import Colores, input_int, request

    
def login(username, password):
    data = {
        "comando": "login",
        "username": username,
        "password": password,
        "permisos": "Digitador"
    }

    response = request('127.0.0.1', 5000, 'AutentificacionService.py', json.dumps(data))
    return json.loads(response)

def logout():
    return "break"

def get_auditoria(auditoria_id):
    data = {
        "comando": 'get_auditoria',
        'auditoria_id': auditoria_id
    }
        
    response = request('127.0.0.1', 5000, 'AuditoriaService.py', json.dumps(data))
    response = json.loads(response)
    return response

def get_formulario(id_grupo_campos):
    data = {
        "comando": 'get_all_forms_group',
        "body": {
            "id_grupo_campos" : id_grupo_campos
        }
    }
    response = request('127.0.0.1', 5000, 'GestionFormulariosService.py', json.dumps(data))
    if response:
        response = json.loads(response)
    else:
        print ("No recibe respuesta")
    return response

def eliminar_auditoria(auditoria_id):
    print("Esta seguro de que desea eliminar?")
    comando = input('[S] o [N] > ')

    if comando.lower() == 'n':
        return
    
    elif comando.lower() == 's':
        data = {
            "comando": 'delete_auditoria',
            "auditoria_id": auditoria_id 
        }

        response = request('127.0.0.1', 5000, 'AuditoriaService.py', json.dumps(data))


def ver_buses():
    data = {
        "comando": 'get_all_buses'
    }

    response = request('127.0.0.1', 5000, 'GestionBusesService.py', json.dumps(data))
    buses = json.loads(response)['buses']

    print(Colores.HEADER + "Num   | " + "%-15s" % "ID" + " | " + "%-20s" % "N Interno" + " | " + "%-7s" % "Año" + " | " + "%-15s" % "Chasis" + " | " + "%-20s" % "Plazas" + Colores.ENDC)
    for i, bus in enumerate(buses):
        print(f"{i + 1:<5} | {bus['id']:<15} | {bus['n_interno']:<20} | {bus['anio']:<7} | {bus['chasis']:<15} | {bus['plazas']:<20}")

    input(Colores.OKCYAN + "Presione enter para continuar... > " + Colores.ENDC)
        


def ver_auditorias():
    while True:
        data = {
            "comando": 'get_all_auditorias'
        }

        response = request('127.0.0.1', 5000, 'AuditoriaService.py', json.dumps(data))
        auditorias = json.loads(response)

        os.system('cls')
        print(Colores.HEADER + "Num   | " + "%-15s" % "Formulario" + " | " + "%-20s" % "Fecha" + " | " + "%-7s" % "Bus" + " | " + "%-15s" % "Tipo Auditoria" + " | " + "%-20s" % "Auditor" + Colores.ENDC)
        for i, auditoria in enumerate(auditorias['auditorias']):
            print(f"{i + 1:<5} | {auditoria['formulario']:<15} | {auditoria['marca_temporal']:<20} | {auditoria['bus']:<7} | {auditoria['tipo']:<15} | {auditoria['auditor']:<20}")

        comando = input(Colores.OKCYAN + "Ver auditoria [ID] o .salir > " + Colores.ENDC)

        if comando == ".salir":
            return
        
        try:
            auditoria_index = int(comando) - 1
        except ValueError:
            continue

        if not 0 <= auditoria_index < len(auditorias['auditorias']):
            continue
        
        auditoria_id = auditorias['auditorias'][auditoria_index]['id']
        
        ver_auditoria(auditoria_id)


def ver_auditoria(auditoria_id):
    data = {
        "comando": 'get_auditoria',
        'auditoria_id': auditoria_id
    }
        
    response = request('127.0.0.1', 5000, 'AuditoriaService.py', json.dumps(data))
    response = json.loads(response)
    auditoria = response['auditoria']['auditoria']

    os.system('cls')
    print(Colores.HEADER + "Auditoria " + str(auditoria['id']) + Colores.ENDC)

    print(f"""{"%-20s" % 'Fecha'}: {auditoria['marca_temporal']}
{"%-20s" % 'Bus'}: {auditoria['n_interno']}
{"%-20s" % 'Tipo Auditoria'}: {auditoria['tipo']}
{"%-20s" % 'Auditor'}: {auditoria['auditor']}
""")
    
    print(Colores.HEADER + auditoria['formulario'] + Colores.ENDC)
    
    for respuesta in response['auditoria']['respuestas']:
        print(f"{respuesta['titulo']:<20}: {respuesta['valor']:<40}")

    comando = input(Colores.OKCYAN + ".eliminar, .modificar o Enter > " + Colores.ENDC)

    if comando == ".eliminar":
        eliminar_auditoria(auditoria_id)

    if comando == ".modificar":
        editAuditoria(auditoria_id)

    
def retrieveGruposCampos():
    data = {
        "comando": 'get_all_forms_group',
    }
    response = request('127.0.0.1', 5000, 'GestionFormulariosService.py', json.dumps(data))
    if response:
        response = json.loads(response)
        return response['body']
    else:
        print ("No recibe respuesta")
        return "error"

def addAuditoria(marca_temporal, id_grupo_campos, id_bus, id_tipo_auditoria, id_auditor, respuestas):
    data = {
        "comando": 'registerAuditoria',
        "body": {
            "marca_temporal": marca_temporal,
            "fecha" : "2024-12-10 01:00:00",
            "id_grupo_campos" : id_grupo_campos,
            "id_bus" : id_bus,
            "id_tipo_auditoria" : id_tipo_auditoria,
            "id_auditor" : id_auditor,
            "respuestas" : respuestas 
        }
    }
    response = request('127.0.0.1', 5000, 'AuditoriaService.py', json.dumps(data))
    if response:
        response = json.loads(response)
    else:
        print ("No recibe respuesta")
    return response

def answerCampos(id_grupo_campos):
    data = {
        "comando": 'get_form',
        "body": {
            "id_grupo_campos" : id_grupo_campos
        }
    }
    response = request('127.0.0.1', 5000, 'GestionFormulariosService.py', json.dumps(data))
    if response:
        response = json.loads(response)
    else:
        print ("No recibe respuesta")
        return "error"
    
    print("\n" + Colores.HEADER + response['body']['formulario']['nombre'] + Colores.ENDC)
    
    respuestas = []
    for campo in response['body']['preguntas']:
        respuestaCampo = input(Colores.OKCYAN + f"{campo['titulo']} > " + Colores.ENDC)
        respuestas.append({
            "id": campo['id'],
            "titulo": respuestaCampo
        })
    return respuestas

#Funciones de la interfaz
def registerAuditoria():
    while True:
        os.system('cls')
        grupoCampos = retrieveGruposCampos()
        print(Colores.HEADER + f"Seleccione Formulario: " + Colores.ENDC)
        for i, grupoCampo in enumerate(grupoCampos):
            print(f"{i + 1}.-  {grupoCampo["nombre"]}")

        comando = input(Colores.OKCYAN + " [ID] Formulario o .salir > " + Colores.ENDC)

        if comando == '.salir':
            return
        
        try:
            formulario_index = int(comando) - 1
        except ValueError:
            continue

        if not 0 <= formulario_index < len(grupoCampos):
            continue

        break

    id_grupo_campos = grupoCampos[formulario_index]["id"]
    marca_temporal = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    os.system('cls')
    print(Colores.HEADER + 'General' + Colores.ENDC)

    id_bus = input(Colores.OKCYAN + "Bus > " + Colores.ENDC)
    id_tipo_auditoria = input(Colores.OKCYAN + "Tipo Auditoria > " + Colores.ENDC)
    id_auditor = input(Colores.OKCYAN + "Auditor > " + Colores.ENDC)
    
    respuestas = answerCampos(id_grupo_campos)
    response = addAuditoria(marca_temporal, id_grupo_campos, id_bus, id_tipo_auditoria, id_auditor, respuestas)
    return response


def editAuditoria(auditoria_id):
    data = {
        "comando": 'get_auditoria',
        'auditoria_id': auditoria_id
    }
    
    response = request('127.0.0.1', 5000, 'AuditoriaService.py', json.dumps(data))
    response = json.loads(response)
    
    auditoria = response['auditoria']['auditoria']
    
    new_data = {
        "comando": 'editAuditoria',
        "body": {
            "auditoria_id": auditoria['id'],
            "marca_temporal": auditoria['marca_temporal'],
            "fecha" : auditoria['fecha'],
            "id_grupo_campos" : auditoria['id_grupo_campos'],
            "id_bus" : auditoria['id_bus'],
            "id_tipo_auditoria" : auditoria['id_tipo_auditoria'],
            "id_auditor" : auditoria['id_auditor'],
            "respuestas" : response['auditoria']['respuestas']
        }
    }
    
    while True:
        os.system('cls')
        print(Colores.HEADER + 'Editar auditoria' + Colores.ENDC +
f"""
--- {"%-20s" % 'Fecha'}: {new_data['body']['marca_temporal']}
1.- {"%-20s" % 'ID Bus'}: {new_data['body']['id_bus']}
2.- {"%-20s" % 'ID Tipo Auditoria'}: {new_data['body']['id_tipo_auditoria']}
3.- {"%-20s" % 'ID Auditor'}: {new_data['body']['id_auditor']}
        """)
        print(Colores.HEADER + "Grupo " + auditoria['formulario'] + Colores.ENDC)
            
        for i, respuesta in enumerate(new_data['body']['respuestas'], start=4):
            print(f"{i}.- {respuesta['titulo']:<20}: {respuesta['valor']:<40}")

        opcion = input(Colores.OKCYAN + "[Numero] Campo a editar o .guardar > " + Colores.ENDC)

        if opcion == '.guardar':
            result = request('127.0.0.1', 5000, 'AuditoriaService.py', json.dumps(new_data))
            if result:
                result = json.loads(result)
                print(Colores.OKGREEN + 'Auditoria editada con exito!' + Colores.ENDC)
                time.sleep(3)
                break
            else:
                print ("No recibe respuesta")
                return "error"
            
        try:
            opcion = int(opcion)
        except ValueError:
            continue

        if not 1 <= opcion <= 3 + len(new_data['body']['respuestas']):
            continue

        if opcion == 1:
            print("Escriba nuevo ID Bus")
            new_data["body"]['id_bus'] = input(" > ")
        elif opcion == 2:
            print("Escriba nuevo ID Tipo Auditoria")
            new_data["body"]['id_tipo_auditoria'] = input(" > ")
        elif opcion == 3:
            print("Escriba nuevo ID Auditor")
            new_data["body"]['id_auditor'] = input(" > ")
        elif 4 <= opcion < 4 + len(new_data['body']['respuestas']):
            preguntaEditada = input(f"{new_data['body']['respuestas'][opcion - 4]['titulo']} > ")
            new_data['body']['respuestas'][opcion - 4]['valor'] = preguntaEditada
        else:
            print("Opción no válida")


if __name__ == '__main__':
    locked_in = True

    comandos = [
        ("Registrar Auditoria", lambda x: registerAuditoria()),
        ("Ver Auditorias", lambda x: ver_auditorias()),
        ("Ver Buses", lambda x: ver_buses()),
        ("Logout", lambda x: logout())
    ]

    try:
        while True:
            os.system('cls')
            print(Colores.HEADER + "Login como Digitador" + Colores.ENDC)

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

    except KeyboardInterrupt:
        quit()
