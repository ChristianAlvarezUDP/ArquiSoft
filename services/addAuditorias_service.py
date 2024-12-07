import sys
import socket
import threading
import json
import sqlite3

def service_worker(service_name, host, port):
    print(f"{service_name} iniciando en {host}:{port}")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((host, port))
        server_socket.listen()
        while True:
            bus_socket, _ = server_socket.accept()
            data = bus_socket.recv(1024).decode('utf-8')

            response = "Something failed"
            data = json.loads(data)      
            print(f"Data: {data}")

            if data['comando'] == 'retrieve':
                conn = sqlite3.connect("sqlite/arqui.db")
                cursor = conn.cursor()
                
                cursor.execute(f'''
                    SELECT * FROM auditoria
                    ''')
                result = cursor.fetchall()
                print(f"Obtenido: {result}")
                response = json.dumps(result)
            
            if data['comando'] == 'add':
                conn = sqlite3.connect("sqlite/arqui.db")
                cursor = conn.cursor()
                cursor.execute(f'''
                    INSERT INTO auditoria VALUES (
                        {data['body']['id']}, {data['body']['marca_temporal']}, {data['body']['fecha']}, {data['body']['id_grupo_campos']}, {data['body']['id_bus']}, {data['body']['id_tipo_auditoria']}, {data['body']['id_auditor']}
                    )           
                    ''')
                result = conn.commit()
                print(f"Obtenido: {result}")
                response = json.dumps("Added one row")

            if data['comando'] == 'register':
                conn = sqlite3.connect("sqlite/arqui.db")
                cursor = conn.cursor()
                cursor.execute(f'''
                    INSERT INTO auditoria VALUES (
                        {data['body']['id']}, {data['body']['marca_temporal']}, {data['body']['fecha']}, {data['body']['id_grupo_campos']}, {data['body']['id_bus']}, {data['body']['id_tipo_auditoria']}, {data['body']['id_auditor']}
                    )           
                    ''')
                result = conn.commit()
                print(f"Obtenido: {result}")
                response = json.dumps("Added one row")
            
            
            bus_socket.sendall(response.encode('utf-8'))
            bus_socket.close()


def request(bus_host, bus_port, service_name, message):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((bus_host, bus_port))
        request = f"{service_name}:{message}"
        client_socket.sendall(request.encode('utf-8'))
        response = client_socket.recv(1024)
        print(f"Response: {response.decode('utf-8')}")

        return response.decode('utf-8')


if __name__ == '__main__':
    threading.Thread(target=service_worker, args=(sys.argv[0].split('/')[-1], '127.0.0.1', int(sys.argv[1]))).start()