import socket
import json
import os
from tabulate import tabulate


userId = -1

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
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            client_socket.connect((bus_ip, bus_port))
            request = f"{service_name}:{message}"
            client_socket.sendall(request.encode('utf-8'))
            response = client_socket.recv(1024)
            return response.decode('utf-8')
    except ConnectionRefusedError:
        return json.dumps({"status": "error", "message": "El servidor no está disponible."})
    except socket.timeout:
        return json.dumps({"status": "error", "message": "El servidor no respondió a tiempo."})
    except Exception as e:
        return json.dumps({"status": "error", "message": f"Error inesperado: {str(e)}"})

    
def pause():
    input("\nPresiona Enter para continuar...")

def ObtenerAuditoriasPorAuditor(idAuditor):
    data = {
        'comando': 'AuditoriasPorAuditor',
        'id_auditor': idAuditor
    }

    response = request('127.0.0.1', 5000, 'GenerateReportService.py', json.dumps(data))
    if not response or response.strip() == "":
        print("La respuesta está vacía o no es válida")
        pause()
        return

    try:
        parsed_response = json.loads(response)
        table = tabulate(parsed_response, headers="keys", tablefmt="plain")
        print(table)

    except json.JSONDecodeError as e:
        print(f"Error al decodificar JSON: {e}")
        print(f"Respuesta recibida: {response}")
    pause()

def login(username, password):
    data = {
        "comando": "login",
        "username": username,
        "password": password,
        "permisos": "Auditoria"
    }

    try:
        response = request('127.0.0.1', 5000, 'AutentificacionService.py', json.dumps(data))
        response = json.loads(response)
        return response
    except json.JSONDecodeError:
        return {"status": "error", "message": "Respuesta del servidor no válida."}
    except Exception as e:
        return {"status": "error", "message": f"Error inesperado: {str(e)}"}
    
def logout():
    global userId, locked_in
    print(Colores.WARNING + "Cerrando sesión..." + Colores.ENDC)
    userId = -1
    locked_in = False
    pause()

def listar_auditorias():
    data = {
        'comando': 'get_all_auditorias',
    }

    response = json.loads(request('127.0.0.1', 5000, 'AuditoriaService.py', json.dumps(data)))['auditorias']
    table = tabulate(response, headers="keys", tablefmt="plain")
    print(table)
    pause()

def agregar_formulario(nombre, preguntas):
    data = {
        'comando': 'agregar',
        'nombre': nombre,
        'preguntas': preguntas
    }

    response = request('127.0.0.1', 5000, 'forms_service.py', json.dumps(data))
    response = json.loads(response)
    print(response)
    pause()
    return response

def crear_formulario():
    print('Crear formulario')
    print("Escriba el nombre del formulario")

    nombre = input(" > ")

    preguntas = []
    while True:
        print("Escriba pregunta o 'terminar'")
        pregunta = input(" > ")

        if pregunta == "terminar":
            break

        preguntas.append(pregunta)
    if len(preguntas) == 0:
        print("No se puede crear un formulario sin preguntas")
        pause()
        return
    agregar_formulario(nombre, preguntas)

def responder_auditoria():
    print('Responder auditoria')

    print("Elija formulario (numero):")

    data = {
        'comando': 'get_all'
    }

    response = request('127.0.0.1', 5000, 'forms_service.py', json.dumps(data))

    form_data = json.loads(response)

    print(form_data)

    for form_id in form_data["forms"].keys():
        form = form_data["forms"][form_id]
      
    form_id = input(" > ")
    form = form_data["forms"][form_id]
    respuestas = []

    for pregunta in form["preguntas"]:
        print(pregunta["titulo"])
        respuesta = input(" > ")

        respuestas.append({"id_pregunta:": pregunta["id"], "respuesta": respuesta})

    data = {
        "comando": "agregar",
        "id_formulario": form_id,
        "respuestas": respuestas,
    }

    response = request('127.0.0.1', 5000, 'auditorias_service.py', json.dumps(data))
    print(response)
    pause()

def auditar_bus():
    selectedBus = input("Escriba la id del bus")

    data = {
        'comando': 'auditarBus',
        "body": {
            "selectedBus": selectedBus,
        }
    }

    response = request('127.0.0.1', 5000, 'GestionBusesService.py', json.dumps(data))
    print(response)
    pause()
    return response

def listar_buses_auditados():
    data = {
        'comando': 'listarBusesAuditados',
        "body": {}
    }

    response = request('127.0.0.1', 5000, 'GestionBusesService.py', json.dumps(data))
    response = json.loads(response)
    table = tabulate(response, headers="keys", tablefmt="grid")
    print(table)
    pause()
    
    return response

def listar_auditorias_por_auditor(id_auditor):
    data = {
        'comando': 'verAuditoriasHechas',
        "body": {
            'id_auditor': id_auditor,
        }
    }
    response = request('127.0.0.1', 5000, 'GestionBusesService.py', json.dumps(data))
    response = json.loads(response)
    table = tabulate(response, headers="keys", tablefmt="grid")

    print(table)
    pause()
    
if __name__ == '__main__':
    locked_in = False

    comandos = [
        ("listar auditorias", lambda x: listar_auditorias()),
        ("agregar formulario", lambda x: crear_formulario()),
        ("responder auditoria", lambda x: responder_auditoria()),
        ("auditar bus", lambda x: auditar_bus()),
        ("listar buses auditados", lambda x: listar_buses_auditados()),
        ("obtener", lambda x: ObtenerAuditoriasPorAuditor(userId)),
        ("logout", lambda x: logout()),
    ]

    while True:
        os.system('cls')
        print(Colores.HEADER + "Login como Auditor" + Colores.ENDC)

        username = input("Usuario > ")
        password = input("Contraseña > ")

        response = login(username, password)
        
        if response['status'] == 'correct':
            locked_in = True
            userId =  response['idUsuario'][0][0]
            
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
