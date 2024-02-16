# Apro e leggo il file, linea per linea
def sum_csv(my_file):
    my_file = open(my_file, 'r')
    vendite = 0
    
    for line in my_file:
        elements = line.split(',')
        if elements[0] != 'Date' and not elements[1].isalpha():
            value = float(elements[1])            
            vendite = vendite + value
            
    my_file.close()
    if vendite == 0:
        return None
    else:
        return vendite
        
