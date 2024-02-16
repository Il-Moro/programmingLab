def sum_list(my_list):
    if len(my_list) == 0:
        return None
    sum = 0
    for item in my_list:
        sum = sum + item
    return sum
    