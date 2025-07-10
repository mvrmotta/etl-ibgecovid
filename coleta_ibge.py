import requests
import pandas as pd

def extrair_dados_ibge(ano=2021):
    """
    Extrai e retorna um DataFrame com dados de população estimada por município (IBGE - tabela 6579).
    """

    url = f"https://servicodados.ibge.gov.br/api/v3/agregados/6579/periodos/{ano}/variaveis/9324?localidades=N6[all]"

    print(f"Solicitando dados do IBGE para o ano {ano}...")
    response = requests.get(url)

    if response.status_code != 200:
        raise Exception(f"Erro ao acessar a API do IBGE: {response.status_code}")

    json_data = response.json()

    # ===== TRANSFORMAÇÃO =====
    dados_extraidos = []

    for municipio in json_data[0]['resultados'][0]['series']:
        nome_municipio = municipio['localidade']['nome']
        cod_municipio = municipio['localidade']['id']
        populacao = municipio['serie'].get(str(ano), None)

        if populacao is not None:
            try:
                populacao = int(float(populacao))
            except ValueError:
                populacao = None

        if " - " in nome_municipio:
            nome, uf = nome_municipio.split(" - ")
        else:
            nome, uf = nome_municipio, ""

        dados_extraidos.append({
            "codigo_municipio": cod_municipio,
            "nome_municipio": nome,
            "uf": uf,
            "populacao_estimada": populacao
        })

    df = pd.DataFrame(dados_extraidos)

    print(f"Total de registros extraídos: {len(df)}")

    # ===== TRATAMENTO =====
    duplicatas = df.duplicated().sum()
    df = df.drop_duplicates()
    print(f"Duplicatas removidas: {duplicatas}")

    nulos = df.isnull().sum()
    total_nulos = nulos.sum()
    print("Valores nulos detectados por coluna:")
    print(nulos[nulos > 0])

    df = df.dropna()
    print(f"Total de linhas com nulos removidas: {total_nulos}")

    df = df.sort_values(by=["uf", "nome_municipio"]).reset_index(drop=True)

    print(f"Total final de registros após limpeza: {len(df)}")
    
    return df