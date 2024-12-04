import socket
import json

def client_request(bus_host, bus_port, service_name, num_questions, questions):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((bus_host, bus_port))
        
        # Prepare the request in the format 'service_name:num_questions:{num_questions};question_1:{question_text};question_2:{question_text};...'
        request = f"{service_name}:num_questions:{num_questions}"
        
        # Add each question to the request
        for i, question in enumerate(questions, 1):
            request += f";question_{i}:{question}"
        
        # Send the request
        client_socket.sendall(request.encode('utf-8'))  
        
        # Receive and print the response
        response = client_socket.recv(1024)
        print(f"Response: {response.decode('utf-8')}")
    return response.decode('utf-8')


def login(username, password):
    data = {
        "comando": 'login',
        "data": {
            "user": username,
            "password": password
        }
    }

    response = client_request('127.0.0.1', 5000, 'login', json.dumps(data))

    response = json.loads(response)

    if 'status' not in response:
        return False

    return response['status'] == "correct"


def listar_auditorias():
    client_request('127.0.0.1', 5000, 'login', json.dumps(data))
    return "hola"


def logout():
    return "break"

def agregar_formulario():
    client_request('127.0.0.1', 5000, 'createForm_service', 3, questions)

if __name__ == '__main__':

    questions = [
        "What is your name?",
        "What is your age?",
        "Where do you live?"
    ]
    
 
    locked_in = True

    comandos = {
        "listar auditorias": lambda x: listar_auditorias(),
        "logout": lambda x: logout(),
        "agregar formulario": lambda x: agregar_formulario()
    }


 
    while locked_in:
        for comando in comandos.keys():
            print(comando)

        comando = input("Comando > ").lower()

        if comando not in comandos:
            continue

        x = comandos[comando](1)

        if x == "break":
            break

