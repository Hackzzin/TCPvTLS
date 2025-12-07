# sender_tls.py — Envio usando TLS

import socket
import ssl
from utils import read_file_chunks, file_exists, get_filename
import config

def send_tls(filepath: str):
    """Envia um arquivo usando TLS para garantir confidencialidade."""

    if not file_exists(filepath):
        print(f"[ERRO] Arquivo não encontrado: {filepath}")
        return

    try:
        # Cria o contexto TLS (modo cliente)
        context = ssl.create_default_context()

        # Se você quiser validar o certificado do servidor,
        # assegure que possui o arquivo CA (CA_CERT_PATH)
        # Caso não valide, você pode usar: ssl._create_unverified_context()
        if config.CA_CERT_PATH:
            context.load_verify_locations(config.CA_CERT_PATH)

        # Cria socket TCP normal
        raw_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Encapsula o socket com TLS
        tls_socket = context.wrap_socket(
            raw_socket,
            server_hostname=config.SERVER_HOST   # SNI
        )

        # Conecta ao servidor TLS
        tls_socket.connect((config.SERVER_HOST, config.SERVER_PORT_TLS))

        # Envia o nome do arquivo (mesma ideia do sender_plain.py)
        filename = get_filename(filepath)
        tls_socket.sendall(filename.encode() + b"\n")

        # Envia conteúdo em chunks
        print("[DEBUG] Enviando conteúdo...")
        for chunk in read_file_chunks(filepath, config.BUFFER_SIZE):
            print(f"[DEBUG] Chunk size: {len(chunk)}")
            tls_socket.sendall(chunk)

        print(f"[OK] Arquivo '{filename}' enviado com TLS.")

    except Exception as e:
        print(f"[ERRO] Falha no envio TLS: {e}")

    finally:
        # Fecha socket TLS (e o underlying socket)
        try:
            tls_socket.close()
        except:
            pass
