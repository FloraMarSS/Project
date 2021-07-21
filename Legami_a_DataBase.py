from selenium import webdriver
import time
import csv
import re

# PATH='C:\Program Files/phantomjs.exe' #Path per phantomJS
# driver = webdriver.PhantomJS(PATH)
PATH = 'C:\Program Files\chromedriver.exe' #path è la cartella dove è stato installato il webdriver
driver = webdriver.Chrome(PATH)
driver.get('https://servizi.ivass.it/RuirPubblica/') #pagina iniziale di ricerca IVASS-RUI
## seleziona Ricerca per società.
## Per ricerca per persona fisica, commentare il bottone sottostante, in quanto la casella è selezionata per default
search = driver.find_element_by_id('FormSearch:j_id_jsp_558348152_13:1') #id della casella "Ricerca per società"
search.click()
search = driver.find_element_by_id('FormSearch:j_id_jsp_558348152_16:1') #id della casella "Ricerca per settori"
search.click()
search = driver.find_element_by_id('FormSearch:SecA') #id della casella "Settore A"
search.click()
## avvia ricerca
invio = driver.find_element_by_id('FormSearch:SearchButton') #id del bottone "Ricerca"
invio.click()
cartella = "C:\\Users\\NIT-Lap12\\Desktop\\Lavoro\\"
data = ['numero_iscrizione_1', 'numero_iscrizione_2', 'tipo_legame']
# Esporta in  CSV nella stassa cartella dove ci sono i json
csv_filename = 'legami_A.csv'
with open((cartella + csv_filename), "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerows([data])
for click in range (1,50):
    print(time.strftime("%H:%M:%S"))
    ## trova numeri iscrizione
    a_tag = driver.find_elements_by_tag_name('a') #trova tutti tag 'a' in tabella
    numeri = []

    ## crea una lista di numeri iscrizione presenti nella pagina dei risultati (riga per riga)
    for s in a_tag:
        if s.text.isnumeric():
            numeri.append(s.text)


    ## clicca sui link dei numeri di iscrizione
    for i in numeri:
        link = driver.find_element_by_link_text(i)
        link.click()
        time.sleep(2) #3 sec è il tempo per caricare la pagina con la mia connessione lenta
    ## prende i dati da ogni pagina dei risultati
        valori = driver.find_elements_by_xpath('//td[@class="detailTableColValue"]')  # path per colonne di valori in pg
        cat = driver.find_elements_by_xpath('//td[@class="detailTableColDesc"]')
        id_principale = valori[0].text
        lista = []
        rvs_lista = []
        for valore in range(len(cat)):
            if cat[valore].text == 'Data Inizio Inoperatività :':
                data_inoperativo = valori[valore].text
        target = driver.find_elements_by_class_name('commandLinkSottolineato')
        time.sleep(1)
        hrefs=[]
        for a in target:
            hrefs.append(a.text)
        for link in hrefs:
            find = driver.find_element_by_link_text(link)
            find.click()
            time.sleep(2)
            valori = driver.find_elements_by_xpath('//td[@class="detailTableColValue"]')  # path per colonne di valori in pg
            cat = driver.find_elements_by_xpath('//td[@class="detailTableColDesc"]')
            prov=[]
            prov_1 = []
            prov.append(id_principale)
            prov.append(valori[0].text)
            prov.append("Responsabile dell'attività di intermediazione")
            prov_1.append(valori[0].text)
            prov_1.append(id_principale)
            prov_1.append("Responsabile dell'attività di intermediazione")
            lista.append(prov)
            rvs_lista.append(prov_1)

            driver.back()
            try:
                prov.append(data_inoperativo)
            except NameError:
                continue

        with open(csv_filename,'a') as f:
            writer = csv.writer(f)
            for legame in lista:
                writer.writerows([legame])
            for legame_inv in rvs_lista:
                writer.writerows([legame_inv])


        ## torna a pagina precedente
        driver.back()

    element = driver.execute_script("return document.querySelectorAll('#paginatore a')[2]")
    element.click()

