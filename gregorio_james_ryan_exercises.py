mylist = list (("chess", "basketball", "badminton"))
mylist.insert(-3,"orange")
print(mylist)

list = ["chess","basketball","badminton"]
list.append("orange")
print(list)

male = ["John", "Mark"]
male[0] = "Kenny"
print(male[0])

list = ["chess","basketball","badminton"]
list.pop(2)
print(list)

list = ["chess","basketball","badminton"]
list.clear()
print(list)

numList = [18, 28, 19, 24, 69]
numList.sort()
print(numList)

numList = [18, 28, 19, 24, 69]
numList.reverse()
print(numList)

numList = [18, 28, 19, 24, 69]
numList.sort()
numList.reverse()
print(numList)

fruits = ["\napple", "banana", "cherry\n"]
for x in fruits:
    print(x)

for x in "mango\n":
    print(x, end="\t")

for y in range(5):
    print(y, end="\n\n")

for y in range(1, 7):
    print(y, end="\n")

