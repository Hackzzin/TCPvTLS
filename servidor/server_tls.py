# server_tls.py — Servidor TLS robusto

import socket
import ssl
import os
import config

print("[INFO] Iniciando servidor com TLS...")


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

    os.makedirs(config.OUTPUT_DIR, exist_ok=True)

    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain(certfile=config.SERVER_CERT, keyfile=config.SERVER_KEY)

    raw_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    raw_sock.bind((config.SERVER_HOST, config.SERVER_PORT_TLS))
    raw_sock.listen(5)

    print(f"[SERVIDOR TLS] Aguardando conexões em {config.SERVER_HOST}:{config.SERVER_PORT_TLS} ...")

    while True:
        conn, addr = raw_sock.accept()
        print(f"[CONEXÃO TLS] Cliente conectado: {addr}")

        try:
            tls_conn = context.wrap_socket(conn, server_side=True)

            filename = recv_line(tls_conn)
            filesize = int(recv_line(tls_conn))

            print(f"[INFO] Recebendo '{filename}' ({filesize} bytes) via TLS")

            filedata = recv_exact(tls_conn, filesize)

            filepath = os.path.join(config.OUTPUT_DIR, filename)
            with open(filepath, "wb") as f:
                f.write(filedata)

            print(f"[OK] Arquivo salvo: {filepath}")

        except Exception as e:
            print(f"[ERRO TLS] {e}")

        finally:
            try:
                tls_conn.close()
            except:
                pass
            print("[CONEXÃO TLS] Encerrada.\n")


if __name__ == "__main__":
    start_server_tls()
