import socket
import json
import os
import os

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
    
def login(username, password):
    data = {
        "comando": "login",
        "username": username,
        "password": password,
        "permisos": "digitador"
    }

    response = request('127.0.0.1', 5000, 'AutentificacionService.py', json.dumps(data))
    return json.loads(response)

def logout():
    return "break"

#TODO: Revisar direcciones de servicios, cambiar comandos

def request(bus_ip, bus_port, service_name, message):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((bus_ip, bus_port))
        request = f"{service_name}:{message}"
        client_socket.sendall(request.encode('utf-8'))
        response = client_socket.recv(1024)

        return response.decode('utf-8')
    
def retrieveAuditoriaAnswersByID():
    data = {
        "comando": 'retrieve',
        "body": {
            "id" : id
        }
    }
    response = request('127.0.0.1', 5000, 'AuditoriaService.py', json.dumps(data))
    if response:
        response = json.loads(response)
    else:
        print ("No recibe respuesta")
    print(response)

def retrieveAuditoriaByID(id):
    data = {
        "comando": 'retrieveAuditoriaByID',
        "body": {
            "id" : id
        }
    }
    response = request('127.0.0.1', 5000, 'auditorias_serviceXDD.py', json.dumps(data))
    if response:
        response = json.loads(response)
    else:
        print ("No recibe respuesta")
    return response

def retrieveCampos(id_grupo_campos):
    data = {
        "comando": 'retrieve',
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

    
def retrieveGruposCampos():
    data = {
        "comando": 'register'
    }
    response = request('127.0.0.1', 5000, 'serviceRetrieveGruposCampos.py', json.dumps(data))
    if response:
        response = json.loads(response)
        return response['body']['nombre']
    else:
        print ("No recibe respuesta")
        return "error"

def addAuditoria(id, marca_temporal, fecha, id_grupo_campos, id_bus, id_tipo_auditoria, id_auditor, respuestas):
    data = {
        "comando": 'add',
        "body": {
            "id" : id,
            "marca_temporal": marca_temporal,
            "fecha" : fecha,
            "id_grupo_campos" : id_grupo_campos,
            "id_bus" : id_bus,
            "id_tipo_auditoria" : id_tipo_auditoria,
            "id_auditor" : id_auditor,
            "respuestas" : respuestas 
        }
    }
    response = request('127.0.0.1', 5000, 'auditorias_serviceXDD.py', json.dumps(data))
    if response:
        response = json.loads(response)
    else:
        print ("No recibe respuesta")
    print(response)
    return response

def answerCampos(id_grupo_campos):
    data = {
        "comando": 'retrieve',
        "body": {
            "id_grupo_campos" : id_grupo_campos
        }
    }
    response = request('127.0.0.1', 5000, 'serviceRetrieveCampos.py', json.dumps(data))
    if response:
        response = json.loads(response)
    else:
        print ("No recibe respuesta")
        return "error"
    respuestas = []
    for campo in response['body']:
        print(f"Responda: {campo}")
        respuestaCampo = input(" > ")
        respuestas.append(respuestaCampo)
    return respuestas

#Funciones de la interfaz
def registerAuditoria():
    #Cambiar por un FOR
    print(f"Seleccione id_grupo_campos: {retrieveGruposCampos()}")
    id_grupo_campos = input(" > ")
    print("Escriba id")
    id = input(" > ")
    print("Escriba marca_temporal")
    marca_temporal = input(" > ")
    print("Escriba fecha")
    fecha = input(" > ")
    print("Escriba id_bus")
    id_bus = input(" > ")
    print("Escriba id_tipo_auditoria")
    id_tipo_auditoria = input(" > ")
    print("Escriba id_auditor")
    id_auditor = input(" > ")
    
    respuestas = answerCampos(id_grupo_campos)
    response = addAuditoria(id, marca_temporal, fecha, id_grupo_campos, id_bus, id_tipo_auditoria, id_auditor, respuestas)
    return response

def editAuditoria():
    print("Escriba id de la auditoria a editar")
    idAuditoria = input(" > ")
    
    respuestas = retrieveAuditoriaAnswersByID(idAuditoria)
    datos = retrieveAuditoriaByID(idAuditoria)
    preguntas = retrieveCampos(datos['id_grupo_campos'])
    
    response = {
        "comando": 'edit',
        "body": {
            "id" : id,
            "marca_temporal": datos['marca_temporal'],
            "fecha" : datos['fecha'],
            "id_grupo_campos" : datos['id_grupo_campos'],
            "id_bus" : datos['id_bus'],
            "id_tipo_auditoria" : datos['id_tipo_auditoria'],
            "id_auditor" : datos['id_auditor'],
            "respuestas" : respuestas 
        }
    }
    
    while True:
        print(f"ID: {datos['id']}\n Marca Temporal: {datos['marca_temporal']}\n Fecha: {datos['fecha']}\n ID Grupo Campos: {datos['id_grupo_campos']}\n ID Bus: {datos['id_bus']}\n ID Tipo Auditoria: {datos['id_tipo_auditoria']}\n ID Auditor: {datos['id_auditor']}")
        print("Respuestas Formulario:")
        for respuesta in respuestas:
            print(f"[{respuesta.enumerate()}] Pregunta: {preguntas[respuesta.enumerate()]}")
            print(f"Respuesta: {respuesta}")
        
        print("Seleccione el campo a editar:")
        print("1. Marca Temporal")
        print("2. Fecha")
        print("3. ID Grupo Campos")
        print("4. ID Bus")
        print("5. ID Tipo Auditoria")
        print("6. ID Auditor")
        print("7. Respuestas")
        print("8. Enviar Cambios")
        print("9. Salir")

        opcion = int(input(" > "))

        if opcion == 1:
            print("Escriba nueva Marca Temporal")
            response["body"]['marca_temporal'] = input(" > ")
        elif opcion == 2:
            print("Escriba nueva Fecha")
            response["body"]['fecha'] = input(" > ")
        elif opcion == 3:
            print("Escriba nuevo ID Grupo Campos")
            response["body"]['id_grupo_campos'] = input(" > ")
        elif opcion == 4:
            print("Escriba nuevo ID Bus")
            response["body"]['id_bus'] = input(" > ")
        elif opcion == 5:
            print("Escriba nuevo ID Tipo Auditoria")
            response["body"]['id_tipo_auditoria'] = input(" > ")
        elif opcion == 6:
            print("Escriba nuevo ID Auditor")
            response["body"]['id_auditor'] = input(" > ")
        elif opcion == 7:
            print("Elija la respuesta a editar")
            preguntaEditar = input(" > ")    
            print("Escriba nueva respuesta")
            preguntaEditada = input(" > ")
            response["body"]["respuestas"][preguntaEditar] = preguntaEditada
        elif opcion == 8:
            response = request('127.0.0.1', 5000, 'serviceRetrieveCampos.py', json.dumps(response))
            if response:
                response = json.loads(response)
            else:
                print ("No recibe respuesta")
                return "error"
        elif opcion == 9:
            return "break"
        else:
            print("Opción no válida")


def login(username, password):
    data = {
        "comando": "login",
        "username": username,
        "password": password,
        "permisos": "Digitador"
    }

    response = request('127.0.0.1', 5000, 'AutentificacionService.py', json.dumps(data))
    return json.loads(response)


if __name__ == '__main__':
    locked_in = False

    comandos = [
        ("Registrar Auditoria", lambda x: registerAuditoria()),
        ("Editar Auditoria", lambda x: editAuditoria()),
        ("Ver Auditorias", lambda x: ver_auditorias()),
        ("Logout", lambda x: logout()),
    ]

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