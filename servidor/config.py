# config.py — Configurações básicas do servidor
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))      # servidor/
ROOT_DIR = os.path.dirname(BASE_DIR)                       # TCPvTLS/

SERVER_CERT = "certificados/server_cert.pem"
SERVER_KEY  = "certificados/server_key.pem"
CA_CERT     = "certificados/ca_cert.pem"

# Endereços e portas de escuta
SERVER_HOST = "0.0.0.0"     # Aceita conexões externas também
SERVER_PORT_PLAIN = 5000    # Porta para conexões sem TLS
SERVER_PORT_TLS = 5001      # Porta para conexões TLS

# Tamanho do buffer de recebimento (em bytes)
BUFFER_SIZE = 4 * 1024  # 4 KB

# Pasta de saída dos arquivos recebidos
OUTPUT_DIR = "recebidos"
