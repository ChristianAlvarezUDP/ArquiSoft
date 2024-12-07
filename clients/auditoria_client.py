import socket
import json

def request(bus_ip, bus_port, service_name, message):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((bus_ip, bus_port))
        request = f"{service_name}:{message}"
        client_socket.sendall(request.encode('utf-8'))
        response = client_socket.recv(1024)

        return response.decode('utf-8')
    
def retriveAuditoria():
    data = {
        "comando": 'retrieve',
    }
    
    response = request('127.0.0.1', 5000, 'auditorias_serviceXDD.py', json.dumps(data))

    if response:
        response = json.loads(response)
    else:
        print ("No recibe respuesta")
    
    print(response)

if __name__ == '__main__':
    print("Comienza ejecucion")
    
    retriveAuditoria()