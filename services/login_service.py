import sys
import socket
import threading
import json

bus_ip = '127.0.0.1'
bus_port = 5000

def service_worker(service_name, host, port):
    print(f"{service_name} iniciando en {host}:{port}")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((host, port))
        server_socket.listen()
        while True:
            client_socket, _ = server_socket.accept()
            data = client_socket.recv(1024).decode('utf-8')

            data = json.loads(data)
            print(data)
            response = ""

            if data['comando'] == 'login':
                response = request('db_service.py', json.dumps(data))

            else:
                response = {
                    'status': 'error',
                    'mesage': 'Comando incorrecto'
                }

            print(f"{service_name} received: {data}")
            client_socket.sendall(response.encode('utf-8'))
            client_socket.close()


def request(service_name, message):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((bus_ip, bus_port))
        request = f"{service_name}:{message}"
        client_socket.sendall(request.encode('utf-8'))
        response = client_socket.recv(1024)
        print(f"Response: {response.decode('utf-8')}")

        return response.decode('utf-8')


if __name__ == '__main__':
    bus_ip = sys.argv[2]
    bus_port = int(sys.argv[3])

    threading.Thread(target=service_worker, args=(sys.argv[0].split('/')[-1], '127.0.0.1', int(sys.argv[1]))).start()
