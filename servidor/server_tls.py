# server_tls.py — Servidor para conexões via TLS

import socket
import ssl
import os
import config

def start_server_tls():

    # Garante que a pasta de saída exista
    os.makedirs(config.OUTPUT_DIR, exist_ok=True)

    # Cria contexto TLS
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)

    # Carrega certificado e chave do servidor
    context.load_cert_chain(certfile=config.SERVER_CERT, keyfile=config.SERVER_KEY)

    # (Opcional) Validar certificados de cliente — não obrigatório no trabalho
    if config.CA_CERT:
        context.load_verify_locations(config.CA_CERT)
        # context.verify_mode = ssl.CERT_REQUIRED   # Só se quiser mutual TLS

    # Socket normal
    raw_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    raw_socket.bind((config.SERVER_HOST, config.SERVER_PORT_TLS))
    raw_socket.listen(5)

    print(f"[SERVIDOR-TLS] Aguardando conexões em {config.SERVER_HOST}:{config.SERVER_PORT_TLS} ...")

    while True:
        conn, addr = raw_socket.accept()
        print(f"[CONEXÃO TLS] Cliente conectado: {addr}")

        try:
            # Encapsula o socket com TLS
            tls_conn = context.wrap_socket(conn, server_side=True)

            # Recebe nome do arquivo
            filename = b""
            while not filename.endswith(b"\n"):
                filename += tls_conn.recv(1)

            filename = filename.decode().strip()

            filepath = os.path.join(config.OUTPUT_DIR, filename)
            print(f"[INFO] Recebendo arquivo (TLS): {filename}")

            # Recebe conteúdo
            with open(filepath, "wb") as f:
                while True:
                    data = tls_conn.recv(config.BUFFER_SIZE)
                    if not data:
                        break
                    f.write(data)

            print(f"[OK] Arquivo salvo em: {filepath}")

        except Exception as e:
            print(f"[ERRO TLS] {e}")

        finally:
            try:
                tls_conn.close()
            except:
                pass
            print("[CONEXÃO TLS] Encerrada.\n")
