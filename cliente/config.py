# Configurações básicas do cliente

# Endereço e porta do servidor
SERVER_HOST = "127.0.0.1"   # Pode ser alterado caso o servidor rode em outra máquina
SERVER_PORT_PLAIN = 5000    # Porta para conexões sem TLS
SERVER_PORT_TLS = 5001      # Porta para conexões com TLS

# Tamanho do buffer para envio (em bytes)
BUFFER_SIZE = 10 * 1024  # 10 KB

# Caminho para o certificado da CA (usado apenas no modo TLS)
# Caso você não valide o certificado do servidor, pode deixar None
CA_CERT_PATH = "certs/ca.crt"
