import sys
import socket
import threading
import sqlite3
import json

def dict_factory(cursor, row):
    fields = [column[0] for column in cursor.description]
    return {key: value for key, value in zip(fields, row)}

def service_worker(service_name, host, port):
    print(f"{service_name} iniciando en {host}:{port}")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 65536) 
        server_socket.bind((host, port))
        server_socket.listen()
        while True:
            client_socket, _ = server_socket.accept()
            data = client_socket.recv(4096).decode('utf-8')
            print(f"{service_name} received: {data}")

            data = json.loads(data)

            response = ""
            if data['comando'] == 'get_auditoria':
                auditoria = get_auditoria(data['auditoria_id'])

                result = {
                    'status': 'correct',
                    'auditoria': auditoria
                }

                response = json.dumps(result)

            elif data['comando'] == 'get_all_auditorias':
                auditorias = get_all_auditorias()

                result = {
                    'status':  'correct',
                    'auditorias': auditorias
                }

                response = json.dumps(result)
            
            elif data['comando'] == 'registerAuditoria':
                registerAuditoria(data['body'])
                response = {
                    'status': 'correct',
                    'message': 'Auditoria registrada correctamente'
                }
                
                response = json.dumps(response)
            
            elif data['comando'] == 'editAuditoria':
                editAuditoria(data['body']['auditoria_id'], data['body'])
                response_data = {
                    'status': 'correct',
                    'message': 'Auditoria editada correctamente'
                }
                
                response = json.dumps(response_data)
            
            elif data['comando'] == 'delete_auditoria':
                success = delete_auditoria(data['auditoria_id'])

                result = {
                    'status':  'correct'
                }

                response = json.dumps(result)
            elif data['comando'] == 'get_auditoriaIDs':
                print("HOLA")
                auditoriaIDs = get_auditoriaIDs(data['auditoria_id'])

                result = {
                    'status':  'correct',
                    'auditoriaIDs': auditoriaIDs
                }

                response = json.dumps(result)

            else:
                response_data = {
                    'status': 'error',
                    'mesage': 'Comando incorrecto'
                }

                response = json.dumps(response_data)

            print(f"{service_name} responde: {response}")

            serialized = response.encode('utf-8')
            client_socket.sendall(serialized)


def get_auditoria(auditoria_id):
    conn = sqlite3.connect("sqlite/arqui.db")
    conn.row_factory = dict_factory 
    cursor = conn.cursor()

    cursor.execute(f'''
        SELECT a.id, a.marca_temporal, a.fecha, gc.id as id_grupo_campos, gc.nombre as formulario, b.id as id_bus, b.n_interno, ta.id as id_tipo_auditoria, ta.nombre as tipo, au.id as id_auditor, au.nombre as auditor FROM auditoria AS a
        JOIN grupo_campos AS gc ON a.id_grupo_campos = gc.id
        JOIN bus AS b ON a.id_bus = b.id
        JOIN tipo_auditoria AS ta ON a.id_tipo_auditoria = ta.id
        JOIN auditor AS au ON a.id_auditor = au.id
        WHERE a.id = (?)
        ''', (auditoria_id,))
    
    auditoria = cursor.fetchone()

    cursor.execute(f'''
        SELECT ca.titulo, ra.valor, ra.id_campo_auditoria FROM respuesta_auditoria AS ra
        JOIN campo_auditoria AS ca ON ra.id_campo_auditoria = ca.id
        WHERE ra.id_auditoria = (?)
        ''', (auditoria_id,))
    
    respuestas = cursor.fetchall()

    conn.close()

    return {'auditoria': auditoria, 'respuestas': respuestas}

def get_auditoriaIDs(auditoria_id):
    conn = sqlite3.connect("sqlite/arqui.db")
    conn.row_factory = dict_factory 
    cursor = conn.cursor()

    cursor.execute(f'''
        SELECT * FROM auditoria
        WHERE id = (?)
        ''', (auditoria_id,))
    
    auditoriaIDs = cursor.fetchall()
    conn.close()

    return auditoriaIDs

def get_all_auditorias():
    conn = sqlite3.connect("sqlite/arqui.db")
    conn.row_factory = dict_factory 
    cursor = conn.cursor()

    cursor.execute(f'''
        SELECT a.id, a.marca_temporal, a.fecha, gc.id as id_formulario, gc.nombre as formulario, b.n_interno as bus, ta.nombre as tipo, au.nombre as auditor FROM auditoria AS a
        JOIN grupo_campos AS gc ON a.id_grupo_campos = gc.id
        JOIN bus AS b ON a.id_bus = b.id
        JOIN tipo_auditoria AS ta ON a.id_tipo_auditoria = ta.id
        JOIN auditor AS au ON a.id_auditor = au.id
        ''')
    
    result = cursor.fetchall()
    conn.close()

    return result

def registerAuditoria(body):
    conn = sqlite3.connect("sqlite/arqui.db")
    conn.row_factory = dict_factory 
    cursor = conn.cursor()

    cursor.execute(f'''
        INSERT INTO auditoria (marca_temporal, fecha, id_grupo_campos, id_bus, id_tipo_auditoria, id_auditor)
        VALUES (?, ?, ?, ?, ?, ?)
        ''', (body['marca_temporal'], body['fecha'], body['id_grupo_campos'], body['id_bus'], body['id_tipo_auditoria'], body['id_auditor']))
    
    id_auditoria = cursor.lastrowid
    for campo in body['respuestas']:
        cursor.execute(f'''
            INSERT INTO respuesta_auditoria(id_auditoria, id_campo_auditoria, valor) 
            VALUES (?, ?, ?)
            ''', (id_auditoria, campo['id'], campo['titulo'] ))
    conn.commit()
    conn.close()

def delete_auditoria(auditoria_id):
    conn = sqlite3.connect("sqlite/arqui.db")
    cursor = conn.cursor()

    cursor.execute(f'''
        DELETE FROM auditoria 
        WHERE id = (?)
        ''', (auditoria_id,))
    
    conn.commit()
    conn.close()

def editAuditoria(auditoria_id, body):
        conn = sqlite3.connect("sqlite/arqui.db")
        cursor = conn.cursor()

        cursor.execute(f'''
            UPDATE auditoria
            SET marca_temporal = ?, fecha = ?, id_grupo_campos = ?, id_bus = ?, id_tipo_auditoria = ?, id_auditor = ?
            WHERE id = ?
            ''', (body['marca_temporal'], body['fecha'], body['id_grupo_campos'], body['id_bus'], body['id_tipo_auditoria'], body['id_auditor'], auditoria_id))
        
        for campo in body['respuestas']:
            cursor.execute(f'''
                WITH t AS (
                    SELECT id FROM campo_auditoria
                    WHERE titulo = ?
                )
                UPDATE respuesta_auditoria
                SET valor = ?
                FROM t
                WHERE id_auditoria = ? AND id_campo_auditoria = t.id
                ''', ( campo['titulo'], campo['valor'], auditoria_id))

        conn.commit()
        conn.close()

if __name__ == '__main__':
    threading.Thread(target=service_worker, args=(sys.argv[0].split('/')[-1], '127.0.0.1', int(sys.argv[1]))).start()