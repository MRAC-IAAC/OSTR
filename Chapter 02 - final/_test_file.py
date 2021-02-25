list_X = [366, 370, 387, 400]

# for i in range(len(myList)-1):
#     print (myList[i + 1], '\n' )

# list_pts_x = [10, 20, 30, 40, 50, 60]

# for x in range(len(list_pts_x)-1):
#     next_pt_X = list_pts_x[x + 1]
#     print (next_pt_X)

# list_a = [1,3]
# list_b = [10,5]

# delta_x = abs(list_b[0]-list_a[0])
# delta_y = abs(list_b[1]-list_a[1])

# print ('delta_x is equal to: ', delta_x)
# print ('delta_y is equal to: ', delta_y)

lst = [10, 50, 75, 83, 98, 84, 32] 
 
res = list(map(lambda x:x, lst[x+1]))
 
print(res) 

print('\n')
print('\n')
print('\n')


for a in list_X:
    print('a is: ', a)

print('\n')

for x in range(len(list_X)-1):
    x2 = list_X[x+1]
    print('x2 is: ', x2)
list_next_x = [0]
list_next_x.append(x2)
print(list_next_x)

print('\n')

new_list_x = []
operation_1 = (x2 - a)  
print('operation 1 is: ', a)  
new_list_x.append(operation_1)

print(new_list_x)