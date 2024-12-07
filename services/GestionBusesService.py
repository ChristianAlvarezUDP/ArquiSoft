import sys
import socket
import threading
import sqlite3
import json


def GetBus(id):
    try:
        conn = sqlite3.connect('sqlite/arqui.db')
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM buses WHERE id = ?", (id,))
        bus = cursor.fetchone()
        conn.close()
        return bus
    except sqlite3.Error as e:
        print(f"SQLite error: {e}")

def createBus(id, patente, anio, chasis, plazas):
    try:
        conn = sqlite3.connect('sqlite/arqui.db')
        cursor = conn.cursor()

        cursor.execute("INSERT INTO buses (id, patente, anio, chasis, plazas) VALUES (?, ?, ?, ?, ?)", (id, patente, anio, chasis, plazas))
        conn.commit()
        conn.close()
        return "Bus creado correctamente"
    except sqlite3.Error as e:
        print(f"SQLite error: {e}")

def updateBus(id, patente, anio, chasis, plazas):

    try:
        conn = sqlite3.connect('sqlite/arqui.db')
        cursor = conn.cursor()

        cursor.execute("UPDATE buses SET patente = ?, anio = ?, chasis = ?, plazas = ? WHERE id = ?", (patente, anio, chasis, plazas, id))
        conn.commit()
        conn.close()
        return "Bus actualizado correctamente"
    except sqlite3.Error as e:
        print(f"SQLite error: {e}")

def auditarBus(id):

        

    
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
            
            if data["comando"] == "GetBus":
                response = GetBus(data["id"])
            elif data["comando"] == "createBus":
                response = createBus(data["id"], data["placa"], data["marca"], data["modelo"], data["capacidad"])
            elif data["comando"] == "updateBus":
                response = updateBus(data["id"], data["placa"], data["marca"], data["modelo"], data["capacidad"])
            elif data["comando"] == "auditarBus":
                response = auditarBus(data["body"]["selectedBus"])


            client_socket.sendall(response.encode('utf-8'))
            client_socket.close()

if __name__ == '__main__':
    threading.Thread(target=service_worker, args=(sys.argv[0].split('/')[-1], '127.0.0.1', int(sys.argv[1]))).start()
