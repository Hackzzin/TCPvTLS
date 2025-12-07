# server_tls.py — Servidor TLS robusto

import socket
import ssl
import os
import threading
import config

print("[INFO] Iniciando servidor com TLS...")

# Flag global para controlar quando parar o servidor
server_running = True


def recv_line(sock):
    """Lê até '\n' — compatível com TLS."""
    data = b""
    while not data.endswith(b"\n"):
        chunk = sock.recv(1)
        if not chunk:
            raise ConnectionError("Conexão encerrada inesperadamente.")
        data += chunk
    return data.decode().strip()


def recv_exact(sock, total_bytes):
    """Lê exatamente total_bytes bytes, mesmo com TLS."""
    data = b""
    while len(data) < total_bytes:
        chunk = sock.recv(min(config.BUFFER_SIZE, total_bytes - len(data)))
        if not chunk:
            raise ConnectionError("Conexão encerrou antes do envio completo.")
        data += chunk
    return data


def start_server_tls():
    global server_running
    
    # Define pasta de saída relativa ao diretório pai (../recebidos)
    base_dir = os.path.dirname(os.path.abspath(__file__))  # servidor/
    output_dir = os.path.normpath(os.path.join(base_dir, os.pardir, config.OUTPUT_DIR))
    os.makedirs(output_dir, exist_ok=True)

    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain(certfile=config.SERVER_CERT, keyfile=config.SERVER_KEY)

    raw_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    raw_sock.bind((config.SERVER_HOST, config.SERVER_PORT_TLS))
    raw_sock.listen(5)
    raw_sock.settimeout(1.0)  # Define timeout para permitir verificar flag de parada

    print(f"[SERVIDOR TLS] Aguardando conexões em {config.SERVER_HOST}:{config.SERVER_PORT_TLS} ...")
    print("[DICA] Digite 'x' e pressione Enter para parar o servidor.\n")

    while server_running:
        try:
            conn, addr = raw_sock.accept()
            print(f"[CONEXÃO TLS] Cliente conectado: {addr}")

            tls_conn = None
            try:
                print(f"[DEBUG] Iniciando TLS handshake com {addr}...")
                tls_conn = context.wrap_socket(conn, server_side=True)
                print(f"[DEBUG] TLS handshake completo com {addr}")

                # Primeiro recebo o nome do arquivo (protocolo atual do cliente)
                filename = recv_line(tls_conn)

                # Se o cliente não envia tamanho, lemos até o socket fechar
                print(f"[INFO] Recebendo '{filename}' via TLS (lendo até EOF)")

                # Lê todo o restante até EOF
                file_chunks = []
                while True:
                    chunk = tls_conn.recv(config.BUFFER_SIZE)
                    if not chunk:
                        break
                    file_chunks.append(chunk)

                filedata = b"".join(file_chunks)

                # Debug: mostrar quantos bytes recebidos
                print(f"[DEBUG] Bytes recebidos: {len(filedata)}")

                # Assegura extensão .txt
                if not filename.lower().endswith('.txt'):
                    filename = filename + '.txt'

                filepath = os.path.join(output_dir, filename)
                with open(filepath, "wb") as f:
                    f.write(filedata)

                print(f"[OK] Arquivo salvo: {filepath}")

            except Exception as e:
                print(f"[ERRO TLS] {e}")

            finally:
                if tls_conn is not None:
                    try:
                        tls_conn.close()
                    except:
                        pass
                else:
                    try:
                        conn.close()
                    except:
                        pass
                print("[CONEXÃO TLS] Encerrada.\n")
        
        except socket.timeout:
            # Timeout para permitir verificar a flag de parada
            continue
        except Exception as e:
            if server_running:
                print(f"[ERRO] {e}")

    raw_sock.close()
    print("\n[SERVIDOR TLS] Encerrado.")


def input_listener_tls():
    """Escuta entrada do usuário e sinaliza parada quando 'x' é digitado."""
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
    input_thread = threading.Thread(target=input_listener_tls, daemon=True)
    input_thread.start()
    
    start_server_tls()
