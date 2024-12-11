import socket
import json

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


def input_int(prompt: int) -> int:
    while True:
        try:
            return int(input(prompt))
        except KeyboardInterrupt:
            quit()
        except:
            print(Colores.FAIL + "Ingrese un numero" + Colores.ENDC)


def request(bus_ip, bus_port, service_name, message):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            client_socket.connect((bus_ip, bus_port))
            request = f"{service_name}:{message}"
            client_socket.sendall(request.encode('utf-8'))
            response = client_socket.recv(8192)
            return response.decode('utf-8')
    except ConnectionRefusedError:
        return json.dumps({"status": "error", "message": "El servidor no está disponible."})
    except socket.timeout:
        return json.dumps({"status": "error", "message": "El servidor no respondió a tiempo."})
    except Exception as e:
        return json.dumps({"status": "error", "message": f"Error inesperado: {str(e)}"})
