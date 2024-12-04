import socket
import threading

def service_worker(service_name, host, port):
    print(f"{service_name} starting on {host}:{port}")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((host, port))
        server_socket.listen()
        while True:
            client_socket, _ = server_socket.accept()
            data = client_socket.recv(1024).decode('utf-8')
            print(f"{service_name} received: {data}")
            response = f"{service_name} processed: {data}"
            client_socket.sendall(response.encode('utf-8'))
            client_socket.close()


if __name__ == '__main__':
    threading.Thread(target=service_worker, args=("service1", '127.0.0.1', 6000)).start()
    threading.Thread(target=service_worker, args=("service2", '127.0.0.1', 6001)).start()
