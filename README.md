# TCPvTLS
A repo made for an uni project that implements a client-server conection in both TCP and TLS, comparing them.


## How to generate certificates and keys
You must have [OpenSSL](https://slproweb.com/products/Win32OpenSSL.html) to run the script. It was also made with Windows Powershell in mind.
After that, from the root directory, run `Python .\gerar_certificados.ps1`

## How to run the code
Before all, the user has to be in the root directory i.e. TCPvTLS to run the code.

First, you can run an instance of each type of server using:
`Python .\servidor\server_plain.py` for the server without TLS.
`Python .\servidor\server_tls.py` for the server with TLS.
All configs for the server are in `TCPvTLS\servidor\config.py`

After that, for the client to send a message to the server you created, you must run:
`Python .\cliente\main.py`
All confis for the client are in `TCPvTLS\cliente\config.py`
