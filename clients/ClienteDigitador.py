import socket
import json
import os

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
    response = request('127.0.0.1', 5000, 'auditorias_serviceXDD.py', json.dumps(data))
    if response:
        response = json.loads(response)
    else:
        print ("No recibe respuesta")
    return response
    
def retrieveAllAuditorias(id):
    data = {
        "comando": 'retrieve',
    }
    response = request('127.0.0.1', 5000, 'auditorias_serviceXDD.py', json.dumps(data))
    if response:
        response = json.loads(response)
    else:
        print ("No recibe respuesta")
    print(response)
    
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
    
    print(f"ID: {datos['id']}\n Marca Temporal: {datos['marca_temporal']}\n Fecha: {datos['fecha']}\n ID Grupo Campos: {datos['id_grupo_campos']}\n ID Bus: {datos['id_bus']}\n ID Tipo Auditoria: {datos['id_tipo_auditoria']}\n ID Auditor: {datos['id_auditor']}")
    print("Respuestas Formulario:")
    for respuesta  in respuestas:
        print(f"Pregunta: {pregunta[respuesta.enumerate()]}")
        print(f"Respuesta: {respuesta}")
        
    
    data = {
        "comando": 'edit',
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


if __name__ == '__main__':
    
    #Funciones Necesarias
    
    print("Bienvenido a la interfaz de ClienteDigitador")
    print("Seleccione una opcion")
    print("1. Registrar Auditoria")
    print("2. Editar Auditoria")
    print("3. Eliminar Auditoria")
    print("4. Listar Auditorias")
    print("5. Salir")
    
    switcher = {
        1: registerAuditoria,
        2: editAuditoria,
        3: deleteAuditoria,
        4: retrieveAllAuditorias,
        5: exit
    }