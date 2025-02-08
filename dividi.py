import os

# Função para dividir um arquivo grande em partes menores de no máximo 100 MB
def dividir_arquivo(nome_arquivo, tamanho_max_mb):
    tamanho_max_bytes = tamanho_max_mb * 1024 * 1024  # Converter MB para bytes
    with open(nome_arquivo, 'rb') as arquivo:  # Abrir o arquivo em modo binário
        cont = 1
        while True:
            parte = arquivo.read(tamanho_max_bytes)
            if not parte:
                break
            nome_base, extensao = os.path.splitext(nome_arquivo)
            novo_arquivo = f"{nome_base}_dividido{cont}.txt"
            with open(novo_arquivo, 'wb') as arquivo_parte:
                arquivo_parte.write(parte)
            cont += 1

# Função para calcular e mostrar o progresso
def mostrar_progresso(atual, total):
    progresso = (atual / total) * 100
    print(f"Progresso: {progresso:.2f}%")

# Função principal que busca todos os arquivos .txt na pasta e realiza a divisão
def dividir_arquivos_na_pasta(pasta, tamanho_max_mb):
    arquivos_txt = [f for f in os.listdir(pasta) if f.endswith('.txt')]
    total_arquivos = len(arquivos_txt)
    
    for indice, arquivo in enumerate(arquivos_txt, start=1):
        caminho_arquivo = os.path.join(pasta, arquivo)
        print(f"Dividindo o arquivo: {arquivo}")
        dividir_arquivo(caminho_arquivo, tamanho_max_mb)
        mostrar_progresso(indice, total_arquivos)

# Caminho da pasta onde os arquivos estão
pasta_atual = os.getcwd()

# Dividir os arquivos em partes de no máximo 100 MB
dividir_arquivos_na_pasta(pasta_atual, 100)
