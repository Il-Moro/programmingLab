import re


class ExamException(Exception):
    pass

class CSVFile:
    def __init__(self, name):
        self.name = name
        
    def get_data(self):
        try:
            data = []
            my_file = open(self.name, 'r')
            my_file.readline()  # Salta la prima riga
            
            pattern1 = r'(\d{4}-\d{2},\d*)'  # Sequenza di quattro numeri, trattino, seguiti da zero o più numeri
            pattern2 = r'(\d{4}-\d{2})'  # Sequenza di quattro numeri, trattino, seguiti da due numeri                
            non_passato = True  # Flag per il primo elemento
            i = 0
            for line in my_file:
                line = line.strip()  # Rimuovi spazi all'inizio e alla fine
                if not line:  # Controlla se la linea è vuota
                    continue  # Salta il resto del ciclo e passa alla prossima linea
                else:
                    temp = [
                    ]  # Lista che contine l'elemento [anno-mese,passeggero]
                    line = line.strip()  # Rimuovi spazi all'inizio e alla fine
                    
                    try:
                        match1 = re.search(pattern1, line)
                        match2 = re.search(pattern2, line)
        
                        if match1:
                            temp = match1.group().split(
                                ','
                            )  # match contiene data e valore ancora combinato, quindi splitto
                        elif match2:
                            temp = match2.group().split(
                                ','
                            )  # match contiene data e valore ancora combinato, quindi splitto
        
                        if non_passato:  #primo elemento di data[]
                            for j in range(len(temp) - 1):
                                temp[j] = temp[j].strip()
                            data.append(temp)
                            i += 1
                            #print('primo:')
                            #print(temp)
                            non_passato = False  # Cambio il flag dopo il primo elemento
        
                        elif not non_passato and temp[0] == data[
                                i - 1][0] and temp[1] != data[i - 1][1]:
                            raise ExamException("Errore: due 'valori passeggeri' diversi per lo stesso mese")
        
                        elif not non_passato and temp != data[
                                i - 1]:  # Aggiungi solo se non è duplicato
                            #print('Data i-1:')
                            #print(data[i-1])
                            #print('TMP sec:')
                            #print(temp)
                            for j in range(len(temp) - 1):
                                temp[j] = temp[j].strip()
                            data.append(temp)
                            i += 1
                    except IndexError:
                        pass
                    except ExamException:
                        pass

            my_file.close()
            #print(data)
            return data
        
        except FileNotFoundError as e:
            raise ExamException("File '{}' non trovato".format(self.name)) from e
        except Exception as e:
            raise ExamException("Errore non gestito: '{}'".format(e)) from None


