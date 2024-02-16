class CSVFile:

    def __init__(self, name):
        self.name = name
        self.esiste = True
        try:
            my_file = open(self.name, 'r')
            my_file.readline()
        except Exception as e:
            self.esiste = False
            print('Errore: "{}"'.format(e))


    def get_data(self):
        if not self.esiste:
            print('Errore')
            return None
        else:
            data = []
            my_file = open(self.name, 'r')
            my_file.readline()
            List = my_file.readlines()
            for item in List:                
                elements = item.split(',')
                elements[-1] = elements[-1].strip()
                data.append(elements)
            my_file.close()
            return data
