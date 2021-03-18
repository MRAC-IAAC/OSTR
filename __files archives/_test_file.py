# list_X = [366, 370, 387, 400]

# # for i in range(len(myList)-1):
# #     print (myList[i + 1], '\n' )

# # list_pts_x = [10, 20, 30, 40, 50, 60]

# # for x in range(len(list_pts_x)-1):
# #     next_pt_X = list_pts_x[x + 1]
# #     print (next_pt_X)

# # list_a = [1,3]
# # list_b = [10,5]

# # delta_x = abs(list_b[0]-list_a[0])
# # delta_y = abs(list_b[1]-list_a[1])

# # print ('delta_x is equal to: ', delta_x)
# # print ('delta_y is equal to: ', delta_y)

# lst = [10, 50, 75, 83, 98, 84, 32] 
 
# res = list(map(lambda x:x, lst))
 
# print(res) 

# print('\n')
# print('\n')
# print('\n')


# for a in list_X:
#     print('a is: ', a)

# print('\n')

# for x in range(len(list_X)-1):
#     x2 = list_X[x+1]
#     print('x2 is: ', x2)
# list_next_x = [0]
# list_next_x.append(x2)
# print(list_next_x)

# print('\n')

# new_list_x = []
# operation_1 = (x2 - a)  
# print('operation 1 is: ', a)  
# new_list_x.append(operation_1)

# print(new_list_x)

# ints = [1,2,3]
# string_ints = ['F' + str(+int) for int in ints]

# str_of_ints = ",".join(string_ints)

# print(str_of_ints)

import numpy as np
import math

# list_of_pts = np.array([[1,2,3],[0,3,4]])
# print(list_of_pts)

# myList = list_of_pts.tolist()
# print(myList)

list_1 = [[1,2,3], [4,5,6]]
list_2 = [[10,20,30], [40,50,60]]

list_3 = []
# expected outcome: list_3 [[11, 22, 33], [44, 55, 66]]

# list_1[0][0] + list_2[0][0]

# zipped = zip(list_1,list_2)
# for x, y in zipped:
#     for x2, y2 in x, y:
#         print('sum is: ', x + y)    
#         # print('sum is: ', sum(x+y))
#         list_3.append(x+y)
#         print('list 3 is: ',list_3)


list_1 = [[10, 20, 30], [2, 3, 4], [100,200,300]]
list_2 = [[2, 4], [5, 1], [10,20,30]]
# desired_result = [[3, 6], [7, 8]]
list_3 = []
list_4 = []
# for a in range(len(list_1)):
#     new_coordinates = []
#     new_coordinate = abs(list_1[a][-1] + list_1[a][0])
#     new_coordinates.append(new_coordinate)
#     list_4.append(new_coordinates)
# print('List 4 is: ', list_4)
# # [[3, 6], [7, 8]]

last_values = [i[-1] for i in list_1]
last_values.pop(-1)
print(last_values)

first_values = [i[0] for i in list_1]
first_values.pop(0)
print(first_values)

zip_lists = zip(last_values, first_values)
sublist = []
for l, f in zip_lists:
    operation = []
    extra = [0]
    op = (abs(l - f))
    operation.append(op)
    sublist.append(operation)
sublist.append(extra)
print('sublist is: ', sublist)

for i in range(len(list_1)):
    list_4.append(list_1[i])
    list_4.append(sublist[i])
print('List 4 is: ', list_4)


# ints = [[1,2,3], [4, 5, 6]]
# strings = []
# for i in ints:
#     list0 = []
#     string_ints = [str(num) for num in i]
#     for i in string_ints:
#         str_of_ints = ",".join(i)
#         list0.append(str_of_ints)
#     strings.append(list0)
# print(strings)