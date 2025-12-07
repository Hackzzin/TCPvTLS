# server_plain.py — Servidor sem TLS (protocolo robusto)
import socket
import os
import config


def recv_line(sock):
    """Lê até '\n', sem TLS."""
    data = b""
    while not data.endswith(b"\n"):
        chunk = sock.recv(1)
        if not chunk:
            raise ConnectionError("Conexão encerrada inesperadamente.")
        data += chunk
    return data.decode().strip()


def recv_exact(sock, total_bytes):
    """Lê exatamente total_bytes bytes."""
    data = b""
    while len(data) < total_bytes:
        chunk = sock.recv(min(config.BUFFER_SIZE, total_bytes - len(data)))
        if not chunk:
            raise ConnectionError("Conexão encerrou antes do envio completo.")
        data += chunk
    return data


def start_server_plain():

    os.makedirs(config.OUTPUT_DIR, exist_ok=True)

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((config.SERVER_HOST, config.SERVER_PORT_PLAIN))
    server.listen(5)

    print(f"[SERVIDOR] Aguardando conexões em {config.SERVER_HOST}:{config.SERVER_PORT_PLAIN} ...")

    while True:
        conn, addr = server.accept()
        print(f"[CONEXÃO] Cliente conectado: {addr}")

        try:
            filename = recv_line(conn)
            filesize = int(recv_line(conn))

            print(f"[INFO] Recebendo '{filename}' ({filesize} bytes)")

            filedata = recv_exact(conn, filesize)

            filepath = os.path.join(config.OUTPUT_DIR, filename)
            with open(filepath, "wb") as f:
                f.write(filedata)

            print(f"[OK] Arquivo salvo: {filepath}")

        except Exception as e:
            print(f"[ERRO] {e}")

        finally:
            conn.close()
            print("[CONEXÃO] Encerrada.\n")


if __name__ == "__main__":
    start_server_plain()
