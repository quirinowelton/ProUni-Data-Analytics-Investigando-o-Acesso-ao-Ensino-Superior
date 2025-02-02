#%%
import pandas as pd 

df_2015 = pd.read_csv("pda-prouni-2015.csv", sep=";", encoding="latin-1")
df_2016 = pd.read_csv("pda-prouni-2016.csv", sep=";", encoding="latin-1")
df_2017 = pd.read_csv("pda-prouni-2017.csv", sep=";", encoding="latin-1")
df_2018 = pd.read_csv("pda-prouni-2018.csv", sep=";", encoding="latin-1")
df_2019 = pd.read_csv("pda-prouni-2019.csv", sep=";", encoding="latin-1")
df_2020 = pd.read_csv("ProuniRelatorioDadosAbertos2020.csv", sep=";", encoding="latin-1")

#.columns retorna os nomes das colunas do DataFrame como um objeto Index.
#Essas linhas armazenam as colunas de cada DataFrame em variáveis separadas.
columns_2020 = df_2020.columns
columns_2019 = df_2019.columns
columns_2018 = df_2018.columns
columns_2017 = df_2017.columns
columns_2016 = df_2016.columns
columns_2015 = df_2015.columns

#lista_colunas é uma lista de tuplas, onde cada tupla contém:
#O ano como string ("2017", "2018", etc.).
#As colunas do respectivo DataFrame.

lista_colunas = lista_colunas = [
    ("2015", columns_2017),
    ("2016", columns_2018),
    ("2017", columns_2017),
    ("2018", columns_2018),
    ("2019", columns_2019),
    ("2020", columns_2020)
]
for ano, colunas in lista_colunas:
    print(f"Colunas para o ano {ano}:")
    for coluna in colunas:
        print(f"- {coluna}")
    print()
#%%
import pandas as pd

def verificar_colunas_iguais(*dataframes):
    """
    Verifica se todas as colunas dos DataFrames fornecidos são iguais.
    
    - True se todas as colunas forem iguais, False caso contrário.
    """
    colunas_padrao = dataframes[0].columns  # Pega as colunas do primeiro DataFrame

    for i, df in enumerate(dataframes[1:], start=1):
        if not colunas_padrao.equals(df.columns):  # Compara com os outros DataFrames
            print(f"As colunas do DataFrame {i+1} são diferentes.")
            print(f"Esperado: {list(colunas_padrao)}")
            print(f"Encontrado: {list(df.columns)}\n")
            return False  # Retorna False se encontrar diferença

    print("Todas as colunas são iguais!")
    return True  # Retorna True se todas forem idênticas

# Exemplo de uso
colunas_iguais = verificar_colunas_iguais(df_2015, df_2016, df_2017, df_2018, df_2019, df_2020)
#%%
# Dicionário com os novos nomes das colunas
novo_nomes = {
    'CPF_BENEFICIARIO_BOLSA': 'CPF_BENEFICIARIO',
    'SEXO_BENEFICIARIO_BOLSA': 'SEXO_BENEFICIARIO',
    'RACA_BENEFICIARIO_BOLSA': 'RACA_BENEFICIARIO',
    'DT_NASCIMENTO_BENEFICIARIO': 'DATA_NASCIMENTO',
    'REGIAO_BENEFICIARIO_BOLSA': 'REGIAO_BENEFICIARIO',
    'SIGLA_UF_BENEFICIARIO_BOLSA': 'UF_BENEFICIARIO',
    'MUNICIPIO_BENEFICIARIO_BOLSA': 'MUNICIPIO_BENEFICIARIO'
}

# Lista de DataFrames
dataframes = [df_2015, df_2016, df_2017, df_2018, df_2019]

# Renomeando as colunas em cada DataFrame de forma dinâmica
for df in dataframes:
    df.rename(columns=novo_nomes, inplace=True)

#%%

# Unificando as bases de dados
df_unificado = pd.concat(dataframes, axis=0)  # axis=0 para unir verticalmente

# Exibindo o DataFrame unificado
print(df_unificado.head())