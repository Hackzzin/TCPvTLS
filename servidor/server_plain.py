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
    # Define pasta de saída relativa ao diretório pai (../recebidos)
    base_dir = os.path.dirname(os.path.abspath(__file__))  # servidor/
    output_dir = os.path.normpath(os.path.join(base_dir, os.pardir, config.OUTPUT_DIR))
    os.makedirs(output_dir, exist_ok=True)

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((config.SERVER_HOST, config.SERVER_PORT_PLAIN))
    server.listen(5)

    print(f"[SERVIDOR] Aguardando conexões em {config.SERVER_HOST}:{config.SERVER_PORT_PLAIN} ...")

    while True:
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
            print(f"[ERRO] {e}")

        finally:
            conn.close()
            print("[CONEXÃO] Encerrada.\n")


if __name__ == "__main__":
    start_server_plain()
