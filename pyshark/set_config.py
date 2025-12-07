import sys
import os

# Adiciona o diretório do cliente ao path
sys.path.append(os.path.abspath("../cliente"))
import config as client_config


print(client_config.SERVER_HOST)
print(client_config.SERVER_PORT_PLAIN)
print(client_config.SERVER_PORT_TLS)
