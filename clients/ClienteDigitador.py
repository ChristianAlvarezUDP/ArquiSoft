import socket
import json
import os
import datetime
from utils import input_int, Colores

    
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

#TODO: Revisar direcciones de servicios, cambiar comandos

def request(bus_ip, bus_port, service_name, message):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((bus_ip, bus_port))
        request = f"{service_name}:{message}"
        client_socket.sendall(request.encode('utf-8'))
        response = client_socket.recv(1024)

        return response.decode('utf-8')

def get_auditoria(auditoria_id):
    data = {
        "comando": 'get_auditoria',
        'auditoria_id': auditoria_id
    }
        
    response = request('127.0.0.1', 5000, 'AuditoriaService.py', json.dumps(data))
    response = json.loads(response)
    print(response) 
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

def addAuditoria(marca_temporal, fecha, id_grupo_campos, id_bus, id_tipo_auditoria, id_auditor, respuestas):
    data = {
        "comando": 'registerAuditoria',
        "body": {
            "marca_temporal": marca_temporal,
            "fecha" : fecha,
            "id_grupo_campos" : id_grupo_campos,
            "id_bus" : id_bus,
            "id_tipo_auditoria" : id_tipo_auditoria,
            "id_auditor" : id_auditor,
            "respuestas" : respuestas 
        }
    }
    response = request('127.0.0.1', 5000, 'GestionFormularioService.py', json.dumps(data))
    if response:
        response = json.loads(response)
    else:
        print ("No recibe respuesta")
    print(response)
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
    grupoCampos = retrieveGruposCampos()
    print(Colores.HEADER + f"Seleccione Formulario: " + Colores.ENDC)
    for i, grupoCampo in enumerate(grupoCampos):
        print(f"{i + 1}.-  {grupoCampo["nombre"]}")

    formulario_index = input_int(" > ") - 1

    id_grupo_campos = grupoCampos[formulario_index]["id"]
    marca_temporal = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    os.system('cls')
    print(Colores.HEADER + 'General' + Colores.ENDC)

    fecha = input(Colores.OKCYAN + "Fecha > " + Colores.ENDC)
    id_bus = input(Colores.OKCYAN + "Bus > " + Colores.ENDC)
    id_tipo_auditoria = input(Colores.OKCYAN + "Tipo Auditoria > " + Colores.ENDC)
    id_auditor = input(Colores.OKCYAN + "Auditor > " + Colores.ENDC)
    
    respuestas = answerCampos(id_grupo_campos)
    response = addAuditoria(marca_temporal, fecha, id_grupo_campos, id_bus, id_tipo_auditoria, id_auditor, respuestas)
    return response


def editAuditoria(auditoria_id):
    datos = get_auditoria(auditoria_id)
    preguntas = get_formulario(datos['id_grupo_campos'])
    
    response = {
        "comando": 'editAuditoria',
        "body": {
            "marca_temporal": datos['auditoria']['auditoria'][1],
            "fecha" : datos['auditoria']['auditoria'][2],
            "id_grupo_campos" : datos['auditoria']['auditoria'][3],
            "id_bus" : datos['auditoria']['auditoria'][4],
            "id_tipo_auditoria" : datos['auditoria']['auditoria'][5],
            "id_auditor" : datos['auditoria']['auditoria'][6],
            "respuestas" : datos['auditoria']['respuestas']
        }
    }
    
    while True:
        print("Seleccione el campo a editar:")
        print("1. Marca Temporal")
        print("2. Fecha")
        print("4. Bus")
        print("5. Tipo Auditoria")
        print("6. Auditor")
        print("7. Respuestas")
        print("8. Enviar Cambios")
        print("9. Salir")

        opcion = input_int(" > ")

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
            response["body"]["respuestas"][preguntaEditar - 1][1] = preguntaEditada
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

def ver_auditorias():
    while True:
        data = {
            "comando": 'get_all_auditorias'
        }

        os.system('cls')
        print(Colores.HEADER + "Num   | " + "%-15s" % "Formulario" + " | " + "%-20s" % "Fecha" + " | " + "%-7s" % "Bus" + " | " + "%-15s" % "Tipo Auditoria" + " | " + "%-20s" % "Auditor" + Colores.ENDC)
        response = request('127.0.0.1', 5000, 'AuditoriaService.py', json.dumps(data))
        auditorias = json.loads(response)
        print (auditorias)
        for i, auditoria in enumerate(auditorias['auditorias']):
            print(f"{i + 1:<5} | {auditoria['formulario']:<15} | {auditoria['fecha']:<20} | {auditoria['bus']:<7} | {auditoria['tipo']:<15} | {auditoria['auditor']:<20}")

        comando = input(Colores.OKCYAN + "Ver auditoria [ID] o .salir > " + Colores.ENDC)

        if comando == ".salir":
            return
        
        if not comando.isdigit():
            print("ID no valido")
            return
        
        if int(comando) > len(auditorias['auditorias']) or int(comando) < 1:
            print("ID no valido")
            return 
           
        auditoria_id = auditorias['auditorias'][int(comando) - 1]['id']
        
        data = {
            "comando": 'get_auditoria',
            'auditoria_id': auditoria_id
        }
        
        response = request('127.0.0.1', 5000, 'AuditoriaService.py', json.dumps(data))
        response = json.loads(response)
        os.system('cls')
        print(Colores.HEADER + "Auditoria" + Colores.ENDC)

        print(f"""
            {"%-20s" % 'Marca Temporal'}: {response['auditoria']['auditoria'][1]}
            {"%-20s" % 'Fecha'}: {response['auditoria']['auditoria'][2]}
            {"%-20s" % 'Bus'}: {response['auditoria']['auditoria'][4]}
            {"%-20s" % 'Tipo Auditoria'}: {response['auditoria']['auditoria'][5]}
            {"%-20s" % 'Auditor'}: {response['auditoria']['auditoria'][6]}
        """)
        
        print(Colores.HEADER + response['auditoria']['auditoria'][3] + Colores.ENDC)
        
        print(response)
        
        for respuesta in response['auditoria']['respuestas']:
            print(f"{respuesta[0]:<20}: {respuesta[1]:<40}")

        comando = input(Colores.OKCYAN + ".eliminar, .modificar o Enter > " + Colores.ENDC)

        if comando == ".eliminar":
            eliminar_auditoria(auditoria_id)

        if comando == ".modificar":
            editAuditoria(response)

if __name__ == '__main__':
    locked_in = True

    comandos = [
        ("Registrar Auditoria", lambda x: registerAuditoria()),
        ("Ver Auditorias", lambda x: ver_auditorias()),
        ("Ver Buses", lambda x: ver_buses()),
        ("Logout", lambda x: logout())
    ]

    '''while True:
        os.system('cls')
        print(Colores.HEADER + "Login como Digitador" + Colores.ENDC)

        username = input("Usuario > ")
        password = input("Contraseña > ")

        response = login(username, password)

        if response['status'] == 'correct':
            locked_in = True
            break
        else:
            print(response['message'])'''

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
        
        {'status': 
            'correct',
            'auditoria': 
                {'auditoria': 
                    [1, '2024-12-07 23:57:59', '2024-12-06 2:00:00', 'Torniquete', 'B-001', 'Seguimiento', 'Auditor1'], 
                        'respuestas':[
                            ['Funcionamiento', 'Funciona'], 
                            ['Limpieza', 'Limpio'], 
                            ['Tipo', '3 Brazos']
                            ]
                        }
                }