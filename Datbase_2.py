import os,json
import glob
import csv

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
    data.append([
          json_file.get('Numero Iscrizione',''),
          json_file.get('Nominativo',''),
          json_file.get('Ragione o denominazione sociale',''),
          json_file.get('tipo',''),
          json_file.get('Data Iscrizione',''),
          json_file.get('Data di Nascita',''),
          json_file.get('Luogo Nascita',''),
          json_file.get('Qualifica di esercizio / Operatività','').rsplit('/',1)[-1],
          json_file.get('aggiornato il',''),
      ])


# Aggiunge intestazione
data.insert(0, ['numero_iscrizione', 'nome_cognome', 'ragione_sociale', 'tipo', 'data_iscrizione', 'data_di_nascite', 'luogo_nascita', 'operativo', 'aggiornamento'])
print(data)
# Esporta in  CSV nella stassa cartella dove ci sono i json
csv_filename = 'anagrafica.csv'
with open((cartella + csv_filename), "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerows(data)

