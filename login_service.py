import socket
import threading
import json

def service_worker(service_name, host, port, stop_flag):
    print(f"{service_name} iniciando en {host}:{port}")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((host, port))
        server_socket.listen()
        while not stop_flag.is_set():
            server_socket.settimeout(1)

            try:
                client_socket, _ = server_socket.accept()
                data = client_socket.recv(1024).decode('utf-8')

                data = json.loads(data)

                print(data)

                response = ""

                if data['comando'] == 'login':
                    response = request('127.0.0.1', 5000, 'db', json.dumps(data))

                else:
                    response = {
                        'status': 'error',
                        'mesage': 'Comando incorrecto'
                    }

                print(f"{service_name} received: {data}")
                client_socket.sendall(response.encode('utf-8'))
                client_socket.close()
            except socket.timeout:
                continue


def request(bus_host, bus_port, service_name, message):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((bus_host, bus_port))
        request = f"{service_name}:{message}"
        client_socket.sendall(request.encode('utf-8'))
        response = client_socket.recv(1024)
        print(f"Response: {response.decode('utf-8')}")

        return response.decode('utf-8')


if __name__ == '__main__':
    stop_flag = threading.Event()

    threading.Thread(target=service_worker, args=("login", '127.0.0.1', 6001, stop_flag)).start()

    while True:
        command = input("Enter 'stop' to terminate the services: ").strip().lower()
        if command == 'stop':
            stop_flag.set()
            break

    

