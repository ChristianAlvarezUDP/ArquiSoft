import socket
import json

def request(bus_ip, bus_port, service_name, message):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((bus_ip, bus_port))
        request = f"{service_name}:{message}"
        client_socket.sendall(request.encode('utf-8'))
        response = client_socket.recv(1024)

        return response.decode('utf-8')
    
def retriveAuditoria():
    data = {
        "comando": 'retrieve',
    }
    response = request('127.0.0.1', 5000, 'auditorias_serviceXDD.py', json.dumps(data))
    if response:
        response = json.loads(response)
    else:
        print ("No recibe respuesta")
    print(response)

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
    print(response)
    return response
    
def addAuditoria(id, marca_temporal, fecha, id_grupo_campos, id_bus, id_tipo_auditoria, id_auditor):
    data = {
        "comando": 'add',
        "body": {
            "id" : id,
            "marca_temporal": marca_temporal,
            "fecha" : fecha,
            "id_grupo_campos" : id_grupo_campos,
            "id_bus" : id_bus,
            "id_tipo_auditoria" : id_tipo_auditoria,
            "id_auditor" : id_auditor
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
    array = []
    while True:
        for campo in response['body']:
            print(f"{campo}")
            respuestaCampo = input(" > ")
            array.append(respuestaCampo)

def registerAuditoria():
    data = {
        "comando": 'register'
    }
    response = request('127.0.0.1', 5000, 'serviceRetrieveCampos.py', json.dumps(data))
    if response:
        response = json.loads(response)
    else:
        print ("No recibe respuesta")
        return "error"
    while True:
        print(f"Seleccione id_grupo_campos: {response['body']['id_grupo_campos']}")
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
        
        addAuditoria(id, marca_temporal, fecha, id_grupo_campos, id_bus, id_tipo_auditoria, id_auditor)
        
        
        print("Desea agregar otra auditoria? (si/no)")
        respuesta = input(" > ")
        if respuesta == "no":
            break
    return response

if __name__ == '__main__':
    locked_in = True

    comandos = {
        "listar auditorias": lambda x: listar_auditorias(),
        "agregar formulario": lambda x: crear_formulario(),
        "responder auditoria": lambda x: responder_auditoria(),
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