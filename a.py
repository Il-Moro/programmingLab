def controllo_doppi(self, lista):
    lista_pulita = []  # Lista per memorizzare gli elementi senza duplicati
    seen = set()  # Insieme per tenere traccia degli elementi già visti
    #set è un insieme che non ha doppi
    for i in range(0,len(lista)-1):
        seen2 = set() #preparo un'altro insieme per verificare che nello stesso mese non ci siano più valori
        for j in range (0,len(lista)):
            
        
