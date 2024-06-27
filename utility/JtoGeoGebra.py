#open text file 
# file = open("../postOp.txt", "r")
#read the file
with open("../rotated_post.txt", "r") as file:
    data = file.readlines()
    dataToWrite1=[]
    dataToWrite2=[]
    indexsplit=10
    for i,line in enumerate(data[:-2]):
        twonumbers=line.split('\t')
        #remove the new line character
        twonumbers[1]=twonumbers[1].replace('\n','')
        twonumbers[0]=float(twonumbers[0])/100
        twonumbers[1]=float(twonumbers[1])/100
        if i<indexsplit:
            dataToWrite1.append((twonumbers[0],twonumbers[1]))
        else:
            dataToWrite2.append((twonumbers[0],twonumbers[1]))
print("{")
for lol in dataToWrite1:
    print(lol,",")
print("}")
print("{")
for lol in dataToWrite2:
    print(lol,",")
print("}")

