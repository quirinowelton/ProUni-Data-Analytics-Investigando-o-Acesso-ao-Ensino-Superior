import psycopg2
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from dotenv import load_dotenv
import os

load_dotenv()

#Função para conectar ao BD do postgreSQL
def conn():
    try:
        pwd = os.getenv('DB_PASSWORD')
        us = os.getenv('USER')
        connection = psycopg2.connect(
            host="localhost",
            port="5433",
            dbname="postgres",
            user=us,
            password=pwd
        )
        print("Conexão bem-sucedida!")
        return connection
    except psycopg2.Error as e:
        print(f"Erro ao conectar ao banco de dados: {e}")
        return None

#Função para encerrar a conexão com o BD
def encerra_conn(connection):
    if connection:
        connection.close()
        print("Conexão encerrada.")

#Função para recuperar dados de uma tabela no banco de dados. Retornando um DF
def fetch_data():
    connection = None
    cursor = None
    try:
        connection = conn()
        if not connection:
            return pd.DataFrame()
        cursor = connection.cursor()
        cursor.execute("SELECT* FROM tabela_prouni") 
        rows = cursor.fetchall()
        colunas = [desc[0] for desc in cursor.description]
        return pd.DataFrame(rows, columns=colunas)
    except Exception as e:
        print(f"Erro ao executar a consulta: {e}")
        return pd.DataFrame()
    finally:
        if cursor:
            cursor.close()
        if connection:
            encerra_conn(connection)

# Recupera os dados do banco
df = fetch_data()

# Configuração de estilo para gráficos
sns.set(style='whitegrid')


cores_terrosas = {
    'mocha_mousse': '#967969',  # Pantone Mocha Mousse
    'terracota': '#E2725B',     # Terracota
    'verde_oliva': '#556B2F',   # Verde-oliva
    'bege': '#F5DEB3',          # Bege
    'marrom_suave': '#8B7355'   # Marrom suave
}

# Dados do Censo 2022 de população por região do país
dados = {
    'Região': ['NORTE', 'NORDESTE', 'SUDESTE', 'SUL', 'CENTRO-OESTE'],
    'População': [17354884, 54658515, 84840113, 29937706, 16289538]
}
df_pop = pd.DataFrame(dados)

# Cria uma nova coluna 'pop_%' com a % da população de cada região
total_populacao = df_pop['População'].sum()
df_pop['pop_%'] = (df_pop['População'] / total_populacao) * 100
df_pop['pop_%'] = df_pop['pop_%'].round(2)

# Criando um df que contenha a relação entre regiões do Brasil e número de Bolsas e renomeando as colunas
bolsas_regiao = df['REGIAO'].value_counts().reset_index()
bolsas_regiao.columns = ['Região', 'Bolsas'] 

# Criando a coluna de bolsas_% que apresenta a % de bolsas concedidas por cada região
total_bolsas = bolsas_regiao['Bolsas'].sum()
bolsas_regiao['bolsas_%'] = (bolsas_regiao['Bolsas'] / total_bolsas) * 100
bolsas_regiao['bolsas_%'] = bolsas_regiao['bolsas_%'].round(2)
df_bolsas_regiao = pd.DataFrame(bolsas_regiao)

# Combinar os DataFrames para geração do gráfico de barras 
df_combinado = pd.merge(df_pop[['Região', 'pop_%']], df_bolsas_regiao[['Região', 'bolsas_%']], on='Região', how='inner')
bar_width = 0.35

# Criando o gráfico de barras
plt.figure(figsize=(10, 6))
bars1 = plt.bar(np.arange(len(df_combinado['Região'])), df_combinado['pop_%'], width=bar_width, label='População (%)', color=cores_terrosas['mocha_mousse'], alpha=0.8)
bars2 = plt.bar(np.arange(len(df_combinado['Região'])) + bar_width, df_combinado['bolsas_%'], width=bar_width, label='Bolsas (%)', color=cores_terrosas['terracota'], alpha=0.8)
for bar in bars1:
    height = bar.get_height()
    plt.annotate(f'{height:.2f}%', xy=(bar.get_x() + bar.get_width() / 2, height), xytext=(0, 3), textcoords='offset points', ha='center', va='bottom', fontsize=9)

for bar in bars2:
    height = bar.get_height()
    plt.annotate(f'{height:.2f}%', xy=(bar.get_x() + bar.get_width() / 2, height), xytext=(0, 3), textcoords='offset points', ha='center', va='bottom', fontsize=9)

