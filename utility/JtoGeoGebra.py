#open text file 
# file = open("../postOp.txt", "r")
#read the file
with open("../rotated.txt", "r") as file:
    data = file.readlines()
    dataToWrite=set()
    for line in data:
        twonumbers=line.split('\t')
        #remove the new line character
        twonumbers[1]=twonumbers[1].replace('\n','')
        twonumbers[0]=float(twonumbers[0])/100
        twonumbers[1]=float(twonumbers[1])/100
        dataToWrite.add((twonumbers[0],twonumbers[1]))
print(dataToWrite)

