import function

time_series_file = function.CSVTimeSeriesFile('data.csv')
time_series = time_series_file.get_data()

#print('\n')
#print(time_series)

#print('\n')
#print(function.lista_anni_medie(function.lista_con_soli_anni(time_series)))
#print('\n') 
dizionario = function.compute_increments(time_series, '1949','1960')
print(dizionario)
      