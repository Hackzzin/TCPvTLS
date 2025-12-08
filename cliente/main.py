import os
import config
from sender_plain import send_plain
from sender_tls import send_tls


def main():

    print("=== Cliente de Envio de Arquivos ===")

    # Escolha do modo
    mode = ""
    while mode not in ("plain", "tls"):
        mode = input("Escolha o modo de envio ('plain' ou 'tls'): ").strip().lower()

    # Escolha do arquivo
    filename = input("Digite o nome do arquivo (sem extensão .txt): ").strip()
    filepath = os.path.join("mensagens", filename + ".txt")

    # Verifica existência antes de enviar
    if not os.path.isfile(filepath):
        print(f"\n[ERRO] Arquivo não encontrado em: {filepath}")
        return

    # Envio
    if mode == "plain":
        print("\n[INFO] Enviando arquivo em texto plano...")
        send_plain(filepath)
    else:
        print("\n[INFO] Enviando arquivo com TLS...")
        send_tls(filepath)


if __name__ == "__main__":
    main()
