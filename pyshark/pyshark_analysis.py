import pyshark
import statistics
from dotenv import load_dotenv
import os
from set_config import client_config

load_dotenv()
TSHARK_PATH = os.getenv('TSHARK_PATH')

# Inicializa listas para armazenar métricas
plain_sizes = []
tls_sizes = []
plain_times = []
tls_times = []

# Captura ao vivo
capture = pyshark.LiveCapture(
    interface=r'\Device\NPF_Loopback',  # ou outra interface correta
    bpf_filter=f'tcp port {client_config.SERVER_PORT_PLAIN} or tcp port {client_config.SERVER_PORT_TLS}',
    tshark_path= TSHARK_PATH # caminho exato do TShark no seu PC
)


print("Capturando pacotes... pressione Ctrl+C para parar")

try:
    for packet in capture.sniff_continuously():
        try:
            port = int(packet.tcp.port)
            size = int(packet.length)
            timestamp = float(packet.sniff_time.timestamp())

            if port == client_config.SERVER_PORT_PLAIN:
                plain_sizes.append(size)
                plain_times.append(timestamp)
            elif port == client_config.SERVER_PORT_TLS:
                tls_sizes.append(size)
                tls_times.append(timestamp)

        except AttributeError:
            # Pacote sem TCP
            continue

except KeyboardInterrupt:
    print("\nCaptura finalizada!")

# --- Análise de tamanho ---
if plain_sizes:
    print("=== Texto plano ===")
    print(f"Número de pacotes: {len(plain_sizes)}")
    print(f"Tamanho médio: {statistics.mean(plain_sizes):.2f} bytes")
    print(f"Tamanho total: {sum(plain_sizes)} bytes")
else:
    print("Nenhum pacote de texto plano capturado.")

if tls_sizes:
    print("=== TLS ===")
    print(f"Número de pacotes: {len(tls_sizes)}")
    print(f"Tamanho médio: {statistics.mean(tls_sizes):.2f} bytes")
    print(f"Tamanho total: {sum(tls_sizes)} bytes")
else:
    print("Nenhum pacote TLS capturado.")

# --- Análise de tempo ---
if plain_times:
    plain_latency = plain_times[-1] - plain_times[0]
    print(f"Tempo de envio texto plano: {plain_latency:.6f} s")

if tls_times:
    tls_latency = tls_times[-1] - tls_times[0]
    print(f"Tempo de envio TLS: {tls_latency:.6f} s")
