import socket
import threading

class SOABus:
    def __init__(self, host='127.0.0.1', port=5000):
        self.host = host
        self.port = port
        self.services = {} 
        self.lock = threading.Lock()
        self.stop_flag = threading.Event()

    def register_service(self, service_name, address):
        with self.lock:
            self.services[service_name] = address
            print(f"Service '{service_name}' registered at {address}")

    def get_service_address(self, service_name):
        with self.lock:
            return self.services.get(service_name, None)

    def handle_client(self, client_socket):
        try:
            data = client_socket.recv(1024).decode('utf-8')
            print(f"Received request: {data}")
            service_name, message = data.split(':', 1)

            # Forward request to the appropriate service
            address = self.get_service_address(service_name)
            if address:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as service_socket:
                    service_socket.connect(address)
                    service_socket.sendall(message.encode('utf-8'))
                    response = service_socket.recv(1024)
                client_socket.sendall(response)
            else:
                client_socket.sendall(b"Error: Service not found")
        except Exception as e:
            print(f"Error handling client: {e}")
        finally:
            client_socket.close()

    def start(self):
        print(f"Starting SOA Bus on {self.host}:{self.port}")
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            server_socket.bind((self.host, self.port))
            server_socket.listen()
            while not self.stop_flag.is_set():
                server_socket.settimeout(1)
                try:
                    client_socket, _ = server_socket.accept()
                    threading.Thread(target=self.handle_client, args=(client_socket,)).start()
                except socket.timeout:
                    continue
    
    def stop(self):
        print("Stopping SOA Bus...")
        self.stop_flag.set()


threads = []

if __name__ == '__main__':
    bus = SOABus()

    threads.append(threading.Thread(target=bus.start))

    threads[0].start()

    bus.register_service("db", ('127.0.0.1', 6000))
    bus.register_service("login", ('127.0.0.1', 6001))
    bus.register_service("gestionDeFormularios", ('127.0.0.1', 6002))

    while True:
        command = input("Enter 'stop' to terminate the bus: ").strip().lower()
        if command == 'stop':
            bus.stop()
            break
