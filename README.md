# Case Técnico – ETL com Dados do IBGE e COVID-19 (Brasil.IO)

Este projeto tem como objetivo demonstrar um pipeline ETL utilizando Python, integrando dados públicos do IBGE e Brasil.IO para construção de um banco de dados relacional com modelagem adequada. O projeto foi desenvolvido como parte de um case técnico para a WeBurn.

---

## Tecnologias e Ferramentas Utilizadas

- **Python 3.x**
- **pandas** e **requests** (ETL)
- **SQLite3** (armazenamento relacional simples)
- **Jupyter Notebook** (execução e visualização)
- **APIs utilizadas**:
  - [IBGE - População por município (API de agregados)](https://servicodados.ibge.gov.br/api/docs/agregados)
  - [Brasil.IO - Dados de COVID-19](https://brasil.io/dataset/covid19/)

---

## Estrutura do Projeto

```
├── coleta_ibge.py             # Script de extração e tratamento dos dados do IBGE
├── coleta_covid.py            # Script de extração e tratamento dos dados do Brasil.IO
├── CASE_ETL_WEBURN.ipynb      # Notebook principal que executa o pipeline completo
├── requirements.txt           # Dependências do projeto
├── README.md                  # Instruções e documentação
```

---

##  Como Executar este Projeto

### 1. Clone o repositório

```bash
git clone https://github.com/mvrmotta/etl-ibgecovid.git
cd etl-ibgecovid
```

### 2. Crie um ambiente virtual (opcional, mas recomendado)

```bash
python -m venv venv
source venv/bin/activate   # ou venv\Scripts\activate no Windows
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

### 4. Obtenha sua API Key do Brasil.IO

- Cadastre-se em: https://brasil.io/auth/register/
- Copie sua chave pessoal: https://brasil.io/token/

### 5. Execute o notebook

Abra o arquivo `CASE_ETL_WEBURN.ipynb` com Jupyter Notebook ou VSCode e siga as instruções.

Durante a execução, será solicitada sua API Key via `getpass`.

---

## O que o projeto faz

1. Extrai os dados populacionais do IBGE via API
2. Extrai os dados de COVID-19 por município via API Brasil.IO
3. Realiza limpeza, tratamento e normalização dos dados
4. Cria um banco de dados SQLite (`dados_case.db`)
5. Armazena os dados em duas tabelas modeladas com chave primária e estrangeira:
   - `populacao_ibge`
   - `covid_brasilio`

---

## Scripts SQL utilizados

O script responsável por criar o schema do banco está dentro do notebook:

```sql
CREATE TABLE populacao_ibge (
    codigo_municipio INTEGER PRIMARY KEY,
    nome_municipio TEXT NOT NULL,
    uf TEXT NOT NULL,
    populacao_estimada INTEGER NOT NULL
);

CREATE TABLE covid_brasilio (
    codigo_municipio INTEGER,
    nome_municipio TEXT NOT NULL,
    uf TEXT NOT NULL,
    casos_confirmados INTEGER,
    obitos_confirmados INTEGER,
    taxa_mortalidade REAL,
    FOREIGN KEY (codigo_municipio) REFERENCES populacao_ibge(codigo_municipio)
);
```

---

- O projeto foi construído para ser **escalável**, **simples de rodar** e **com boa modelagem de dados**.
- O uso de scripts `.py` separados favorece organização, reuso e testes modulares.

---

Feito com 💙 por [Marcos Vinícius Motta]
