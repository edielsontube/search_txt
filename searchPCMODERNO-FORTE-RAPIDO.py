import os
import re
from concurrent.futures import ProcessPoolExecutor
from colorama import Fore, Style, init

# Inicializa o Colorama para cores no terminal
init(autoreset=True)

def exibir_banner():
    banner = f"""
{Fore.CYAN}==========================================
{Fore.YELLOW}    FERRAMENTA DE BUSCA LOCAL EM TXT
{Fore.CYAN}==========================================
    """
    print(banner)

def buscar_no_arquivo(padrao_arquivo):
    """Busca um padrão em um arquivo e retorna as linhas encontradas."""
    padrao, arquivo = padrao_arquivo  # Desempacota o padrão e o arquivo
    linhas_encontradas = set()  # Usar um conjunto para evitar duplicatas
    with open(arquivo, 'r', encoding='utf-8', errors='ignore') as f:
        for linha in f:
            if re.search(padrao, linha):
                linhas_encontradas.add(linha.strip())
    return linhas_encontradas

def buscar_em_arquivos_paralelo(padrao, arquivos):
    """Busca em vários arquivos usando paralelismo."""
    resultados = set()
    total_arquivos = len(arquivos)

    # Usar ProcessPoolExecutor para paralelismo
    with ProcessPoolExecutor() as executor:
        # Mapear os arquivos com o padrão
        jobs = ((padrao, arquivo) for arquivo in arquivos)
        for i, resultado_parcial in enumerate(executor.map(buscar_no_arquivo, jobs), start=1):
            progresso = (i / total_arquivos) * 100
            print(f"{Fore.GREEN}[{i}/{total_arquivos}] {Fore.WHITE}Procurando em: ({Fore.YELLOW}{progresso:.2f}%{Fore.WHITE})")
            resultados.update(resultado_parcial)

    return resultados

def buscar_em_arquivos(padrao):
    """Busca um padrão em todos os arquivos .txt na pasta atual."""
    pasta = os.getcwd()
    arquivos_txt = [os.path.join(pasta, f) for f in os.listdir(pasta) if f.endswith('.txt')]
    return buscar_em_arquivos_paralelo(padrao, arquivos_txt)

def limpar_caracteres_invalidos(nome_arquivo):
    """Remove caracteres inválidos do nome do arquivo e evita que comece com ponto."""
    nome_arquivo = re.sub(r'[\\/*?:"<>|]', '_', nome_arquivo)  # Substitui caracteres inválidos por "_"
    nome_arquivo = re.sub(r'^[.]', '', nome_arquivo)  # Remove ponto no início do nome
    return nome_arquivo

def salvar_resultados(padrao, resultados):
    """Salva os resultados encontrados em um arquivo na pasta 'ENCONTRADO'."""
    pasta_resultados = os.path.join(os.getcwd(), 'ENCONTRADO')
    os.makedirs(pasta_resultados, exist_ok=True)

    # Limpar caracteres especiais do nome do arquivo
    nome_arquivo = limpar_caracteres_invalidos(padrao)

    arquivo_resultado = os.path.join(pasta_resultados, f"{nome_arquivo}.txt")
    with open(arquivo_resultado, 'w', encoding='utf-8') as f:
        f.write("\n".join(resultados))

    print(f"\n{Fore.CYAN}Total de resultados únicos encontrados: {Fore.GREEN}{len(resultados)}")
    print(f"{Fore.CYAN}Resultados salvos em: {Fore.GREEN}{arquivo_resultado}")

def limpar_terminal():
    """Limpa o terminal de acordo com o sistema operacional."""
    os.system('cls' if os.name == 'nt' else 'clear')

def main():
    while True:
        exibir_banner()
        padrao = input(f"{Fore.YELLOW}Digite a palavra-chave para buscar: {Style.RESET_ALL}").strip()

        if not padrao:
            print(f"{Fore.RED}Você deve digitar uma palavra-chave válido.")
            continue

        print(f"{Fore.CYAN}Buscando por '{padrao}' nos arquivos .txt na pasta atual...")
        resultados = buscar_em_arquivos(padrao)

        if resultados:
            salvar_resultados(padrao, resultados)
        else:
            print(f"{Fore.RED}Nenhum resultado encontrado.")

        limpar = input(f"\n{Fore.YELLOW}Deseja limpar o terminal antes de continuar? (s/n): {Style.RESET_ALL}").strip().lower()
        if limpar == 's':
            limpar_terminal()

if __name__ == "__main__":
    main()
