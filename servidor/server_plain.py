# server_plain.py — Servidor sem TLS (protocolo robusto)
import socket
import os
import threading
import config

# Flag global para controlar quando parar o servidor
server_running = True


def recv_line(sock):
    #Lê até '\n', sem TLS
    data = b""
    while not data.endswith(b"\n"):
        chunk = sock.recv(1)
        if not chunk:
            raise ConnectionError("Conexão encerrada inesperadamente.")
        data += chunk
    return data.decode().strip()


def recv_exact(sock, total_bytes):
    #Lê exatamente total_bytes bytes
    data = b""
    while len(data) < total_bytes:
        chunk = sock.recv(min(config.BUFFER_SIZE, total_bytes - len(data)))
        if not chunk:
            raise ConnectionError("Conexão encerrou antes do envio completo.")
        data += chunk
    return data


def start_server_plain():
    global server_running
    
    # Define pasta de saída relativa ao diretório pai (../recebidos)
    base_dir = os.path.dirname(os.path.abspath(__file__))  # servidor/
    output_dir = os.path.normpath(os.path.join(base_dir, os.pardir, config.OUTPUT_DIR))
    os.makedirs(output_dir, exist_ok=True)

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((config.SERVER_HOST, config.SERVER_PORT_PLAIN))
    server.listen(5)
    server.settimeout(1.0) # Timeout para checar flag de parada

    print(f"[SERVIDOR] Aguardando conexões em {config.SERVER_HOST}:{config.SERVER_PORT_PLAIN} ...")
    print("[DICA] Digite 'x' e pressione Enter para parar o servidor.\n")

    while server_running:
        try:
            conn, addr = server.accept()
            print(f"[CONEXÃO] Cliente conectado: {addr}")

            try:
                filename = recv_line(conn)

                # Se o cliente não envia tamanho, lemos até o socket fechar
                print(f"[INFO] Recebendo '{filename}' (lendo até EOF)")

                # Lê todo o restante até EOF
                file_chunks = []
                while True:
                    chunk = conn.recv(config.BUFFER_SIZE)
                    if not chunk:
                        break
                    file_chunks.append(chunk)

                filedata = b"".join(file_chunks)

                print(f"[DEBUG] Bytes recebidos: {len(filedata)}")

                if not filename.lower().endswith('.txt'):
                    filename = filename + '.txt'

                # Salva o arquivo recebido
                filepath = os.path.join(output_dir, filename)
                with open(filepath, "wb") as f:
                    f.write(filedata)

                print(f"[OK] Arquivo salvo: {filepath}")

            except Exception as e:
                print(f"[ERRO] {e}")

            finally:
                try:
                    conn.close()
                except:
                    pass
                print("[CONEXÃO] Encerrada.\n")
        
        except socket.timeout:
            # Timeout para permitir verificar a flag de parada
            continue
        except Exception as e:
            if server_running:
                print(f"[ERRO] {e}")

    server.close()
    print("\n[SERVIDOR] Encerrado.")


def input_listener_plain():
    #Escuta entrada do usuário e sinaliza parada quando 'x' é digitado
    global server_running
    while server_running:
        try:
            user_input = input().strip().lower()
            if user_input == 'x':
                print("\n[INFO] Sinal de parada recebido...")
                server_running = False
                break
        except:
            pass


if __name__ == "__main__":
    # Inicia thread de escuta de entrada
    input_thread = threading.Thread(target=input_listener_plain, daemon=True)
    input_thread.start()
    
    start_server_plain()
