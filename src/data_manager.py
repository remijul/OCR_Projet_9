def inspector(df):
    # Debut de l'inspection
    print("#####     DEBUT DE L'INSPECTION     #####")
    
    # Structure du DataFrame avec df.shape
    print("\n----------------------")
    print("Structure du DataFrame:")
    print(f'Nb de lignes: {df.shape[0]} ; Nb de colonnes: {df.shape[1]}')
    
    # Types de données avec df.dtypes
    print("\n----------------------")
    print("Types de données:")
    print(df.dtypes)
    
    # Présence d'une potentielle clé unique (identifiant) avec df.nunique()
    print("\n----------------------")
    print("Nombre de valeurs uniques (pour identifiant PK / FK):")
    print(df.nunique())
    
    # Présence de valeurs manquantes avec df.isnull().sum()
    print("\n----------------------")
    print("Valeurs manquantes:")
    print(df.isnull().sum())
    
    # Fin de l'inspection
    print("\n#####     FIN DE L'INSPECTION     #####")
    

# Tester la fonction d'inspection sur le DataFrame customers
# Test possible depuis le terminal ou depuis un notebook
import pandas as pd
DATA_PATH = "../data/"
customers = pd.read_csv(DATA_PATH + "raw/customers.csv", sep=";")
inspector(customers)