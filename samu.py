class CSVFile:

    def __init__(self, name):

        self.name = name
        self.esiste = True
        
        if type(name) is not str:
            raise Exception('Errore 4: stringa')
        try:
            my_file = open(self.name, 'r')
            my_file.readline()
        except Exception as e:
            self.esiste = False
            print('Errore 1: "{}"'.format(e))
            
    def get_data(self, start = None, end = None):
        if not self.esiste:
            print('Errore 2')
            return None
        elif type(start) != int:
            raise Exception('Errore inizio')
        elif type(end) != int:
            raise Exception('Errore fine')
        else:                
            data = []
            my_file = open(self.name, 'r')
            List = my_file.readlines()

            if start < 0:
                raise Exception('Errore 5 start < 0')
            if end < start:
                raise Exception('Errore 6 end < start')
            if end > len(List)-1:
                raise Exception('Errore 7 end > len')

            List = List[start-1:end]
            
            for item in List:                
                elements = item.split(',')
                if elements[0] !=  'Date':
                    for i in range (0, len(elements)-1):
                        elements[i] = elements[i].strip()
                        data.append(elements)
            my_file.close()
            return data

class NumericalCSVFile(CSVFile):
    
    def get_data(self, start = None, end = None):
        data = super().get_data(start,end)
        numerical_data = []
        for item in data:
            try:
                if item[0] != 'Date':
                    for i in range(1, len(item)):
                        item[i] = float(item[i])
                        numerical_data.append(item)
            except Exception as e:
                print('Errore 3: "{}"'.format(e))
                continue
        return numerical_data

