import socket
import threading
import time

# --- Configuración del Servidor ---
HOST = '127.0.0.1'  # IP local (localhost)
PORT = 65432        # Puerto (puedes usar > 1024)

def handle_client(conn, addr):
    """
    Esta es la función 'worker'.
    Cada hilo ejecutará esta función para un cliente.
    """
    print(f"[NUEVO WORKER] Conectado con {addr}")

    try:
        while True:
            # 1. Recibir la tarea del cliente
            # (1024 es el tamaño del buffer en bytes)
            data = conn.recv(1024)
            
            # Si no hay datos, el cliente cerró la conexión
            if not data:
                print(f"[WORKER {addr}] Cliente desconectado.")
                break

            # Convertimos los bytes a string
            task = data.decode('utf-8')
            print(f"[WORKER {addr}] Tarea recibida: '{task}'")

            # 2. "Procesar" la tarea (simulamos trabajo)
            print(f"[WORKER {addr}] Procesando tarea...")
            time.sleep(5) # Simula 5 segundos de un trabajo pesado
            print(f"[WORKER {addr}] Tarea completada.")

            # 3. Enviar el resultado de vuelta
            response = f"Tarea '{task}' procesada exitosamente."
            conn.sendall(response.encode('utf-8'))
            
    except ConnectionResetError:
        print(f"[WORKER {addr}] Conexión reseteada por el cliente.")
    except Exception as e:
        print(f"[WORKER {addr}] Error: {e}")
    finally:
        # Cerrar la conexión con este cliente
        conn.close()
        print(f"[WORKER {addr}] Conexión cerrada.")

def main_server():
    """
    Función principal del servidor.
    Se encarga de escuchar y aceptar conexiones.
    """
    # 1. Crear el socket del servidor
    # AF_INET = familia de direcciones IPv4
    # SOCK_STREAM = protocolo TCP (sockets de flujo)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        
        # 2. "Atar" el socket al HOST y PORT
        s.bind((HOST, PORT))
        
        # 3. Poner el socket en modo "escucha"
        s.listen()
        
        print(f"[SERVIDOR PRINCIPAL] Escuchando en {HOST}:{PORT}...")
        
        # 4. Bucle infinito para aceptar conexiones
        while True:
            # accept() bloquea la ejecución hasta que llega un cliente
            # conn = el nuevo socket para hablar con el cliente
            # addr = la IP y puerto del cliente
            conn, addr = s.accept()
            
            # 5. Crear y lanzar el hilo worker para este cliente
            # target = la función que debe ejecutar el hilo
            # args = los argumentos que se le pasan a la función (la tupla es importante)
            client_thread = threading.Thread(target=handle_client, args=(conn, addr))
            client_thread.start()
            
            # Opcional: Imprimir cuántos workers están activos
            print(f"[SERVIDOR PRINCIPAL] Workers activos: {threading.active_count() - 1}")

if __name__ == "__main__":
    main_server()