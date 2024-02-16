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
            if item[0] in seen:  # se questo elemento c'è già
                # Se l'elemento è già stato visto, salta questo elemento
                if not (item[0],item[1]) in seen2:
                    raise ExamException("Errore: due 'valori passeggeri' diversi per lo stesso mese")
                    
            else:  # altrimenti tale elemento viene salvato in seen()
                # Se l'elemento non è stato visto, lo aggiungo alla lista pulita
                lista_pulita.append(item)
                seen.add((item[0]))
                seen2.add((item[0],item[1]))
        #print(lista_pulita)
        return lista_pulita


    def controllo_ordine(self, numerical_data):  #verifico che la lista sia ordinata
        anni = []
        for i in range(len(numerical_data)): #modifico i valori degli anni e dei mesi in interi per un rapido confronto
            elements = numerical_data[i][0].split('-') #splitto
            try: # e provo a fare un cast 
                elements[0] = int(elements[0].strip())
                elements[1] = int(elements[1].strip())
            except TypeError as e:
                print(f"Errore {e} in anno o mese: non è possiblie convertirli")
            except Exception as e:
                raise ExamException("Errore non gestito: '{}'".format(e)) from None

            anni.append([elements[0], elements[1]])

        for i in range(0, len(anni) - 1): #qui faccio il vero e prorpio controllo
            if anni[i][0] > anni[i + 1][0]: #l'anno succ >= anno prec
                return False
            if anni[i][0] == anni[i + 1][0] and anni[i][1] > anni[i + 1][1]: #e anche i giorni
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
        if Lista[i][0] != Lista[i + 1][0] - 1 and Lista[i][0] < Lista[-1][0]:
            nuovo_anno = Lista[i][0] + 1
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
            if time_series[i][0] != time_series[i + 1][0]:
                if div == 0:  # se l'anno cambia verifico se ho avuto delle somme: devo confrontare quindi l'ultimo anno ancora non preso in considerazione
                    if time_series[i][1] is not None:
                        #se l'ultimo anno ha passeggeri nulli, bene ho un unico dato di tutto l'anno
                        s = s + time_series[i][1]
                        lista_intermedia.append([time_series[i][0], s])
                        #print(f'1 {lista_intermedia}\n')
                    else: # altrimenti quell'anno non ha nessun dato -> valore passeggeri = None 
                        lista_intermedia.append([time_series[i][0], None])
                        #print(f'2 {lista_intermedia}\n')
                else:  # anche qui, v != 0 -> ho avuto almeno 1 somma
                    if time_series[i][1] is not None:
                        # se l'ultimo mese di quell'anno non None -> ulteriore somma -> ulteriore divisoew
                        s = s + time_series[i][1]
                        lista_intermedia.append(
                            [time_series[i][0], s / (div + 1)])
                        #print(f'3 {lista_intermedia}\n')
                    else: #altrimenti se l'ultimo mese = None utilizzo i dati che avevo già
                        lista_intermedia.append([time_series[i][0], s / div])
                s = 0
                div = 0
            else: #se l'anno_succ == anno_corr posso stare tranquillo e fare la somma dei pass. se il valore != none
                if time_series[i][1] is not None:
                    s = s + time_series[i][1]
                    div += 1
        except IndexError: #quando arrivo alla fine della lista originale confronto l'ultimo elemento con uno successivo -> che però non esiste, quindi vado in IndexError
            if div == 0: # quindi controllo come sempre l'ultimo mese che ancora non ho controllato
                if time_series[i][1] is not None:
                    s = s + time_series[i][1]
                    lista_intermedia.append([time_series[i][0], s / (div + 1)])
                else:
                    lista_intermedia.append([time_series[i][0], None])
            else:
                s = s + time_series[i][1]
                lista_intermedia.append([time_series[i][0], s / (div + 1)])
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
            if first_year <= nuovo_time_series[i][0] and nuovo_time_series[i][1] is not None:
                #verifico se l'anno_corrente è compreso tra first_year e last_year e che non abbia come valore dei passeggeri None, altrimenti vado avanti finchè non ne trovo uno o nessuno (esco dal ciclo)
                for j in range(i + 1, len(nuovo_time_series)):
                    #se ho trovato un anno_corrente != None che sia compreso nel range controllo per l'anno successivo la setssa cosa con un ciclo for
                    if nuovo_time_series[j][0] <= last_year and nuovo_time_series[j][1] is not None:
                        # se l'anno_succ è compreso nel range ed è != None allora posso calcolatre l'incremento
                        increments = {}
                        incremento = nuovo_time_series[j][
                            1] - nuovo_time_series[i][1]
                        #anno successivo - corrente
                        intervallo = f"{nuovo_time_series[i][0]}-{nuovo_time_series[j][0]}"
                        increments[intervallo] = incremento
                        list_increments.update(increments)
                        #update del dizionario
                        break
    return list_increments