# server_plain.py — Servidor para conexões sem TLS

import socket
import os
import config

def start_server_plain():

    # Garante que a pasta de saída exista
    os.makedirs(config.OUTPUT_DIR, exist_ok=True)

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((config.SERVER_HOST, config.SERVER_PORT_PLAIN))
    server_socket.listen(5)

    print(f"[SERVIDOR-PLAIN] Aguardando conexões em {config.SERVER_HOST}:{config.SERVER_PORT_PLAIN} ...")

    while True:
        conn, addr = server_socket.accept()
        print(f"[CONEXÃO] Cliente conectado: {addr}")

        try:
            # Recebe o nome do arquivo (até encontrar '\n')
            filename = b""
            while not filename.endswith(b"\n"):
                filename += conn.recv(1)

            filename = filename.decode().strip()

            # Caminho completo para salvar
            filepath = os.path.join(config.OUTPUT_DIR, filename)
            print(f"[INFO] Recebendo arquivo: {filename}")

            with open(filepath, "wb") as f:
                while True:
                    data = conn.recv(config.BUFFER_SIZE)
                    if not data:
                        break
                    f.write(data)

            print(f"[OK] Arquivo salvo em: {filepath}")

        except Exception as e:
            print(f"[ERRO] Problema na recepção: {e}")

        finally:
            conn.close()
            print("[CONEXÃO] Encerrada.\n")
