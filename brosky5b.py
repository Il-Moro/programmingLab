class CSVFile:

    def __init__(self, name):
        self.name = name
        self.esiste = True
        try:
            my_file = open(self.name, 'r')
            my_file.readline()
        except Exception as e:
            self.esiste = False
            print('Errore 1: "{}"'.format(e))
            
    def get_data(self):
        if not self.esiste:
            print('Errore 2')
            return None
        else:
            data = []
            my_file = open(self.name, 'r')
            List = my_file.readlines()
            
            for item in List:                
                elements = item.split(',')
                if elements[0] !=  'Date':
                    for i in range (0, len(elements)-1):
                        elements[i] = elements[i].strip()
                        data.append(elements)
            my_file.close()
            return data

class NumericalCSVFile(CSVFile):
    
    def get_data(self):
        data = super().get_data()
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

zio = NumericalCSVFile('shampoo_sales.csv')
print(zio.get_data())
