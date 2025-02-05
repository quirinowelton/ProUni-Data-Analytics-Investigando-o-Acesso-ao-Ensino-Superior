#%%
import pandas as pd 
import unidecode
#%%
# Carregando os arquivos CSV

df_2015 = pd.read_csv("pda-prouni-2015.csv", sep=";", encoding="latin-1")
df_2016 = pd.read_csv("pda-prouni-2016.csv", sep=";", encoding="latin-1")
df_2017 = pd.read_csv("pda-prouni-2017.csv", sep=";", encoding="latin-1")
df_2018 = pd.read_csv("pda-prouni-2018.csv", sep=";", encoding="latin-1")
df_2019 = pd.read_csv("pda-prouni-2019.csv", sep=";", encoding="latin-1")
df_2020 = pd.read_csv("ProuniRelatorioDadosAbertos2020.csv", sep=";", encoding="latin-1")

# Obtendo os nomes das colunas de cada DataFrame
columns_2020 = df_2020.columns
columns_2019 = df_2019.columns
columns_2018 = df_2018.columns
columns_2017 = df_2017.columns
columns_2016 = df_2016.columns
columns_2015 = df_2015.columns
#%%
# Criando lista de colunas
lista_colunas = [
    ("2015", columns_2015),
    ("2016", columns_2016),
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
# Função para verificar se os DataFrames possuem colunas idênticas
def verificar_colunas_iguais(*dataframes):
    colunas_padrao = dataframes[0].columns  # Pega as colunas do primeiro DataFrame
    
    for i, df in enumerate(dataframes[1:], start=1):
        if not colunas_padrao.equals(df.columns):
            print(f"As colunas do DataFrame {i+1} são diferentes.")
            print(f"Esperado: {list(colunas_padrao)}")
            print(f"Encontrado: {list(df.columns)}\n")
            return False
    
    print("Todas as colunas são iguais!")
    return True

# Verificando se as colunas são iguais
colunas_iguais = verificar_colunas_iguais(df_2015, df_2016, df_2017, df_2018, df_2019, df_2020)
#%%
# Dicionário com os novos nomes das colunas
novo_nomes = {
    'ï»¿ANO_CONCESSAO_BOLSA': 'ANO_CONCESSAO',
    'ANO_CONCESSAO_BOLSA': 'ANO_CONCESSAO',
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
#%%
# Renomeando colunas
for df in dataframes:
    df.rename(columns=novo_nomes, inplace=True)

# Unificando os DataFrames
df_unificado = pd.concat(dataframes, axis=0)

# Exibindo o DataFrame unificado
print(df_unificado.head())
#%%
# Alterando nome das colunas para retirar "BENEFICIARIO_" e "_BENEFICIARIO"
df_unificado.columns = df_unificado.columns.str.replace('BENEFICIARIO_', '', regex=True)
df_unificado.columns = df_unificado.columns.str.replace('_BENEFICIARIO', '', regex=True)

df_unificado.columns = df_unificado.columns.str.replace('BOLSA_', '', regex=True)
df_unificado.columns = df_unificado.columns.str.replace('_BOLSA', '', regex=True)

print(df_unificado.shape)

# Verificando valores nulos
nulo = df_unificado[['ANO_CONCESSAO', 'NOME_IES', 'NOME_CURSO', 'SEXO', 'RACA', 'DATA_NASCIMENTO', 'DEFICIENTE_FISICO', 'UF']].isnull().sum()
#%%
# Convertendo "ANO_CONCESSAO_BOLSA" para inteiro, tratando nulos
if 'ANO_CONCESSAO' in df_unificado.columns:
    df_unificado['ANO_CONCESSAO'] = pd.to_numeric(df_unificado['ANO_CONCESSAO'], errors='coerce').fillna(0).astype(int)

# Verificando valores únicos em "ANO_CONCESSAO_BOLSA"
print(df_unificado['ANO_CONCESSAO'].unique())

# Convertendo "DATA_NASCIMENTO" para datetime
#%%
df_unificado['DATA_NASCIMENTO'] = pd.to_datetime(df_unificado['DATA_NASCIMENTO'], format='%d/%m/%Y', errors='coerce')
print(df_unificado['DATA_NASCIMENTO'].isnull().sum())

# Analisando valores únicos das colunas
for coluna in df_unificado.columns:
    valores_unicos = df_unificado[coluna].unique()
    print(f"Valores únicos na coluna {coluna}:")
    print(valores_unicos)
    print("-" * 30)

# Padronizando os dados tornando maiúsculas e removendo acentos
def padronizar(texto):
    if isinstance(texto, str):
        texto = unidecode.unidecode(texto).upper()
    return texto

# Aplicando a função em todas as colunas
for coluna in df_unificado.columns:
    df_unificado[coluna] = df_unificado[coluna].apply(padronizar)
#%%
# Padronizando os valores da coluna "TIPO_BOLSA"
df_unificado['TIPO'] = df_unificado['TIPO'].replace({'BOLSA PARCIAL 50%': 'PARCIAL', 'BOLSA INTEGRAL': 'INTEGRAL'})
df_unificado['SEXO'] = df_unificado['SEXO'].replace({'F': 'FEMININO', 'M': 'MASCULINO'})

# Verificando se o DataFrame está vazio
print(df_unificado.columns)