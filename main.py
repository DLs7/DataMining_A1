import pandas

def main():
    csv = pandas.read_csv('_ASSOC_PadelStars.csv')
    print(csv)

if __name__ == "__main__":
    main()