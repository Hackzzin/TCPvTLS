import os

#Funções auxiliares do cliente para manipulação de arquivos. (uteis para envio com e sem TLS)
def file_exists(filepath: str) -> bool:
    #Verifica se o arquivo existe e é um arquivo regular
    return os.path.isfile(filepath)

def read_file_chunks(filepath: str, chunk_size: int):
    #Lê um arquivo em chunks
    with open(filepath, "rb") as f:
        while True:
            data = f.read(chunk_size)
            if not data:
                break
            yield data

def get_filename(filepath: str) -> str:
    #Extrai somente o nome do arquivo do path
    return os.path.basename(filepath)
