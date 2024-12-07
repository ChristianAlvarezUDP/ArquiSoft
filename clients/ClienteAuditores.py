import socket
import json

def request(bus_ip, bus_port, service_name, message):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((bus_ip, bus_port))
        request = f"{service_name}:{message}"
        client_socket.sendall(request.encode('utf-8'))
        response = client_socket.recv(1024)

        return response.decode('utf-8')


def login(username, password):
    data = {
        "comando": 'login',
        "data": {
            "user": username,
            "password": password
        }
    }

    response = request('127.0.0.1', 5000, 'auth_service.py', json.dumps(data))
    response = json.loads(response)

    if 'status' not in response:
        return False

    return response['status'] == "correct"


def listar_auditorias():
    data = {
    }

    request('127.0.0.1', 5000, 'auth_service.py', json.dumps(data))
    return "hola"


def logout():
    return "break"

def agregar_formulario(nombre, preguntas):
    data = {
        'comando': 'agregar',
        'nombre': nombre,
        'preguntas': preguntas
    }

    response = request('127.0.0.1', 5000, 'forms_service.py', json.dumps(data))
    response = json.loads(response)

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
        print(f"{form["id"]}: {form["nombre"]}")

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
    print()

def auditar_bus():

  selectedBus = input("Escriba la id del bus")

  data = {
        'comando': 'auditarBus',
        "body": {
            "selectedBus": selectedBus,
        }
    }

  response = request('127.0.0.1', 5000, 'GestionBusesService.py', json.dumps(data))
  return

def listar_buses_auditados():
    data = {
        'comando': 'listarBusesAuditados',
        "body": {
        }
    }

    response = request('127.0.0.1', 5000, 'GestionBusesService.py', json.dumps(data))
    response = json.loads(response)
    for item in response:
        print(item)
    return response

def listar_auditorias_por_auditor():
    
    data = {
        'comando': 'verAuditoriasHechas',
        "body":{
            'id_auditor': id_auditor,
        }
    }


if __name__ == '__main__':
    locked_in = True

    comandos = {
        "listar auditorias": lambda x: listar_auditorias(),
        "agregar formulario": lambda x: crear_formulario(),
        "responder auditoria": lambda x: responder_auditoria(),
        "auditar bus": lambda x: auditar_bus(),
        "listar buses auditados": lambda x: listar_buses_auditados(),
        "logout": lambda x: logout(),
    }
    
    """
    while True:
        print("Login")
        username = input("Usuario > ")
        password = input("Contraseña > ")
    
        if login(username, password):
            locked_in = True
            break
        else:
            print("Credenciales incorrectas")
    """

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







