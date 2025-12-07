import os
from datetime import datetime, timedelta

from cryptography import x509
from cryptography.x509.oid import NameOID, ExtendedKeyUsageOID
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.serialization import Encoding, PrivateFormat, NoEncryption


PASTA = "certificados"
os.makedirs(PASTA, exist_ok=True)


# =====================================================
# 1️⃣ GERAR CA (Certificate Authority)
# =====================================================
def gerar_ca():
    print("[1/4] Gerando chave privada da CA...")

    ca_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048
    )

    print("[2/4] Criando certificado da CA...")

    subject = issuer = x509.Name([
        x509.NameAttribute(NameOID.COUNTRY_NAME, "BR"),
        x509.NameAttribute(NameOID.ORGANIZATION_NAME, "Minha CA Local"),
        x509.NameAttribute(NameOID.COMMON_NAME, "Minha CA Local"),
    ])

    ca_cert = (
        x509.CertificateBuilder()
        .subject_name(subject)
        .issuer_name(issuer)
        .public_key(ca_key.public_key())
        .serial_number(x509.random_serial_number())
        .not_valid_before(datetime.utcnow())
        .not_valid_after(datetime.utcnow() + timedelta(days=3650))  # 10 anos
        .add_extension(x509.BasicConstraints(ca=True, path_length=None), critical=True)
        .sign(private_key=ca_key, algorithm=hashes.SHA256())
    )

    print("[3/4] Salvando chave e certificado da CA...")

    with open(f"{PASTA}/ca_key.pem", "wb") as f:
        f.write(ca_key.private_bytes(
            Encoding.PEM,
            PrivateFormat.TraditionalOpenSSL,
            NoEncryption()
        ))

    with open(f"{PASTA}/ca_cert.pem", "wb") as f:
        f.write(ca_cert.public_bytes(Encoding.PEM))

    print("[OK] CA gerada com sucesso!\n")
    return ca_key, ca_cert


# =====================================================
# 2️⃣ GERAR CERTIFICADO DO SERVIDOR
# =====================================================
def gerar_certificado_servidor(ca_key, ca_cert):
    print("[1/4] Gerando chave privada do servidor...")

    server_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048
    )

    subject = x509.Name([
        x509.NameAttribute(NameOID.COUNTRY_NAME, "BR"),
        x509.NameAttribute(NameOID.ORGANIZATION_NAME, "Servidor TLS"),
        x509.NameAttribute(NameOID.COMMON_NAME, "localhost"),
    ])

    print("[2/4] Gerando CSR (pedido de certificado)...")

    csr = (
        x509.CertificateSigningRequestBuilder()
        .subject_name(subject)
        .sign(server_key, hashes.SHA256())
    )

    print("[3/4] Assinando certificado do servidor com a CA...")

    server_cert = (
        x509.CertificateBuilder()
        .subject_name(csr.subject)
        .issuer_name(ca_cert.subject)
        .public_key(server_key.public_key())
        .serial_number(x509.random_serial_number())
        .not_valid_before(datetime.utcnow())
        .not_valid_after(datetime.utcnow() + timedelta(days=365))
        .add_extension(x509.BasicConstraints(ca=False, path_length=None), critical=True)
        .add_extension(x509.ExtendedKeyUsage([ExtendedKeyUsageOID.SERVER_AUTH]), critical=False)
        .sign(private_key=ca_key, algorithm=hashes.SHA256())
    )

    print("[4/4] Salvando chave e certificado do servidor...")

    with open(f"{PASTA}/server_key.pem", "wb") as f:
        f.write(server_key.private_bytes(
            Encoding.PEM,
            PrivateFormat.TraditionalOpenSSL,
            NoEncryption()
        ))

    with open(f"{PASTA}/server_cert.pem", "wb") as f:
        f.write(server_cert.public_bytes(Encoding.PEM))

    print("[OK] Certificado do servidor gerado!\n")


# =====================================================
# MAIN
# =====================================================
if __name__ == "__main__":
    print("=== GERADOR DE CERTIFICADOS TLS (cryptography) ===\n")

    ca_key, ca_cert = gerar_ca()
    gerar_certificado_servidor(ca_key, ca_cert)

    print("=== TODOS OS CERTIFICADOS FORAM GERADOS COM SUCESSO ===")
    print(f"Arquivos criados na pasta: {PASTA}")
