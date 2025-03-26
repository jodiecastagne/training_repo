import pandas as pd
import re
import os
import glob

def main():
    nom_chemin = glob.glob("C:\ecg\*.csv")  # liste des fichiers dans doc avec paths entier
    nom_fichier = []
    i = 0
    for element in nom_chemin:
        nom_fichier.append(re.findall(r'C:\\ecg\\(ecg_[0-9]+.csv)', element))  # liste des fichiers dans doc
        i += 1
    print(nom_fichier)
    id = []
    for indice in range(0, i):
        id.append(re.findall(r'ecg_([0-9]+).csv)', nom_fichier[indice]))
    print(id)
    d = {}
    print(id[1])
    print(nom_fichier[1])
    for i in range(len(nom_fichier)):
        d[id[i]] = pd.read_csv(nom_fichier[i])
    C = pd.concat(d)
    print(C.to_string())

    # d = {'10517002': A, '10517003': B}  #A,B : pd.read_csv()
    # C = pd.concat(d)
    d = {'10517002': A, '10517003': B}
    C = pd.concat(d)
    #A1 = C.loc[['10517002']]
    #B1 = C.loc[['10517003']]
    # print(A1.to_string())

    # print(A['timestamp_machine'])
    #Z = C.loc[['10517002']]['timestamp_machine']
    #print(Z.to_string())

if __name__ == '__main__':
    main()
