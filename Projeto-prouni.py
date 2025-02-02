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