class CSVTimeSeriesFile(CSVFile):
    
    def controllo_doppi(self, lista):
        lista_pulita = []  # Lista per memorizzare gli elementi senza duplicati
        seen = set()  # Insieme per tenere traccia degli elementi già vistiù
        seen2 = set()
        # set è un insieme che non ha doppi
        for item in lista:
            # Confronta la tupla (anno, valore) di ogni elemento della lista
            anno = item[0]
            mese = item[1]
            if anno in seen:  # se questo elemento c'è già
                # Se l'elemento è già stato visto, salta questo elemento
                if not (anno,mese) in seen2:
                    raise ExamException("Errore: due 'valori passeggeri' diversi per lo stesso mese")
                    
            else:  # altrimenti tale elemento viene salvato in seen()
                # Se l'elemento non è stato visto, lo aggiungo alla lista pulita
                lista_pulita.append(item)
                seen.add((anno))
                seen2.add((anno,mese))
        #print(lista_pulita)
        return lista_pulita


    def controllo_ordine(self, numerical_data):  #verifico che la lista sia ordinata
        nuova_lista = []
        for i in range(len(numerical_data)): #modifico i valori degli anni e dei mesi in interi per un rapido confronto
            anno_mese = numerical_data[i][0]
            elements = anno_mese.split('-') #splitto
            anno = elements[0]
            mese = elements[1]
            try: # e provo a fare un cast 
                anno = int(anno.strip())
                mese = int(mese.strip())
            except TypeError as e:
                print(f"Errore {e} in anno o mese: non è possiblie convertirli")
            except Exception as e:
                raise ExamException("Errore non gestito: '{}'".format(e)) from None

            nuova_lista.append([anno, mese])

        for i in range(0, len(nuova_lista) - 1): #qui faccio il vero e prorpio controllo
            anno_pres = nuova_lista[i][0]
            anno_succ = nuova_lista[i+1][0]
            mese_pres = nuova_lista[i][1]
            mese_succ = nuova_lista[i + 1][1]
            if anno_pres > anno_succ: #l'anno succ >= anno prec
                return False
            if anno_pres == anno_succ and mese_pres > mese_succ: #e anche i giorni
                return False
        return True

    def get_data(self):
        data = super().get_data() #ricevo da get_data padre i dati 'grezzi'
        numerical_data = []
        for item in data: #scorro tutta la lista per modificare i passeggeri in interi
            for i in range(1, len(item)):
                try:
                    item[i] = int(item[i])
                    #controllo che sia intero e maggiore di zero
                    if item[1] <= 0:
                        item[i] = None
                except ValueError:
                    item[1] = None 
                numerical_data.append(item) #salvo tutti i dati in numerical_data

        #print(f'Secondo get_data: "{numerical_data}"')
        #print('\n')
        
        numerical_data = self.controllo_doppi(numerical_data) 
        #verifico che non ci siano doppi e li elimino, o che non ci siano più valori passeggeri per lo stesso mese
        
        #print(f'terzo get_data: "{numerical_data}"')
        #print('\n')

        if not self.controllo_ordine(numerical_data):
            #controllo che tutte le date siano in ordine
            raise ExamException("I dati non sono in ordine")
        return numerical_data


def controllo(anno, lista): #verifico che l'anno considerato (firts e last) siano compresi nei dati disponibili
    return any(anno == lista[i][0] for i in range(0, len(lista)))


def lista_con_soli_anni(time_series): #è una lista in cui ci sono ancora tutti i valori senza i mesi
    #output: lista completa con anno e numero passeggeri in numero
    data = [] 
    for item in time_series:
        cont = item[0].split('-')
        year = cont[0].strip()
        year = int(year)
        month_passengers = item[1]
        data.append([year, month_passengers]) #salvo tutto in data
    return data


def refull(Lista):  #per la LISTA CON SOLI ANNI-PASEGGERI
    #print(f'{Lista}')
    #se mancano degli anni tra due estremi per facilitare le operazioni nella funzione _increments, allora la riempio assegnando None al valore passeggeri per l'anno mancante
    for i in range(len(Lista) - 1):
        #se l'anno corrente è diverso da quello successivo - 1 e se l'anno corrente è minore dell'ultimo anno nella lista
        anno_pres = Lista[i][0]
        anno_succ = Lista[i + 1][0]
        ultimo_anno = Lista[-1][0]
        if anno_pres != anno_succ - 1 and anno_pres < ultimo_anno:
            nuovo_anno = anno_pres + 1
            Lista.insert(i + 1, [nuovo_anno, None])
    #print(f'{Lista}')
    return Lista


