import os,json
import glob
import csv
import re

# trova tutti file json in una directory
cartella = "C:\\Users\\NIT-Lap12\\Desktop\\Lavoro\\"
data = [] #lista provvisoria da cui costruire csv
json_pattern = os.path.join(cartella, '*.json')
# salve tutti i file di una cartella
files = glob.glob(json_pattern, recursive=True)

# Loop attraverso i files
for file in files:
  with open(file, 'r') as f:
    json_file = json.load(f) #carica il singolo json file
    #appende in lista i valori corrispondenti alle diverse chiavi, se non trova la chiave, il valore rimane vuoto
    prov = [json_file.get('Numero Iscrizione','')]
    lista_sedi = [['Sede Legale','SL'], ['Sedi Secondarie','SS'],['Sedi Operative','SO']]
    for lista in lista_sedi:
        if lista[0] in json_file: #verifica che esita la chiave 'Sede Legale' e/o 'Sedi Secondarie' e/o 'Sedi Operative'
            prov.append([lista[1]]) #appende numero identificazione
            indirizzo = json_file.get(lista[0], '').rsplit('-') #separa la stringa valore dove c'è il trattino
            for sublista in indirizzo:
                posizioni = re.finditer('\d',sublista) #per ogni sublista verifica se ci sono dei numeri
                for posizione in posizioni:
                    pos = posizione.span()[0]# prendo la prima tra le 2 posizioni dove ha trovato il match
                    if sublista[pos:pos+5].isdecimal():#verifico che anche le successive 5 posizioni siano numeri (CAP)
                        #A questo punto appendo a lista provvisoria e tolgo gli spazi
                        prov.append([indirizzo[0].strip()])
                        prov.append([indirizzo[indirizzo.index(sublista)][pos:pos+5].strip()])
                        prov.append([indirizzo[1][pos+5:-4].strip()])

        if len(prov) > 1:
            data.append(prov)


# Aggiunge intestazione
data.insert(0, ['numero_iscrizione', 'tipo_indirizzo', 'indirizzo', 'cap', 'comune'])
print(data)
# Esporta in  CSV nella stassa cartella dove ci sono i json
csv_filename = 'indirizzi.csv'
with open((cartella + csv_filename), "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerows(data)