# Personalizando o gráfico
plt.title('Porcentagem de População e Bolsas do ProUni por Região do Brasil', fontsize=14)
plt.xticks(np.arange(len(df_combinado['Região'])) + bar_width / 2, df_combinado['Região'], rotation=45, fontsize=10)
plt.ylabel('Porcentagem (%)', fontsize=12)
plt.legend(fontsize=10)

plt.tight_layout()
plt.show()

# Dados do Censo 2022 de população por raça no país
dados = {
    'Raça': ['PARDA', 'BRANCA', 'PRETA', 'INDIGENA', 'AMARELA'],
    'População': [45.3, 43.5, 10.2, 0.6, 0.4]
}
df_cor = pd.DataFrame(dados)

# Criando um df que contenha a relação entre Cor/Raça e número de Bolsas
bolsas_cor = df['RACA'].value_counts().reset_index()
bolsas_cor.columns = ['Raça', 'Bolsas']
df_bolsas_cor = pd.DataFrame(bolsas_cor)

# Excluindo valores marcados como não informada
df_bolsas_cor = df_bolsas_cor.query("Raça != 'NAO INFORMADA'")

# Criando a coluna de bolsas_% que apresenta a % de bolsas concedidas por cada raça
total_bolsa = df_bolsas_cor['Bolsas'].sum()
df_bolsas_cor['bolsas_%'] = (df_bolsas_cor['Bolsas'] / total_bolsa) * 100
df_bolsas_cor['bolsas_%'] = df_bolsas_cor['bolsas_%'].round(2)
 
df_unico = pd.merge(df_cor[['Raça', 'População']], df_bolsas_cor[['Raça', 'bolsas_%']], on='Raça', how='inner')
bar_width = 0.35
plt.figure(figsize=(10, 6))

bars1 = plt.bar(np.arange(len(df_unico['Raça'])), df_unico['População'], width=bar_width, label='População (%)', color=cores_terrosas['mocha_mousse'], alpha=0.8)
bars2 = plt.bar(np.arange(len(df_unico['Raça'])) + bar_width, df_unico['bolsas_%'], width=bar_width, label='Bolsas (%)', color=cores_terrosas['terracota'], alpha=0.8)

for bar in bars1:
    height = bar.get_height()
    plt.annotate(f'{height:.1f}%', xy=(bar.get_x() + bar.get_width() / 2, height), xytext=(0, 3), textcoords='offset points', ha='center', va='bottom', fontsize=9)

for bar in bars2:
    height = bar.get_height()
    plt.annotate(f'{height:.2f}%', xy=(bar.get_x() + bar.get_width() / 2, height), xytext=(0, 3), textcoords='offset points', ha='center', va='bottom', fontsize=9)

# Personalizando o gráfico
plt.title('Porcentagem de População e Bolsas do ProUni por Raça no Brasil', fontsize=14)
plt.xticks(np.arange(len(df_unico['Raça'])) + bar_width / 2, df_unico['Raça'], rotation=45, fontsize=10)
plt.ylabel('Porcentagem (%)', fontsize=12)
plt.legend(fontsize=10)

plt.tight_layout()
plt.show()

# Dados do Censo 2022 de população por gênero
dados = {
    'Gênero': ['MASCULINO', 'FEMININO'],
    'Porcentagem': [48.5, 51.5]
}
df_genero = pd.DataFrame(dados)

# Criando um df que contenha a relação entre gênero e número de Bolsas
bolsas_genero = df['SEXO'].value_counts().reset_index()
bolsas_genero.columns = ['Gênero', 'Bolsas']

# Criando a coluna de bolsas_% que apresenta a % de bolsas concedidas por cada gênero
total_bolsa = bolsas_genero['Bolsas'].sum()
bolsas_genero['bolsas_%'] = (bolsas_genero['Bolsas'] / total_bolsa) * 100
bolsas_genero['bolsas_%'] = bolsas_genero['bolsas_%'].round(2)
df_bolsas_genero = pd.DataFrame(bolsas_genero)

df_genero_geral = pd.merge(df_genero[['Gênero', 'Porcentagem']], df_bolsas_genero[['Gênero', 'bolsas_%']], on='Gênero', how='inner')
bar_width = 0.35

plt.figure(figsize=(10, 6))
bars1 = plt.bar(np.arange(len(df_genero_geral['Gênero'])), df_genero_geral['Porcentagem'], width=bar_width, label='Porcentagem (%)', color=cores_terrosas['mocha_mousse'], alpha=0.8)
bars2 = plt.bar(np.arange(len(df_genero_geral['Gênero'])) + bar_width, df_genero_geral['bolsas_%'], width=bar_width, label='Bolsas (%)', color=cores_terrosas['terracota'], alpha=0.8)

