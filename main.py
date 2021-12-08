import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

import numpy, pandas
from mlxtend.frequent_patterns import association_rules, apriori
from itertools import chain

def main():
    # Fazemos a leitura das 3 primeiras colunas do CSV, que tem a informação que a gente quer
    csv = pandas.read_csv('_ASSOC_PadelStars.csv').iloc[:, :3]
    
    # Limpamos o ruído
    csv = csv.apply(lambda s: s.astype(str).str.lower())
    csv = csv.apply(lambda s: s.astype(str).str.replace(' ', ''))
    csv = csv.apply(lambda s: s.astype(str).str.replace('.', ''))
    csv = csv.apply(lambda s: s.astype(str).str.replace('*', ''))
    csv = csv.apply(lambda s: s.astype(str).str.replace('juam', 'juan'))
    csv = csv.apply(lambda s: s.astype(str).str.replace('lúcia', 'lucia'))

    # Parsamos os resultados para True e False e colocamos os times em tuplas
    d = {'ganhou': True, 'perdeu': False}
    csv["Resultado"] = csv["Resultado"].map(d)
    csv["Jogadore(a)s"] = csv["Jogadore(a)s"].apply(lambda s: tuple(s.split(',')))

    # Pegamos nomes individuais da lista e transformamos eles em colunas na matriz binária
    unique_names = csv["Jogadore(a)s"].unique().tolist()
    names = set(chain(*unique_names))
    
    # Criamos a matriz binária
    binary_matrix = pandas.DataFrame()
    for name in names:
        binary_matrix[name] = csv["Jogadore(a)s"].apply(lambda x: name in x)
    binary_matrix["Resultado"] = csv["Resultado"]

    # Aplicamos apriori e regras de associação
    frequent_itemsets = apriori(binary_matrix, min_support=0.01, use_colnames=True)
    rules = association_rules(frequent_itemsets, metric="support", min_threshold=0.05)
    rules = rules[rules['consequents'] == {'Resultado'}]

    # Imprimimos a tabela de regras de associação
    print("Regras de associação: ")
    print(rules)
    print("\n")

    # Criamos um CSV de equipes a partir do CSV lido.
    # Agrupamos todos os jogos por equipe
    teamStats = csv.groupby("Jogadore(a)s")["Resultado"].agg(list).reset_index(name="Resultados")
    # Contamos quantos jogos a equipe jogou a partir do tamanho do array de resultados gerado
    teamStats["Jogos"] = teamStats["Resultados"].str.len()
    # Contamos as vitórias desta equipe pela quantidade de "ganhou" no array
    teamStats["Vitórias"] = teamStats["Resultados"].apply(lambda x: x.count(1))
    # Contamos as derrotas desta equipe pela quantidade de "perdeu" no array
    teamStats["Derrotas"] = teamStats["Resultados"].apply(lambda x: x.count(0))
    # Contamos o win ratio desta equipe dividindo o número de vitórias pelas partidas totais jogadas
    teamStats["Win ratio"] = round(teamStats["Vitórias"] / teamStats["Jogos"], 2)

    # A partir do CSV de equipes, podemos gerar um CSV individual
    # Separamos o array de equipes em várias linhas, cada uma com um jogador e a informação da partida que ele jogou
    individualStats = teamStats.explode("Jogadore(a)s")
    # Agrupamos todos os jogos por jogador
    individualStats = individualStats.groupby("Jogadore(a)s")["Jogos", "Vitórias", "Derrotas"].agg(list)
    # Contamos quantos jogos o jogador jogou a partir da soma dos jogos contados na tabela anterior
    individualStats["Jogos"] = individualStats["Jogos"].map(sum)
    # Contamos o número de vitórias a partir da soma das vitórias contadas na tabela anterior
    individualStats["Vitórias"] = individualStats["Vitórias"].map(sum)
    # Contamos o número de derrotas a partir da soma das derrotas contadas na tabela anterior
    individualStats["Derrotas"] = individualStats["Derrotas"].map(sum)
    # Contamos o win ratio deste jogador dividindo o número de vitórias pelas partidas totais jogadas
    individualStats["Win ratio"] = round(individualStats["Vitórias"] / individualStats["Jogos"], 2)

    # Imprimimos as informações
    print("Melhores duplas/trios por qtd. de vitórias: ")
    print(teamStats.sort_values("Vitórias", ascending=False))

    print("\nMelhores duplas/trios por win ratio: ")
    print(teamStats.sort_values("Win ratio", ascending=False))

    print("\n\nMelhor jogador individual por qtd. de vitórias: ")
    print(individualStats.sort_values("Vitórias", ascending=False))

    print("\nMelhor jogador individual por win ratio: ")
    print(individualStats.sort_values("Win ratio", ascending=False))
    print("\n")

if __name__ == "__main__":
    main()