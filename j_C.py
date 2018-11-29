import csv
import matplotlib.pyplot as plt

x=[]
y=[]

lol=list(csv.reader(open("S088_U(I)_B7_6mA.txt","rt"), delimiter="\t"))
for row in lol:
    if len(row) > 1:
        x.append(float(row[0]))
        y.append(float(row[1]))


plt.plot(x,y,label="hello")
plt.xlabel('x')
plt.ylabel('y')
plt.title('Interesting Graph\nCheck it out')
plt.legend()
plt.savefig("test.png")
plt.show
