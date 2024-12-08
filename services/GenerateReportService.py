import sys
import socket
import threading
import sqlite3
import json

def dict_factory(cursor, row):
    fields = [column[0] for column in cursor.description]
    return {key: value for key, value in zip(fields, row)}

def GenerarReporte(fecha_inicio, fecha_fin):
    return
def get_auditorias_by_auditor(idAuditor):
    query = '''
        SELECT a.id, a.marca_temporal, a.fecha, gc.nombre AS grupo_campos_nombre, 
               b.n_interno AS bus_interno, ta.nombre AS tipo_auditoria_nombre, 
               au.nombre AS auditor_nombre
        FROM auditoria AS a
        JOIN grupo_campos AS gc ON a.id_grupo_campos = gc.id
        JOIN bus AS b ON a.id_bus = b.id
        JOIN tipo_auditoria AS ta ON a.id_tipo_auditoria = ta.id
        JOIN auditor AS au ON a.id_auditor = au.id
        WHERE a.id_auditor = ?
    '''
    try:
        conn = sqlite3.connect('sqlite/arqui.db')
        conn.row_factory = dict_factory
        cursor = conn.cursor()
        cursor.execute(query, (idAuditor,))
        result = cursor.fetchall()
        print(result)
    except sqlite3.Error as e:
        print(f"Error fetching data: {e}")
        return json.dumps({"error": str(e)})
    finally:
        cursor.close()
        conn.close()

    # Convert the list of dictionaries to a JSON string and return
    return json.dumps(result)

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
            
            if data["comando"] == "AuditoriasPorAuditor":
                response = get_auditorias_by_auditor(data["id_auditor"])
                if response == []:
                    response = "No se encontraron auditorias"
                else :
                    response = json.dumps(response)
                    
            client_socket.sendall(response.encode('utf-8'))
            client_socket.close()

if __name__ == '__main__':
    threading.Thread(target=service_worker, args=(sys.argv[0].split('/')[-1], '127.0.0.1', int(sys.argv[1]))).start()
