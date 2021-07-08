from selenium import webdriver
import time
import json

PATH='C:\Program Files/phantomjs.exe' #Path per phantomJS, link per scaricarlo: https://phantomjs.org/download.html
driver = webdriver.PhantomJS(PATH)
driver.get('https://servizi.ivass.it/RuirPubblica/') #pagina iniziale di ricerca IVASS-RUI
## seleziona Ricerca per società.
## Per ricerca per persona fisica, commentare il bottone sottostante, in quanto la casella è selezionata per default
search = driver.find_element_by_id('FormSearch:j_id_jsp_558348152_13:1') #id della casella "Ricerca per società"
search.click()
## avvia ricerca
invio = driver.find_element_by_id('FormSearch:SearchButton') #id del bottone "Ricerca"
invio.click()

## for loop per girare fino a ultima pagina di ricerca
# end = driver.find_element_by_xpath('//span[@class="defaultText"]') #Path per trovare parte di
#pagina con il numero totale di pagine di risultato ricerca
# print(end.text)
for click in range (1,50):
    print(time.strftime("%H:%M:%S"))
    ## trova numeri iscrizione
    a_tag = driver.find_elements_by_tag_name('a') #trova tutti tag 'a' in tabella
    numeri = []
    diz_societa = {}
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

        ## trova tutti i valori della tabella
        valori = driver.find_elements_by_xpath('//td[@class="detailTableColValue"]')#path per colonne di valori in pg
        numero_id = valori[0].text
        ## crea un dizionario la cui key è n iscrizione
        if numero_id[1:].isnumeric():
            lista_prov = []
            json_name = numero_id + ".json"
            list_valori = []
            list_cat = []
            ## crea una lista contenente i valori trovati
            for dato in range(len(valori)):
                list_valori.append(valori[dato].text)

            ## trova tutti i nomi delle categorie della tabella e crea una lista contenente i nomi trovati

            cat = driver.find_elements_by_xpath('//td[@class="detailTableColDesc"]')#path per colonne di valori in pg
            for nome in range(len(cat)):
                list_cat.append(cat[nome].text)

        ## crea una lista unica di dati
        lista_prov= [list(a) for a in zip(list_cat, list_valori)]

        ## aggiunge tipo a lista dati
        try:
            if search in globals():#vede se esiste la variabile search (nome del bottone di "Ricerca per società")
                lista_prov.append(['tipo :','pg'])
        except NameError: #se non esiste, è una pf
            lista_prov.append(['tipo :', 'pf'])

        ## aggiunge data e ora aggiornamento dati
        lista_prov.append(['aggiornato il :', time.strftime("%d/%m/%Y alle %H")])

        ## crea nuova coppia key,value, dove il value è la lista di dati
        for lists in lista_prov:
            lists[0] = lists[0][:-2]#elimina gli ultimi due caratteri di tutte le sottoliste nella lista_prov
            diz_societa[lists[0]] = lists[1] #
        ## crea e scrive il file json dal dizionario
        with open(json_name, 'w') as outfile:
            json.dump(diz_societa, outfile)

        ## torna a pagina precedente
        driver.back()


    element =  driver.execute_script("return document.querySelectorAll('#paginatore a')[2]")
    element.click()

