import socket
import json

def request(bus_ip, bus_port, service_name, message):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((bus_ip, bus_port))
        request = f"{service_name}:{message}"
        client_socket.sendall(request.encode('utf-8'))
        response = client_socket.recv(1024)
        print(f"Response: {response.decode('utf-8')}")

        return response.decode('utf-8')

def retriveAuditoria():
    data = {
        "comando": 'retrieve',
    }
    
    response = request('127.0.0.1', 5000, 'auditorias_servicesXDD.py', json.dumps(data))

    resonse = json.loads(response)
    
    print(response)

if __name__ == '__main__':
    locked_in = True

    retriveAuditoria()