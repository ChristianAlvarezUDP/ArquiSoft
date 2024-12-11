import sys
import socket
import threading
import sqlite3
import json
from datetime import datetime


def dict_factory(cursor, row):
    fields = [column[0] for column in cursor.description]
    return {key: value for key, value in zip(fields, row)}


def get_all_buses():
    try:
        conn = sqlite3.connect('sqlite/arqui.db')
        conn.row_factory = dict_factory
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM bus")
        buses = cursor.fetchall()
        conn.close()
        return buses
    except sqlite3.Error as e:
        print(f"SQLite error: {e}")


def GetBus(id):
    try:
        conn = sqlite3.connect('sqlite/arqui.db')
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM bus WHERE id = ?", (id,))
        bus = cursor.fetchone()
        conn.close()
        return bus
    except sqlite3.Error as e:
        print(f"SQLite error: {e}")

def createBus(id, patente, anio, chasis, plazas):
    try:
        conn = sqlite3.connect('sqlite/arqui.db')
        cursor = conn.cursor()

        cursor.execute("INSERT INTO bu (id, patente, anio, chasis, plazas) VALUES (?, ?, ?, ?, ?)", (id, patente, anio, chasis, plazas))
        conn.commit()
        conn.close()
        return "Bus creado correctamente"
    except sqlite3.Error as e:
        print(f"SQLite error: {e}")

def updateBus(id, patente, anio, chasis, plazas):

    try:
        conn = sqlite3.connect('sqlite/arqui.db')
        cursor = conn.cursor()

        cursor.execute("UPDATE bus SET patente = ?, anio = ?, chasis = ?, plazas = ? WHERE id = ?", (patente, anio, chasis, plazas, id))
        conn.commit()
        conn.close()
        return "Bus actualizado correctamente"
    except sqlite3.Error as e:
        print(f"SQLite error: {e}")

def auditarBus(id):
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    query = """
            INSERT INTO buses_auditados (bus_id, fecha_auditado)
            VALUES (?, ?)
            """
    try:
        conn = sqlite3.connect('sqlite/arqui.db')
        cursor = conn.cursor()
        cursor.execute(query, (id, current_time))
        conn.commit()
    except sqlite3.Error as e:
        print(f"Error inserting data: {e}")
    finally:
        cursor.close()
        conn.close()
        return "Bus auditado correctamente"
        
def listarBusesAuditados():
    query = """
    SELECT * 
    FROM buses_auditados AS ba
    JOIN bus AS b ON ba.bus_id = b.id
    WHERE fecha_auditado BETWEEN datetime('now', '-1 day') AND datetime('now');
    """
    try:
        conn = sqlite3.connect('sqlite/arqui.db')
        cursor = conn.cursor()
        cursor.execute(query)
        buses = cursor.fetchall()

        columns = [description[0] for description in cursor.description]
        
        buses_list = [dict(zip(columns, row)) for row in buses]
        conn.commit()
    except sqlite3.Error as e:
        print(f"Error inserting data: {e}")
    finally:
        cursor.close()
        conn.close()
        
    return json.dumps(buses_list)
    

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
            
            if data["comando"] == 'get_all_buses':
                buses = get_all_buses()

                result = {
                    'status':  'correct',
                    'buses': buses
                }

                response = json.dumps(result)

            if data["comando"] == "GetBus":
                response = GetBus(data["id"])
            elif data["comando"] == "createBus":
                response = createBus(data["id"], data["placa"], data["marca"], data["modelo"], data["capacidad"])
            elif data["comando"] == "updateBus":
                response = updateBus(data["id"], data["placa"], data["marca"], data["modelo"], data["capacidad"])
            elif data["comando"] == "auditarBus":
                response = auditarBus(data["body"]["selectedBus"])
            elif data["comando"] == "listarBusesAuditados":
                response = listarBusesAuditados()

            client_socket.sendall(response.encode('utf-8'))
            client_socket.close()

if __name__ == '__main__':
    threading.Thread(target=service_worker, args=(sys.argv[0].split('/')[-1], '127.0.0.1', int(sys.argv[1]))).start()
