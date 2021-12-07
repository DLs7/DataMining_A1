import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

import numpy, pandas

def main():
    csv = pandas.read_csv('_ASSOC_PadelStars.csv').iloc[:, :3]
    
    csv = csv.apply(lambda s: s.astype(str).str.lower())
    csv = csv.apply(lambda s: s.astype(str).str.replace(' ', ''))
    csv = csv.apply(lambda s: s.astype(str).str.replace('.', ''))
    csv = csv.apply(lambda s: s.astype(str).str.replace('*', ''))
    csv = csv.apply(lambda s: s.astype(str).str.replace('juam', 'juan'))
    csv = csv.apply(lambda s: s.astype(str).str.replace('lúcia', 'lucia'))

    # csv = csv.sort_values("Jogadore(a)s")
    csvGrouped = csv.groupby("Jogadore(a)s")["Resultado"].agg(list).reset_index(name="Resultados")
    csvGrouped["Jogadore(a)s"] = csvGrouped["Jogadore(a)s"].apply(lambda s: s.split(","))
    csvGrouped["Jogos"] = csvGrouped["Resultados"].str.len()
    csvGrouped["Vitórias"] = csvGrouped["Resultados"].apply(lambda x : x.count("ganhou"))
    csvGrouped["Derrotas"] = csvGrouped["Resultados"].apply(lambda x : x.count("perdeu"))
    csvGrouped["Win ratio"] = round(csvGrouped["Vitórias"] / csvGrouped["Qtd."], 2)

    # csvPersonal = csv

    # with pandas.option_context('display.max_rows', None, 'display.max_columns', None):
    print("Melhores duplas/trios por vitórias: ")
    print(csvGrouped.sort_values("Vitórias", ascending=False))

    print("\nMelhores duplas/trios por win ratio: ")
    print(csvGrouped.sort_values("Win ratio", ascending=False))

if __name__ == "__main__":
    main()