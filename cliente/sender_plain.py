# sender_plain.py — Envio sem TLS (texto plano)

import socket
from utils import read_file_chunks, file_exists, get_filename
import config

def send_plain(filepath: str):
    """Envia um arquivo para o servidor usando TCP sem criptografia."""

    if not file_exists(filepath):
        print(f"[ERRO] Arquivo não encontrado: {filepath}")
        return

    try:
        # Cria socket TCP normal
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((config.SERVER_HOST, config.SERVER_PORT))

        # Envia primeiro o nome do arquivo (simples protocolo)
        filename = get_filename(filepath)
        client_socket.sendall(filename.encode() + b"\n")

        # Envia o conteúdo do arquivo em chunks
        for chunk in read_file_chunks(filepath, config.BUFFER_SIZE):
            client_socket.sendall(chunk)

        print(f"[OK] Arquivo '{filename}' enviado sem TLS.")

    except Exception as e:
        print(f"[ERRO] Falha no envio: {e}")

    finally:
        client_socket.close()
