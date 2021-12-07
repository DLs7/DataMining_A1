import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

import pandas
import numpy

def main():
    csv = pandas.read_csv('_ASSOC_PadelStars.csv').iloc[:, :2].apply(lambda s: s.astype(str).str.lower())
    csv = csv.apply(lambda s: s.astype(str).str.replace(' ', ''))
    csv = csv.apply(lambda s: s.astype(str).str.replace('.', ''))
    csv = csv.apply(lambda s: s.astype(str).str.replace('*', ''))
    csv = csv.apply(lambda s: s.astype(str).str.replace('juam', 'juan'))
    csv = csv.apply(lambda s: s.astype(str).str.replace('lúcia', 'lucia'))

    print(csv)

if __name__ == "__main__":
    main()