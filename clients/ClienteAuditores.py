import json
import os
from utils import Colores, input_int, request
from tabulate import tabulate

userId = -1

    
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
        print("Escriba pregunta o .terminar")
        pregunta = input(" > ")

        if pregunta == ".terminar":
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
    selectedBus = input(Colores.OKCYAN + "Escriba la id del bus > " + Colores.ENDC)

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

    print(Colores.HEADER + "Buses auditados:" + Colores.ENDC)
    for item in response:
        print(item['n_interno'])

    
    table = tabulate(response, headers="keys", tablefmt="grid")
    print(table)

    input(Colores.OKCYAN + "Presione enter para continuar... > " + Colores.ENDC)
    
    return response

def ver_auditorias(id_auditor):
    while True:
        data = {
            'comando': 'AuditoriasPorAuditor',
            "body": {
                'id_auditor': id_auditor,
            }
        }

        response = request('127.0.0.1', 5000, 'GenerateReportService.py', json.dumps(data))
        auditorias = json.loads(response)

        os.system('cls')
        print(Colores.HEADER + "Num   | " + "%-15s" % "Formulario" + " | " + "%-20s" % "Fecha" + " | " + "%-7s" % "Bus" + " | " + "%-15s" % "Tipo Auditoria" + " | " + "%-20s" % "Auditor" + Colores.ENDC)
        
        for i, auditoria in enumerate(auditorias):
            print(f"{i + 1:<5} | {auditoria['grupo_campos_nombre']:<15} | {auditoria['marca_temporal']:<20} | {auditoria['bus_interno']:<7} | {auditoria['tipo_auditoria_nombre']:<15} | {auditoria['auditor_nombre']:<20}")

        comando = input(Colores.OKCYAN + "Ver auditoria [ID] o .salir > " + Colores.ENDC)

        if comando == ".salir":
            return
        
        try:
            auditoria_index = int(comando) - 1
        except:
            continue
        
        auditoria_id = auditorias[auditoria_index]['id']
        break
        
    data = {
        "comando": 'get_auditoria',
        'auditoria_id': auditoria_id
    }
        
    response = request('127.0.0.1', 5000, 'AuditoriaService.py', json.dumps(data))
    response = json.loads(response)

    os.system('cls')
    print(Colores.HEADER + f"Auditoria {auditoria_index}" + Colores.ENDC)

    print(f"""{"%-20s" % 'Fecha'}: {response['auditoria']['auditoria']['marca_temporal']}
{"%-20s" % 'Bus'}: {response['auditoria']['auditoria']['n_interno']}
{"%-20s" % 'Tipo Auditoria'}: {response['auditoria']['auditoria']['tipo']}
{"%-20s" % 'Auditor'}: {response['auditoria']['auditoria']['auditor']}
""")
    
    print(Colores.HEADER + response['auditoria']['auditoria']['formulario'] + Colores.ENDC)
    
    for respuesta in response['auditoria']['respuestas']:
        print(f"{respuesta['titulo']:<20}: {respuesta['valor']:<40}")

    comando = input(Colores.OKCYAN + "Presiona Enter para continuar > " + Colores.ENDC)


if __name__ == '__main__':
    locked_in = False

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

    comandos = [
        ("Auditar bus", lambda x: auditar_bus()),
        ("Listar buses auditados", lambda x: listar_buses_auditados()),
        ("Ver Auditorias", lambda x: ver_auditorias(userId)),
        ("Logout", lambda x: logout()),
    ]

    while locked_in:
        os.system('cls')
        print(Colores.HEADER + "Seleccione comando:" + Colores.ENDC)
        for i, comando in enumerate(comandos):
            print(f"{i + 1}.- {comando[0]}")

        try:
            comando = input_int(Colores.OKGREEN + "Comando > " + Colores.ENDC) - 1
        except KeyboardInterrupt:
            quit()

        if comando > len(comandos):
            continue
        
        os.system('cls')
        x = comandos[comando][1](1)

        if x == "break":
            break
