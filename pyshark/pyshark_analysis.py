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
    interface=r'\Device\NPF_Loopback', 
    bpf_filter=f'tcp port {client_config.SERVER_PORT_PLAIN} or tcp port {client_config.SERVER_PORT_TLS}',
    tshark_path=TSHARK_PATH  # caminho exato do TShark
)

print("Capturando pacotes... pressione Ctrl+C para parar")

try:
    for packet in capture.sniff_continuously():
        try:
            # Extrai informações TCP
            port = int(packet.tcp.port)
            size = int(packet.length)
            timestamp = float(packet.sniff_time.timestamp())

            # Armazena dados conforme porta
            if port == client_config.SERVER_PORT_PLAIN:
                plain_sizes.append(size)
                plain_times.append(timestamp)
            elif port == client_config.SERVER_PORT_TLS:
                tls_sizes.append(size)
                tls_times.append(timestamp)

        except AttributeError:
            continue

except (KeyboardInterrupt, EOFError):
    print("\nCaptura finalizada!")


print("\n=== Análise de Tamanho ===")
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


print("\n=== Análise de Latência ===")
if plain_times:
    plain_latency_total = plain_times[-1] - plain_times[0]
    print(f"Tempo total de envio texto plano: {plain_latency_total:.6f} s")
    if len(plain_times) > 1:
        plain_intervals = [t2 - t1 for t1, t2 in zip(plain_times[:-1], plain_times[1:])]
        print(f"Latência média entre pacotes: {statistics.mean(plain_intervals):.6f} s")

if tls_times:
    tls_latency_total = tls_times[-1] - tls_times[0]
    print(f"Tempo total de envio TLS: {tls_latency_total:.6f} s")
    if len(tls_times) > 1:
        tls_intervals = [t2 - t1 for t1, t2 in zip(tls_times[:-1], tls_times[1:])]
        print(f"Latência média entre pacotes: {statistics.mean(tls_intervals):.6f} s")
