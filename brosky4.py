
class CSVFile:

    def __init__(self, name):
        self.name = name
        self.esiste = True
        try:
            my_file = open(self.name, 'r')
            my_file.readline()
        except Exception as e:
            self.esiste = False
            raise Exception("Errore type error '{}'".format(e))

    def get_data(self):
        if self.esiste == False:
            print("Errore")
            return None
        elif self.esiste == True:
            data = []
            my_file = open(self.name, 'r')
            my_file.readline()
            List = my_file.readlines()            
            for item in List:
                elements = item.split(',')
                elements[1] = elements[1].strip()
                data.append(elements)
        
        my_file.close()
        return data
        