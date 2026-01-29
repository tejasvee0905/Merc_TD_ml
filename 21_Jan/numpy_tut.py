import numpy as np

list = np.array([10,20,30,40])
list1 = np.array([20,30,50,40])

list3 = np.array([
    [1,2,3,4],
    [5,6,7,8],
    [9,10,11,12]
])

# print((list[2]))

list2 = list + list1
# print(list2)

# print((list[1:3]))

# print((list2[:,1]))
# print((list2[1,:]))

a = np.resize(list3, (3,3))
print (a)