for bar in bars1:
    height = bar.get_height()
    plt.annotate(f'{height:.1f}%', xy=(bar.get_x() + bar.get_width() / 2, height), xytext=(0, 3), textcoords='offset points', ha='center', va='bottom', fontsize=9)

for bar in bars2:
    height = bar.get_height()
    plt.annotate(f'{height:.2f}%', xy=(bar.get_x() + bar.get_width() / 2, height), xytext=(0, 3), textcoords='offset points', ha='center', va='bottom', fontsize=9)

# Personalizando o gráfico
plt.title('Porcentagem de População e Bolsas do ProUni por Gênero no Brasil', fontsize=14)
plt.xticks(np.arange(len(df_genero_geral['Gênero'])) + bar_width / 2, df_genero_geral['Gênero'], rotation=45, fontsize=10)
plt.ylabel('Porcentagem (%)', fontsize=12)
plt.legend(fontsize=10)

plt.tight_layout()
plt.show()

# Criando um df que contenha a relação entre ano e número de Bolsas
bolsas_ano = df['ANO_CONCESSAO'].value_counts().reset_index().sort_values(by="ANO_CONCESSAO")
bolsas_ano.columns = ['Ano', 'Bolsas']
df_bolsas_ano = pd.DataFrame(bolsas_ano)

anos_completos = range(2015, 2020)
df_bolsas_ano = df_bolsas_ano.set_index('Ano').reindex(anos_completos, fill_value=0).reset_index()


plt.figure(figsize=(10, 6))
plt.plot(df_bolsas_ano['Ano'], df_bolsas_ano['Bolsas'], marker='o', linestyle='-', color=cores_terrosas['verde_oliva'], alpha=0.8)
for x, y in zip(df_bolsas_ano['Ano'], df_bolsas_ano['Bolsas']):
    plt.annotate(str(y), xy=(x, y), textcoords='offset points', xytext=(0, 5), ha='center', fontsize=9)

# Personalizando o gráfico
plt.title('Bolsas Concedidas Por Ano', fontsize=14)
plt.xlabel('Ano', fontsize=12)
plt.ylabel('Número de Bolsas', fontsize=12)
plt.grid(True, linestyle='--', alpha=0.6)
plt.xticks(anos_completos, fontsize=10)

plt.show()

# Gráfico para analisar a quantidade de bolsas distribuídas em cada ano por tipo de Bolsa 
# Agrupar os dados por ano e modalidade
df_grouped = df.groupby(['ANO_CONCESSAO', 'MODALIDADE_ENSINO']).size().reset_index(name='Contagem')

# Transformar o DataFrame em formato "wide" usando pivot
df_wide = df_grouped.pivot(index='ANO_CONCESSAO', columns='MODALIDADE_ENSINO', values='Contagem').fillna(0)
anos_completos = range(2015, 2021)
df_wide = df_wide.reindex(anos_completos, fill_value=0).reset_index()

# Renomear as colunas para facilitar o acesso
df_wide.columns.name = None  # Remove o nome das colunas (MODALIDADE_ENSINO)
df_wide = df_wide.rename(columns={'index': 'ANO_CONCESSAO'})

print(df_wide)

# Criar o gráfico de barras agrupado
plt.figure(figsize=(10, 6))
bar_width = 0.35
index = df_wide['ANO_CONCESSAO']

bars1 = plt.bar(index - bar_width/2, df_wide['PRESENCIAL'], bar_width, label='Presencial', color=cores_terrosas['mocha_mousse'], alpha=0.8)
bars2 = plt.bar(index + bar_width/2, df_wide['EAD'], bar_width, label='EAD', color=cores_terrosas['terracota'], alpha=0.8)

for x, y1, y2 in zip(index, df_wide['PRESENCIAL'], df_wide['EAD']):
    plt.annotate(str(int(y1)), xy=(x - bar_width/2, y1), xytext=(0, 3), textcoords='offset points', ha='center', va='bottom', fontsize=9)
    plt.annotate(str(int(y2)), xy=(x + bar_width/2, y2), xytext=(0, 3), textcoords='offset points', ha='center', va='bottom', fontsize=9)

# Personalizar o gráfico
plt.ylabel('Número de Bolsas', fontsize=12)
plt.title('Distribuição de Bolsas por Modalidade e Ano', fontsize=14)
plt.xticks(index, rotation=45, fontsize=10)
plt.legend(fontsize=10)

plt.tight_layout()
plt.show()
