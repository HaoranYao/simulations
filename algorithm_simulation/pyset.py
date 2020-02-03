from itertools import combinations

def comb(temp_list, n):
    temp_list2 = []
    for c in combinations(temp_list,n):
        temp_list2.append(c)
    return temp_list2


list1 = [1,2,3]

end_list = []
for i in range(len(list1)+1):
    end_list.extend(comb(list1,i))
print(end_list)