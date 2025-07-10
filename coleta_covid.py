import requests
import pandas as pd
import getpass

def extrair_dados_covid():
    """
    Extrai dados de COVID-19 por município a partir da API do Brasil.IO,
    mantendo apenas as colunas relevantes e retornando um DataFrame.
    """

    # Solicita a chave de API de forma segura
    token = getpass.getpass("Digite sua API Key do Brasil.IO: ")
    headers = {"Authorization": f"Token {token}"}

    url = "https://api.brasil.io/v1/dataset/covid19/caso_full/data/?is_last=True&place_type=city"

    print("Coletando dados da API Brasil.IO...")
    dados = []

    while url:
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            raise Exception(f"Erro na requisição: {response.status_code}")

        json_data = response.json()
        dados.extend(json_data["results"])
        url = json_data["next"]

    # ===== TRANSFORMAÇÃO =====
    df_covid = pd.DataFrame(dados)

    # Selecionar apenas as colunas desejadas
    df_covid = df_covid[[
        "city",
        "city_ibge_code",
        "state",
        "last_available_confirmed",
        "last_available_deaths",
        "last_available_death_rate"
    ]]

    # Renomear colunas para padronizar
    df_covid.rename(columns={
        "city": "nome_municipio",
        "city_ibge_code": "codigo_municipio",
        "state": "uf",
        "last_available_confirmed": "casos_confirmados",
        "last_available_deaths": "obitos_confirmados",
        "last_available_death_rate": "taxa_mortalidade"
    }, inplace=True)

    # ===== LIMPEZA =====
    duplicatas = df_covid.duplicated().sum()
    df_covid = df_covid.drop_duplicates()
    nulos = df_covid.isnull().sum()
    total_nulos = nulos.sum()

    # ===== LOG =====
    print(f"Registros extraídos: {len(df_covid)}")
    print(f"Duplicatas removidas: {duplicatas}")
    print("Valores nulos por coluna:")
    print(nulos[nulos > 0])
    print(f"Total de nulos: {total_nulos}")

    return df_covid
