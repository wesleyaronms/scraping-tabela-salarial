import pandas as pd
import string
import requests
# No terminal: pip install html5lib


header = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36",
    "Language": "pt-PT,pt;q=0.9,en-US;q=0.8,en;q=0.7",
}

# O site não disponibiliza os seus dados a não ser em sua própria página
# (apesar dos inúmeros pedidos nos comentários por outros formatos).
# As profissões são divididas por cada letra do alfabeto.
# Para cada letra, uma tabela, e uma página diferente.

# Vamos coletar a primeira tabela.
url = "https://www.salario.com.br/tabela-salarial/?cargos=A#listaSalarial"
response = requests.get(url, headers=header)
data = response.text
df = pd.read_html(data)[0]

# Para então apenas concatenar as demais com a primeira, dado que as colunas são as mesmas.
for letter in string.ascii_uppercase:
    if letter != "A" and letter != "W":     # A letra 'A' já coletamos, e não há profissões com a letra 'W'.
        url = f"https://www.salario.com.br/tabela-salarial/?cargos={letter}#listaSalarial"
        response = requests.get(url, headers=header)
        data = response.text
        table = pd.read_html(data)[0]
        df = pd.concat([df, table])

# Agora basta converter os dados destas colunas de str para float.
df["Piso Salarial"] = df["Piso Salarial"].map(lambda x: (float(x.replace(",", "").replace(".", "")) / 100))
df["Média Salarial"] = df["Média Salarial"].map(lambda x: (float(x.replace(",", "").replace(".", "")) / 100))
df["Salário Mediana"] = df["Salário Mediana"].map(lambda x: (float(x.replace(",", "").replace(".", "")) / 100))
df["Teto Salarial"] = df["Teto Salarial"].map(lambda x: (float(x.replace(",", "").replace(".", "")) / 100))
df.to_csv("data/tabela-salarial.csv", index=False)


###

# Antes de fazer deste modo, eu salvei as tabelas separadamente, e só depois as juntei. Para tal:
# Excluir as linhas 18 a 21.
# na linha 25:
#     if letter != "W":
# na linha 30:
# table.to_csv(f"data/tabela-salarial-{letter.lower()}.csv", index=False)
# Antes da linha 33:
# list_tables = [pd.read_csv(f"data/tabela-salarial-{letter}.csv") for letter in string.ascii_lowercase if letter != "w"]
# df = pd.concat([table for table in list_tables])
