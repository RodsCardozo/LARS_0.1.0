import pandas as pd


import pandas as pd
import glob


# Lista todos os arquivos CSV em um diretório específico
arquivos_csv = []
n = 25
for i in range(0,n+1):
    nome = (f"temperaturas_transiente_4/resultado_temp_{i}.csv")
    arquivos_csv.append(nome)

print(arquivos_csv)

# Cria uma lista vazia para armazenar os DataFrames de cada arquivo CSV
dataframes = []

# Loop pelos arquivos CSV e carrega cada um em um DataFrame separado
for arquivo in arquivos_csv:
    df = pd.read_csv(arquivo)
    dataframes.append(df)

# Concatena os DataFrames em um único DataFrame
df_final = pd.concat(dataframes)

# Salva o DataFrame final em um arquivo CSV
df_final.to_csv('temperaturas_transiente_4/resultado.csv', index=False)

# Plot dos resultados

df_final = pd.read_csv('temperaturas_transiente_4/resultado.csv')
import matplotlib.pyplot as plt
import numpy as np

s = np.array(df_final['Face1'])
t = np.linspace(0,len(s), len(s))
fig, ax = plt.subplots()
ax.plot(t, s)

ax.set(xlabel='time (s)', ylabel='Tempratura [k]',
       title='Temperatura da Face 1')
ax.grid()

fig.savefig("temperaturas_transiente_4/temp_4_face1.png")
plt.show()