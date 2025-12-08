
# Endereço e porta do servidor
SERVER_HOST = "127.0.0.1"   
SERVER_PORT_PLAIN = 5000    # Porta para conexões sem TLS
SERVER_PORT_TLS = 5001      # Porta para conexões com TLS

# Tamanho do buffer para envio (em bytes)
BUFFER_SIZE = 4 * 1024  # 4 KB

# Caminho para o certificado da CA (usado apenas no modo TLS)
CA_CERT_PATH = "certificados/ca.crt"
