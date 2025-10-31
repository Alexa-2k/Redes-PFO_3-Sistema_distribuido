import socket

# --- Configuración del Cliente ---
HOST = '127.0.0.1'  # El HOST del servidor
PORT = 65432        # El PORT del servidor

def run_client():
    # 1. Crear el socket del cliente
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        
        try:
            # 2. Conectarse al servidor
            print(f"Conectando a {HOST}:{PORT}...")
            s.connect((HOST, PORT))
            print("¡Conectado!")

            # 3. Pedir al usuario la tarea a enviar
            message = input("Introduce la tarea a enviar (o 'salir' para cerrar): ")

            if message.lower() == 'salir':
                return False # Termina el bucle

            # 4. Enviar la tarea (codificada a bytes)
            print(f"Enviando tarea: '{message}'")
            s.sendall(message.encode('utf-8'))

            # 5. Recibir la respuesta del servidor
            data = s.recv(1024)
            response = data.decode('utf-8')
            
            print(f"[RESPUESTA SERVIDOR] {response}")
            print("-" * 30)

        except ConnectionRefusedError:
            print("Error: No se pudo conectar. ¿Está el servidor corriendo?")
            return False # Termina el bule
        except Exception as e:
            print(f"Ocurrió un error: {e}")
            return False # Termina el bucle
            
    return True # Sigue en el bucle

if __name__ == "__main__":
    while True:
        if not run_client():
            break
    print("Cliente cerrado.")