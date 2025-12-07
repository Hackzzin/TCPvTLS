$OpenSSL = "C:\Program Files\OpenSSL-Win64\bin\openssl.exe"

# ================================
# Script PowerShell para gerar:
# - CA (ca.crt, ca.key)
# - Certificado Servidor (servidor.crt, servidor.key)
# - Certificado Cliente (cliente.crt, cliente.key)
# ================================

# Caminho da saída
$certDir = "certificados"
if (-Not (Test-Path $certDir)) {
    New-Item -ItemType Directory $certDir | Out-Null
}

Write-Host "Gerando certificados em: $certDir"
Set-Location $certDir

# -------- 1. Cria CA --------
Write-Host "`n[1/8] Gerando CA..."
& $OpenSSL genrsa -out ca.key 4096
& $OpenSSL req -x509 -new -nodes -key ca.key -sha256 -days 3650 -out ca.crt -subj "/CN=MinhaCA"

# -------- 2. Cria chave servidor --------
Write-Host "`n[2/8] Gerando chave do servidor..."
& $OpenSSL genrsa -out servidor.key 2048

# -------- 3. CSR do Servidor --------
Write-Host "`n[3/8] Gerando CSR do servidor..."
& $OpenSSL req -new -key servidor.key -out servidor.csr -subj "/CN=localhost"

# -------- 4. Cria arquivo de extensões SAN --------
Write-Host "`n[4/8] Criando arquivo SAN..."
@"
authorityKeyIdentifier=keyid,issuer
basicConstraints=CA:FALSE
keyUsage = digitalSignature, keyEncipherment
extendedKeyUsage = serverAuth
subjectAltName = @alt_names

[alt_names]
DNS.1 = localhost
IP.1 = 127.0.0.1
"@ | Set-Content san_server.ext

# -------- 5. Assina certificado do Servidor --------
Write-Host "`n[5/8] Assinando certificado do servidor com a CA (com SAN)..."
& $OpenSSL x509 -req -in servidor.csr -CA ca.crt -CAkey ca.key -CAcreateserial `
    -out servidor.crt -days 825 -sha256 -extfile san_server.ext

# -------- 6. Cria chave cliente --------
Write-Host "`n[6/8] Gerando chave do cliente..."
& $OpenSSL genrsa -out cliente.key 2048

# -------- 7. CSR do Cliente --------
Write-Host "`n[7/8] Gerando CSR do cliente..."
& $OpenSSL req -new -key cliente.key -out cliente.csr -subj "/CN=cliente"

# -------- 8. Assina certificado do Cliente --------
Write-Host "`n[8/8] Assinando certificado do cliente com a CA..."
& $OpenSSL x509 -req -in cliente.csr -CA ca.crt -CAkey ca.key -CAcreateserial `
    -out cliente.crt -days 825 -sha256

Write-Host "`n==============================="
Write-Host "Certificados gerados com sucesso!"
Write-Host "Pasta: $certDir"
Write-Host "Arquivos criados:"
Write-Host " - ca.key / ca.crt"
Write-Host " - servidor.key / servidor.csr / servidor.crt (COM SAN)"
Write-Host " - cliente.key / cliente.csr / cliente.crt"
Write-Host "==============================="
