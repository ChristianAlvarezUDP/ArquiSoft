import socket

def client_request(bus_host, bus_port, service_name, message):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((bus_host, bus_port))
        request = f"{service_name}:{message}"
        client_socket.sendall(request.encode('utf-8'))
        response = client_socket.recv(1024)
        print(f"Response: {response.decode('utf-8')}")


if __name__ == '__main__':
    client_request('127.0.0.1', 5000, 'service1', 'Hello from Client 1')
    client_request('127.0.0.1', 5000, 'service2', 'Hello from Client 2')
    client_request('127.0.0.1', 5000, 'service3', 'Hello from Client 3')  # Service not registered
