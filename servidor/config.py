# config.py — Configurações básicas do servidor

# Endereços e portas de escuta
SERVER_HOST = "0.0.0.0"     # Aceita conexões externas também
SERVER_PORT_PLAIN = 5000    # Porta para conexões sem TLS
SERVER_PORT_TLS = 5001      # Porta para conexões TLS

# Tamanho do buffer de recebimento (em bytes)
BUFFER_SIZE = 4 * 1024  # 4 KB

# Caminhos para certificados (usados no TLS)
SERVER_CERT = "certificados/server.crt"
SERVER_KEY  = "certificados/server.key"
CA_CERT     = "certificados/ca.crt"   # Caso valide o cliente; opcional

# Pasta de saída dos arquivos recebidos
OUTPUT_DIR = "recebidos"
