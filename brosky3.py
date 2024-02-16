def sum_csv(name_file):
    my_file = open(name_file, 'r')    
    contenuto = my_file.readlines()
    s = 0    
    try:
        for item in contenuto:
            elements = item.split(',')
            if elements[1] != 'Sales':
                try:
                    numb = float(elements[1])
                    s = s + numb
                except Exception:
                    continue
        return s
    except Exception:
        return None
