import sys
import socket
import threading
import sqlite3
import json


def service_worker(service_name, host, port):
    print(f"{service_name} starting on {host}:{port}")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((host, port))
        server_socket.listen()
        while True:
            client_socket, _ = server_socket.accept()
            data = client_socket.recv(1024).decode('utf-8')

            # Custom

            print(f"{service_name} received: {data}")
            
            data = json.loads(data)
            response = ""

            if data["comando"] == "agregar":
                insert_form(data["nombre"], data["preguntas"])

            if data["comando"] == "get_all":
                form_data = get_all_forms()

                data = {
                    "status": "correct",
                    "forms": form_data
                }

                response = json.dumps(data)

            # end custom

            client_socket.sendall(response.encode('utf-8'))
            client_socket.close()