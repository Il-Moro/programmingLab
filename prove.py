
# open the sample file used 
file = open('test.txt') 
  
# read the content of the file opened 
content = file.readlines() 
  
# read 10th line from the file 
print("tenth line") 
print(content[9]) 
  
# print first 3 lines of file 
print("first three lines") 
print(content[0:3]) 