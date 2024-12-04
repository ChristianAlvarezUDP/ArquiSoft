import sys
import socket
import threading
import sqlite3

def service_worker(service_name, host, port):
    print(f"{service_name} starting on {host}:{port}")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((host, port))
        server_socket.listen()
        while True:
            client_socket, _ = server_socket.accept()
            data = client_socket.recv(1024).decode('utf-8')
            print(f"{service_name} received: {data}")
            response = handle_service_request(service_name, data)
            client_socket.sendall(response.encode('utf-8'))
            client_socket.close()

def handle_service_request(service_name, data):
    """
    Handle the service request based on the received operation.
    """
    # Initialize an empty list for questions
    questions = []

    try:
        # Parse the incoming data (assuming it's in the format `key:value` or JSON-like)
        request = parse_request(data)
    except ValueError:
        return f"{service_name} error: Invalid request format"

    # Get the operation from the request (e.g., 'crear')
    operacion = request.get('operacion')

    if operacion == "crear":
        return handle_create_operation(request)
    elif operacion == "otro":  # Placeholder for another operation
        return handle_other_operation(request)
    else:
        return f"{service_name} error: Unsupported operation '{operacion}'"

#Crear formularios
def handle_create_operation(request):
    """
    Handle the 'crear' operation to insert questions into the database.
    """
    questions = []

    # Ask for the number of questions
    if 'num_questions' in request:
        try:
            num_questions = int(request['num_questions'])
        except ValueError:
            return f"crear error: Invalid number of questions"

        # Ask for the text of each question
        for i in range(1, num_questions + 1):
            question_text = request.get(f'question_{i}')
            if question_text:
                questions.append(question_text)
                # Insert the question into the database
                insert_question_into_db(question_text)
            else:
                return f"crear error: Missing question text for question {i}"

        # Return the list of questions
        return f"crear success: {questions}"
    
    else:
        return f"crear error: Number of questions not provided"

def insert_question_into_db(question_text):
    """
    Insert the question into the SQLite database (arqui.db).
    The questions will be inserted into the 'campo_auditoria.titulo' table.
    """
    try:
        # Connect to SQLite database (arqui.db)
        conn = sqlite3.connect('sqlite/arqui.db')
        cursor = conn.cursor()

        # Create a group first (if needed)
        cursor.execute("INSERT INTO grupo_campos (nombre, responsable) VALUES (?, ?)", ("Grupo test", True))

        # Insert the question into the 'campo_auditoria' table
        cursor.execute("INSERT INTO campo_auditoria (titulo, id_grupo) VALUES (?, ?)", (question_text, 1))  # Assuming 'id_grupo' = 1
        
        # Commit the transaction and close the connection
        conn.commit()
        conn.close()
        print(f"Question inserted: {question_text}")
    except sqlite3.Error as e:
        print(f"Error inserting question into database: {e}")

def parse_request(data):
    """
    Parse the incoming request.
    For simplicity, we're assuming data is in a key-value format like 'key:value'.
    You can extend this to JSON parsing if needed.
    """
    request = {}
    for item in data.split(';'):  # Assume data is semicolon-separated
        try:
            key, value = item.split(':')
            request[key.strip()] = value.strip()
        except ValueError:
            pass
    return request



#Otras weas
def handle_other_operation(request):
    """
    Placeholder for handling other types of operations (e.g., 'actualizar', 'eliminar', etc.).
    """
    # For example, handle some other operation (this can be expanded based on your requirements)
    return "otro operation executed"


if __name__ == '__main__':
    threading.Thread(target=service_worker, args=(sys.argv[0].split('/')[-1], '127.0.0.1', int(sys.argv[1]))).start()
