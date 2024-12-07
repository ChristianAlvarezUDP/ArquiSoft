import sys
import socket
import threading
import sqlite3
import json


def GenerarReporte(fecha_inicio, fecha_fin):
    return

def auditoriasPorAuditor(id_auditor):
    

    return

def service_worker(service_name, host, port):
    print(f"{service_name} starting on {host}:{port}")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((host, port))
        server_socket.listen()
        while True:
            client_socket, _ = server_socket.accept()
            data = client_socket.recv(1024).decode('utf-8')
            print(f"{service_name} received: {data}")
            
            data = json.loads(data)
            response = ""

            if data["comando"] == "GenerarReporte":
                response = GenerarReporte(data["id_form"], data["fecha_inicio"], data["fecha_fin"])
            elif data["comando"] == "GenerarReporte":
                response = auditoriasPorAuditor(data["id_auditor"])


            client_socket.sendall(response.encode('utf-8'))
            client_socket.close()

if __name__ == '__main__':
    threading.Thread(target=service_worker, args=(sys.argv[0].split('/')[-1], '127.0.0.1', int(sys.argv[1]))).start()
