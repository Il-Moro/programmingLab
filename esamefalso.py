class MovingAverage:
    def __init__(self, lenght):
        if lenght < 0:
            raise ExamException("lunghezza minore di zero")
        try:
            float(lenght)
        except Exception as e:
            raise ExamException("lenght non è un numero") from e        
        self.lunghezza = lenght
    
    def compute(self, L):
        list_media = []
        for i in range(0, len(L) - self.lunghezza + 1):
            media = 0
            for j in range(0, self.lunghezza):
                try:
                    media = media + L[i+j]
                except Exception as e:
                    
            list_media.append(media/self.lunghezza)            
        return list_media
        
    def print(self, List):
        for item in List:
            print(item)
            
class ExamException(Exception):
    pass


moving_average = MovingAverage(3)
result = moving_average.compute([2,4,8,16])
print(result) # Deve stampare a schermo [3.0,6.0,12.0]


#ECCEZIONI da controllare:
#    che i valori non sino negativi
#    i valori inseriti siano stringhe 
#    per compute i valori 