def lista_anni_medie(time_series):  # Lista:  anno per anno - media_passeggeri
    lista_intermedia = []
    s = 0
    div = 0
    # un po' artificioso -> il problema è che non so il numero di volte che devo dividere (ci sono passeggeri = None)
    # inoltre non so quanti mesi ho da considerare (potrebbero esserci dati mancanti)
    for i in range(0, len(time_series)): 
        # scorro tutta la lista e confronto l'anno corrente con quello successivo per capire quando terminare le somme dei passeggeri
        try:  # anno_pres != anno_succ
            anno_pres = time_series[i][0]
            anno_succ = time_series[i + 1][0]
            val_passeggeri = time_series[i][1]
            if anno_pres != anno_succ:
                if div == 0:  # se l'anno cambia verifico se ho avuto delle somme: devo confrontare quindi l'ultimo anno ancora non preso in considerazione
                    if val_passeggeri is not None:
                        #se l'ultimo anno ha passeggeri nulli, bene ho un unico dato di tutto l'anno
                        s = s + val_passeggeri
                        lista_intermedia.append([anno_pres, s])
                        #print(f'1 {lista_intermedia}\n')
                    else: # altrimenti quell'anno non ha nessun dato -> valore passeggeri = None 
                        lista_intermedia.append([anno_pres, None])
                        #print(f'2 {lista_intermedia}\n')
                else:  # anche qui, v != 0 -> ho avuto almeno 1 somma
                    if val_passeggeri is not None:
                        # se l'ultimo mese di quell'anno non None -> ulteriore somma -> ulteriore divisoew
                        s = s + val_passeggeri
                        lista_intermedia.append(
                            [anno_pres, s / (div + 1)])
                        #print(f'3 {lista_intermedia}\n')
                    else: #altrimenti se l'ultimo mese = None utilizzo i dati che avevo già
                        lista_intermedia.append([anno_pres, s / div])
                s = 0
                div = 0
            else: #se l'anno_succ == anno_corr posso stare tranquillo e fare la somma dei pass. se il valore != none
                if val_passeggeri is not None:
                    s = s + val_passeggeri
                    div += 1
        except IndexError: #quando arrivo alla fine della lista originale confronto l'ultimo elemento con uno successivo -> che però non esiste, quindi vado in IndexError
            anno_pres = time_series[i][0]
            val_passeggeri = time_series[i][1]
            if div == 0: # quindi controllo come sempre l'ultimo mese che ancora non ho controllato
                if val_passeggeri is not None:
                    s = s + val_passeggeri
                    lista_intermedia.append([anno_pres, s / (div + 1)])
                else:
                    lista_intermedia.append([anno_pres, None])
            else:
                s = s + val_passeggeri
                lista_intermedia.append([anno_pres, s / (div + 1)])
    lista_intermedia = refull(lista_intermedia)
    return lista_intermedia


def compute_increments(time_series, first_year, last_year): #finalmente eccoci qua

    if not isinstance(first_year, str) or not isinstance(last_year, str): #faccio una rapida verifica che i dati inseriti siano corretti
        raise ExamException(
            "Errore: Range di valori passati come non stringhe")
    #dopo faccio un cast a intero sugli intervalli di anni da considerare per facilitare le operazioni 
    first_year = int(first_year.strip())
    last_year = int(last_year.strip())

    list_increments = {}  #dizionario dell'output

    nuovo_time_series = lista_anni_medie(lista_con_soli_anni(time_series))
    #lista che contiene all'interno i dati formato anno-passeggeri, per confrontare solo gli anni

    if not (controllo(first_year, nuovo_time_series) and controllo(last_year, nuovo_time_series)):
        raise ExamException("Errore: range non valido")
    #faccio una verifica che gli estremi degli intervalli siano inclusi all'interno della lista di anno di cui si dispongono i dati

    else: #a questo punto:
        for i in range(len(nuovo_time_series)):  #scorro tutti anno per anno
            anno_corr = nuovo_time_series[i][0]
            val_passeggeri = nuovo_time_series[i][1]
            if first_year <= anno_corr and val_passeggeri is not None:
                #verifico se l'anno_corrente è compreso tra first_year e last_year e che non abbia come valore dei passeggeri None, altrimenti vado avanti finchè non ne trovo uno o nessuno (esco dal ciclo)
                for j in range(i + 1, len(nuovo_time_series)):
                    #se ho trovato un anno_corrente != None che sia compreso nel range controllo per l'anno successivo la setssa cosa con un ciclo for
                    anno_succ = nuovo_time_series[j][0]
                    val_passeggeri_succ = nuovo_time_series[j][1]
                    if anno_succ <= last_year and val_passeggeri_succ is not None:
                        # se l'anno_succ è compreso nel range ed è != None allora posso calcolatre l'incremento
                        increments = {}
                        incremento = val_passeggeri_succ - val_passeggeri
                        #anno successivo - corrente
                        intervallo = f"{anno_corr}-{anno_succ}"
                        increments[intervallo] = incremento
                        list_increments.update(increments)
                        #update del dizionario
                        break
    return list_increments

