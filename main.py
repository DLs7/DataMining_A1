import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

import numpy, pandas

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

    # Criamos um CSV de equipes a partir do CSV lido.
    # Agrupamos todos os jogos por equipe
    teamStats = csv.groupby("Jogadore(a)s")["Resultado"].agg(list).reset_index(name="Resultados")
    # Transformamos a equipe em um array
    teamStats["Jogadore(a)s"] = teamStats["Jogadore(a)s"].apply(lambda s: s.split(","))
    # Contamos quantos jogos a equipe jogou a partir do tamanho do array de resultados gerado
    teamStats["Jogos"] = teamStats["Resultados"].str.len()
    # Contamos as vitórias desta equipe pela quantidade de "ganhou" no array
    teamStats["Vitórias"] = teamStats["Resultados"].apply(lambda x: x.count("ganhou"))
    # Contamos as derrotas desta equipe pela quantidade de "perdeu" no array
    teamStats["Derrotas"] = teamStats["Resultados"].apply(lambda x: x.count("perdeu"))
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

if __name__ == "__main__":
    main()