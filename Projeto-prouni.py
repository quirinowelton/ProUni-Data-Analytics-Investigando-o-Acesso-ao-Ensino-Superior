import pandas as pd 
from unidecode import unidecode
import re

df_2020 = pd.read_csv("ProuniRelatorioDadosAbertos2020.csv", sep=";")
print(df_2020.head())