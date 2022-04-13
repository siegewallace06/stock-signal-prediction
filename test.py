import numbers


i = 0
j = 10
tmp = 0

pivot = numbers[(0 + 10)/2]

while i <= j:
    while numbers[i] < pivot:
        i = i + 1
    
    while numbers[j] < pivot :
        j = j - 1
    
    if(i <= j):
        tmp = numbers[i]
        numbers[i] = numbers[j]
        numbers[j] = tmp
        i = i + 1
        j = j - 1
    
    print(i)
